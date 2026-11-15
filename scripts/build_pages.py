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
import diagrams
from highlight import highlight

SITE = Path(__file__).resolve().parent.parent
VERSION = "v0.5.0-dev.6"
RELEASED = "15 November 2026"
RELEASES = "https://github.com/writfold-dev/writfold/releases/"
REL = RELEASES + "tag/" + VERSION
ALT = ("The folded-W Writfold mark on navy with the headline: Project memory in Git that says when it is stale. "
       f"Below it: Git-native project continuity for coding agents. Preview {VERSION}.")
NAV = [("/", "Overview"), ("/how.html", "How it works"), ("/status.html", "Status")]

def head(title, desc, path):
    url = "https://writfold.dev/" + path
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
  <link rel="stylesheet" href="/assets/site.css">
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
    (SITE / name).write_text(head(title, desc, "" if name == "index.html" else name) + header(current) + main + FOOTER, encoding="utf-8")

def pre(label, text, lang="session"):
    return (f'<pre class="code-panel" tabindex="0" aria-label="{label}"><code>'
            f'{highlight(text.strip(chr(10)), lang)}</code></pre>')

def panel(label, text, caption=None, lang="session", chip="Example"):
    cap = f'<figcaption><span class="chip chip-today">{chip}</span> {caption}</figcaption>' if caption else ""
    return f'<figure class="example">{cap}{pre(label, text, lang)}</figure>'

def pill(text, kind):
    return f'<span class="pill pill-{kind}">{text}</span>'

ANSWER = f'''<figure id="example" class="visual">
        <figcaption><span class="chip chip-parts">Illustration</span> One <code>kb why</code> answer as a card. Invented content; the parts are what the command prints.</figcaption>
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
        <p class="fine-print">Every line names its file and line. The evidence is code pinned at a commit, flagged because those lines have moved.</p>
      </figure>'''

def board(caption):
    def row(kind, title, badge, text, nxt=""):
        nxt = f'<p class="rb-next"><code>next: {nxt}</code></p>' if nxt else ""
        return f'<li><span class="rb-kind">{kind}</span><div><p class="rb-title"><strong>{title}</strong> {badge}</p><p>{text}</p>{nxt}</div></li>'
    rows = "".join([
        row("plan", "Step 4 of 6: findings", pill("current", "note"), "Owes the gate <code>findings</code>, which is open.", "writfold kb gate attest findings --statement TEXT --by WHO"),
        row("retrieval", "Tuft search", "", "3 rows at <code>harbor-api@4be03f78</code>, each with a citation."),
        row("edit", "Splicery recipes", pill("applied", "ok"), "2 files, 3 splices. The recipes and the preview are kept."),
        row("gate", "unit", pill("stale", "warn"), "Passed, then <code>src/audit.rs</code> and <code>src/ledger.rs</code> changed in its scope.", "writfold kb gate run unit"),
    ])
    return f"""<figure class="visual">
        <figcaption><span class="chip chip-today">From real output</span> {caption}</figcaption>
        <div class="card">
          <p class="card-cmd"><code><span class="syntax-prompt">$ </span>writfold kb resume</code></p>
          <p class="answer-head">{pill("open", "note")} <strong>Retry ledger connections</strong> <span class="src">harbor-api · main</span></p>
          <ol class="run-board">{rows}</ol>
          <ul class="card-foot"><li>step 4 of 6</li><li>1 retrieval</li><li>2 edits</li><li class="warn">2 gates stale</li></ul>
        </div>
      </figure>"""

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

FRAMES = Path(__file__).parent / "frames"

def frame(name, label, cls="term-frame", style=""):
    """A captured terminal frame: the <span> fragment the capture tool wrote to scripts/frames/<name>.html."""
    body = (FRAMES / f"{name}.html").read_text(encoding="utf-8").rstrip("\n")
    style = f' style="{style}"' if style else ""
    return f'<pre class="{cls}"{style} tabindex="0" aria-label="{label}"><code>{body}</code></pre>'

def flow_figure(pfx, caption):
    return (f'<figure class="diagram-figure">{diagrams.flow(pfx)}'
            f'<figcaption class="fine-print">{caption}</figcaption></figure>')

def spine_figure(pfx):
    return (f'<figure class="diagram-figure spine-figure"><p class="figure-lead"><span class="chip chip-today">From real output</span> '
            f'One run&rsquo;s plan, drawn from what <code>plan status</code> prints for a demo repository.</p>{diagrams.spine(pfx)}'
            f'<figcaption class="fine-print">A skill spliced its two steps in before <code>ship</code>. <code>implement</code> is flagged <code>!stale</code>: '
            f'a later edit moved the bytes its gate checked, and done stays done.</figcaption></figure>')

# ---------------------------------------------------------------- index
GUIDE = "https://github.com/writfold-dev/writfold/blob/main/docs/guide/"

def guide(page, label):
    return f'<a href="{GUIDE}{page}.md">{label}</a>'

def more(*links):
    """The one link out of a section: the matching guide in the Writfold repository."""
    return f'<p class="guide-link"><span aria-hidden="true">→</span> Full skeleton: {" and ".join(links)}</p>'

INSTALL = f'''base={RELEASES}download/{VERSION}
curl -LO "$base/writfold-x86_64-linux-musl" -LO "$base/writfold-x86_64-linux-musl.sha256"
echo "$(cut -d' ' -f1 writfold-x86_64-linux-musl.sha256)  writfold-x86_64-linux-musl" | sha256sum -c
install -m 755 writfold-x86_64-linux-musl ~/.local/bin/writfold

claude plugin marketplace add writfold-dev/writfold
claude plugin install writfold@writfold'''

DESC_HOME = ("Git-native project continuity for coding agents: why we decided X, where we stand on Y, the tracker item for Z, what changing X touches. "
             f"Every answer names its source and says when it has moved. Preview: {VERSION}.")
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
      <div class="actions"><a class="button" href="#try">Try it <span aria-hidden="true">↓</span></a><a class="text-action" href="/how.html">How it works <span aria-hidden="true">→</span></a><a class="text-action" href="/status.html">Status and roadmap <span aria-hidden="true">→</span></a></div>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span>Released {RELEASED}: <a href="{REL}">{VERSION}</a>, one static Linux x86_64 binary.</span></p>
      {ANSWER}
    </section>

    <section id="flow" class="section" aria-labelledby="flow-title">
      <div class="section-heading"><p class="eyebrow">The flow</p><h2 id="flow-title">Research, plan, execute, deliver. Each stage writes back.</h2><p>The agent keeps its own loop and model. What it finds, checks or drafts at each stage goes back into the knowledge base, so the next session starts from more than this one did.</p></div>
      {flow_figure("hf", f"Everything drawn here runs in {VERSION}.")}
      <p class="boundary">The knowledge base is plain Markdown and JSON in Git. Writes are left uncommitted for you to review and commit. The index refreshes itself on every read; <code>kb check</code> re-checks citations, the index, gate evidence and the plan on demand. <a href="/how.html">Walk through the stages</a>.</p>
    </section>

    <section id="runs" class="section" aria-labelledby="runs-title">
      <div class="section-heading"><p class="eyebrow">Inside a run</p><h2 id="runs-title">Steps, gates, and what is still owed</h2><p>A plan is an ordered list of steps, each naming the gates it owes. A gate is one small check: a command and the paths it covers, a statement someone must make, or a check of the run&rsquo;s own records. <code>gate run</code> keeps a receipt for the exact bytes checked, and <code>plan advance</code> records a step as done only when every gate is met.</p></div>
      {spine_figure("sp")}
      {board('The same run, drawn from what <code>resume</code> prints.')}
      <p class="boundary">Writfold records the plan and the agent walks it. Gates and steps report; a guard rule you add can hold a command until they are met.</p>
      {more(guide("run-graph", "the run graph guide"), guide("gates", "the gates guide"))}
    </section>

    <section id="watch" class="section" aria-labelledby="watch-title">
      <div class="section-heading"><p class="eyebrow">Watching a run</p><h2 id="watch-title">The plan as a map, in your terminal</h2><p><code>writfold watch</code> lists the runs on the left and draws the selected run&rsquo;s plan: skills spliced in as nested groups, each step&rsquo;s state and gates, and <code>▶</code> on the next step to pick up. Select a step and the inspector shows its gates, checklist items and the evidence behind them. It is read-only and adds nothing the records do not say.</p></div>
      <figure class="example"><figcaption><span class="chip chip-today">Captured</span> <code>writfold watch</code> at 136&times;38, on a test-fixture knowledge base: its gate and template definitions are files, as in any project, and its run, splices, steps, receipts and covers were written through the <code>kb</code> verbs.</figcaption>{frame("home", "writfold watch: runs on the left, the plan map in the middle, the inspector on the right", "term-frame term-frame-hero")}</figure>
      <p class="guide-link"><span aria-hidden="true">→</span> More: <a href="/how.html#watch">watching the run</a> and {guide("watch", "the watch guide")}</p>
    </section>

    <section id="try" class="section" aria-labelledby="try-title">
      <div class="section-heading"><p class="eyebrow">Try it</p><h2 id="try-title">Download, verify, install the plugin</h2><p>Linux x86_64 or WSL2. The plugin adds a project brief, the plan position and an inbox at session start, and keeps local checkpoint drafts.</p></div>
      {pre("Download and install commands", INSTALL, "shell")}
      <p class="fine-print">Single user, cooperating agents, local clones only; nothing is fetched. Setup is in the <a href="https://github.com/writfold-dev/writfold#readme">README</a>.</p>
    </section>

    <section id="first" class="section" aria-labelledby="first-title">
      <div class="section-heading"><p class="eyebrow">Built</p><h2 id="first-title">What the preview runs</h2></div>
      <dl class="verbs">
        <div><dt>Read</dt><dd><code>brief</code> <code>why</code> <code>status</code> <code>find</code> <code>impact</code> <code>resume</code>: {guide("kb-layout", "layout")}</dd></div>
        <div><dt>Write</dt><dd><code>checkpoint</code> <code>record</code> <code>cite make</code>: {guide("feeding-back", "feeding back")}</dd></div>
        <div><dt>Propose</dt><dd><code>propose</code> <code>proposals accept | drop</code>: {guide("feeding-back", "proposals")}</dd></div>
        <div><dt>Check</dt><dd><code>check</code> <code>stale</code> <code>index verify</code>: {guide("validation", "validation")}</dd></div>
        <div><dt>Plan</dt><dd><code>plan set | use | status | advance | skip</code>: {guide("run-graph", "run graph")}</dd></div>
        <div><dt>Gates</dt><dd><code>gate run | status | verify</code>: {guide("gates", "gates")}</dd></div>
        <div><dt>Deliver</dt><dd><code>deliver prepare | check</code>: {guide("delivery-modes", "delivery modes")}</dd></div>
        <div><dt>Plugin</dt><dd>Claude Code: {guide("hooks", "hooks")}, {guide("skills", "skills")}</dd></div>
      </dl>
      <p class="fine-print">Also <code>edit apply</code> for Splicery recipes, <code>tuft run --cite</code> and <code>writfold watch</code>. What is proved, tested and trusted: {guide("assurance", "assurance")}. Next: <a href="/status.html#next">the roadmap</a>.</p>
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
MODE = '''$ cat .writfold/deliveries/commit-message.toml
%toml
schema = "writfold-delivery-mode/1"
mode = "commit-message"
description = "checked before git commit; nothing binds the checked bytes to the commit that is made"
checks = ["references.denied"]
gates = ["commit-format", "language-guidelines"]
$ writfold kb deliver prepare --mode commit-message --audience external --from MSG
$ writfold kb deliver check
$ writfold kb deliver attest --check language-guidelines --statement "Read the guideline; plain words" --by agent
delivery 20261113T011927Z-9d72c6 [ready] commit-message audience=external destination=(unstated) candidate=7d9d22a36379 bytes=139 @runs/run-…/deliveries/…/candidate.md:1
  check: references.denied [satisfied] mechanical pass for 7d9d22a36379 (2 rules for external) @runs/run-…/checks/references.denied-….json:1
  check: commit-format [satisfied] mechanical pass for 7d9d22a36379 (exit=0) @runs/run-…/checks/commit-format-….json:1
  check: language-guidelines [attested] attested by agent: Read the guideline; plain words @runs/run-…/statements/language-guidelines-….json:1 !attested
  read: instructions for language-guidelines @.writfold/gates/language-guidelines.md:1
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
CHECK = '''$ writfold kb check             # the three below in one summary, plus the plan when the run has one
$ writfold kb stale             # which cited sources moved, changed or expired
$ writfold kb index verify      # the index equals a fresh rebuild
$ writfold kb gate status       # which gates are met, and which are owed again'''
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
      <p class="lede">Each part below is two sentences, one example and a link to the full guide. The commands are real and all of it runs in the preview; the one planned item is marked.</p>
      <nav class="actions" aria-label="Page sections"><a href="#kb">Knowledge base</a><a href="#research">1 Research</a><a href="#plan">2 Plan</a><a href="#execute">3 Execute</a><a href="#deliver">4 Deliver</a><a href="#reflect">Reflect</a><a href="#gates">Gates</a><a href="#check">Checking</a><a href="#plugin">Plugin</a></nav>
    </section>

    <section id="kb" class="section" aria-labelledby="kb-title">
      <div class="section-heading"><p class="eyebrow">The base</p><h2 id="kb-title">Records in Git, an index you can rebuild</h2><p>The knowledge base is a Git repository of plain Markdown and JSON: decisions, tickets, assets, the links between them and one folder per run. Every row of an answer ends in its source, and the last line says what was examined and how many sources are stale.</p></div>
      {panel("kb why output", WHY, REAL)}
      {more(guide("kb-layout", "the knowledge base layout"))}
    </section>

    <section id="research" class="section" aria-labelledby="research-title">
      <div class="section-heading"><p class="eyebrow">Stage 1 / Research</p><h2 id="research-title">Ask the knowledge base, or search the code</h2><p>The <code>kb</code> verbs answer from what the project already knows, and a short Tuft program finds exact text in code at one pinned commit. With <code>--cite</code> each row carries a citation, and what the agent concludes it writes down with <code>record</code>.</p></div>
      {panel("Research commands", RESEARCH)}
      <p class="fine-print">In a run with a plan, a required <code>research</code> step owes <code>backfilled</code>, a check of the run&rsquo;s own records. It passes only once the step wrote a record, a citation or a retrieval receipt.</p>
      {more(guide("feeding-back", "what each stage writes back"))}
    </section>

    <section id="plan" class="section" aria-labelledby="plan-title">
      <div class="section-heading"><p class="eyebrow">Stage 2 / Plan</p><h2 id="plan-title">Start a run, set its plan</h2><p>A run records the task, the repository, branch, worktree and base commit, and <code>plan set</code> copies a template&rsquo;s steps into it, each step naming the gates it owes. Templates listed in <code>.writfold/plans/required.toml</code> are added to every plan: here a <code>research</code> step at the start and a <code>reflect</code> step at the end.</p></div>
      {panel("Starting a run and setting its plan", NEWRUN, REAL)}
      <p class="fine-print">Writfold records the steps and the agent walks them; it schedules nothing. A template can include another with <code>use=</code>, and the run keeps a snapshot of each, so a template edited later is flagged <code>!template-moved</code> and the run is not rewritten.</p>
      {more(guide("run-graph", "the run graph"))}
    </section>

    <section id="execute" class="section" aria-labelledby="execute-title">
      <div class="section-heading"><p class="eyebrow">Stage 3 / Execute</p><h2 id="execute-title">Edit, check, advance</h2><p>The agent edits the run&rsquo;s worktree with Splicery recipes for repeated or structural edits, or with ordinary tools for one small change, and any gate whose scope covers the change is owed again. <code>plan advance</code> records the current step as done only when each of its gates is met; a done step whose gate later goes stale is flagged <code>!stale</code> and stays done.</p></div>
      {panel("Execute commands and plan status", EXECUTE, REAL)}
      <p class="fine-print">A skill adds its own steps with one line, <code>plan use</code>; a repeat writes nothing. <code>plan skip --reason TEXT --by WHO</code> closes a step without calling it done.</p>
      <p class="fine-print">Two sessions, two clones: every plan write re-checks its decision under the knowledge base&rsquo;s write lock, and refuses and writes nothing if the plan changed since the command read it. After two clones merge, <code>plan status</code>, <code>resume</code> and <code>kb check</code> flag <code>!out-of-order</code> (a done step after an open one), <code>!two-plans</code> and <code>!repeated</code> and exit 2; they never change the plan. A TLC model of the run graph found both gaps.</p>
      {more(guide("run-graph", "steps, splicing and stale"), guide("skills", "skills that splice"))}
      <h3 id="watch">Watching the run</h3>
      <p><code>writfold watch</code> draws the run&rsquo;s plan as a map in a terminal: one row per step in order, skills spliced in as nested groups under the step they belong to, a glyph for each step&rsquo;s state (<code>✓</code> done, <code>!</code> done but a gate went stale, <code>–</code> skipped, <code>▶</code> the next step to pick up, <code>○</code> later) and a chip for each of its gates. Select a step with <code>j</code>/<code>k</code> and the inspector beside the map shows its gates, checklist items, evidence paths, why it is flagged and the next command. Every state comes from a <code>kb</code> verb. The marker is the recorded position, not a claim that an agent is working; the view adds no percentage or time estimate, has no key that writes, and never starts a checker.</p>
      <figure class="example"><figcaption><span class="chip chip-today">Captured</span> <code>writfold watch</code> {VERSION} at 160&times;40 in the default clay theme, on a test-fixture knowledge base: its gate and template definitions are files, as in any project, and its run, splices, steps, receipts and covers were written through the <code>kb</code> verbs. A review skill was spliced under <code>change#1/review</code>, with a findings template under it; the lint file changed after its receipt, so <code>implement</code> is flagged and the checklist item citing that gate turned stale.</figcaption>{frame("how", "writfold watch: the plan map of a run at step 7 of 11, with the inspector open on the current step")}</figure>
      <details class="exact"><summary>The same frame in the clay-light theme</summary>{frame("how-light", "writfold watch in the clay-light theme", style="background:#faf9f5;color:#1f1e1d")}</details>
      <p class="guide-link"><span aria-hidden="true">→</span> Keys, layouts, refresh and themes: {guide("watch", "watching a run")}</p>
    </section>

    <section id="deliver" class="section" aria-labelledby="deliver-title">
      <div class="section-heading"><p class="eyebrow">Stage 4 / Deliver</p><h2 id="deliver-title">Drafts, checked. Nothing sent.</h2><p><code>kb deliver prepare</code> copies a PR comment or Slack summary into the run as the exact text that would be posted, and <code>deliver check</code> runs three checks on those bytes: paragraph length, references the audience must not see, and whether every citation is still fresh. Writfold has no network code, so posting stays with you or your agent.</p></div>
      {drafts()}
      {panel("A commit-message delivery mode", MODE, "Your own mode is one file, <code>.writfold/deliveries/&lt;name&gt;.toml</code>. This one checks a commit message with a script its gate ships and a guideline to read and attest. " + REAL)}
      <p class="fine-print">The checks are mechanical: they do not judge tone or truth. An optional Claude Code hook, off unless configured, can deny a listed publishing command until a ready draft holds the exact bytes: a guard, not enforcement.</p>
      <p class="fine-print"><span class="chip chip-planned">Planned</span> A delivery mode as a plan step&rsquo;s gate.</p>
      {more(guide("delivery-modes", "delivery modes, deny lists and the guard"))}
    </section>

    <section id="reflect" class="section" aria-labelledby="reflect-title">
      <div class="section-heading"><p class="eyebrow">Before the run ends</p><h2 id="reflect-title">Reflect, propose, close</h2><p>The required <code>reflect</code> step owes two gates: a run-record check that passes only when the run holds a <code>reflection:</code> entry and a proposal or an explicit <code>no proposal</code>, and a statement that the reflection covers what its instructions ask. A proposal is a <code>record</code> call not yet made, kept in a local queue until you accept or drop it.</p></div>
      {panel("Closing a run", REFLECT, REAL)}
      <p class="fine-print">The bundled <code>writfold:evaluate</code> skill walks this step in a forked subagent and never accepts a proposal itself. The check shows that a reflection was written, not that it is good.</p>
      {more(guide("feeding-back", "proposals and the reflection checks"), guide("skills", "the evaluate skill"))}
    </section>

    <section id="gates" class="section" aria-labelledby="gates-title">
      <div class="section-heading"><p class="eyebrow">The thread</p><h2 id="gates-title">Who owes a gate, and what meets it</h2><p>Plan steps, runs and delivery drafts owe gates, and evidence that Writfold records meets them. Gates report; on their own they block nothing (a guard rule can hold a command until they are met); receipts resist mistakes, such as a forgotten check or a stale &ldquo;tests pass&rdquo;, and they are tracked files, not signatures.</p></div>
      <figure class="diagram-figure">{diagrams.gates("wg")}<figcaption class="fine-print">Evidence is tied to exact bytes. When they change, the gate is owed again.</figcaption></figure>
      <p class="fine-print">A step can owe a Weft assessment. The agent states the step&rsquo;s assumptions and checks in a Weft file and cites evidence for each assumption. A check is met only when Weft entails it from assumptions whose every citation Writfold found fresh or satisfied, which Weft calls a &ldquo;grounded basis&rdquo;; otherwise it is shown as hypothetical and does not meet the gate.</p>
      {more(guide("gates", "every gate class, with examples"), guide("assurance", "what is proved, tested and trusted"))}
    </section>

    <section id="check" class="section" aria-labelledby="check-title">
      <div class="section-heading"><p class="eyebrow">Any time</p><h2 id="check-title">Check that it still holds</h2><p>The index refreshes itself on every read, so there is no sync step. <code>kb check</code> re-checks the rest in one summary: cited sources, the index against a rebuild, gate evidence, and the plan when the run has one.</p></div>
      {panel("Validation commands", CHECK)}
      {more(guide("validation", "validation, flag by flag"))}
    </section>

    <section id="plugin" class="section" aria-labelledby="plugin-title">
      <div class="section-heading"><p class="eyebrow">In Claude Code</p><h2 id="plugin-title">The plan position at session start, drafts at the end</h2><p>The plugin puts <code>brief</code>, <code>resume</code>, the plan position and an inbox of drafts, proposals and runs that ended without a reflection into a new session with no tool call, and re-injects the plan position after a compaction. It reads local files and refs only, runs no model, and does nothing when the binary or the knowledge base is missing.</p></div>
      {panel("Session-start context", HOOK, "What session start adds, from a demo repository; <code>…</code> marks rows left out. The first line appears only when the clone is behind its remote, judged from local refs with no fetch.", "output", "From real output")}
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
TODAY = "".join([
    row(GUIDE + 'kb-layout.md', 'Read verbs', '<code>brief | context | why | status | find | match | impact | uses | timeline | resume | runs</code>. Every row names its source; every answer ends with what was examined and omitted'),
    row(GUIDE + 'feeding-back.md', 'Write verbs and proposals', '<code>checkpoint</code>, <code>record ticket | decision | link</code>, <code>status --set</code>, <code>cite make</code>. <code>propose</code> queues a record locally; <code>proposals list | show | accept | drop</code> decides it'),
    row(GUIDE + 'validation.md', 'Citations, the index and <code>kb check</code>', '<code>stale</code> reports each pinned citation as fresh, moved, changed or gone; <code>index verify</code> checks the index equals a rebuild; <code>check</code> runs both with gate and plan status'),
    row(GUIDE + 'gates.md', 'Gates', '<code>gate run | status | verify | lines | attest | waive | cover</code>. Receipts pinned to exact bytes; a gate can name an instructions file and ship its own script; a checklist gate is covered item by item with evidence that is re-checked on every read; a timeout or crash is never a pass'),
    row(GUIDE + 'hooks.md#guard-rules', 'Guard rules', 'A rule in <code>.writfold/guards/</code> denies or asks about a command such as <code>git commit</code>, or a tool such as <code>Edit</code>, until the run&rsquo;s gates are met, naming what is owed and the command that meets it. A <code>stop</code> rule reminds once per session. A guard, not enforcement'),
    row(GUIDE + 'checkers.md', 'External checkers', 'A kind declared <code>checked</code> in <code>.writfold/sources/</code> names a program, <code>writfold-check-&lt;name&gt;</code> on your <code>PATH</code>, that <code>kb stale</code> asks over JSON lines. Credentials stay with the program; the knowledge base never runs a command it names'),
    row(GUIDE + 'run-graph.md', 'The run graph', '<code>plan set | use | status | advance | skip</code>. Templates in <code>.writfold/plans/</code>, a skill splicing its steps in, <code>use=</code> includes, and the <code>!stale</code> and <code>!template-moved</code> flags. Plan writes re-check under the write lock; after a merge, <code>!out-of-order</code>, <code>!two-plans</code> and <code>!repeated</code> flag what it left'),
    row(GUIDE + 'run-graph.md#required-steps', 'Required steps and run-record checks', 'Start and end templates from <code>required.toml</code> join every plan. <code>research.backfilled</code> and <code>run.reflected</code> judge the run&rsquo;s own records'),
    row(GUIDE + 'gates.md#weft-assessed-gates', 'Weft assessed gate', 'A plan step can require a Weft assessment. A check is met only when it is entailed from assumptions whose citations hold; otherwise it is shown as hypothetical'),
    row(GUIDE + 'delivery-modes.md', 'Delivery drafts and your own modes', '<code>deliver prepare | check | status | attest | waive</code> for PR comments, Slack summaries and any mode you define; a commit-message mode is included. Nothing is sent'),
    row(GUIDE + 'feeding-back.md', 'Tuft and Splicery in a run', '<code>tuft run --cite</code> adds citations and a retrieval receipt; <code>edit apply | recover</code> replays recipes and keeps an edit receipt'),
    row(GUIDE + 'hooks.md', 'Claude Code plugin', 'At session start: the brief, the plan position, an inbox and a line when the clone is behind its remote; the plan position again after compaction. Checkpoint drafts, the <code>writfold:kb</code> and <code>writfold:evaluate</code> skills, and an optional guard hook'),
    row(GUIDE + 'assurance.md', 'Proofs of three kernels', 'Lean proofs over the shipped Rust for the run-graph, gate and assessed-gate decisions. Parsers, file reads and globs are tested, not proved'),
    row(GUIDE + 'assurance.md#model-checked', 'A model of the run graph', '<code>spec/RunGraph.tla</code>, checked with TLC at small bounds: two runs finished with no violation, the widest was stopped unfinished with none found, and ten mutants each fail their property. Evidence about the design, not a refinement of the Rust'),
    row('/how.html#watch', '<code>writfold watch</code>', 'A read-only terminal view of a run&rsquo;s recorded progress: each plan step with its gates and checklist items, the inbox, guard rules and the run&rsquo;s checkpoints. Six colour themes; it never runs a check'),
])
def step(title, text, chip):
    cls = {"Done": "chip-today", "Next": "chip-progress", "Planned": "chip-planned", "Deferred": "chip-planned", "Not planned": "chip-parts"}[chip]
    return f'<li><div><h3>{title}</h3><p>{text} <span class="chip {cls}">{chip}</span></p></div></li>'
ROAD = "".join([
    step('The four questions', 'Read and write verbs, the index, pinned citations and the Claude Code plugin.', 'Done'),
    step('Runs with gates, edits and drafts', 'Receipts, statements, Splicery edits, Tuft citations, delivery drafts and <code>watch</code>.', 'Done'),
    step('Instruction gates and your own delivery modes', 'A gate can point to written instructions and ship its script; a mode such as a commit message lists its gates.', 'Done'),
    step('The run graph, splicing and required steps', '<code>plan set | use | status | advance | skip</code>; required steps checked against the run&rsquo;s own records.', 'Done'),
    step('Hooks that show the plan', 'The plan position at session start and after compaction, with an inbox. No model in a hook.', 'Done'),
    step('Proofs, proposals and the closing step', 'Proofs of the plan and gate kernels, a TLC model of the run graph, <code>kb check</code>, proposals, the evaluation skill, and Weft assessments of plan steps.', 'Done'),
    step('Guard rules, checklists and citation kinds', 'Rules that deny a command until gates are met, checklist gates covered item by item, per-kind citation lifetimes, and concluded investigations.', 'Done'),
    step('Checks against systems outside Git', 'External checkers that <code>kb stale</code> runs for citation kinds Git cannot check, with cached verdicts; decision states bound to a commit and a gate receipt; renames with edits followed.', 'Done'),
    step('Check receipts other machines can read', 'A tracked record of what a checker found, so a machine without the checker or its credentials can read when a citation was last checked.', 'Planned'),
    step('Observations, clones and batch cover', '<code>kb observe</code> for lookups and their outcome, <code>kb repos</code> for missing clones, several checklist items in one call, proposals kept in the knowledge base, path-scoped guard rules.', 'Done'),
    step('Run progress in <code>writfold watch</code>', 'Plan steps with their gates and checklist items, the inbox, guard rules and a timeline in the terminal view, with colour themes. Read-only.', 'Done'),
    step('The plan map in <code>writfold watch</code>', 'The run&rsquo;s plan drawn as a map with nested splices, a glyph and gate chips per step, the next step to pick up, and an inspector for each step.', 'Done'),
    step('Tuft for everyday search', 'Branch names where a commit is expected, a one-line search, several repositories in one query and symbol finds from a ctags index, still pinned to a commit.', 'Done'),
    step('One week of real use', 'Count what the checks caught, and what was waived, before adding more.', 'Next'),
    step('A delivery mode as a step&rsquo;s gate', 'A plan step that owes a checked draft.', 'Planned'),
    step('Trailer and tracker edges, and <code>--at</code>', 'Links read from commit trailers and tracker references, and answers as of a given commit.', 'Planned'),
    step('An MCP server', 'Deferred until a harness without a shell needs one. The CLI and the plugin are the interface.', 'Deferred'),
    step('A governed profile', 'Authority levels, exception routes and signing. Writfold stays single user with cooperating agents.', 'Not planned'),
])
LOG = "".join(f"<li><time>{d}</time><p>{t}</p></li>" for d, t in [
    ('15 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.6">v0.5.0-dev.6</a>: the plan map in <code>writfold watch</code>. The run&rsquo;s plan is drawn as rows in order, with skills spliced in as nested groups under the step they belong to, a glyph for each step&rsquo;s state, a chip for each gate and <code>▶</code> on the next step to pick up. An inspector shows the selected step&rsquo;s gates, checklist items, evidence and next command; <code>x</code> keeps the text list. <code>plan status --gates</code> adds <code>splice</code> and <code>under</code> lines and <code>timeline</code> of a run lists its plan events. A new default theme, clay, with clay-light. <a href="/how.html#watch">See it</a>.'),
    ('14 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.5">v0.5.0-dev.5</a>: run progress in <code>writfold watch</code>. Each plan step with its gates and checklist items, and a strip with one cell per step; a done step whose gate went stale stays done and is flagged. Separate views for gates, the inbox of drafts and proposals, the guard rules as they would judge the current run, and the run&rsquo;s own checkpoint timeline. Layouts for wide and narrow terminals, refresh when the knowledge base or the repository changes, and six colour themes with ANSI and no-colour modes. Every number comes from a <code>kb</code> verb; the view adds no percentage or time estimate, has no key that writes, and never starts a checker. <code>plan status --gates</code>, <code>runs --plan</code>, <code>guard status</code> and <code>timeline &lt;run&gt;</code> give the same answers on the command line.'),
    ('13 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.4">v0.5.0-dev.4</a>: Tuft for everyday search. <code>writfold tuft grep</code> runs the common search in one line; a branch name or <code>HEAD</code> is accepted and resolved to the commit it names, which the output shows and every citation and receipt keeps; one search covers several repositories, each with its own coverage line; path globs in scopes; every parse error reported, with the fix named; a working-tree mode whose citations of uncommitted bytes are marked and never read as fresh; and definitions and references from a ctags index built at the same commit.'),
    ('13 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.3">v0.5.0-dev.3</a>: <code>kb observe</code> records a lookup and its outcome, so a timeout or an empty answer stays visible under a checklist item without ever counting as support; <code>kb repos</code> lists the repositories your citations name and which have no clone, and a partial clone no longer stops <code>kb stale</code>; several checklist items covered in one call (<code>gate cover --from</code>); proposals kept in the knowledge base so they survive losing the clone; guard rules scoped to file paths, and a stop reminder that can repeat every turn; and a maximum age for a checker&rsquo;s cached verdict.'),
    ('13 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.2">v0.5.0-dev.2</a>: external checkers, programs on your <code>PATH</code> that <code>kb stale</code> asks about citation kinds Git cannot check (an absent or failing checker leaves those citations unverifiable, never fresh), and <code>cite make --kind</code> to build such citations; a decision&rsquo;s <code>accepted</code>, <code>applied</code> and <code>verified</code> states, each bound to something Writfold checks (the reviewed design, a commit on the target branch, a passing gate receipt); and code citations followed through a rename that also edited the file, <code>moved</code> only when the cited lines are found at the new path.'),
    ('13 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.5.0-dev.1">v0.5.0-dev.1</a>: guard rules that deny or ask about a command or tool until the run&rsquo;s gates are met, with a once-per-session Stop reminder; checklist gates covered item by item (<code>gate cover</code>) with evidence re-checked on every read; per-kind citation lifetimes in <code>.writfold/sources/</code>; a stale-citation count at session start; the <code>--json</code> envelope documented; and investigations that can be concluded once their write-up is complete.'),
    ('13 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.4.0-dev.1">v0.4.0-dev.1</a>: the run graph (<code>plan set | use | status | advance | skip</code>) with splicing, required steps and run-record checks; instruction gates and your own delivery modes; proposals and <code>kb check</code>; the Weft assessed gate; the plan position and an inbox at session start; the <code>writfold:evaluate</code> skill; and Lean proofs of the run-graph, gate and assessed-gate kernels. A TLC model of the run graph, <code>spec/RunGraph.tla</code>, found two gaps, both fixed in this release: plan writes now re-check their decision under the write lock, and a merge of two clones is flagged <code>!out-of-order</code>, <code>!two-plans</code> or <code>!repeated</code>.'),
    ('12 Nov 2026', 'The site is shorter. Full file layouts, configuration and output moved to the <a href="https://github.com/writfold-dev/writfold/blob/main/docs/guide/README.md">guides</a> in the Writfold repository. Direction set: the run graph, required steps and model-free hooks, all planned.'),
    ('12 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.3.0-dev.1">v0.3.0-dev.1</a>: gates, Splicery edits in a run, <code>writfold watch</code>, delivery drafts and an optional guard hook.'),
    ('12 Nov 2026', 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.2.0-dev.1">v0.2.0-dev.1</a>: the <code>kb</code> read and write verbs, the index, citations checked for staleness, and the Claude Code plugin.'),
    ('11 Nov 2026', 'Mission set: Git-native project continuity for coding agents.'),
])
def faq(q, a): return f"<details><summary>{q}</summary><p>{a}</p></details>"
FAQ = "".join([
    faq('Can I use Writfold today?', 'Yes, as a preview: <a href="/#try">download the binary and install the plugin</a>. Single user, cooperating agents, local clones (plus any external checkers you install), Linux x86_64 or WSL2.'),
    faq('Does it need a server or a database?', 'No. One static binary, records in Git, and a local index that Writfold derives and can always rebuild.'),
    faq('Does Writfold run or schedule my agent?', 'No. It records the plan and what met each gate. The agent reads the current step, does the work its own way and asks to advance. No hook runs a model.'),
    faq('Can an agent skip a gate or a step?', 'Yes. Gates and steps record what was checked and report whether it still holds; on their own they block nothing. A gate that was never run shows as open, a skipped step shows as skipped with a reason and a name, and the plan is complete only when every step is done or skipped. A guard rule you add can deny or ask about a command such as <code>git commit</code> until the gates are met; it is a guard, not enforcement, and only sees the tool calls Claude Code shows it.'),
    faq('Is it formally verified?', 'In part. Three decision kernels are proved in Lean over an Aeneas translation of the Rust that ships. The run graph: a step is recorded as done exactly when it is the current step and every gate is met; a splice keeps every existing step, and repeating it changes nothing. Gate obligations: only exit status 0 on bytes that did not move is a pass, and an attestation or a waiver never counts as satisfied. The Weft assessed gate: a hypothetical entailment never passes. The proof check audits 54 claims across all proved kernels and requires each of 45 mutants of the Rust source to break its named theorem. The rest is tested, not proved: template and gate parsers, the fold from event files to steps, file and Git reads, and scope globs. The write protocol and the run graph are model-checked, not proved (next answer). The proofs trust the Charon and Aeneas translation and the Lean kernel. Details are in <a href="https://github.com/writfold-dev/writfold/blob/main/docs/guide/assurance.md">the assurance guide</a>.'),
    faq('What did model checking cover?', 'Two TLA+ models, checked with TLC at small bounds. The write protocol: five invariants over about 18 million states, with a power loss at any moment. The run graph, <code>spec/RunGraph.tla</code>: two runs finished with no violation, two merging clones without drift or a crash (about 2.1 million states) and two sessions in one clone with drift and a crash (about 44 million states). The widest run, two merging clones with drift and a crash, was stopped unfinished at depth 21 with no violation found, so that case is checked only to that depth. Ten mutants of the run-graph model each fail their property. The models are hand-written evidence about the design, not a refinement of the Rust; tests tie them to the code. The run-graph model found two gaps, both now fixed in the Rust: a plan write re-checks its decision under the write lock and refuses if the plan changed, and after a merge <code>plan status</code>, <code>resume</code> and <code>kb check</code> flag <code>!out-of-order</code>, <code>!two-plans</code> and <code>!repeated</code> without changing the plan. Details are in <a href="https://github.com/writfold-dev/writfold/blob/main/docs/guide/assurance.md">the assurance guide</a>.'),
    faq('Does Writfold post PR comments or Slack messages?', 'No. <code>kb deliver</code> keeps drafts with their checks in the run. Nothing is sent.'),
    faq('Who accepts a proposal?', 'You do. <code>kb propose</code> queues a record call locally, and the <code>writfold:evaluate</code> skill may queue up to three. Only <code>proposals accept</code> writes the record, and it is refused when a citation in it is no longer fresh.'),
    faq('Other harnesses?', 'The CLI works wherever an agent has a shell. An MCP server is deferred until a harness without a shell needs one.'),
    faq('Is the source available?', 'Yes: <a href="https://github.com/writfold-dev/writfold">Writfold</a>, <a href="https://github.com/writfold-dev/weft">Weft</a> and <a href="https://github.com/writfold-dev/splicery">Splicery</a> are public, and this website is under the MIT license.'),
])
status = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="status-title">
      <p class="eyebrow">Status</p>
      <h1 id="status-title">What runs today.<br><span>What comes next.</span></h1>
      <p class="lede">Writfold is <a href="/">Git-native project continuity for coding agents</a>. The preview covers the whole flow: research, the run graph, execution, delivery drafts and a closing reflection.</p>
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
      <div class="section-heading"><p class="eyebrow">02 / Roadmap</p><h2 id="next-title">Done, next, and not planned</h2><p>The run graph as built is in {guide("run-graph", "the run graph guide")}.</p></div>
      <ol class="workflow">{ROAD}</ol>
    </section>
    <section id="changelog" class="section" aria-labelledby="changelog-title">
      <div class="section-heading"><p class="eyebrow">03 / Changelog</p><h2 id="changelog-title">What changed</h2></div>
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
