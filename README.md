# Writfold website

The pre-release introduction to Writfold at **writfold.dev**. Plain HTML and CSS with a small local theme script; no external fonts, analytics, dependency installation or product build. The source files are the publication input. The folded-W assets are unchanged copies of Writfold's brand files.

## Pages

- `index.html`: the overview. Writfold's direction, Git-native project continuity for coding agents, with an example answer labelled as illustrative, not real output.
- `status.html`: what runs today (frozen demos), the roadmap, a short changelog and FAQ.
- `earlier.html`: an index of the earlier work that still builds and runs from source, with build commands at `#try`.
- `docs.html`, `tuft.html`, `weft.html`, `splicery.html`, `glossary.html`: the earlier-work guides. They keep their URLs, are marked "(earlier work)" in their titles and carry a "Frozen demo" badge where they show a demo.
- `404.html`: the missing-page response.

Nothing on the site describes the planned project-continuity tool as built. Keep planned behavior in planned tense, and describe only exercised capabilities as running.

## Serve locally

From this checkout:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/`. This development server exposes repository files; do not bind it to a public interface. It does not emulate GitHub Pages' custom missing-page behavior: inspect `/404.html` directly, then check an unknown URL after deployment.

## Review and package

After changing site content, regenerate the content manifest and package the files:

```sh
rm -rf _site
python3 scripts/package.py --refresh-manifest
python3 -m http.server 8081 --bind 127.0.0.1 --directory _site
```

`_site/` must not already exist; the script refuses to replace it. The script copies only a fixed public allowlist (`FILES` in `scripts/package.py`) and writes its SHA-256 manifest. It does not render docs, run Rust, fetch content or copy other repository files. Without `--refresh-manifest`, it refuses bytes that differ from the committed manifest. Commit `content-manifest.json` with the source change, and add any new published file to the allowlist. For an out-of-tree artifact, pass `--output /absolute/path/to/new-artifact`.

Before publishing, check:

- every internal link and anchor resolves, the HTML is well-formed and IDs are unique;
- `index.html`, `status.html` and `earlier.html` at 1440 and 360 pixels wide, in light and dark, with no horizontal overflow;
- the System, Light and Paper Dark theme choices, disabled JavaScript, 200% text zoom, and the keyboard skip link and focus;
- the packaged artifact in `_site/`, not only the working tree.

These are website checks, not product qualification.

## Social card

`assets/og-image.png` is a 1200×630 card: the folded-W mark on the navy background with the overview headline, rendered from HTML with headless Chromium. When the headline changes, re-render it and update `og:image:alt` on every page to match the card's text.

## Publish with GitHub Pages

1. Review and commit the static source, manifest, packaging script and workflow on `main`. Push only with publication authorization.
2. The repository's Pages source is **GitHub Actions** and its custom domain is **writfold.dev**. `CNAME` alone does not configure Pages. Preserve the existing DNS and domain verification.
3. The `github-pages` environment is protected by the publication approver and limited to `main`. The workflow checks that the nominated full SHA is a commit on `main`; environment approval is the publication boundary, not the manifest.
4. Manually run **Publish reviewed static site** from `main` with the full reviewed site commit SHA. A push alone does not deploy. The workflow checks commit ancestry and content hashes, packages those exact bytes, uploads and deploys. It does not build the product or generate documentation.
5. Check the deployment, HTTPS, apex and `www` behavior, root and anchor routes, a real missing URL, asset caching and external links. Record the site SHA and manifest with the Pages run. Keep the previous approved commit for rollback; dispatch its SHA to republish.

A website deployment does not release or qualify any Writfold build.

## Design

The folded mark, navy and off-white surfaces and teal accent are Writfold's. Amber marks planned or frozen material; teal marks what runs. System is the default theme, following the operating system's light or dark setting. The native Theme control offers System, Light and the Paper Dark website palette; `assets/theme.js` stores an explicit choice in local storage, and choosing System clears it. With JavaScript disabled the control stays hidden and the system theme still works. If storage is unavailable, the choice applies to the current page only.

Code panels on the earlier-work pages use static HTML highlighting, not a client-side parser.

## License

The product and this website use the MIT license. `LICENSE.txt` is included in the published artifact.
