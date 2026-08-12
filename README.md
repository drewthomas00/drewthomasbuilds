# drewthomasbuilds.com

Personal site. Static, no dependencies, no framework. Deployed on Cloudflare Pages.

## Editing

Edit the files in `src/` — **not** the ones in `public/`.

| File | What it is |
|---|---|
| `src/site.html` | The site. All copy and CSS live here. ~28 KB. |
| `src/resume.html` | The one-page résumé. |
| `src/fonts.json` | Base64 woff2 payloads. Don't edit by hand. |

The sources carry `__BRIC600__`-style placeholders where the font data goes, which
keeps them small enough to actually work in. Page content starts after `</style>`.

Then rebuild:

```sh
./build.py          # writes public/index.html and public/resume.html
./build.py --pdf    # also re-renders public/drew-thomas-resume.pdf
```

`public/` is the build output and what Cloudflare Pages serves. Committing it is
deliberate: it means the deploy needs no build step at all.

## Deploying

Pushing to `main` publishes. Cloudflare Pages is configured with no build command
and `public` as the output directory.

## Notes

- The testimonials section in `src/site.html` is commented out until there are real
  quotes to put in it. Uncomment the block to bring it back, styling intact.
- The résumé fits on one page by design. After editing it, run `./build.py --pdf`
  and check the page count — a résumé that spills onto a second page with a third of
  it empty looks worse than either a full one-pager or a full two-pager.
- Fonts are embedded rather than linked so the pages have zero external requests.
