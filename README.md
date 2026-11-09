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

On 8 November 2026 the home and guide status copy added the separately exercised owner-side Rust components (native Omnigraph data path, retained objects, Worktrunk creation, ledger-head decoding and structural procedure admission). The copy states that none is yet connected to a ledger, grant, service or write path.

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

The Weft and Splicery pages include downloadable, executed source examples and accessible inline SVG diagrams. The example changes only `docs_only` from entailed to refuted; `restore_works` remains undetermined and the original file remains unchanged. Both Weft reports are hypothetical, with no grounding or effect authority. The public manifest binds the exact executable/example receipt; it does not qualify owner services.

Highlighting is static HTML, not a client-side parser. Token roles follow Strop's language handovers: Weft predicates are functions; declaration names and labels are variables. Splicery's `@` sigils and `:=` are operators, handle names are variables, and `keep` is a keyword. Code panels use Strop's exact Dark, Paper (light), and Paper Dark palettes. Paper is used instead of Strop Light to retain at least 4.5:1 code contrast. Website chrome keeps its existing colors.

The packaged language-page browser run checked 45 page/width/theme combinations, exact displayed/downloadable source equality, rendered role colors, OS-dark switching, keyboard skip focus, 200% text zoom, disabled JavaScript, and an actual source download. The diagrams retain named titles/descriptions and fit the mobile viewport. These are website checks, not editor-grammar or product qualification.

When an actual pinned installation artifact and exercised scope exist, add qualified installation instructions in `docs.html` immediately after `#assurance`, and link them from the home-page `#docs` section. Update the availability and runtime-status copy at that time against the actual implementation. Keep disposable-data restrictions adjacent to installation commands; do not substitute historical reference commands or speculative downloads.

## Publish with GitHub Pages

1. Review and commit the static source, manifest, packaging script and workflow on `main`. Push only with publication authorization.
2. Configure this repository's Pages source as **GitHub Actions**, and its custom domain as **writfold.dev**. `CNAME` alone does not configure Pages. Preserve existing DNS and domain verification; inspect current records before any change.
3. Protect the `github-pages` environment with the intended publication approver and constrain deployments to `main`. The workflow checks that the nominated full SHA is a commit on `main`; environment approval is the publication-authority boundary, not the manifest.
4. Manually run **Publish reviewed static site** from `main`, supplying the full reviewed site commit SHA. Pinned checkout/upload/deploy actions validate commit ancestry, check content hashes, package those exact static bytes, upload, and deploy. They do not build the product or generate documentation.
5. Verify the deployment receipt, HTTPS certificate/enforcement, apex and `www` behavior, root/anchor routes, a real missing URL, asset caching and external links. Record the site SHA and manifest alongside the Pages run. Retain the prior approved commit for rollback; dispatch its SHA to republish.

Publication is a separate authorized operation. Inspect the GitHub Actions deployment for the nominated site commit and live serving status. A website deployment does not complete product stage P13 or qualify a Rust release.

## Design and content

**8 November 2026 restructure.** After an independent editorial review, the site was reorganized for newcomers. Pages: Overview (`index.html`), How it works (`docs.html`, including architecture), Weft, Splicery, Status (`status.html`: parts table, blocked scenarios, verification, roadmap, dated changelog and FAQ) and Glossary (`glossary.html`). Every page shares one nav order, footer and Open Graph metadata, with a static `assets/og-image.png` rendered from the folded-W polygons. Status caveats now live once on the status page instead of being repeated on every page. The overview's six-step flow is a decorative CSS-animated SVG; it pauses on hover, shows its final frame under `prefers-reduced-motion`, and is hidden below 700px, where the card list carries the content. Each step card has a Runs today, Parts tested or Planned chip. The Splicery page replaces its pipeline diagram with an original/candidate two-pane view whose highlights draw in once, and the Weft page shows its result as a table. Packaged-site checks: every internal link and anchor resolves, the HTML is well-formed with no duplicate IDs, and headless Chromium found no console errors or horizontal overflow on any of the seven pages at 1440px and 360px in light and dark. Keyboard, zoom and Paper Dark checks were not re-run for this change.

**8 November 2026 harness framing.** The overview now presents Writfold as an evidence-and-approval harness underneath a coding agent: know (Writfold retains cited evidence), conclude (Weft checks the plan), change (Splicery prepares, Writfold applies in its own worktree) and record (receipts). The hero carries a decorative agent ↔ harness ↔ repository SVG, hidden below 700px where the copy and four status-chipped cards carry the content. `docs.html` gained a harness section, the glossary gained harness, citation and grant, and the FAQ states that the source repositories are public. Copy keeps the design separate from what runs today. Packaged-site checks: internal links, anchors and IDs; headless Chromium screenshots at 1440px and 360px in light and dark.

**9 November 2026 claims audit.** Every page was checked against the current repositories. Stale "not built" and "tested on its own" wording for approval, apply and recovery now names the trial profile; `docs.html#assurance` became "How we know" (calculus specification, proofs over the shipped Rust for the named kernels, Lean-exported cross-checks, tests) with a one-sentence trust base, and the status-page link moved to `#status-link`. "Proved over the shipped Rust" is used only for Writfold's ledger and grant kernels, Weft's set/verdict/reuse decisions and Splicery's edit rendering; nothing claims Writfold as a whole is verified. Installation instructions, when they exist, still belong immediately after `#assurance`.

**9 November 2026 preview refresh (`v0.1.0-dev.1`).** Every page was re-audited against the tagged source. The site now describes a source-only preview and a cooperating single-user trial that runs end to end. It covers four tools (Tuft added), the README's exact Try-it commands, the newly proved decisions (revocation, recovery outcome, required-check gate) with 20/20 mutants, the adversarial campaign, the latency budget and measurements, Dolt as the interim backend behind a swappable boundary, and a 9 November changelog entry. Following the agent-boundary plan's website wording rules, the pages avoid containment, grounding, corpus, ranking, alpha and installability claims; that plan's dated record governs earlier notes here. The Weft example's context string was renamed and re-executed with the same pinned binary, and the manifest binds that new receipt.

The content below is the original design rationale.

Six compact content sections: introduction, product goals, intended workflow, scribes, implementation status, and documentation. The folded mark, navy/off-white surfaces and teal evidence accent are Writfold's. Omnigraph's public site informed the editorial spacing, crisp monospace metadata, hairline modular structure and explanation through a process sequence; no Omnigraph copy, logo, assets or interactive layout is reproduced. System remains the default, preserving the original OS light/dark appearance. The native Theme control offers System, Light and the companion Paper Dark website palette. The allowlisted local `assets/theme.js` stores explicit choices in local storage; selecting System clears the override. With JavaScript disabled the control stays hidden and the original system theme and folded-W asset selection still work. If storage is unavailable, the control works for the current page without persistence. This website option does not imply a released native product theme.

The product and website use the MIT license, selected by Tarek on 2 November 2026. `LICENSE.txt` is included in the published artifact. The footer adapts Gripsack's attribution and compact status layout, with a development label rather than an invented product release version. Future installation and runnable quickstart content must come from actual pinned artifacts with explicitly qualified experimental limits; the disposable-alpha direction is not itself a release.
