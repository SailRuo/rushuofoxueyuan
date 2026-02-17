import argparse
import html
import os
import re
from pathlib import Path
from urllib.parse import unquote


_ATTR_RE = re.compile(r"(?is)\b(?:href|src)\s*=\s*([\"'])(.*?)\1")


def _is_external(ref: str) -> bool:
    ref_l = ref.lower()
    return ref_l.startswith((
        "http://",
        "https://",
        "mailto:",
        "javascript:",
        "data:",
    ))


def _normalize_ref(ref: str) -> str:
    # Unescape HTML entities and URL encoding
    ref = html.unescape(ref)
    ref = unquote(ref)

    # Remove fragment and query
    ref = ref.split("#", 1)[0]
    ref = ref.split("?", 1)[0]

    return ref.strip()


def _resolve_path(html_file: Path, ref: str) -> Path | None:
    ref = _normalize_ref(ref)
    if not ref:
        return None

    if _is_external(ref) or ref.startswith("#"):
        return None

    # protocol-relative (//example.com/..)
    if ref.startswith("//"):
        return None

    # Windows UNC path (\\server\share)
    if ref.startswith("\\\\"):
        return None

    # Normalize slashes
    ref = ref.replace("/", os.sep)

    base_dir = html_file.parent

    try:
        if os.path.isabs(ref):
            return Path(ref).resolve()
        return (base_dir / ref).resolve()
    except OSError:
        return None


def scan(root: Path, limit: int) -> tuple[list[dict], int]:
    missing: list[dict] = []
    total_refs = 0

    html_files = list(root.rglob("*.htm")) + list(root.rglob("*.html"))

    for f in html_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for m in _ATTR_RE.finditer(content):
            raw = m.group(2).strip()
            if not raw:
                continue

            resolved = _resolve_path(f, raw)
            if resolved is None:
                continue

            total_refs += 1

            if not resolved.exists():
                if len(missing) < limit:
                    missing.append({
                        "html": str(f),
                        "ref": raw,
                        "resolved": str(resolved),
                    })

    return missing, total_refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan local href/src references in .htm/.html and report missing files.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan")
    parser.add_argument("--limit", type=int, default=200, help="Max number of missing items to print")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing, total_refs = scan(root, args.limit)

    for item in missing:
        print(f"HTML     : {item['html']}")
        print(f"REF      : {item['ref']}")
        print(f"RESOLVED : {item['resolved']}")
        print("-")

    print(f"Checked refs: {total_refs}")
    print(f"Missing shown: {len(missing)} (limit={args.limit})")
    print("Note: count shown is capped by --limit; run with a higher limit to see more.")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
