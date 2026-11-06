# Writfold website

A deliberately small, pre-release product introduction for **writfold.dev**. Plain HTML and CSS with a small local theme script; no external fonts, analytics, dependency installation or product build. The rendered source files are the publication input. Folded-W assets are unchanged copies from Writfold's supplied brand handover.

## Serve locally

From this checkout:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/`. This development server exposes repository files; do not bind it to a public interface. It does not emulate GitHub Pages' custom missing-page behavior: inspect `/404.html` directly, then verify an unknown URL after deployment.

## Review and package

Product status copy was updated on 6 November 2026 for an experimental disposable alpha. The site distinguishes the exercised 12 real-process scenarios, 29 invocations and 8 coverage admission tests (control and local artifact paths) from the intended retained-input → Weft assessment → Splicery preparation → Writfold authorization → native worktree effect → durable receipt/recovery flow. The latest owner decision pauses Dolt-specific alpha work to evaluate exact upstream Omnigraph PR #1235 source as a development unblocker, preferring a supported upstream release before publication. No source-build pass, public alpha readiness, production support or automatic fallback is claimed. Public pages expose no private source/evidence paths or private playbook material.

After changing site content, locally regenerate the content manifest and package the already-rendered files:

```sh
python3 scripts/package.py --refresh-manifest
python3 -m http.server 8081 --bind 127.0.0.1 --directory _site
```

`_site/` must not already exist: preserve or remove an earlier artifact explicitly. The packaging script only copies a fixed public allowlist and its SHA-256 manifest. It does not render docs, run Rust, fetch content, or copy repository/private files. Without `--refresh-manifest`, it refuses bytes that differ from the committed manifest. Review manifest changes with the source and commit both. The initial manifest is prepared, not a verification receipt.

For an out-of-tree review without replacing an earlier `_site/`, pass
`--output /absolute/path/to/new-artifact`. The public manifest records the
implementation base commit separately from the exact component-receipt and
binary digests; it does not claim that uncommitted regression work belongs to
that base commit.

Check 360/768/1440px layouts, OS light/dark modes, System/Light/Paper Dark choices and saved overrides across home, guide and missing pages, disabled JavaScript, text zoom, keyboard skip link and focus, all main/footer anchors, every external link, the favicon and `/404.html`. Check the packaged artifact, not only the working tree. The initial desktop/mobile light/dark browser smoke exercised overflow, images, anchor navigation and keyboard skip focus; it is not product qualification.

The six-step home-page diagram uses a semantic ordered list, visible role labels and decorative, non-focusable SVG arrows. It follows existing theme variables and becomes one column on small screens. The 6 November packaged-site browser run exercised home/guide/missing pages at 360/768/1440px in all three theme choices (27 combinations), OS light/dark switching, saved theme navigation, keyboard skip focus, JavaScript-disabled content and 200% text zoom. The zoom check exposed overflowing long headings; emergency word wrapping corrected it without clipping text. This is website evidence, not product qualification.

When an actual pinned installation artifact and exercised scope exist, add qualified installation instructions in `docs.html` immediately after `#assurance`, and link them from the home-page `#docs` section. Update the availability and runtime-status copy at that time against the actual implementation. Keep disposable-data restrictions adjacent to installation commands; do not substitute historical reference commands or speculative downloads.

## Publish with GitHub Pages

1. Review and commit the static source, manifest, packaging script and workflow on `main`. Push only with publication authorization.
2. Configure this repository's Pages source as **GitHub Actions**, and its custom domain as **writfold.dev**. `CNAME` alone does not configure Pages. Preserve existing DNS and domain verification; inspect current records before any change.
3. Protect the `github-pages` environment with the intended publication approver and constrain deployments to `main`. The workflow checks that the nominated full SHA is a commit on `main`; environment approval is the publication-authority boundary, not the manifest.
4. Manually run **Publish reviewed static site** from `main`, supplying the full reviewed site commit SHA. Pinned checkout/upload/deploy actions validate commit ancestry, check content hashes, package those exact static bytes, upload, and deploy. They do not build the product or generate documentation.
5. Verify the deployment receipt, HTTPS certificate/enforcement, apex and `www` behavior, root/anchor routes, a real missing URL, asset caching and external links. Record the site SHA and manifest alongside the Pages run. Retain the prior approved commit for rollback; dispatch its SHA to republish.

Publication is a separate authorized operation. Inspect the GitHub Actions deployment for the nominated site commit and live serving status. A website deployment does not complete product stage P13 or qualify a Rust release.

## Design and content

Six compact content sections: introduction, product goals, intended workflow, scribes, implementation status, and documentation. The folded mark, navy/off-white surfaces and teal evidence accent are Writfold's. Omnigraph's public site informed the editorial spacing, crisp monospace metadata, hairline modular structure and explanation through a process sequence; no Omnigraph copy, logo, assets or interactive layout is reproduced. System remains the default, preserving the original OS light/dark appearance. The native Theme control offers System, Light and the companion Paper Dark website palette. The allowlisted local `assets/theme.js` stores explicit choices in local storage; selecting System clears the override. With JavaScript disabled the control stays hidden and the original system theme and folded-W asset selection still work. If storage is unavailable, the control works for the current page without persistence. This website option does not imply a released native product theme.

The product and website use the MIT license, selected by Tarek on 2 November 2026. `LICENSE.txt` is included in the published artifact. The footer adapts Gripsack's attribution and compact status layout, with a development label rather than an invented product release version. Future installation and runnable quickstart content must come from actual pinned artifacts with explicitly qualified experimental limits; the disposable-alpha direction is not itself a release.
