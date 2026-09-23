"""Wiki link graph checks for wiki-lint: dead links (forward and reverse),
ambiguous link targets, and index coverage for newly added wiki pages.

Usage: python .claude/scripts/wiki_link_check.py   (run from inside the repo)

Scope: this commit's changes to 2-wiki/ -- `git diff HEAD -M` (staged +
unstaged) plus untracked new files under 2-wiki/, restricted to that subtree.
In a repository with no commits yet, everything under 2-wiki/ counts as newly
added. Renames are split into a synthetic delete (old path) + add (new path)
pair so downstream logic only ever sees A/M/D; the add-half keeps
"renamed_from" so the index-coverage check can skip it -- a rename is not
newly-created content, and an index entry left pointing at the old path is
reported as a dead link instead.

The link graph is built from the current working-tree content of every
2-wiki/**/*.md file. deadlink_reverse resolves against a separate resolver
built from the HEAD tree's page set, not the current one -- resolving a
removed link against today's (already-edited) graph would misattribute what
it used to point to.

Wikilink parsing: `[[target]]`, `[[target|alias]]`, `[[target#section]]`,
`[[target#section|alias]]`; embeds (`![[...]]`), self-section links
(`[[#section]]`), and anything inside fenced or inline code is excluded.

Target resolution tries, in order, and stops at the first tier with >=1
candidate:
  1. exact normalized path (relative to 2-wiki/, no extension)
  2. path relative to the linking file's own directory
  3. unique path-suffix match (matches the tail components of exactly one page)
  4. unique basename match (matches the filename of exactly one page)
A tier with more than one candidate is ambiguous, not a fall-through to the
next tier. Targets under 1-raw/ are treated as valid (existence-checked on
disk) but are not part of the wiki graph.

Index coverage: every newly added page needs at least one incoming link from
the index layer -- 2-wiki/index.md or any _index.md route page. 2-wiki/index.md
itself is exempt, since nothing links to the root index.

Prints one JSON object to stdout:
  {"deadlink_forward": [...], "deadlink_reverse": [...], "ambiguous": [...],
   "unindexed": [...]}
Each list is empty when that check is clean.

Exit codes: 0 = all clean, 1 = at least one finding, 2 = the script itself
failed (traceback on stderr, no JSON printed).
"""

import json
import posixpath
import re
import subprocess
import sys
import traceback
from pathlib import Path

WIKI_DIR = "2-wiki"
RAW_DIR = "1-raw"
INDEX_ROOT = "index"  # 2-wiki/index.md, exempt from index coverage
ROUTE_BASENAME = "_index"  # per-category route pages, part of the index layer

LINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")


def run_git(*args: str) -> str:
    # core.quotepath=false keeps non-ASCII paths as raw UTF-8 instead of
    # octal-escaped and quoted, which would never match the on-disk names.
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return result.stdout


def repo_root() -> Path:
    return Path(run_git("rev-parse", "--show-toplevel").strip())


def has_head() -> bool:
    """False in a repository whose first commit has not been made yet."""
    try:
        run_git("rev-parse", "--verify", "HEAD")
        return True
    except subprocess.CalledProcessError:
        return False


def strip_inline_code(line: str) -> str:
    """Blank CommonMark-style backtick-run code spans (`` `x` ``, ` ``x`` `,
    ...): a run of N backticks opens, only a run of exactly N backticks
    closes it. Unmatched runs are left as literal text."""
    out = []
    i, n = 0, len(line)
    while i < n:
        if line[i] != "`":
            out.append(line[i])
            i += 1
            continue
        j = i
        while j < n and line[j] == "`":
            j += 1
        run_len = j - i
        k = j
        close_start = close_end = -1
        while k < n:
            if line[k] == "`":
                k2 = k
                while k2 < n and line[k2] == "`":
                    k2 += 1
                if k2 - k == run_len:
                    close_start, close_end = k, k2
                    break
                k = k2
            else:
                k += 1
        if close_start == -1:
            out.append(line[i:j])
            i = j
        else:
            out.append(" " * (close_end - i))
            i = close_end
    return "".join(out)


def strip_code(text: str) -> str:
    """Blank out fenced/inline code so link regex can't match inside it,
    without changing line count or offsets. Fenced blocks track the opening
    marker's character and length; a closing fence must use the same
    character, be at least as long, and contain nothing else."""
    lines = text.split("\n")
    out = []
    fence_char = None
    fence_len = 0
    for line in lines:
        stripped = line.strip()
        if fence_char is None:
            m = FENCE_RE.match(stripped)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                out.append("")
                continue
            out.append(strip_inline_code(line))
        else:
            if stripped and set(stripped) == {fence_char} and len(stripped) >= fence_len:
                fence_char = None
                fence_len = 0
            out.append("")
    return "\n".join(out)


def normalize_target(raw_target: str) -> str:
    link_part = raw_target.split("|", 1)[0]
    target = link_part.split("#", 1)[0].strip()
    if not target:
        return ""  # self-section link [[#...]]
    if target.endswith(".md"):
        target = target[:-3]
    if target.startswith(f"{WIKI_DIR}/"):
        target = target[len(WIKI_DIR) + 1:]
    return target.lstrip("/")


def extract_links(content: str):
    """Yield (line_no, target, raw_bracket_text) for each page-type wikilink."""
    cleaned = strip_code(content)
    for i, line in enumerate(cleaned.split("\n"), start=1):
        for m in LINK_RE.finditer(line):
            raw = m.group(1)
            target = normalize_target(raw)
            if target:
                yield i, target, raw


def changed_wiki_files(head_exists: bool):
    """Return list of {"status": "A"|"M"|"D", "path": repo-root-relative}.
    A rename's new-path entry additionally carries "renamed_from": old_path."""
    entries = []
    if head_exists:
        diff_out = run_git("diff", "HEAD", "-M", "--name-status", "--", f"{WIKI_DIR}/")
        for line in diff_out.splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0]
            if status.startswith("R"):
                old_path, new_path = parts[1], parts[2]
                entries.append({"status": "D", "path": old_path})
                entries.append({"status": "A", "path": new_path, "renamed_from": old_path})
            elif status in ("A", "M", "D"):
                entries.append({"status": status, "path": parts[1]})
            # other statuses (T, C, U, X) shouldn't occur for plain markdown pages
    else:
        for line in run_git("ls-files", "--", f"{WIKI_DIR}/").splitlines():
            if line.strip():
                entries.append({"status": "A", "path": line.strip()})
    untracked = run_git("ls-files", "--others", "--exclude-standard", "--", f"{WIKI_DIR}/")
    for line in untracked.splitlines():
        if line.strip():
            entries.append({"status": "A", "path": line.strip()})
    return entries


def head_wiki_paths(head_exists: bool) -> set:
    """relpaths (relative to 2-wiki/, no ext) that existed at HEAD."""
    if not head_exists:
        return set()
    out = run_git("ls-tree", "-r", "--name-only", "HEAD", "--", f"{WIKI_DIR}/")
    paths = set()
    prefix = f"{WIKI_DIR}/"
    for line in out.splitlines():
        line = line.strip()
        if line.startswith(prefix) and line.endswith(".md"):
            paths.add(line[len(prefix):-3])
    return paths


def current_pages(root: Path) -> dict:
    """relpath (relative to 2-wiki/, no ext, posix) -> absolute Path."""
    pages = {}
    for p in (root / WIKI_DIR).rglob("*.md"):
        rel = p.relative_to(root / WIKI_DIR).as_posix()[:-3]
        pages[rel] = p
    return pages


def rel_of(repo_path: str) -> str:
    prefix = f"{WIKI_DIR}/"
    p = repo_path[len(prefix):] if repo_path.startswith(prefix) else repo_path
    if p.endswith(".md"):
        p = p[:-3]
    return p


class Resolver:
    def __init__(self, pages: dict):
        self.pages = pages
        self.parts = {rel: rel.split("/") for rel in pages}

    def resolve(self, target: str, source_rel: str):
        """Return (status, result): status in
        {"resolved", "ambiguous", "unresolved"}; result is a relpath for
        "resolved", a list of relpaths for "ambiguous", None otherwise."""
        target = posixpath.normpath(target)

        if target in self.pages:
            return "resolved", target

        source_dir = posixpath.dirname(source_rel)
        candidate = posixpath.normpath(posixpath.join(source_dir, target))
        if candidate in self.pages:
            return "resolved", candidate

        target_parts = target.split("/")

        suffix_matches = [
            rel for rel, parts in self.parts.items()
            if len(parts) >= len(target_parts) and parts[-len(target_parts):] == target_parts
        ]
        if len(suffix_matches) == 1:
            return "resolved", suffix_matches[0]
        if len(suffix_matches) > 1:
            return "ambiguous", suffix_matches

        basename_matches = [
            rel for rel, parts in self.parts.items() if parts[-1] == target_parts[-1]
        ]
        if len(basename_matches) == 1:
            return "resolved", basename_matches[0]
        if len(basename_matches) > 1:
            return "ambiguous", basename_matches

        return "unresolved", None


def is_valid_external(target: str, root: Path) -> bool:
    if target.startswith(f"{RAW_DIR}/"):
        if (root / target).exists():
            return True
        if (root / f"{target}.md").exists():
            return True
    return False


def is_index_layer(rel: str) -> bool:
    return rel == INDEX_ROOT or rel.rsplit("/", 1)[-1] == ROUTE_BASENAME


def wiki_path(rel: str) -> str:
    return f"{WIKI_DIR}/{rel}.md"


def main() -> int:
    # Windows consoles often default stdout/stderr to a non-UTF-8 codepage
    # (e.g. cp950); force UTF-8 so JSON with Chinese text round-trips cleanly.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    root = repo_root()
    head_exists = has_head()
    pages = current_pages(root)
    resolver = Resolver(pages)
    changed = changed_wiki_files(head_exists)
    head_paths = head_wiki_paths(head_exists)
    head_resolver = Resolver({rel: None for rel in head_paths})

    changed_md = [e for e in changed if e["path"].endswith(".md")]
    changed_by_rel = {rel_of(e["path"]): e["status"] for e in changed_md}

    # single extraction pass over every current page's current content
    all_links = {}  # rel -> list[(line_no, target, raw)]
    for rel, path in pages.items():
        all_links[rel] = list(extract_links(path.read_text(encoding="utf-8")))

    # forward resolution: incoming index (all pages) + forward/ambiguous
    # findings (changed A/M pages only)
    incoming = {rel: [] for rel in pages}
    deadlink_forward = []
    ambiguous = []

    for rel, links in all_links.items():
        is_changed_am = changed_by_rel.get(rel) in ("A", "M")
        for line_no, target, raw in links:
            status, result = resolver.resolve(target, rel)
            if status == "resolved":
                if result != rel:  # self-links don't count as incoming
                    incoming[result].append((rel, line_no))
            elif status == "ambiguous":
                if is_changed_am:
                    ambiguous.append({
                        "file": wiki_path(rel), "line": line_no,
                        "link": f"[[{raw}]]",
                        "matches": [wiki_path(m) for m in result],
                    })
            else:
                if is_changed_am and not is_valid_external(target, root):
                    deadlink_forward.append({
                        "file": wiki_path(rel), "line": line_no,
                        "link": f"[[{raw}]]",
                    })

    # deadlink_reverse: pages deleted/renamed-away this commit, still
    # referenced (per how the link resolved at HEAD, not by name-string
    # comparison) by pages that were NOT touched this commit (touched ones
    # are already covered above, since the old target no longer resolves)
    deadlink_reverse = []
    deleted = [e for e in changed_md if e["status"] == "D"]
    for e in deleted:
        old_rel = rel_of(e["path"])
        for rel, links in all_links.items():
            if rel in changed_by_rel:
                continue
            for line_no, target, raw in links:
                status, result = head_resolver.resolve(target, rel)
                if status == "resolved" and result == old_rel:
                    deadlink_reverse.append({
                        "file": wiki_path(rel), "line": line_no,
                        "link": f"[[{raw}]]",
                        "stale_link_to": wiki_path(old_rel),
                    })

    # unindexed: newly added pages need at least one incoming link from the
    # index layer (2-wiki/index.md or an _index.md route page). A page added
    # purely via `git mv` (renamed_from set) is not new content; an index
    # entry still pointing at its old path surfaces as deadlink_reverse.
    unindexed = []
    for e in changed_md:
        if e["status"] != "A" or e.get("renamed_from"):
            continue
        rel = rel_of(e["path"])
        if rel == INDEX_ROOT or rel not in pages:
            continue
        if any(is_index_layer(src) for src, _ in incoming.get(rel, [])):
            continue
        unindexed.append({"file": e["path"]})

    findings = {
        "deadlink_forward": deadlink_forward,
        "deadlink_reverse": deadlink_reverse,
        "ambiguous": ambiguous,
        "unindexed": unindexed,
    }
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    return 1 if any(findings.values()) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
