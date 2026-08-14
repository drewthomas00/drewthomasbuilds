# drewthomasbuilds.com

Personal site. Static, no framework, no build step. Deployed on Cloudflare Pages.

## Editing

`public/` holds the real files — edit them directly.

| File | What it is |
|---|---|
| `public/base.css` | Typefaces, palette, reset, base type. Shared by everything except the résumé. |
| `public/index.html` | The site. Its layout CSS is inline. |
| `public/resume.html` | The one-page résumé. **Deliberately self-contained** — see below. |
| `public/writing.html` | Index of the posts. |
| `public/writing/*.html` | One file per post. |
| `public/writing/post.css` | Article typography, shared by every post. |
| `public/drew-thomas.{webp,jpg}` | Portrait in the "How I got here" section. |
| `public/fonts/*.woff2` | Bricolage Grotesque, Newsreader, IBM Plex Mono. |
| `public/_headers` | Cache-control and security headers. |

**The palette lives in exactly one place.** `base.css` holds the tokens, the
`@font-face` set and the base type; each page adds only its own layout. Posts link
`base.css` first, then `post.css`.

**`resume.html` is the exception and must stay one.** It has its own palette — pure
white paper, a darker brass — because it is tuned for print and is what `build.py`
renders the PDF from. Pointing it at `base.css` would change the résumé's appearance
and the PDF with it.

Push to `main` and Cloudflare publishes it. There is no build command, so nothing
in CI can break between a commit and a live site.

## Adding a post

Copy any file in `public/writing/`, replace the content, and add it in two places:
`public/writing.html` (the index) and the `#writing` section of `public/index.html`
(the four most recent).

Posts carry no CSS of their own — they link `/writing/post.css`, so a change to the
article styling lands on all of them at once. Only the `<head>` needs editing per
post: `<title>`, the description, the canonical URL, and the four `og:` tags.

Two things to keep right:

- **Give each post its own URL.** The point of writing these is having something to
  link to from an answer, a comment or a post; a combined page cannot be pointed at.
- **`og:url` and `<link rel="canonical">` must match the file's real path.** They are
  the two lines most easily left pointing at whichever post was copied.

## The one thing that needs regenerating

The downloadable résumé PDF is rendered from `public/resume.html`:

```sh
./build.py
```

It prints the page count, because the résumé is tuned to fit on exactly one page
and a couple of added lines will silently spill it onto a second.

The script serves `public/` over a local web server rather than opening the file
directly. That is deliberate: the pages load fonts as separate files, and Chromium
will not fetch subresources into a `file://` document, so a direct render comes out
set in fallback typefaces — which looks plausible and is wrong.

If a render hangs, look for stranded headless browsers before retrying:

```sh
ps -eo pid,etimes,args | grep -- --headless=new
```

## Notes

- **Fonts are separate files, not embedded.** Earlier versions inlined them as
  base64, which made every page ~700 KB and forced a second download of the same
  typefaces when someone opened the résumé. Splitting them dropped the HTML to
  ~27 KB and lets the browser cache the fonts across every page.
- **Preload only what is above the fold, at the weight actually used.** A preload for
  a face the page never requests is a wasted round trip, and one at the wrong weight
  is worse than none — it fetches a file the page will not use and still stalls on the
  one it needs. The posts preload four because all four are visible before scrolling:
  body, body-italic (the standfirst), display 800, mono 400.
- **Font URLs must stay absolute** (`/fonts/x.woff2`). This is no longer theoretical —
  the posts live in `/writing/`, so a relative path resolves against the wrong
  directory and silently falls back to a system typeface.
- **`build.py` will not run from a Claude Code shell.** Headless Brave hangs past the
  script's 180-second timeout there — not a stranded process and not a stale
  `.render-profile`. Run it from a normal terminal.
- **The portrait floats.** `.col` is a flex column and floats do not apply to flex
  items, so the paragraphs in `#who` are wrapped in a `.prose` block for the float to
  work inside. It stacks again below 34rem, where wrapping would leave twelve-character
  lines beside the photo.
- The testimonials section in `index.html` is commented out until there are real
  quotes for it. Uncomment the block to bring it back, styling intact.
- `og.png` is the social preview card shown when the link is shared. If the hero
  copy changes, that image goes stale — it is a rendered screenshot, not live text.
