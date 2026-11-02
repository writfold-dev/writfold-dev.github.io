# Writfold website

A deliberately small, pre-release product introduction for **writfold.dev**. Plain HTML and CSS, no JavaScript, external fonts, analytics, dependency installation or product build. The rendered source files are the publication input. Folded-W assets are unchanged copies from Writfold's supplied brand handover.

## Serve locally

From this checkout:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/`. This development server exposes repository files; do not bind it to a public interface. It does not emulate GitHub Pages' custom missing-page behavior: inspect `/404.html` directly, then verify an unknown URL after deployment.

## Review and package

Product implementation/status copy was checked against private core commit `31b27f8b4577b6a3c692597a7da85eaa12387e5f`. The Omnigraph-first roadmap comes from the owner-supplied version-4 architecture handover, not implemented backend support. Public guide pages explain Writfold's own model without copying private playbook material or linking visitors to inaccessible source. No release, production CLI, current proof run or completed product gate is implied.

After changing site content, locally regenerate the content manifest and package the already-rendered files:

```sh
python3 scripts/package.py --refresh-manifest
python3 -m http.server 8081 --bind 127.0.0.1 --directory _site
```

`_site/` must not already exist: preserve or remove an earlier artifact explicitly. The packaging script only copies a fixed public allowlist and its SHA-256 manifest. It does not render docs, run Rust, fetch content, or copy repository/private files. Without `--refresh-manifest`, it refuses bytes that differ from the committed manifest. Review manifest changes with the source and commit both. The initial manifest is prepared, not a verification receipt.

Check 360/768/1440px layouts, OS light/dark modes, text zoom, keyboard skip link and focus, all main/footer anchors, every external link, the favicon and `/404.html`. Check the packaged artifact, not only the working tree. The initial desktop/mobile light/dark browser smoke exercised overflow, images, anchor navigation and keyboard skip focus; it is not product qualification.

## Publish with GitHub Pages

1. Review and commit the static source, manifest, packaging script and workflow on `main`. Push only with publication authorization.
2. Configure this repository's Pages source as **GitHub Actions**, and its custom domain as **writfold.dev**. `CNAME` alone does not configure Pages. Preserve existing DNS and domain verification; inspect current records before any change.
3. Protect the `github-pages` environment with the intended publication approver and constrain deployments to `main`. The workflow checks that the nominated full SHA is a commit on `main`; environment approval is the publication-authority boundary, not the manifest.
4. Manually run **Publish reviewed static site** from `main`, supplying the full reviewed site commit SHA. Pinned checkout/upload/deploy actions validate commit ancestry, check content hashes, package those exact static bytes, upload, and deploy. They do not build the product or generate documentation.
5. Verify the deployment receipt, HTTPS certificate/enforcement, apex and `www` behavior, root/anchor routes, a real missing URL, asset caching and external links. Record the site SHA and manifest alongside the Pages run. Retain the prior approved commit for rollback; dispatch its SHA to republish.

Publication is a separate authorized operation. Inspect the GitHub Actions deployment for the nominated site commit and live serving status. A website deployment does not complete product stage P13 or qualify a Rust release.

## Design and content

Six compact content sections: introduction, product goals, intended workflow, scribes, implementation status, and documentation. The folded mark, navy/off-white surfaces and teal evidence accent are Writfold's. Omnigraph's public site informed the editorial spacing, crisp monospace metadata, hairline modular structure and explanation through a process sequence; no Omnigraph copy, logo, assets or interactive layout is reproduced. The site follows the reader's system theme and does not require a theme-control script.

The product and website use the MIT license, selected by Tarek on 2 November 2026. `LICENSE.txt` is included in the published artifact. The footer adapts Gripsack's attribution and compact status layout, with a development label rather than an invented product release version. Product repository visibility remains private. Future installation and runnable quickstart content must come from actual qualified release artifacts.
