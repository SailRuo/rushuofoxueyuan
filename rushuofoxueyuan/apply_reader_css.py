import argparse
import os
import re
from pathlib import Path


TITLE_RE = re.compile(r"(?is)(<title[^>]*>.*?</title>)")
HEAD_CLOSE_RE = re.compile(r"(?is)</head\s*>")

VIEWPORT_RE = re.compile(r"(?is)<meta\s+name=([\"'])viewport\1")
GOOGLE_FONT_RE = re.compile(r"(?is)fonts\.googleapis\.com/css2\?family=Noto\+Serif\+SC")
READER_CSS_RE = re.compile(r"(?is)reader\.css")


def should_skip(content: str) -> bool:
    c = content.lower()

    # academy/theme pages should keep theme.css
    if "theme.css" in c:
        return True

    return False


def inject_links(content: str, css_href: str, add_font: bool) -> str:
    lines: list[str] = []

    # viewport: fixes mobile forced zoom (980px layout viewport)
    if not VIEWPORT_RE.search(content):
        lines.append("\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")

    # reader.css
    if not READER_CSS_RE.search(content):
        lines.append(f"\t<link rel=\"stylesheet\" href=\"{css_href}\">")

    # Google font
    if add_font and not GOOGLE_FONT_RE.search(content):
        lines.append(
            "\t<link href=\"https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap\" rel=\"stylesheet\">"
        )

    if not lines:
        return content

    inject = "\n" + "\n".join(lines)

    m = TITLE_RE.search(content)
    if m:
        return TITLE_RE.sub(lambda mm: mm.group(1) + inject, content, count=1)

    # fallback: inject before </head>
    m2 = HEAD_CLOSE_RE.search(content)
    if m2:
        return HEAD_CLOSE_RE.sub(lambda mm: inject + "\n" + mm.group(0), content, count=1)

    return content


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Batch-apply reader.css to legacy article pages under a directory. "
            "Skips pages that already use theme.css or already include reader.css."
        )
    )
    parser.add_argument(
        "site_root",
        nargs="?",
        default="My Web Sites",
        help="Directory to scan (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory that contains reader.css",
    )
    parser.add_argument(
        "--css-file",
        default="reader.css",
        help="CSS file path relative to repo root",
    )
    parser.add_argument(
        "--add-font",
        action="store_true",
        help="Also inject Noto Serif SC Google Font link",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    site_root = Path(args.site_root)
    if not site_root.is_absolute():
        site_root = (repo_root / site_root).resolve()

    css_file = (repo_root / args.css_file).resolve()
    if not css_file.exists():
        raise SystemExit(f"CSS file not found: {css_file}")

    html_files = list(site_root.rglob("*.htm")) + list(site_root.rglob("*.html"))

    changed = 0
    skipped = 0
    for f in html_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            skipped += 1
            continue

        if should_skip(content):
            skipped += 1
            continue

        # compute relative href from html file to repo_root/css_file
        try:
            rel_href = css_file.relative_to(repo_root)
        except ValueError:
            rel_href = css_file

        href = os.path.relpath(str(repo_root / rel_href), start=str(f.parent)).replace("\\", "/")

        new_content = inject_links(content, href, add_font=args.add_font)
        if new_content != content:
            changed += 1
            if args.dry_run:
                print(f"WOULD UPDATE: {f}")
            else:
                f.write_text(new_content, encoding="utf-8")

    print(f"Scanned: {len(html_files)}")
    print(f"Updated: {changed}")
    print(f"Skipped: {skipped}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
