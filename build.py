#!/usr/bin/env python3
"""Build the site.

Sources in src/ keep __FONT__ placeholders so they stay small and editable.
This splices the woff2 payloads in and writes the self-contained pages to public/,
which is what Cloudflare Pages serves.

    ./build.py            # build the pages
    ./build.py --pdf      # also re-render the resume PDF (needs brave/chromium)
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC, PUB = ROOT / "src", ROOT / "public"

FONTS = {
    "__BRIC600__":  "Bricolage Grotesque|600|normal",
    "__BRIC800__":  "Bricolage Grotesque|800|normal",
    "__NEWS400__":  "Newsreader|400|normal",
    "__NEWS500__":  "Newsreader|500|normal",
    "__NEWS400I__": "Newsreader|400|italic",
    "__PLEX400__":  "IBM Plex Mono|400|normal",
    "__PLEX500__":  "IBM Plex Mono|500|normal",
}

PAGES = [("site.html", "index.html"), ("resume.html", "resume.html")]


def build():
    faces = json.loads((SRC / "fonts.json").read_text())
    for src_name, out_name in PAGES:
        html = (SRC / src_name).read_text()
        for token, key in FONTS.items():
            if token in html:
                if key not in faces:
                    sys.exit(f"{src_name}: no font data for {key}")
                html = html.replace(token, faces[key])
        head = html.split("</style>", 1)[0]
        if "__" in head:
            sys.exit(f"{src_name}: unreplaced font placeholder remains")
        (PUB / out_name).write_text(html)
        print(f"  public/{out_name}  {len(html) // 1024} KB")


def render_pdf():
    for browser in ("brave", "chromium", "google-chrome-stable", "google-chrome"):
        try:
            subprocess.run(
                [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
                 f"--user-data-dir={ROOT / '.render-profile'}",
                 "--no-pdf-header-footer",
                 f"--print-to-pdf={PUB / 'drew-thomas-resume.pdf'}",
                 (PUB / "resume.html").as_uri()],
                check=True, capture_output=True, timeout=120,
            )
            print("  public/drew-thomas-resume.pdf")
            return
        except FileNotFoundError:
            continue
    sys.exit("no chromium-based browser found to render the PDF")


if __name__ == "__main__":
    print("building:")
    build()
    if "--pdf" in sys.argv:
        render_pdf()
    print("done.")
