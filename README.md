# Writfold website

The pre-release introduction to Writfold at **writfold.dev**. Plain HTML and CSS with a small local theme script; no third-party requests, analytics, dependency installation or product build. One self-hosted subset font draws the terminal captures. The source files are the publication input. The folded-W assets are unchanged copies of Writfold's brand files.

## Pages

- `index.html`: the overview. The two ideas (deterministic, resumable) and the install command in the hero, then one section each: a `writfold watch` capture with three callouts, the three resume commands with one answer card, three facts about storage, and the install block (what the installer does, its options, and the manual steps in a disclosure).
- `how.html`: one short end-to-end example (six commands with their real, trimmed output: stop on one machine, resume on another), then nine sections, each one real file (a gate, a plan template, a policy, a skill, a guard rule, a store declaration, a delivery mode, a checkpoint) beside the few commands that use it; two of them (several sessions, an attached store) open with a drawing from `scripts/diagrams.py`, captioned "Drawing". Each command sits in its own block under a one-line caption; the two columns stack on narrow screens. The example and the policy section's output come from a scratch repository and the release binary; run them again when a release changes what they print.
- `status.html`: what runs in the preview (the one such list), the roadmap, a changelog of one line per release, and the FAQ.
- `install.sh`: the installer, served as `https://writfold.dev/install.sh` (see "Releasing the installer").
- `earlier.html`, `docs.html`, `glossary.html` and three more stubs listed in `STUBS` in `scripts/build_pages.py`: redirects for addresses that were published before. Each holds a `meta refresh` and one link to the overview or How it works, and no other content.
- `404.html`: the missing-page response.

Full file layouts, complete configuration files and exact output live in the Writfold repository under `docs/guide/`, and the pages link there (`https://github.com/writfold-dev/writfold/blob/main/docs/guide/<page>.md`). Keep the site short and plain: a first-time visitor should understand it in about five minutes. Move detail to a guide and link it, and leave out anything that is about how Writfold is built rather than what it does for its user.

Describe only exercised capabilities as running. Everything else is labelled with a `Next` or `Planned` chip.

## Writing pages

The HTML pages are written by `scripts/build_pages.py` from shared parts (head, header, footer), with syntax highlighting from `scripts/highlight.py`. Highlighting happens here, at authoring time; the site loads no highlighting script.

```sh
python3 scripts/build_pages.py
```

Edit copy in `scripts/build_pages.py`, run it, and review the HTML it writes. The committed HTML is still the publication input: packaging and publishing never run these scripts.

- Code panels take a language: `session` (lines starting with `$ ` are commands, the rest is `writfold` output), `shell`, `toml` or `md`.
- The files shown on `how.html` are kept in `scripts/examples/`. They must be real: before publishing a change to one, copy it into a demo knowledge base (the `.toml` files under `.writfold/gates/`, `plans/`, `guards/` and `deliveries/`) and run the commands shown beside it with the release binary.
- A command with a Copy button is written with `copy_line`. `assets/copy.js` shows the button only when the clipboard is usable; without JavaScript the command is plain selectable text.
- Output shown as real must be real: run the command with the release binary against an invented demo knowledge base and paste what it printed, shortening only run IDs, digests and paths with `…`. Anything drawn rather than printed is captioned "Illustration" (invented content) or "From real output" (a drawing of real output).
- The release the site describes is `VERSION` and `RELEASED` at the top of `scripts/build_pages.py`, and `product_release` in `scripts/package.py`.

### Terminal captures

A captured `writfold watch` frame is the `<span>` fragment the capture tool writes, kept as `scripts/frames/home.html` (the overview). To publish a new capture, replace the file, adjust its `FRAME_LABELS` entry in `scripts/build_pages.py` if the picture changed, and run the script again. Captions carry the `Captured` chip and say the knowledge base is a test fixture.

Every cell of a frame is drawn with one font, Writfold Term: a subset of DejaVu Sans Mono (regular and bold, about 8 KB each) in `assets/term-*.woff2`, with its licence in `assets/term-LICENSE.txt`. A system monospace lacks some of the symbols a frame uses, and a fallback glyph of another width moves every column after it. The characters the font holds are listed in `scripts/term_glyphs.py`; `build_pages.py` refuses a frame that uses any other character, or any style other than regular and bold. To add a character, extend that list and run `python3 scripts/build_term_font.py` (needs `fontTools`, `brotli` and the DejaVu fonts; authoring time only).

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
- `index.html`, `how.html` and `status.html` at 1440 and 360 pixels wide, in light and dark, with no horizontal overflow, the code panels and the install command included, and the box borders of each terminal capture in straight columns;
- the System, Light and Paper Dark theme choices, disabled JavaScript, 200% text zoom, and the keyboard skip link and focus;
- the packaged artifact in `_site/`, not only the working tree.

These are website checks, not product qualification.

## Releasing the installer

`install.sh` installs one release by default, named by two lines at its top: `WRITFOLD_DEFAULT_VERSION` and `WRITFOLD_DEFAULT_SHA256`. For that version the downloaded binary must match both the release's `.sha256` file and the checksum pinned in the script, so a swapped release asset is refused. Stamp both lines at each release, after the release assets exist and their re-downloaded copies have passed `sha256sum -c` (a script published ahead of its release refuses to install):

```sh
v=0.5.0-dev.10                      # the new release, without the leading v
sha=$(cut -d' ' -f1 /path/to/downloaded/writfold-x86_64-linux-musl.sha256)
sed -i -e "s/^WRITFOLD_DEFAULT_VERSION=.*/WRITFOLD_DEFAULT_VERSION=\"$v\"/" \
       -e "s/^WRITFOLD_DEFAULT_SHA256=.*/WRITFOLD_DEFAULT_SHA256=\"$sha\"/" install.sh
git diff --stat install.sh          # expect exactly 2 lines changed
```

Then:

1. Set `VERSION` in `scripts/build_pages.py` to the same release and run it. It stops if `install.sh` pins a different version, so the manual steps on the page and the installer cannot disagree.
2. Run `bash scripts/test_install.sh` (offline: a fake release on a local server, an emptied environment, a fake `claude`).
3. Check `sh install.sh --dry-run` shows the new version, and `sh install.sh --no-plugin --prefix "$(mktemp -d)"` installs it and reports the new `writfold --version`.
4. Package and publish as below, then confirm `curl -s https://writfold.dev/install.sh | sha256sum` equals the digest of `_site/install.sh`.

## Social card

`assets/og-image.png` is a 1200×630 card: the folded-W mark on the navy background with the overview headline, rendered from HTML with headless Chromium. When the headline or the release changes, re-render it and update `og:image:alt` on every page to match the card's text.

## Publish with GitHub Pages

1. Review and commit the static source, manifest, packaging script and workflow on `main`. Push only with publication authorization.
2. The repository's Pages source is **GitHub Actions** and its custom domain is **writfold.dev**. `CNAME` alone does not configure Pages. Preserve the existing DNS and domain verification.
3. The `github-pages` environment is protected by the publication approver and limited to `main`. The workflow checks that the nominated full SHA is a commit on `main`; environment approval is the publication boundary, not the manifest.
4. Manually run **Publish reviewed static site** from `main` with the full reviewed site commit SHA. A push alone does not deploy. The workflow checks commit ancestry and content hashes, packages those exact bytes, uploads and deploys. It does not build the product or generate documentation.
5. Check the deployment, HTTPS, apex and `www` behavior, root and anchor routes, a real missing URL, asset caching and external links. Record the site SHA and manifest with the Pages run. Keep the previous approved commit for rollback; dispatch its SHA to republish.

A website deployment does not release or qualify any Writfold build.

## Design

The folded mark, navy and off-white surfaces and teal accent are Writfold's. Amber marks planned material; teal marks what runs. System is the default theme, following the operating system's light or dark setting. The native Theme control offers System, Light and the Paper Dark website palette; `assets/theme.js` stores an explicit choice in local storage, and choosing System clears it. With JavaScript disabled the control stays hidden and the system theme still works. If storage is unavailable, the choice applies to the current page only.

Code panels use static HTML highlighting written by `scripts/highlight.py`, not a client-side parser. They scroll sideways on narrow screens instead of wrapping.

## License

The product and this website use the MIT license. `LICENSE.txt` is included in the published artifact.
