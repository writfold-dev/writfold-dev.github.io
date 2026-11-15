#!/usr/bin/env python3
"""Write the site's HTML pages from shared parts, with authoring-time highlighting.

Run `python3 scripts/build_pages.py` after changing copy here, review the HTML it
writes, then package. The committed HTML stays the publication input: nothing here
runs at publish time, fetches anything or reads the product.
"""
import sys
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import re
from html import unescape
import diagrams
from highlight import highlight
from term_glyphs import uncovered

SITE = Path(__file__).resolve().parent.parent
VERSION = "v0.5.0-dev.7"
RELEASED = "15 November 2026"
RELEASES = "https://github.com/writfold-dev/writfold/releases/"
REL = RELEASES + "tag/" + VERSION
ALT = ("The folded-W Writfold mark on navy with the headline: Project memory in Git that says when it is stale. "
       f"Below it: Git-native project continuity for coding agents. Preview {VERSION}.")
NAV = [("/", "Overview"), ("/how.html", "How it works"), ("/status.html", "Status")]

PRELOAD = '\n  <link rel="preload" href="/assets/term-Regular.woff2" as="font" type="font/woff2" crossorigin>'

def head(title, desc, path, frames=False):
    url = "https://writfold.dev/" + path
    preload = PRELOAD if frames else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Writfold">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://writfold.dev/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{ALT}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#101922" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#F7F8F4" media="(prefers-color-scheme: light)">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">{preload}
  <script src="/assets/theme.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
'''

def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''  <header class="site-header wrap">
    <a class="wordmark" href="/" aria-label="Writfold home"><picture><source srcset="/assets/writfold-icon.svg" media="(prefers-color-scheme: light)"><img src="/assets/writfold-icon-dark.svg" width="40" height="40" alt=""></picture><span>writfold</span></a>
    <nav aria-label="Main navigation">{links}<a href="https://github.com/writfold-dev">GitHub</a></nav>
    <label class="theme-control" hidden>Theme <select id="theme" aria-describedby="theme-note"><option value="system">System</option><option value="light">Light</option><option value="paper-dark">Paper Dark</option></select><span id="theme-note" class="visually-hidden">Your choice is remembered in this browser.</span></label>
  </header>
'''

FOOTER = '''  <footer class="site-footer wrap">
    <div class="footer-line">
      <span class="footer-credit"><span class="footer-mark" aria-hidden="true"></span> © 2026 <a href="https://tknawara.dev">Tarek Nawara</a></span>
      <a href="/how.html">How it works</a><a href="/status.html">Status</a><a href="/LICENSE.txt">MIT license</a><a href="https://github.com/writfold-dev">GitHub</a><a href="https://github.com/writfold-dev/writfold-dev.github.io">Website source</a>
      <span class="footer-state">Pre-release</span>
    </div>
    <p class="footer-note">No accounts, no analytics.</p>
  </footer>
</body>
</html>
'''

def page(name, title, desc, current, main):
    frames = 'class="term-frame' in main
    (SITE / name).write_text(head(title, desc, "" if name == "index.html" else name, frames) + header(current) + main + FOOTER, encoding="utf-8")

def pre(label, text, lang="session"):
    return (f'<pre class="code-panel" tabindex="0" aria-label="{label}"><code>'
            f'{highlight(text.strip(chr(10)), lang)}</code></pre>')

def panel(label, text, caption=None, lang="session", chip="Example"):
    cap = f'<figcaption><span class="chip chip-today">{chip}</span> {caption}</figcaption>' if caption else ""
    return f'<figure class="example">{cap}{pre(label, text, lang)}</figure>'

def pill(text, kind):
    return f'<span class="pill pill-{kind}">{text}</span>'

ANSWER = f'''<figure id="example" class="visual">
        <figcaption><span class="chip chip-parts">Illustration</span> Invented content; the parts are what <code>kb why</code> prints. The evidence is code pinned at a commit, flagged because those lines have moved.</figcaption>
        <div class="card answer">
          <p class="card-cmd"><code><span class="syntax-prompt">$ </span>writfold kb why "batch writes"</code></p>
          <p class="answer-head">{pill("accepted", "ok")} <strong>Batch ledger writes</strong> <span class="src">proposals/decision/2026-11-02-batch-writes.md:4</span></p>
          <dl class="answer-rows">
            <div><dt>Decided</dt><dd>by api-review on 2026-11-05 <span class="src">:9</span></dd></div>
            <div><dt>Why</dt><dd>One transaction per 500 rows keeps replay under a minute. <span class="src">:18</span></dd></div>
            <div><dt>Evidence</dt><dd><code>demo-api src/ledger.rs:40-72</code> {pill("moved → 44-76", "warn")} <span class="src">:25</span></dd></div>
          </dl>
          <ul class="card-foot"><li>31 of 31 records examined</li><li>nothing omitted</li><li class="warn">1 source stale</li><li>index fresh</li></ul>
        </div>
      </figure>'''

def drafts():
    def col(state, kind, digest, checks):
        items = "".join(f'<li class="{c}"><code>{n}</code><span>{t}</span></li>' for c, n, t in checks)
        return f'<div class="card"><p class="answer-head">{pill(state, kind)} <strong>PR comment</strong> <span class="src">external · harbor#42 · {digest}</span></p><ul class="checks">{items}</ul></div>'
    return ('''<figure class="visual"><figcaption><span class="chip chip-today">From real output</span> One draft, before and after the fix. The checks are tied to the draft&rsquo;s bytes, so the edit made the first three receipts stale and the draft was checked again.</figcaption><div class="status-grid">'''
            + col("blocked", "warn", "bb69f10c8fd9", [("ok", "paragraphs.bounded", "satisfied: at most 150 words per paragraph"),
                                      ("bad", "references.denied", "failed: line 3 matches <em>internal-host</em> and <em>ticket</em>"),
                                      ("ok", "claims.cited-fresh", "satisfied: 0 citation tokens")])
            + col("ready", "ok", "f5d111e329c7", [("ok", "paragraphs.bounded", "satisfied"), ("ok", "references.denied", "satisfied: 2 rules for external"),
                                  ("ok", "claims.cited-fresh", "satisfied: 0 citation tokens")])
            + "</div></figure>")

# Captured terminal frames. Each is the <span> fragment the capture tool wrote, kept in
# scripts/frames/<name>.html. To publish a new capture, replace the file, adjust its label
# here if the picture changed, and run this script again.
FRAMES = Path(__file__).parent / "frames"
FRAME_LABELS = {
    "home": "writfold watch in its calm default frame: the runs, the plan map of the selected run, and the inspector for its next step",
    "how": "writfold watch after pressing d: the same run with every recorded detail, receipts and timestamps",
}

def frame(name):
    body = (FRAMES / f"{name}.html").read_text(encoding="utf-8").rstrip("\n")
    # Every cell must come from the Writfold Term subset font, or the columns drift.
    text = unescape(re.sub(r"<[^>]+>", "", body))
    stray = uncovered(text)
    if stray:
        raise SystemExit(f"scripts/frames/{name}.html uses characters outside the terminal font: "
                         + " ".join(f"U+{ord(c):04X}" for c in stray) + "; add them to scripts/term_glyphs.py and run scripts/build_term_font.py")
    styles = set(re.findall(r"font-(?:style|weight):[^;\"]+", body)) - {"font-weight:700"}
    if styles:
        raise SystemExit(f"scripts/frames/{name}.html uses {sorted(styles)}; the terminal font has regular and bold only")
    # The widest row, in cells: the stylesheet sizes the text so that many cells fit the column.
    cols = max(len(line) for line in text.split("\n"))
    return f'<pre class="term-frame" style="--cols:{cols}" tabindex="0" aria-label="{FRAME_LABELS[name]}"><code>{body}</code></pre>'

def flow_figure(pfx, caption):
    return (f'<figure class="diagram-figure">{diagrams.flow(pfx)}'
            f'<figcaption class="fine-print">{caption}</figcaption></figure>')

def spine_figure(pfx):
    return (f'<figure class="diagram-figure spine-figure"><p class="figure-lead"><span class="chip chip-today">From real output</span> '
            f'One run&rsquo;s plan, drawn from what <code>plan status</code> prints for a demo repository.</p>{diagrams.spine(pfx)}</figure>')

# ---------------------------------------------------------------- index
GUIDE = "https://github.com/writfold-dev/writfold/blob/main/docs/guide/"

def guide(page, label):
    return f'<a href="{GUIDE}{page}.md">{label}</a>'

def more(*links, lead="Full skeleton"):
    '''The one link out of a section: the matching guide in the Writfold repository.'''
    return f'<p class="guide-link"><span aria-hidden="true">→</span> {lead}: {" and ".join(links)}</p>'

INSTALL = f'''base={RELEASES}download/{VERSION}
curl -LO "$base/writfold-x86_64-linux-musl" -LO "$base/writfold-x86_64-linux-musl.sha256"
echo "$(cut -d' ' -f1 writfold-x86_64-linux-musl.sha256)  writfold-x86_64-linux-musl" | sha256sum -c
install -m 755 writfold-x86_64-linux-musl ~/.local/bin/writfold

claude plugin marketplace add writfold-dev/writfold
claude plugin install writfold@writfold'''

DESC_HOME = ("Project memory in Git for coding agents. A fresh session answers why, status, tracker and impact questions; "
             f"every answer names its source and says when it moved. Preview: {VERSION}.")
index = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="hero-title">
      <p class="eyebrow">Git-native project continuity for coding agents</p>
      <h1 id="hero-title">Project memory in Git<br><span>that says when it is stale.</span></h1>
      <p class="lede">Every new agent session starts without the project&rsquo;s history. With Writfold, a fresh session on any machine can answer four questions, and each answer names the file and commit it came from.</p>
      <ul class="questions">
        <li>Why did we decide X?</li>
        <li>Where do we stand on Y?</li>
        <li>What is the tracker item for Z?</li>
        <li>What does changing X touch?</li>
      </ul>
      <div class="actions"><a class="button" href="#try">Try it <span aria-hidden="true">↓</span></a><a class="text-action" href="/how.html">How it works <span aria-hidden="true">→</span></a></div>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">{VERSION}</a>, {RELEASED}. One static Linux x86_64 binary. <a href="/status.html">Status and roadmap</a></span></p>
    </section>

    <section id="watch" class="section" aria-labelledby="watch-title">
      <div class="section-heading"><p class="eyebrow">The plan, as a map</p><h2 id="watch-title">See where the work stands</h2><p>A run has a plan. Each step owes gates: small checks whose receipts are tied to the exact bytes they checked. <code>writfold watch</code> draws it in your terminal.</p></div>
      <figure class="example"><figcaption><span class="chip chip-today">Captured</span> <code>writfold watch</code> on a test-fixture knowledge base; its run, steps and receipts were written through the <code>kb</code> verbs.</figcaption>{frame("home")}</figure>
      <dl class="callouts">
        <div><dt><code>✓</code> Done, and still true</dt><dd>A step is recorded as done only when every gate it owes is met.</dd></div>
        <div><dt><code>!</code> Done, but something moved</dt><dd>A later edit changed the bytes a gate checked. The step stays done and is flagged.</dd></div>
        <div><dt><code>▶</code> Next</dt><dd>The step to pick up, from the record. It is not a claim that an agent is working.</dd></div>
      </dl>
      <p class="fine-print">Read-only: it shows what the records say and starts no check.</p>
      {more('<a href="/how.html#plan">how a run works</a>', guide("watch", "the watch guide"), lead="More")}
    </section>

    <section id="answer" class="section" aria-labelledby="answer-title">
      <div class="section-heading"><p class="eyebrow">One answer</p><h2 id="answer-title">Every line names its source</h2></div>
      {ANSWER}
    </section>

    <section id="git" class="section" aria-labelledby="git-title">
      <div class="section-heading"><p class="eyebrow">No server</p><h2 id="git-title">Plain records in Git, and one binary</h2></div>
      <div class="three-up">
        <div class="capability"><h3>Git is the source of truth</h3><p>Decisions, tickets, runs and receipts are Markdown and JSON files. Writes are left uncommitted for you to review.</p></div>
        <div class="capability"><h3>The index is derived</h3><p>A local SQLite file, rebuilt from Git whenever needed. A new machine needs <code>git clone</code> and the binary.</p></div>
        <div class="capability"><h3>It records and reports</h3><p>Your agent keeps its own loop and model. Gates block nothing unless you add a guard rule.</p></div>
      </div>
    </section>

    <section id="try" class="section" aria-labelledby="try-title">
      <div class="section-heading"><p class="eyebrow">Try it</p><h2 id="try-title">Download, verify, install the plugin</h2><p>Linux x86_64 or WSL2.</p></div>
      {pre("Download and install commands", INSTALL, "shell")}
      <p class="fine-print">The Claude Code plugin adds a project brief and the plan position at session start. Single user, cooperating agents, local clones only; nothing is fetched. Setup is in the <a href="https://github.com/writfold-dev/writfold#readme">README</a>.</p>
      <p class="boundary">Pre-release: formats and verbs may still change. <a href="/status.html#today">What runs today</a>, <a href="/status.html#next">what is planned</a>, and {guide("assurance", "what is proved and tested")}.</p>
    </section>
  </main>
'''
page("index.html", "Writfold — Git-native project continuity for coding agents", DESC_HOME, "/", index)

# ---------------------------------------------------------------- how
REAL = "Real output from a demo repository; <code>…</code> shortens paths and marks rows left out."
WHY = '''$ writfold kb why "batch ledger writes"
decision proposal/decision/2026-03-02-batch-ledger-writes [accepted] Batch ledger writes in the API @proposals/…/proposal.md:5
  decided: by ops-review on 2026-03-09 @proposals/…/proposal.md:11
  why: Batching keeps the flush under the store's fsync budget. @proposals/…/proposal.md:25
  cite: code:demo-service:src/batch.rs:2-4 [unverifiable] @proposals/…/proposal.md:31 !unverifiable
…
# coverage=complete records=48/48 shown=4 omitted=0 stale=2 kb=4ba5227faf95+dirty:21 index=fresh cursor=none q=dedb9f082fd7'''
RESEARCH = '''$ writfold kb find "harbr-api"                    # records by words, a partial ID or a typo
$ writfold kb impact harbor-db --direction in     # what a change touches, and how far it walked
$ writfold tuft run q.tuft --repo . --cite        # exact text in code, each row with a citation
$ writfold kb record link depends-on quay-worker harbor-db \\
    --evidence harbor-api@4be03f7897b691715114a229ab1acc307f5de90f:src/ledger.rs:3-5
$ writfold kb gate run backfilled                 # the research step's check: did it write back?'''
NEWRUN = '''$ writfold kb checkpoint --new-run --project harbor --task "Retry ledger connections" \\
    --note "Plan: wrap every open(url()) in with_retry; then review and ship."
$ cat .writfold/plans/fix.toml
%toml
schema = "writfold-plan/1"
name = "fix"
description = "change the code, then ship it"
steps = [
  "implement: unit",
  "ship: wording",
]
$ writfold kb plan set fix
step research#1/research [current] owes: backfilled [open] @runs/run-…/plan/splice-research.1.json:1
  next: writfold kb gate run backfilled
step fix#2/implement [later] gates: unit @runs/run-…/plan/splice-fix.2.json:1
step fix#2/ship [later] gates: wording @runs/run-…/plan/splice-fix.2.json:1
step reflect#3/reflect [later] gates: reflected, reflection @runs/run-…/plan/splice-reflect.3.json:1
…'''
EXECUTE = '''$ writfold kb edit apply retry.spl --dry-run      # the preview diff; nothing written
$ writfold kb edit apply retry.spl                # every file or none, with an edit receipt
$ writfold kb gate run unit                       # run the command, keep a receipt
$ writfold kb plan advance                        # record the step as done, or refuse (exit 3) and say what is owed
$ writfold kb plan use review                     # a skill's line: splice its steps in before the current step
$ writfold kb plan status
step research#1/research [done] backfilled [satisfied] @runs/run-…/plan/done-research.1~research.json:1
  done: recorded 2026-11-13T01:19:13Z
step fix#2/implement [done] unit [stale] @runs/run-…/plan/done-fix.2~implement.json:1 !stale
  why: no longer holds: unit [stale] (done stays done; list the gate again on a later step if it must hold there)
  done: recorded 2026-11-13T01:19:17Z
step fix#2/ship/review#1/read-diff [done] no gates @runs/run-…/plan/done-fix.2~ship~review.1~read-diff.json:1
  done: recorded 2026-11-13T01:19:17Z
step fix#2/ship/review#1/findings [current] owes: findings [open] @runs/run-…/plan/splice-fix.2~ship~review.1.json:1
  next: writfold kb gate attest findings --statement TEXT --by WHO
step fix#2/ship [later] gates: wording @runs/run-…/plan/splice-fix.2.json:1
step reflect#3/reflect [later] gates: reflected, reflection @runs/run-…/plan/splice-reflect.3.json:1
…'''
REFLECT = '''$ writfold kb checkpoint --note "reflection: Wrapped three open(url()) calls in with_retry; unit passed on ledger.rs and went stale after the audit.rs edit. Learned: audit.rs opens its own connection. Change: list unit again on the ship step."
$ writfold kb propose ticket HBR-130 --title "Replay is slow after a restart" --assets harbor-api
proposal 16a41fbba45340f7 [pending] ticket HBR-130: Replay is slow after a restart @…/kb/.git/writfold/proposals/16a41fbba45340f7.json !proposal
…
$ writfold kb gate run reflected                  # a reflection entry, and a proposal or "no proposal"
$ writfold kb gate attest reflection --statement "Covers done, learned, change and backfill" --by agent
$ writfold kb plan advance                        # the last step: the plan is complete
$ writfold kb proposals accept 16a41fbba45340f7   # your call; the record goes through the ordinary write
ticket HBR-130 [todo] Replay is slow after a restart @ktlo/2026/hbr-130-replay-is-slow-after-a-restart.md:5
…'''
HOOK = '''KB is 2 commits behind origin/main (never fetched); run git pull
Writfold KB brief (`writfold kb brief`). Rows end in their source; re-check any row with a ! flag before relying on it.
…
Plan position (`writfold kb plan status`) for run run-…: step 3/5
…
step fix#2/implement [current] owes: unit [stale] @runs/run-…/plan/splice-fix.2.json:1
  next: writfold kb gate run unit

Inbox (local only; nothing here is in the KB until confirmed or accepted):
proposal 64ebdafd4dd0a8ed 2026-11-13T01:20:14Z run=run-… ticket HBR-133: Ledger retry count is fixed at three
  review: writfold kb proposals show ID (accept only when the user asks)'''

how = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="how-title">
      <p class="eyebrow">How it works</p>
      <h1 id="how-title">Four stages.<br><span>A record of each.</span></h1>
      <p class="lede">Each part is two sentences, one example and a link to its guide. Everything runs in the preview; the one planned item is marked.</p>
      <nav class="actions" aria-label="Page sections"><a href="#kb">Knowledge base</a><a href="#research">1 Research</a><a href="#plan">2 Plan</a><a href="#gates">Gates</a><a href="#execute">3 Execute</a><a href="#watch">Watch</a><a href="#deliver">4 Deliver</a><a href="#reflect">Reflect</a><a href="#plugin">Plugin</a></nav>
      {flow_figure("hf", f"Each stage writes back to the knowledge base. Everything drawn here runs in {VERSION}.")}
    </section>

    <section id="kb" class="section" aria-labelledby="kb-title">
      <div class="section-heading"><p class="eyebrow">The base</p><h2 id="kb-title">Records in Git, checked on demand</h2><p>The knowledge base is a Git repository of Markdown and JSON: decisions, tickets, assets, their links and one folder per run. Every row of an answer ends in its source, and <code>kb check</code> re-checks citations, the index, gate evidence and the plan in one summary.</p></div>
      {panel("kb why output", WHY, REAL)}
      {more(guide("kb-layout", "the knowledge base layout"), guide("validation", "validation, flag by flag"))}
    </section>

    <section id="research" class="section" aria-labelledby="research-title">
      <div class="section-heading"><p class="eyebrow">Stage 1 / Research</p><h2 id="research-title">Ask the knowledge base, or search the code</h2><p>The <code>kb</code> verbs answer from what the project already knows, and a Tuft search finds exact text in code at one pinned commit. With <code>--cite</code> each row carries a citation, and in a run with a plan the required <code>research</code> step passes only once it wrote a record, a citation or a retrieval receipt.</p></div>
      {panel("Research commands", RESEARCH)}
      {more(guide("feeding-back", "what each stage writes back"))}
    </section>

    <section id="plan" class="section" aria-labelledby="plan-title">
      <div class="section-heading"><p class="eyebrow">Stage 2 / Plan</p><h2 id="plan-title">Start a run, set its plan</h2><p>A run records the task, the repository, branch, worktree and base commit, and <code>plan set</code> copies a template&rsquo;s steps into it. Each step names the gates it owes; Writfold records the steps and schedules nothing.</p></div>
      {spine_figure("sp")}
      {panel("Starting a run and setting its plan", NEWRUN, "The <code>research</code> and <code>reflect</code> steps come from <code>.writfold/plans/required.toml</code>, which joins every plan. " + REAL)}
      {more(guide("run-graph", "the run graph"))}
    </section>

    <section id="gates" class="section" aria-labelledby="gates-title">
      <div class="section-heading"><p class="eyebrow">The thread</p><h2 id="gates-title">Who owes a gate, and what meets it</h2><p>A gate is a command with the paths it covers, a statement someone makes, or a check of the run&rsquo;s own records. Evidence is tied to exact bytes, so a change makes the gate owed again; gates report and block nothing on their own, and receipts are tracked files, not signatures.</p></div>
      <figure class="diagram-figure">{diagrams.gates("wg")}</figure>
      <p class="fine-print">A step can also owe a Weft assessment, met only when the check is entailed from assumptions whose citations hold.</p>
      {more(guide("gates", "every gate class, with examples"), guide("assurance", "what is proved, tested and trusted"))}
    </section>

    <section id="execute" class="section" aria-labelledby="execute-title">
      <div class="section-heading"><p class="eyebrow">Stage 3 / Execute</p><h2 id="execute-title">Edit, check, advance</h2><p>The agent edits the run&rsquo;s worktree with Splicery recipes or ordinary tools, and any gate whose scope covers the change is owed again. <code>plan advance</code> records the current step as done only when each of its gates is met, and a skill adds its own steps with <code>plan use</code>.</p></div>
      {panel("Execute commands and plan status", EXECUTE, REAL)}
      <p class="fine-print">A done step whose gate later goes stale is flagged <code>!stale</code> and stays done. <code>plan skip --reason TEXT --by WHO</code> closes a step without calling it done.</p>
      {more(guide("run-graph", "steps, splicing, stale and merged clones"), guide("skills", "skills that splice"))}
    </section>

    <section id="watch" class="section" aria-labelledby="watch-title">
      <div class="section-heading"><p class="eyebrow">Watching the run</p><h2 id="watch-title">The plan as a map</h2><p><code>writfold watch</code> draws the run&rsquo;s plan in a terminal, with skills spliced in as nested groups and an inspector for the selected step. It opens calm: text only on the next step and the selected row. <code>d</code> shows every detail, receipts included, and <code>?</code> holds the marks. Every state comes from a <code>kb</code> verb; there is no key that writes, and it never starts a check.</p></div>
      <figure class="example"><figcaption><span class="chip chip-today">Captured</span> <code>writfold watch</code> after <code>d</code>, on a test-fixture knowledge base; its run, splices, steps, receipts and covers were written through the <code>kb</code> verbs.</figcaption>{frame("how")}</figure>
      <p class="fine-print"><code>▶</code> marks the recorded position, not a claim that an agent is working; the view adds no percentage or time estimate.</p>
      {more(guide("watch", "watching a run"), lead="Keys, layouts, refresh and themes")}
    </section>

    <section id="deliver" class="section" aria-labelledby="deliver-title">
      <div class="section-heading"><p class="eyebrow">Stage 4 / Deliver</p><h2 id="deliver-title">Drafts, checked. Nothing sent.</h2><p><code>kb deliver prepare</code> keeps the exact text of a PR comment or Slack summary in the run, and <code>deliver check</code> checks those bytes: paragraph length, references the audience must not see, and whether every citation is still fresh. Writfold has no network code, so posting stays with you or your agent.</p></div>
      {drafts()}
      <p class="fine-print">The checks are mechanical: they do not judge tone or truth. An optional Claude Code hook, off unless configured, can deny a listed publishing command until a ready draft holds the exact bytes: a guard, not enforcement.</p>
      <p class="fine-print"><span class="chip chip-planned">Planned</span> A delivery mode as a plan step&rsquo;s gate.</p>
      {more(guide("delivery-modes", "delivery modes, your own modes, deny lists and the guard"))}
    </section>

    <section id="reflect" class="section" aria-labelledby="reflect-title">
      <div class="section-heading"><p class="eyebrow">Before the run ends</p><h2 id="reflect-title">Reflect, propose, close</h2><p>The required <code>reflect</code> step passes only when the run holds a <code>reflection:</code> entry and a proposal or an explicit <code>no proposal</code>. A proposal is a <code>record</code> call not yet made, and only you accept it.</p></div>
      {panel("Closing a run", REFLECT, REAL)}
      <p class="fine-print">The check shows that a reflection was written, not that it is good. The bundled <code>writfold:evaluate</code> skill can walk this step and never accepts a proposal itself.</p>
      {more(guide("feeding-back", "proposals and the reflection checks"), guide("skills", "the evaluate skill"))}
    </section>

    <section id="plugin" class="section" aria-labelledby="plugin-title">
      <div class="section-heading"><p class="eyebrow">In Claude Code</p><h2 id="plugin-title">The plan position at session start</h2><p>The plugin puts the brief, the plan position and an inbox into a new session with no tool call, and the plan position again after a compaction. It reads local files and refs only and runs no model.</p></div>
      {panel("Session-start context", HOOK, "What session start adds, from a demo repository; <code>…</code> marks rows left out.", "output", "From real output")}
      {more(guide("hooks", "hooks"), guide("skills", "skills"))}
      <p class="fine-print">Ready to try it? <a href="/#try">Download the preview</a>, or see <a href="/status.html">what runs and what is next</a>.</p>
    </section>
  </main>
'''
page("how.html", "How it works — Writfold",
     "The Writfold flow stage by stage: research, plan, execute, deliver. Two sentences, one example and a link to the full guide for each.",
     "/how.html", how)

# ---------------------------------------------------------------- status
README = "https://github.com/writfold-dev/writfold#readme"
def row(href, title, text):
    return f'<a href="{href}"><span><strong>{title}</strong><small>{text}</small></span><span aria-hidden="true">→</span></a>'
# The one list of what runs; the overview and How it works link here.
TODAY = "".join([
    row(GUIDE + "kb-layout.md", "Read verbs", "<code>brief | context | why | status | find | match | impact | uses | timeline | resume | runs</code>. Every row names its source"),
    row(GUIDE + "feeding-back.md", "Write verbs and proposals", "<code>checkpoint</code>, <code>record</code>, <code>status --set</code>, <code>cite make</code>, <code>observe</code>. <code>propose</code> queues a record until you accept or drop it"),
    row(GUIDE + "validation.md", "Citations, the index and <code>kb check</code>", "<code>stale</code> reports each citation as fresh, moved, changed or gone; <code>check</code> adds the index, gates and the plan"),
    row(GUIDE + "gates.md", "Gates", "<code>gate run | status | verify | lines | attest | waive | cover</code>. Receipts pinned to exact bytes; a timeout or crash is never a pass"),
    row(GUIDE + "hooks.md#guard-rules", "Guard rules", "A rule denies or asks about a command or tool until the run&rsquo;s gates are met. A guard, not enforcement"),
    row(GUIDE + "checkers.md", "External checkers", "Programs on your <code>PATH</code> that <code>kb stale</code> asks about citation kinds Git cannot check"),
    row(GUIDE + "run-graph.md", "The run graph", "<code>plan set | use | status | advance | skip</code>. Templates, skills that splice steps in, and flags for stale gates and merged clones"),
    row(GUIDE + "run-graph.md#required-steps", "Required steps and run-record checks", "Start and end templates join every plan; their checks judge the run&rsquo;s own records"),
    row(GUIDE + "gates.md#weft-assessed-gates", "Weft assessed gate", "A step can require a Weft assessment; a hypothetical entailment does not meet it"),
    row(GUIDE + "delivery-modes.md", "Delivery drafts and your own modes", "<code>deliver prepare | check | status | attest | waive</code>. Checks tied to the draft&rsquo;s bytes. Nothing is sent"),
    row(GUIDE + "feeding-back.md", "Tuft and Splicery in a run", "<code>tuft run --cite</code> adds citations and a retrieval receipt; <code>edit apply | recover</code> replays recipes and keeps an edit receipt"),
    row(GUIDE + "hooks.md", "Claude Code plugin", "The brief, the plan position and an inbox at session start; the plan position again after compaction; checkpoint drafts and two skills"),
    row(GUIDE + "assurance.md", "Proofs of three kernels", "Lean proofs over the shipped Rust for the run-graph, gate and assessed-gate decisions. Parsers, file reads and globs are tested, not proved"),
    row(GUIDE + "assurance.md#model-checked", "A model of the run graph", "Checked with TLC at small bounds; the widest run was stopped unfinished with no violation found. Evidence about the design, not a refinement of the Rust"),
    row("/how.html#watch", "<code>writfold watch</code>", "A read-only terminal view: the run&rsquo;s plan as a map with an inspector, and its gates, inbox, guard rules and timeline. It never runs a check"),
])
def step(title, text, chip):
    cls = {"Done": "chip-today", "Next": "chip-progress", "Planned": "chip-planned", "Deferred": "chip-planned", "Not planned": "chip-parts"}[chip]
    return f'<li><div><h3>{title}</h3><p>{text} <span class="chip {cls}">{chip}</span></p></div></li>'
ROAD = "".join([
    step("The four questions", "Read and write verbs, the index, pinned citations, external checkers and the Claude Code plugin.", "Done"),
    step("Runs, gates and delivery drafts", "Receipts tied to exact bytes, instruction and checklist gates, Splicery edits, delivery drafts and your own modes.", "Done"),
    step("The run graph, guards and proposals", "Plans with splicing and required steps, guard rules, proposals, the closing reflection, and proofs of three decision kernels.", "Done"),
    step("<code>writfold watch</code> and Tuft search", "The plan map with an inspector and a calm default frame; Tuft with a one-line search, several repositories and symbols.", "Done"),
    step("One week of real use", "Count what the checks caught, and what was waived, before adding more.", "Next"),
    step("Check receipts other machines can read", "A tracked record of what a checker found, so a machine without the checker or its credentials can read when a citation was last checked.", "Planned"),
    step("A delivery mode as a step&rsquo;s gate", "A plan step that owes a checked draft.", "Planned"),
    step("Trailer and tracker edges, and <code>--at</code>", "Links read from commit trailers and tracker references, and answers as of a given commit.", "Planned"),
    step("An MCP server", "Deferred until a harness without a shell needs one. The CLI and the plugin are the interface.", "Deferred"),
    step("A governed profile", "Authority levels, exception routes and signing. Writfold stays single user with cooperating agents.", "Not planned"),
])
def rel(version):
    return f'Preview <a href="{RELEASES}tag/{version}">{version}</a>'
LOG = "".join(f"<li><time>{d}</time><p>{t}</p></li>" for d, t in [
    ("15 Nov 2026", f'{rel(VERSION)}: <code>writfold watch</code> shows a calm frame by default: text follows the next step and the cursor, <code>d</code> shows every detail, and the header, tabs and footer are chips. The site is shorter and leads with the plan map.'),
    ("15 Nov 2026", f'{rel("v0.5.0-dev.6")}: the plan map in <code>writfold watch</code>, with nested splice groups, a glyph and gate chips per step, an inspector, and the clay themes.'),
    ("14 Nov 2026", f'{rel("v0.5.0-dev.5")}: run progress in <code>writfold watch</code>: plan steps with gates and checklist items, the inbox, guard rules and a timeline.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.4")}: Tuft for everyday search: <code>tuft grep</code>, branch names resolved to commits, several repositories, a marked working-tree mode and ctags symbols.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.3")}: <code>kb observe</code>, <code>kb repos</code>, several checklist items covered in one call, proposals kept in the knowledge base, and path-scoped guard rules.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.2")}: external checkers for citation kinds Git cannot check, decision states bound to what Writfold checks, and citations followed through renames with edits.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.1")}: guard rules, checklist gates covered item by item, per-kind citation lifetimes, and the <code>--json</code> envelope documented.'),
    ("13 Nov 2026", f'{rel("v0.4.0-dev.1")}: the run graph with splicing and required steps, instruction gates, your own delivery modes, proposals, <code>kb check</code>, the Weft assessed gate, and Lean proofs of three kernels.'),
    ("12 Nov 2026", f'The site is shorter: full file layouts, configuration and output moved to the <a href="{GUIDE}README.md">guides</a>.'),
    ("12 Nov 2026", f'{rel("v0.3.0-dev.1")}: gates, Splicery edits in a run, <code>writfold watch</code>, delivery drafts and an optional guard hook.'),
    ("12 Nov 2026", f'{rel("v0.2.0-dev.1")}: the <code>kb</code> read and write verbs, the index, citations checked for staleness, and the Claude Code plugin.'),
    ("11 Nov 2026", "Mission set: Git-native project continuity for coding agents."),
])
def faq(q, a): return f"<details><summary>{q}</summary><p>{a}</p></details>"
FAQ = "".join([
    faq("Can I use Writfold today?", 'Yes, as a preview: <a href="/#try">download the binary and install the plugin</a>. Single user, cooperating agents, local clones (plus any external checkers you install), Linux x86_64 or WSL2.'),
    faq("Does it need a server or a database?", "No. One static binary, records in Git, and a local index that Writfold derives and can always rebuild."),
    faq("Does Writfold run or schedule my agent?", "No. It records the plan and what met each gate. The agent reads the current step, does the work its own way and asks to advance. No hook runs a model, and nothing is posted: delivery drafts stay in the run."),
    faq("Can an agent skip a gate or a step?", "Yes. Gates and steps record what was checked and report whether it still holds; on their own they block nothing, so a gate never run shows as open and a skipped step shows as skipped, with a reason and a name. A guard rule you add can deny or ask about a command such as <code>git commit</code> until the gates are met; it is a guard, not enforcement, and only sees the tool calls Claude Code shows it."),
    faq("Is it formally verified?", f'In part. Three decision kernels (the run graph, gate obligations and the Weft assessed gate) are proved in Lean over an Aeneas translation of the Rust that ships; the proofs trust that translation and the Lean kernel. The write protocol and the run graph are model-checked with TLC at small bounds, not proved: the models are hand-written evidence about the design, not a refinement of the Rust, and the widest run-graph configuration was stopped unfinished with no violation found. The rest (parsers, file and Git reads, scope globs) is tested. The numbers and limits are in {guide("assurance", "the assurance guide")}.'),
    faq("Other harnesses?", "The CLI works wherever an agent has a shell. An MCP server is deferred until a harness without a shell needs one."),
    faq("Is the source available?", 'Yes: <a href="https://github.com/writfold-dev/writfold">Writfold</a>, <a href="https://github.com/writfold-dev/weft">Weft</a> and <a href="https://github.com/writfold-dev/splicery">Splicery</a> are public, and this website is under the MIT license.'),
])
status = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="status-title">
      <p class="eyebrow">Status</p>
      <h1 id="status-title">What runs today.<br><span>What comes next.</span></h1>
      <p class="lede">Writfold is <a href="/">Git-native project continuity for coding agents</a>. This page lists what the preview runs, what is planned and what is not.</p>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">{VERSION}</a> · Updated {RELEASED}</span></p>
      <nav class="actions" aria-label="Page sections"><a href="#today">Runs today</a><a href="#next">Roadmap</a><a href="#changelog">Changelog</a><a href="#faq">FAQ</a></nav>
    </section>
    <section id="today" class="section" aria-labelledby="today-title">
      <div class="section-heading"><p class="eyebrow">01 / Runs today</p><h2 id="today-title">In the preview</h2><p>Each entry links to its guide. <a href="/#try">Try it</a>, or read the <a href="{README}">README</a>.</p></div>
      <div class="doc-links">{TODAY}</div>
      <p class="fine-print">Measured: reads at most 45&nbsp;ms on 4,130 records; writes about 120&ndash;130&nbsp;ms. A write killed at any step leaves the old or the new complete file.</p>
      <p class="fine-print">Limits: single user with cooperating agents; local clones only. The run graph has not yet had its week of real use, and no real PR comment or Slack summary has gone through the delivery checks.</p>
    </section>
    <section id="next" class="section" aria-labelledby="next-title">
      <div class="section-heading"><p class="eyebrow">02 / Roadmap</p><h2 id="next-title">Done, next, and not planned</h2><p>What is done is listed in full <a href="#today">above</a>.</p></div>
      <ol class="workflow">{ROAD}</ol>
    </section>
    <section id="changelog" class="section" aria-labelledby="changelog-title">
      <div class="section-heading"><p class="eyebrow">03 / Changelog</p><h2 id="changelog-title">What changed</h2><p>One line per release; the <a href="{RELEASES}">release notes</a> carry the detail.</p></div>
      <ol class="changelog">{LOG}</ol>
      <p class="fine-print">Every published file on this site is listed with its SHA-256 in the <a href="/content-manifest.json">content manifest</a>.</p>
    </section>
    <section id="faq" class="section" aria-labelledby="faq-title">
      <div class="section-heading"><p class="eyebrow">04 / FAQ</p><h2 id="faq-title">Common questions</h2></div>
      <div class="faq">{FAQ}</div>
    </section>
  </main>
'''
page("status.html", "Status — Writfold",
     f"What runs in the Writfold preview {VERSION}, what is next, a short changelog and FAQ.", "/status.html", status)

# ---------------------------------------------------------------- 404 and redirects
page("404.html", "Page not found — Writfold", "This page is not part of writfold.dev.", None,
     '''  <main id="main" class="wrap error-page" tabindex="-1"><p class="eyebrow">404 / Page not found</p><h1>This page isn't in the record.</h1><p>The address may have changed, or the page may never have existed.</p><div class="actions"><a class="button" href="/">Back to the overview</a><a href="/how.html">How it works</a><a href="/status.html">Status</a></div></main>
''')
STUBS = {"earlier.html": ("/", "the overview"), "docs.html": ("/how.html", "How it works"), "glossary.html": ("/how.html", "How it works"),
         "tuft.html": ("/how.html#research", "Retrieval with Tuft, on How it works"),
         "splicery.html": ("/how.html#execute", "Edits with Splicery, on How it works"),
         "weft.html": ("/how.html#gates", "Plan verification with Weft, on How it works")}
for name, (to, label) in STUBS.items():
    (SITE / name).write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <title>Moved — Writfold</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url={to}">
  <link rel="canonical" href="https://writfold.dev{to.split('#')[0]}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <main id="main" class="wrap error-page"><p>This page moved to <a href="{to}">{label}</a>.</p></main>
</body>
</html>
''', encoding="utf-8")
print("built")
