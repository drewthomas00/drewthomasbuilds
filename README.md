# drewthomasbuilds.com

Personal site. Static, no framework, no build step. Deployed on Cloudflare Pages.

## Editing

`public/` holds the real files — edit them directly.

| File | What it is |
|---|---|
| `public/index.html` | The site. All copy and CSS live here. ~27 KB. |
| `public/resume.html` | The one-page résumé. |
| `public/fonts/*.woff2` | Bricolage Grotesque, Newsreader, IBM Plex Mono. |
| `public/_headers` | Cache-control; fonts are cached for a year. |

Push to `main` and Cloudflare publishes it. There is no build command, so nothing
in CI can break between a commit and a live site.

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
  ~27 KB and lets the browser cache the fonts across both pages.
- **Font URLs must stay absolute** (`/fonts/x.woff2`). Relative paths happen to
  work today because both pages sit at the root, but break the moment a page moves
  into a subdirectory.
- The testimonials section in `index.html` is commented out until there are real
  quotes for it. Uncomment the block to bring it back, styling intact.
- `og.png` is the social preview card shown when the link is shared. If the hero
  copy changes, that image goes stale — it is a rendered screenshot, not live text.
