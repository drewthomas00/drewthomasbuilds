#!/usr/bin/env python3
"""Re-render public/drew-thomas-resume.pdf from public/resume.html.

The pages in public/ are the real sources — there is no build step for the site
itself. This exists only because the downloadable resume PDF has to be produced
from the resume page, and it is the one thing you cannot just edit by hand.

Why it stands up a web server to do that: the pages load their fonts as separate
files, and Chromium refuses to fetch subresources into a file:// document. Render
the page from disk and it comes out silently set in fallback typefaces — which
looks fine at a glance and wrong on the page. Serving over http:// avoids it.

    ./build.py
"""
import pathlib
import socket
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
PUB = ROOT / "public"
BROWSERS = ("brave", "chromium", "chromium-browser", "google-chrome-stable", "google-chrome")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for(port, timeout=10):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


def main():
    pdf = PUB / "drew-thomas-resume.pdf"
    port = free_port()
    srv = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port),
         "--bind", "127.0.0.1", "--directory", str(PUB)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        if not wait_for(port):
            sys.exit("local server never came up")

        for browser in BROWSERS:
            try:
                subprocess.run(
                    [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
                     f"--user-data-dir={ROOT / '.render-profile'}",
                     "--hide-scrollbars", "--no-pdf-header-footer",
                     f"--print-to-pdf={pdf}",
                     f"http://127.0.0.1:{port}/resume.html"],
                    check=True, timeout=180,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                break
            except FileNotFoundError:
                continue
        else:
            sys.exit("no chromium-based browser found to render the PDF")
    finally:
        srv.terminate()
        srv.wait(timeout=10)

    print(f"  public/drew-thomas-resume.pdf  {pdf.stat().st_size // 1024} KB")

    # a resume quietly growing to two pages is the failure worth catching
    try:
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        n = next(l.split()[1] for l in info.splitlines() if l.startswith("Pages:"))
        print(f"  {n} page(s)" + ("" if n == "1" else "   <-- expected 1, check the layout"))
    except (FileNotFoundError, StopIteration):
        pass

    print("\nIf this hangs, check for stranded headless renderers:")
    print("  ps -eo pid,etimes,args | grep -- --headless=new")


if __name__ == "__main__":
    main()
