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
REL = "https://github.com/writfold-dev/writfold/releases/tag/v0.3.0-dev.1"
ALT = ("The folded-W Writfold mark on navy with the headline: Project memory in Git that says when it is stale. "
       "Below it: Git-native project continuity for coding agents. Preview v0.3.0-dev.1.")
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

def exact(summary, label, text, lang="session"):
    """Real output, folded away for readers who want the exact bytes."""
    return (f'<details class="exact"><summary>Exact output: {summary}</summary>'
            f'<p class="fine-print">{REAL}</p>{pre(label, text, lang)}</details>')

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
        row("retrieval", "Tuft search", "", "3 rows at <code>harbor-api@4be03f78</code>, each with a citation."),
        row("edit", "Splicery recipes", pill("applied", "ok"), "2 files, 3 splices. The recipes and the preview are kept."),
        row("gate", "unit", pill("stale", "warn"), "Passed, then <code>src/audit.rs</code> and <code>src/ledger.rs</code> changed in its scope.", "writfold kb gate run unit"),
        row("gate", "wording", pill("attested", "note"), "&ldquo;README unchanged; guideline read&rdquo;, by agent. A statement, not a check."),
        row("delivery", "PR comment for harbor#42", pill("ready", "ok"), "3 of 3 checks satisfied. Not sent."),
        row("checkpoint", "Entry 2 of 2", "", "&ldquo;Retry applied in ledger.rs and audit.rs; unit satisfied; PR comment ready. Next: commit and post.&rdquo;"),
    ])
    return f'''<figure class="visual">
        <figcaption><span class="chip chip-today">From real output</span> {caption}</figcaption>
        <div class="card">
          <p class="card-cmd"><code><span class="syntax-prompt">$ </span>writfold kb resume</code></p>
          <p class="answer-head">{pill("open", "note")} <strong>Retry ledger connections</strong> <span class="src">harbor-api · main</span></p>
          <ol class="run-board">{rows}</ol>
          <ul class="card-foot"><li>2 gates</li><li class="warn">1 stale</li><li>1 attested</li><li>1 draft ready</li></ul>
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

def planned(html):
    return f'<div class="planned-panel"><p><span class="chip chip-planned">Planned</span> Not built yet.</p>{html}</div>'

def flow_figure(pfx, caption):
    return (f'<figure class="diagram-figure">{diagrams.LEGEND}{diagrams.flow(pfx)}'
            f'<figcaption class="fine-print">{caption}</figcaption></figure>')

# ---------------------------------------------------------------- index
INSTALL = '''base=https://github.com/writfold-dev/writfold/releases/download/v0.3.0-dev.1
curl -LO "$base/writfold-x86_64-linux-musl" -LO "$base/writfold-x86_64-linux-musl.sha256"
echo "$(cut -d' ' -f1 writfold-x86_64-linux-musl.sha256)  writfold-x86_64-linux-musl" | sha256sum -c
install -m 755 writfold-x86_64-linux-musl ~/.local/bin/writfold

claude plugin marketplace add writfold-dev/writfold
claude plugin install writfold@writfold'''

DESC_HOME = ("Git-native project continuity for coding agents: why we decided X, where we stand on Y, the tracker item for Z, what changing X touches. "
             "Every answer names its source and says when it has moved. Preview: v0.3.0-dev.1.")
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
      <p class="maturity"><span class="badge badge-today">Preview</span> <span>Released 12 November 2026: <a href="{REL}">v0.3.0-dev.1</a>, one static Linux x86_64 binary.</span></p>
      {ANSWER}
    </section>

    <section id="flow" class="section" aria-labelledby="flow-title">
      <div class="section-heading"><p class="eyebrow">The flow</p><h2 id="flow-title">Research, plan, execute, deliver. Each stage leaves a record.</h2><p>The agent keeps its own loop and model. At each stage it picks a tool, and what it found, checked or drafted goes back into the knowledge base. The next session, on any machine, starts from there.</p></div>
      {flow_figure("hf", "Planned: plan steps, Weft verifying a plan, your own delivery modes, MCP.")}
      <p class="boundary">The knowledge base is plain Markdown and JSON in Git, with a local index Writfold can always rebuild. One static binary; no server. <a href="/how.html">Walk through the four stages</a>.</p>
    </section>

    <section id="choose" class="section" aria-labelledby="choose-title">
      <div class="section-heading"><p class="eyebrow">Pick per task</p><h2 id="choose-title">Two ways to retrieve, two ways to edit</h2><p>They work side by side. The agent chooses by the task in front of it.</p></div>
      <div class="status-grid">
        <article class="status-card"><p class="status-label">Retrieval</p>
          <dl class="options">
            <div><dt><code>writfold kb find</code></dt><dd>Records in the knowledge base: decisions, tickets, assets. It tolerates a typo.</dd></div>
            <div><dt><code>writfold tuft run --cite</code></dt><dd>Exact text in code at a pinned commit, within an output budget. Each row carries a citation that later shows whether its lines moved.</dd></div>
          </dl>
          <p><a href="/how.html#research">Retrieval in the flow</a></p></article>
        <article class="status-card"><p class="status-label">Edits</p>
          <dl class="options">
            <div><dt>Splicery recipes, through <code>writfold kb edit apply</code></dt><dd>Repeated or structural edits, replayed exactly: an expected count, every file or none, a receipt in the run.</dd></div>
            <div><dt>Ordinary Edit, grep and sed</dt><dd>One small change. Simpler, and the result is the same kind of Git change.</dd></div>
          </dl>
          <p><a href="/how.html#execute">Edits in the flow</a></p></article>
      </div>
    </section>

    <section id="runs" class="section" aria-labelledby="runs-title">
      <div class="section-heading"><p class="eyebrow">Inside a run</p><h2 id="runs-title">Gates, evidence, and what is still owed</h2><p>A run is one task in one worktree. Each gate result is kept there, so &ldquo;where do we stand on Y?&rdquo; includes what is still owed.</p></div>
      <div class="three-up">
        <article class="capability"><span class="number">01</span><h3>Gates</h3><p>A gate is one small check: a file naming a command and the paths it covers, or a statement someone must make.</p></article>
        <article class="capability"><span class="number">02</span><h3>Evidence</h3><p><code>gate run</code> keeps a receipt for the exact bytes checked. A statement is recorded as attested or waived, never as a pass.</p></article>
        <article class="capability"><span class="number">03</span><h3>What is owed</h3><p><code>resume</code> lists each gate as satisfied, stale, failed or open, with the next command. Draft PR comments and Slack summaries carry their own checks; nothing is sent.</p></article>
      </div>
      {board('One run, drawn from what <code>resume</code> and <code>watch</code> print for a demo repository. <a href="/how.html#execute">Exact output</a>.')}
      <p class="boundary">Gates report; they block nothing. <code>writfold watch</code> shows it all, read-only.</p>
      <p class="fine-print"><span class="chip chip-planned">Planned</span> Gates with written instructions, your own delivery modes such as a commit message, and plan steps the agent advances through once their gates are met. <a href="/how.html#gates">How gates fit together</a>.</p>
    </section>

    <section id="try" class="section" aria-labelledby="try-title">
      <div class="section-heading"><p class="eyebrow">Try it</p><h2 id="try-title">Download, verify, install the plugin</h2><p>Linux x86_64 or WSL2. The plugin adds a project brief at session start and keeps local checkpoint drafts.</p></div>
      {pre("Download and install commands", INSTALL, "shell")}
      <p class="fine-print">Single user, cooperating agents, local clones only; nothing is fetched. Setup is in the <a href="https://github.com/writfold-dev/writfold#readme">README</a>.</p>
    </section>

    <section id="first" class="section" aria-labelledby="first-title">
      <div class="section-heading"><p class="eyebrow">Built</p><h2 id="first-title">What the preview runs</h2></div>
      <dl class="verbs">
        <div><dt>Read</dt><dd><code>brief</code> <code>why</code> <code>status</code> <code>find</code> <code>impact</code> <code>stale</code> <code>resume</code> and more</dd></div>
        <div><dt>Write</dt><dd><code>checkpoint</code> <code>record</code> <code>status --set</code> <code>cite make</code></dd></div>
        <div><dt>Runs</dt><dd><code>gate</code> <code>edit</code> <code>deliver</code> <code>watch</code></dd></div>
        <div><dt>Tools</dt><dd><code>tuft run --cite</code>, Splicery recipes</dd></div>
        <div><dt>Index</dt><dd><code>index status | rebuild | verify</code></dd></div>
        <div><dt>Plugin</dt><dd>Claude Code: brief, checkpoint drafts, one skill</dd></div>
      </dl>
      <p class="fine-print">Next: instruction gates, your own delivery modes, plan steps and Weft plan verification. <a href="/status.html#next">Status and roadmap</a>.</p>
    </section>
  </main>
'''
page("index.html", "Writfold — Git-native project continuity for coding agents", DESC_HOME, "/", index)

# ---------------------------------------------------------------- how
FIND = '''$ writfold kb find "harbr-api" --kind asset,ticket
asset harbor-api [active] Harbor billing API @inventory/assets/harbor-api.json:10 !past-ttl
  match: typo d=1 harbor-api
ticket HBR-101 [in-progress] Slow ledger flush at month end @ktlo/2026/hbr-101-slow-ledger-flush.md:5
  match: text-any assets: [harbor-api, harbor-db] @ktlo/2026/hbr-101-slow-ledger-flush.md:4
…
# coverage=complete records=31/31 shown=3 omitted=0 kb=4ba5227faf95 index=fresh cursor=none q=02fca533ca79'''
TUFT = '''$ cat q.tuft
%tuft
@h := find text "open(url())" in "src/" at "4be03f7897b691715114a229ab1acc307f5de90f";
@e := retain @h around lines 0;
@v := project @e [path, line, excerpt(max_chars: 80)];
emit @v budget_tokens 300;

$ writfold tuft run q.tuft --repo . --cite
writfold tuft: recorded runs/run-…/retrievals/20261112T211036Z-c7b86d.md in …/kb
src/audit.rs:3:     let conn = open(url())?;
  cite: ⟦cite kind=code repo=harbor-api rev=4be03f78… path=src/audit.rs L=3-3 blob=e77382cb… span=0c70393772e189b9 seen=2026-11-12T21:10Z url=…⟧
src/ledger.rs:3:     let conn = open(url())?;
  cite: ⟦cite kind=code repo=harbor-api rev=4be03f78… path=src/ledger.rs L=3-3 blob=b7092119… span=0c70393772e189b9 seen=2026-11-12T21:10Z url=…⟧
src/ledger.rs:11:     let conn = open(url())?;
  cite: ⟦cite kind=code repo=harbor-api rev=4be03f78… path=src/ledger.rs L=11-11 blob=b7092119… span=0c70393772e189b9 seen=2026-11-12T21:10Z url=…⟧
# coverage=complete files=2/2 hits=3 shown=3 omitted=0 cursor=none program=5f03442bdbd6'''
RESEARCH = '''$ writfold kb find "harbr-api"                    # records by words, a partial ID or a typo
$ writfold kb why "batch ledger writes"           # the accepted decision and its reasons
$ writfold kb context HBR-101                     # everything around one record
$ writfold kb impact harbor-db --direction in     # what a change touches, and how far it walked
$ writfold kb stale                               # which citations have moved
$ writfold tuft run q.tuft --repo . --cite        # exact text in code, each row with a citation'''
EXECUTE = '''$ writfold kb edit apply retry.spl --dry-run      # the preview diff; nothing written
$ writfold kb edit apply retry.spl                # every file or none, with an edit receipt
$ writfold kb gate run unit                       # run the command, keep a receipt
$ writfold kb gate attest wording --statement "README unchanged" --by agent
$ writfold kb gate status                         # what is met, and what is still owed
$ writfold kb checkpoint --note "Retry applied; next: commit and post."
$ writfold watch                                  # runs, gates, receipts and drafts, read-only'''
DELIVERY = '''$ writfold kb deliver prepare --mode pr-comment --from comment.md \\
    --audience external --destination harbor#42   # copy the draft into the run
$ writfold kb deliver check                       # three checks on those exact bytes
$ writfold kb deliver status                      # ready or blocked, and why'''
STALE_GATE = '''$ writfold kb gate status
gate unit [stale] mechanical pass exit=0 at harbor-api@4be03f7897b6+dirty:2 scope=01cc14a55a8f paths=2 @runs/run-…/gates/unit-20261112T211036Z-f5f8fb.json:1 !stale
  why: changed in scope: src/audit.rs, src/ledger.rs
  next: writfold kb gate run unit
gate wording [attested] attested: statements only, no command, for harbor-api @harbor-api:.writfold/gates/wording.toml:1 !attested
  attested: README unchanged; guideline read (by agent, 2026-11-12T21:10:36Z) @runs/run-…/statements/wording-20261112T211036Z-273294.json:1
# note: receipts of run run-20261112T211025Z-7fe148 for harbor-api; state is derived on every read, never stored
# coverage=complete records=45/45 shown=2 omitted=0 gates=2 satisfied=0 open=0 stale=1 failed=0 unknown=0 attested=1 waived=0 invalid=0 kb=4ba5227faf95+dirty:18 index=fresh cursor=none q=ea37655d9d25'''
RECORD = '''$ writfold kb record decision --title "Retry ledger connections" \\
    --target-source harbor-api --project harbor
$ writfold kb record ticket HBR-102 --title "Replay too slow" --assets harbor-api,harbor-db
$ writfold kb record link depends-on quay-worker harbor-db \\
    --evidence harbor-api@4be03f7897b691715114a229ab1acc307f5de90f:src/ledger.rs:3-5
$ writfold kb cite make harbor-api src/ledger.rs 3-3     # prints a citation token; writes nothing
$ writfold kb status HBR-101 --set done'''
NEWRUN = '''$ writfold kb checkpoint --new-run --project harbor --task "Retry ledger connections" \\
    --note "Plan: wrap every open(url()) in with_retry; gate unit; PR comment for harbor#42."
run run-20261112T211025Z-7fe148 [open] Retry ledger connections @runs/run-…/manifest.json:8 !current
  field: project=harbor @runs/run-…/manifest.json:5
  field: repo=harbor-api @runs/run-…/writfold-run.json:5
  field: branch=main @runs/run-…/writfold-run.json:6
  field: worktree=…/harbor-api @runs/run-…/writfold-run.json:7
  field: base=4be03f7897b691715114a229ab1acc307f5de90f @runs/run-…/writfold-run.json:8
checkpoint 2026-11-12T21:10:25Z entry 1 of 1 @runs/run-…/checkpoint.md:2
  note: Plan: wrap every open(url()) in with_retry; gate unit; PR comment for harbor#42. @runs/run-…/checkpoint.md:4
# note: written to the work tree; commit it to share it
# coverage=complete records=31/31 shown=2 omitted=0 kb=4ba5227faf95+dirty:3 index=refreshed:3 cursor=none q=bcaf6baf8b52'''
SPL = '''$ cat retry.spl
%spl
edit "src/ledger.rs" {
  each @r in line_matches rx"^\\s+let conn = (?<call>open\\(url\\(\\)\\))\\?;$" expect 2 {
    replace @r.call with ["with_retry(3, || ", keep(@r.call), ")"]
  }
}

$ writfold kb edit apply retry.spl retry-audit.spl --dry-run     # prints the preview diff; writes nothing
$ writfold kb edit apply retry.spl retry-audit.spl
edit src/ledger.rs [applied] recipe=retry.spl splices=2 -22 +58 bytes before=b7092119ef98 after=1632101105b5 @runs/run-…/edits/20261112T211036Z-524711.md:23
  site: line 3 bytes [84,95) -> 29 bytes, recipe [112,174)
  site: line 11 bytes [245,256) -> 29 bytes, recipe [112,174)
edit src/audit.rs [applied] recipe=retry-audit.spl splices=1 -11 +29 bytes before=e77382cb29f8 after=5519381f9fe0 @runs/run-…/edits/20261112T211036Z-524711.md:26
  site: line 3 bytes [84,95) -> 29 bytes, recipe [111,173)
# note: recorded runs/run-…/edits/20261112T211036Z-524711.md
# note: applied in …/harbor-api: an ordinary uncommitted change; review it, run its gates (writfold kb gate status), commit it
# coverage=complete records=33/33 shown=2 omitted=0 kb=4ba5227faf95+dirty:5 index=refreshed:1 cursor=none q=7fa936a84f6a'''
GATEDEF = '''# .writfold/gates/unit.toml: a command gate
schema = "writfold-gate/1"
id = "unit"
version = 1
class = "mechanical"
argv = ["cargo", "test"]
workdir = "."
timeout_seconds = 600
scope = ["src/**", "Cargo.toml"]

# .writfold/gates/wording.toml: an attested gate; it runs nothing
schema = "writfold-gate/1"
id = "wording"
version = 1
class = "attested"
scope = ["README.md"]
description = "README follows the language guideline"'''
GATES = '''$ writfold kb gate status
gate unit [open] mechanical no receipt in this run for harbor-api @harbor-api:.writfold/gates/unit.toml:1 !open
  next: writfold kb gate run unit
gate wording [open] attested: statements only, no command, for harbor-api @harbor-api:.writfold/gates/wording.toml:1 !open
  next: writfold kb gate attest wording --statement TEXT --by WHO
…
$ writfold kb gate run unit
gate unit [satisfied] mechanical pass exit=0 at harbor-api@4be03f7897b6+dirty:2 scope=01cc14a55a8f paths=2 @runs/run-…/gates/unit-20261112T211036Z-f5f8fb.json:1
…
$ writfold kb gate attest wording --statement "README unchanged; guideline read" --by agent
gate wording [attested] attested: statements only, no command, for harbor-api @harbor-api:.writfold/gates/wording.toml:1 !attested
  attested: README unchanged; guideline read (by agent, 2026-11-12T21:10:36Z) @runs/run-…/statements/wording-20261112T211036Z-273294.json:1
…
$ writfold kb gate status
…
# coverage=complete records=35/35 shown=2 omitted=0 gates=2 satisfied=1 open=0 stale=0 failed=0 unknown=0 attested=1 waived=0 invalid=0 kb=4ba5227faf95+dirty:7 index=fresh cursor=none q=ea37655d9d25'''
WATCH = '''$ writfold watch --once
== runs (2 listed, 2 not closed) ==
> [open] run-20261112T211025Z-7fe148 !current
    Retry ledger connections
    project=harbor repo=harbor-api branch=main worktree=…/harbor-api base=4be03f7897b6
    last: 2026-11-12T21:10:45Z Retry applied in ledger.rs and audit.rs; unit satisfied; PR comment ready. Next: commit and post.
  [open] run-20261101T090000Z-a1b2c3
    Batch ledger writes rollout
== resume run-20261112T211025Z-7fe148 ==
gates: gates=2 satisfied=1 open=0 stale=0 failed=0 unknown=0 attested=1 waived=0 invalid=0
…
retrieval 20261112T211036Z-c7b86d tuft/0 program=5f03442bdbd6 harbor-api@4be03f7897b6 rows=3 shown=3 cites=3 @runs/run-…/retrievals/20261112T211036Z-c7b86d.md:1
edit 20261112T211036Z-524711 splicery files=2 splices=3 at harbor-api@4be03f7897b6 @runs/run-…/edits/20261112T211036Z-524711.md:1
gate unit [satisfied] mechanical pass exit=0 at harbor-api@4be03f7897b6+dirty:2 scope=01cc14a55a8f paths=2 @runs/run-…/gates/unit-20261112T211036Z-f5f8fb.json:1
gate wording [attested] attested: statements only, no command, for harbor-api @harbor-api:.writfold/gates/wording.toml:1 !attested
delivery 20261112T211045Z-ee94cc [ready] pr-comment audience=external destination=harbor#42 candidate=f5d111e329c7 bytes=67 @runs/run-…/deliveries/20261112T211045Z-ee94cc/candidate.md:1
checkpoint 2026-11-12T21:10:45Z entry 2 of 2 @runs/run-…/checkpoint.md:6
== kb=4ba5227faf95+dirty:18 index=fresh  read-only; no daemon, nothing here claims a run is live =='''
DELIVER = '''$ writfold kb deliver prepare --mode pr-comment --from comment.md --audience external --destination harbor#42
$ writfold kb deliver check
delivery 20261112T211045Z-ee94cc [blocked] pr-comment audience=external destination=harbor#42 candidate=bb69f10c8fd9 bytes=136 @runs/run-…/deliveries/20261112T211045Z-ee94cc/candidate.md:1 !blocked
  check: paragraphs.bounded [satisfied] mechanical pass for bb69f10c8fd9 (at most 150 words per paragraph) @runs/run-…/checks/paragraphs.bounded-….json:1
  check: references.denied [failed] mechanical fail for bb69f10c8fd9: line 3 internal-host (column 50); line 3 ticket (column 23) @runs/run-…/checks/references.denied-….json:1 !failed
  check: claims.cited-fresh [satisfied] observed pass for bb69f10c8fd9 (0 citation tokens) @runs/run-…/checks/claims.cited-fresh-….json:1
…
$ $EDITOR runs/run-…/deliveries/20261112T211045Z-ee94cc/candidate.md     # remove the internal references
$ writfold kb deliver check
delivery 20261112T211045Z-ee94cc [ready] pr-comment audience=external destination=harbor#42 candidate=f5d111e329c7 bytes=67 @runs/run-…/deliveries/20261112T211045Z-ee94cc/candidate.md:1 !edited
  check: paragraphs.bounded [satisfied] mechanical pass for f5d111e329c7 (at most 150 words per paragraph) @runs/run-…/checks/paragraphs.bounded-….json:1
  check: references.denied [satisfied] mechanical pass for f5d111e329c7 (2 rules for external) @runs/run-…/checks/references.denied-….json:1
  check: claims.cited-fresh [satisfied] observed pass for f5d111e329c7 (0 citation tokens) @runs/run-…/checks/claims.cited-fresh-….json:1
# note: standing is derived on every read; checks are mechanical, attestations are statements, and nothing is sent'''
DENY = '''# .writfold/deliveries/deny-external.toml
schema = "writfold-deny/1"
audience = "external"
rules = ["internal-host: \\\\.corp\\\\.example\\\\.com", "ticket: \\\\bOPS-[0-9]+"]'''
REAL = "Real output from a demo repository. Run IDs, digests and paths are shortened with <code>…</code>."

def cfg_row(path, what, state):
    chip = '<span class="chip chip-today">Runs today</span>' if state else '<span class="chip chip-planned">Planned</span>'
    return f'<tr><th scope="row"><code>{escape(path)}</code></th><td>{what}</td><td>{chip}</td></tr>'
CFG = "".join([
    cfg_row(".writfold/gates/<id>.toml", "A gate: a command with a path scope, or an attested gate met by a statement. In the knowledge base or in the repository it checks.", True),
    cfg_row(".writfold/deliveries/<mode>.toml", "Narrow a built-in delivery mode: which checks, the paragraph bound, statements it needs.", True),
    cfg_row(".writfold/deliveries/deny-<audience>.toml", "References a draft for that audience must not contain.", True),
    cfg_row(".writfold/deliveries/guard.toml", "Publishing commands the optional guard hook watches. Absent means the guard is off.", True),
    cfg_row("a gate's instructions (.md)", "A gate names an <code>.md</code> file the agent reads, and ships its own scripts. Editing the instructions makes earlier evidence stale.", False),
    cfg_row(".writfold/deliveries/<name>.toml", "Your own delivery mode, such as a commit message, listing its gates.", False),
    cfg_row(".writfold/plans/<name>.toml", "Plan templates. A skill names one in a line of its text.", False),
])

how = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="how-title">
      <p class="eyebrow">How it works</p>
      <h1 id="how-title">Four stages.<br><span>A record of each.</span></h1>
      <p class="lede">Writfold follows a piece of work from research to delivery. At each stage the agent picks the tool that fits, and what it learned goes back into a knowledge base in Git. This page walks the flow with real commands, and marks what is planned.</p>
      <nav class="actions" aria-label="Page sections"><a href="#kb">Knowledge base</a><a href="#research">1 Research</a><a href="#plan">2 Plan</a><a href="#execute">3 Execute</a><a href="#deliver">4 Deliver</a><a href="#gates">Gates</a><a href="#configure">Configuration</a></nav>
      {flow_figure("wf", "Every stage writes to the knowledge base, and the knowledge base answers the next session.")}
    </section>

    <section id="kb" class="section" aria-labelledby="kb-title">
      <div class="section-heading"><p class="eyebrow">The base</p><h2 id="kb-title">Records in Git, an index you can rebuild</h2><p>The knowledge base is a Git repository of plain Markdown and JSON: decisions, tickets, assets, links between them, and one folder per run. Git is the only store, so a new machine needs <code>git clone</code> and the binary.</p></div>
      <div class="three-up">
        <article class="capability"><span class="number">01</span><h3>Every row names its source</h3><p>Each line of an answer ends in <code>@path:line</code>. The last line says what was examined, what was omitted and how many sources are stale.</p></article>
        <article class="capability"><span class="number">02</span><h3>Citations are pinned</h3><p>A citation pins <code>path@commit:lines</code> with a digest. <code>kb stale</code> reports each one as fresh, moved, changed or gone, against local clones.</p></article>
        <article class="capability"><span class="number">03</span><h3>The index is derived</h3><p>A local SQLite index speeds up search. <code>kb index verify</code> checks that it equals a fresh rebuild.</p></article>
      </div>
      <p class="boundary">Writes are plain files left uncommitted, for you or the agent to review and commit. With the Claude Code plugin, a session starts with <code>brief</code> and <code>resume</code> already in context.</p>
    </section>

    <section id="research" class="section" aria-labelledby="research-title">
      <div class="section-heading"><p class="eyebrow">Stage 1 / Research</p><h2 id="research-title">Ask the knowledge base, or search the code</h2><p>Two kinds of retrieval, for two kinds of question.</p></div>
      <div class="status-grid">
        <article class="status-card"><p class="status-label">The <code>kb</code> verbs</p><p>For what the project already knows. <code>find</code> searches records by words, a partial ID or a typo. <code>why</code> gives the accepted decision and its reasons. <code>context</code> gathers everything around one record. <code>impact</code> walks the links to show what a change touches, and says how far it walked.</p></article>
        <article class="status-card"><p class="status-label">Tuft</p><p>For what the code says. A short Tuft program finds exact text or a bounded regex at one pinned commit and prints rows within an output budget, with a cursor for the rest. With <code>--cite</code>, each row carries a citation token for its lines.</p></article>
      </div>
      {panel("Research commands", RESEARCH)}
      {exact("<code>kb find</code> with a typo", "kb find output", FIND)}
      {exact("a Tuft program and its rows", "Tuft program and output", TUFT)}
      <p class="boundary"><strong>Into the knowledge base.</strong> Inside an open run, each <code>tuft run</code> records a retrieval receipt: the program, the commit, the row counts and the citations. A citation token pasted into a record is re-checked by <code>kb stale</code>. What the agent concludes, it writes down:</p>
      {panel("Record commands", RECORD)}
      <p class="fine-print">Tuft keeps the bytes it retains in a local state directory; create it once with <code>writfold trial init</code>. Tuft is maintained, and new language features are not a priority. <span class="chip chip-planned">Planned</span> The same answers over MCP, for other harnesses.</p>
    </section>

    <section id="plan" class="section" aria-labelledby="plan-title">
      <div class="section-heading"><p class="eyebrow">Stage 2 / Plan</p><h2 id="plan-title">Start a run. Verified plans are next.</h2><p>Today a run records the task, the repository, branch, worktree and base commit, and the plan is the first checkpoint note. <code>kb resume</code> shows it to any later session.</p></div>
      {panel("Starting a run", NEWRUN.split(chr(10)+"run ")[0])}
      {exact("starting a run", "Starting a run", NEWRUN)}
      {planned("""
        <h3>Plans with steps</h3>
        <p><code>plan set</code> copies a plan into the run. Each step names the gates it owes. <code>plan status</code> shows the current step and what it still owes, and <code>plan advance</code> moves on only when those gates are met. A plan can start from a template in <code>.writfold/plans/</code> that a skill names.</p>
        <h3>Weft verifies a plan step</h3>
        <p>A step can require a Weft assessment. The agent writes the step&rsquo;s assumptions and checks in a Weft file, and each assumption can cite a Writfold receipt or citation. Writfold confirms those are still fresh, runs Weft, and records the result. A check counts only when it follows from assumptions backed by evidence. One that rests on an unbacked assumption is reported as hypothetical and does not meet the gate.</p>""")}
    </section>

    <section id="execute" class="section" aria-labelledby="execute-title">
      <div class="section-heading"><p class="eyebrow">Stage 3 / Execute</p><h2 id="execute-title">Edit, check, and keep track</h2><p>The agent edits the run&rsquo;s worktree, runs the gates, and checkpoints as it goes.</p></div>
      <div class="status-grid">
        <article class="status-card"><p class="status-label">Splicery recipes</p><p>For repeated or structural edits: every line matching a pattern, a block between two anchors, the same change across files. A recipe states how many matches it expects and refuses on any other count. <code>kb edit apply</code> replays it on the worktree&rsquo;s current bytes and writes every file or none. After a crash, <code>kb edit recover</code> finishes the batch.</p></article>
        <article class="status-card"><p class="status-label">Ordinary Edit, grep and sed</p><p>For one small change. No recipe, no receipt, and nothing in Writfold stands in the way. Either way the result is an uncommitted Git change, and any gate whose scope covers it goes stale until it runs again.</p></article>
      </div>
      {panel("Execute commands", EXECUTE)}
      {panel("A Splicery recipe", SPL.split("$ cat retry.spl")[1].split("$ writfold")[0].replace("%spl", "").strip(), "A recipe: wrap both <code>open(url())</code> calls in <code>src/ledger.rs</code>, and refuse unless there are exactly two.", "spl")}
      {exact("the recipe applied", "Splicery recipe and edit apply output", SPL)}
      <h3 class="subhead">Gates</h3>
      <p>A gate is one small check, defined in a TOML file. <code>gate run</code> runs its command and keeps a receipt pinned to the commit and the bytes in scope. An attested gate runs nothing: it is met by a statement with a name on it, and is shown as attested, never as passed. A timeout or crash is unknown, never a pass.</p>
      {panel("Two gate definitions", GATEDEF, "The two kinds of gate definition.", "toml")}
      {exact("gates from open to met", "Gate status, run and attest output", GATES)}
      <h3 class="subhead">Progress</h3>
      <p><code>kb checkpoint --note</code> saves where the work stands. <code>writfold watch</code> keeps runs, gate states, receipts and drafts in view in a terminal pane; it is read-only, and <code>--once</code> prints one frame.</p>
      {board("The same run after one more ordinary edit: the <code>unit</code> receipt is stale, and the next command is named.")}
      {exact("<code>gate status</code> for this run", "gate status output", STALE_GATE)}
      {exact("one <code>watch --once</code> frame, before that edit", "watch output", WATCH)}
      <p class="boundary"><strong>Into the knowledge base.</strong> Checkpoints, an edit receipt per <code>edit apply</code> (the recipe, the sites it changed and the preview diff), a receipt per gate run, and each statement.</p>
      <p class="fine-print">Splicery is maintained, and new language features are not a priority. <span class="chip chip-planned">Planned</span> <code>plan advance</code>, and gates that carry written instructions.</p>
    </section>

    <section id="deliver" class="section" aria-labelledby="deliver-title">
      <div class="section-heading"><p class="eyebrow">Stage 4 / Deliver</p><h2 id="deliver-title">Drafts, checked. Nothing sent.</h2><p><code>kb deliver prepare</code> copies a PR comment or Slack summary into the run as the exact text that would be posted. <code>deliver check</code> runs three checks on those bytes: paragraph length, references the audience must not see, and whether every citation in it is still fresh.</p></div>
      {panel("Delivery commands", DELIVERY)}
      {drafts()}
      {panel("Deny list", DENY, "The deny list behind <code>references.denied</code> in this example.", "toml")}
      {exact("the draft checked, fixed and checked again", "Deliver check output", DELIVER)}
      <p>A failing check names the line and the rule. Editing the draft makes its earlier receipts stale, so it is checked again. Writfold has no network code and no Slack or PR adapter: posting stays with you or your agent.</p>
      <p class="boundary"><strong>Into the knowledge base.</strong> The draft itself and one receipt per check, kept in the run.</p>
      <p class="fine-print">The checks are mechanical. They do not judge tone or truth, and they miss a claim made without a citation. An optional Claude Code hook, off unless configured, can deny a listed publishing command until a ready draft holds the exact bytes: a guard, not enforcement. <span class="chip chip-planned">Planned</span> Your own delivery modes, such as a commit message.</p>
    </section>

    <section id="gates" class="section" aria-labelledby="gates-title">
      <div class="section-heading"><p class="eyebrow">The thread</p><h2 id="gates-title">Gates, evidence, then the next step</h2><p>Gates are the atomic checks. Runs and delivery drafts owe them. Evidence that Writfold records meets them. The agent submits drafts, statements and plans; Writfold writes every receipt.</p></div>
      <figure class="diagram-figure">{diagrams.LEGEND}{diagrams.gates("wg")}<figcaption class="fine-print">Evidence is tied to exact bytes. When they change, the gate is owed again.</figcaption></figure>
      <div class="status-grid gates-grid">
        <article class="status-card"><p class="status-label">Runs today</p><p>Command gates and attested gates. Receipts and statements pinned to bytes. Two delivery modes with three built-in checks. Every gate defined for a repository is owed by every run on it, and <code>gate status</code> exits 0 only when all are met.</p></article>
        <article class="status-card planned-card"><p class="status-label pending">Planned</p><p>Gates that point to written instructions and bring their own scripts. Delivery modes you define, each listing its gates. Plan steps that name their gates, so <code>plan advance</code> moves to the next step once they are met. Skills that start a plan from a template. Weft assessments as evidence for a step.</p></article>
      </div>
      <p class="boundary">Gates report; they block nothing. Receipts resist mistakes, such as a forgotten check or a stale &ldquo;tests pass&rdquo;. They are tracked files, not signatures.</p>
    </section>

    <section id="configure" class="section" aria-labelledby="configure-title">
      <div class="section-heading"><p class="eyebrow">Configuration</p><h2 id="configure-title">What Writfold reads from <code>.writfold/</code></h2><p>Gates and delivery rules are small files in Git, next to the records. A new machine gets them with the clone.</p></div>
      <div class="table-scroll"><table class="status-table">
        <thead><tr><th scope="col">File</th><th scope="col">What it defines</th><th scope="col">State</th></tr></thead>
        <tbody>{CFG}</tbody>
      </table></div>
      <p class="fine-print">Ready to try it? <a href="/#try">Download the preview</a>, or see <a href="/status.html">what runs and what is next</a>.</p>
    </section>
  </main>
'''
page("how.html", "How it works — Writfold",
     "The Writfold flow stage by stage: research, plan, execute, deliver. Which tool fits each stage, what goes back into the knowledge base, and what is planned.",
     "/how.html", how)

# ---------------------------------------------------------------- status
README = "https://github.com/writfold-dev/writfold#readme"
def row(href, title, text):
    return f'<a href="{href}"><span><strong>{title}</strong><small>{text}</small></span><span aria-hidden="true">→</span></a>'
TODAY = "".join([
    row("/how.html#research", "Read verbs", "<code>writfold kb brief | context | why | status | find | match | impact | uses | timeline | stale | resume | runs</code> over plain Markdown and JSON records in Git. Every answer ends with a coverage line: what was examined, what was omitted, and whether any cited source is stale. <code>find</code> tolerates a typo; <code>impact</code> states how far it searched"),
    row("/how.html#research", "Write verbs", "<code>checkpoint</code>, <code>record ticket|decision|link</code>, <code>status --set</code> and <code>cite make</code> write plain files atomically and leave them uncommitted"),
    row("/how.html#kb", "Index and citations", "A local SQLite index derived from Git; <code>index verify</code> checks it equals a rebuild. Each citation pins <code>path@commit:lines</code> with a digest, and <code>stale</code> reports it fresh, moved, changed or gone"),
    row("/how.html#research", "Retrieval with Tuft", "<code>writfold tuft run --cite</code> finds exact text or a bounded regex at one pinned commit, within an output budget. Each row carries a citation token, and a search inside a run is kept as a retrieval receipt"),
    row("/how.html#execute", "Edits with Splicery", "<code>kb edit apply</code> replays Splicery recipes against the run&rsquo;s worktree, uncommitted edits included. If any recipe or file fails, nothing is written; otherwise each file is written atomically after a re-check, and an edit receipt is kept. A crash between files leaves a journal that <code>kb edit recover</code> finishes"),
    row("/how.html#execute", "Gates with pinned receipts", "<code>kb gate run | status | verify | lines | attest | waive</code>. A gate is a small TOML file naming a command and the paths it covers. Each receipt is pinned to the exact bytes in scope, and the state is derived on every read: open, satisfied, stale, failed, unknown, attested or waived. An attested gate runs nothing and is met by a recorded statement. A timeout or crash is never a pass. Writfold&rsquo;s own pushes to main go through <code>kb gate run</code>, with the receipt lines in the commit message"),
    row("/how.html#deliver", "Delivery drafts", "<code>kb deliver prepare | check | status | attest | waive</code> keeps a PR comment or Slack summary in the run as the exact text to post, checked for paragraph length, references denied for the audience and fresh citations. Editing a draft makes its checks stale. Nothing is ever sent"),
    row("/how.html#execute", "<code>writfold watch</code>", "A read-only terminal view of runs, checkpoints, gate states, receipts and drafts, built only from the same verbs. <code>--once</code> prints one frame as text"),
    row("https://github.com/writfold-dev/writfold/tree/main/plugins/writfold", "Claude Code plugin", "A project brief at session start with no tool call, local checkpoint drafts before compaction and at stop, and one skill. An optional PreToolUse hook, off unless configured, denies a listed publishing command unless a ready draft holds the exact bytes: a guard, not enforcement"),
])
def step(title, text, chip):
    cls = {"Done": "chip-today", "Next": "chip-progress", "Planned": "chip-planned"}[chip]
    return f'<li><div><h3>{title}</h3><p>{text} <span class="chip {cls}">{chip}</span></p></div></li>'
ROAD = "".join([
    step("The four questions", "Read and write verbs, the rebuildable index with typo-tolerant search, pinned citations and <code>stale</code>, and the Claude Code plugin.", "Done"),
    step("Runs with gates, edits and drafts", "Gates with pinned receipts, statements, Splicery edits in a run, Tuft citations and retrieval receipts, delivery drafts, <code>writfold watch</code> and the optional guard hook.", "Done"),
    step("Instruction gates and your own delivery modes", "A gate can point to an <code>.md</code> file of instructions and come with its own scripts. A delivery mode, such as a commit message, is a small file listing its gates.", "Next"),
    step("Plans and <code>plan advance</code>", "<code>plan set | status | advance</code>: a plan in the run lists steps and the gates each one owes, and advance refuses until the current step&rsquo;s gates are met. Plan templates live under <code>.writfold/plans/</code>, and a skill names one in a line.", "Planned"),
    step("Weft plan verification", "A plan step can require a Weft assessment of its assumptions and checks, with assumptions backed by Writfold receipts and citations.", "Planned"),
    step("A two-week pause", "Use it on real work and count what the checks caught before adding more.", "Planned"),
    step("MCP", "The same answers over MCP, for other harnesses.", "Planned"),
    step("Trailer and tracker edges, and <code>--at</code>", "Links derived from commit trailers and tracker references, and reads at an earlier commit.", "Planned"),
])
LOG = "".join(f"<li><time>{d}</time><p>{t}</p></li>" for d, t in [
    ("12 Nov 2026", "Direction for the next slices: gates with written instructions, delivery modes you define, plans with <code>plan advance</code>, and Weft verifying plan steps. All planned; none is built. The site now follows the flow from research to delivery."),
    ("12 Nov 2026", f'Preview <a href="{REL}">v0.3.0-dev.1</a>: gates with pinned receipts (<code>kb gate</code>), Splicery edits in a run&rsquo;s worktree (<code>kb edit apply | recover</code>), the read-only <code>writfold watch</code> view, offline PR-comment and Slack-summary drafts with their checks (<code>kb deliver</code>), and an optional guard hook.'),
    ("12 Nov 2026", 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.2.0-dev.1">v0.2.0-dev.1</a>: a static Linux x86_64 binary with the <code>kb</code> read and write verbs, the rebuildable index and citations checked for staleness. A Claude Code plugin brings the brief and checkpoint drafts into a session. <code>writfold tuft run --cite</code> adds citation tokens to its rows and records searches as receipts.'),
    ("11 Nov 2026", "Mission set: Git-native project continuity for coding agents. Git is the only store, with a local index Writfold derives and can always rebuild."),
])
def faq(q, a): return f"<details><summary>{q}</summary><p>{a}</p></details>"
FAQ = "".join([
    faq("Can I use Writfold today?", 'Yes, as a preview: <a href="/#try">download the binary and install the plugin</a>. It is for a single user with cooperating agents, reads local clones only and never fetches, and runs on Linux x86_64 or WSL2.'),
    faq("Does it need a server or a database?", "No. It is one static binary, project memory as plain records in Git, and a local index that Writfold derives and can always rebuild. A new machine needs <code>git clone</code> plus the binary. No hosted service or account."),
    faq("Does it replace my coding agent?", "No. The agent keeps its own loop and model, and asks Writfold about the project. The Claude Code plugin works today; MCP is planned."),
    faq("When should an agent use Tuft or Splicery?", "Tuft when the question is about the code at a known commit and the answer should carry citations; <code>kb find</code> when it is about the project&rsquo;s records. Splicery when an edit repeats or has structure; ordinary Edit, grep and sed for one small change. Both tools are maintained; new language features are not a priority."),
    faq("Does Writfold post PR comments or Slack messages?", "No. <code>kb deliver</code> keeps drafts with their checks in the run; nothing is ever sent, and there are no Slack or PR adapters."),
    faq("Can an agent skip a gate?", "Gates record what was checked and report whether it still holds; on their own they block nothing. Receipts resist mistakes, not adversaries: they are tracked files, so an edited one shows in Git history and <code>gate verify</code>, but nothing is signed. The optional hook is a guard, not enforcement."),
    faq("Can a gate be a judgement, such as &ldquo;the wording is clear&rdquo;?", "Only as a statement. An attested gate records who said so, about which bytes, and is shown as attested, never as passed. Writfold runs no model and does not judge tone or truth."),
    faq("Can a skill require gates?", "Not yet. Today every gate defined for a repository is owed by every run on it, and a skill can only tell the agent which to run. Plan steps that name their gates, started from a template a skill names, are planned."),
    faq("Does Weft check plans today?", "No. Weft verifying a plan step is planned. Today a plan is a checkpoint note in the run."),
    faq("Is the source available?", 'Yes. The <a href="https://github.com/writfold-dev/writfold">Writfold</a>, <a href="https://github.com/writfold-dev/weft">Weft</a> and <a href="https://github.com/writfold-dev/splicery">Splicery</a> repositories are public, and this website is public under the MIT license.'),
])
status = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="status-title">
      <p class="eyebrow">Status</p>
      <h1 id="status-title">What runs today.<br><span>What comes next.</span></h1>
      <p class="lede">Writfold is <a href="/">Git-native project continuity for coding agents</a>. The preview covers research, execution and delivery drafts. Plan steps and plan verification are planned.</p>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">v0.3.0-dev.1</a> · Updated 12 November 2026</span></p>
      <nav class="actions" aria-label="Page sections"><a href="#today">Runs today</a><a href="#next">Roadmap</a><a href="#changelog">Changelog</a><a href="#faq">FAQ</a></nav>
    </section>
    <section id="today" class="section" aria-labelledby="today-title">
      <div class="section-heading"><p class="eyebrow">01 / Runs today</p><h2 id="today-title">In the preview</h2><p>From <a href="{REL}">v0.3.0-dev.1</a>, a static Linux x86_64 binary with a <code>.sha256</code> file. <a href="/#try">Try it</a>, or read the <a href="{README}">README</a>.</p></div>
      <div class="doc-links">{TODAY}</div>
      <p class="fine-print">Measured: reads at most 45&nbsp;ms on 4,130 records; writes about 120&ndash;130&nbsp;ms. Writes of checkpoints, receipts, edits and drafts killed at every step leave the old or the new complete state. A TLA+ model of the write protocol passes, and its five mutants fail.</p>
      <p class="fine-print">Limits: single user with cooperating agents; local clones only. The delivery checks are covered by tests and demo runs; no real PR comment or Slack summary has gone through them yet.</p>
    </section>
    <section id="next" class="section" aria-labelledby="next-title">
      <div class="section-heading"><p class="eyebrow">02 / Roadmap</p><h2 id="next-title">In order</h2><p>The intended flow is on <a href="/how.html">How it works</a>, with the same labels.</p></div>
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
     "What runs in the Writfold preview, what is planned next, a short changelog and FAQ.", "/status.html", status)

# ---------------------------------------------------------------- 404 and redirects
page("404.html", "Page not found — Writfold", "This page is not part of writfold.dev.", None,
     '''  <main id="main" class="wrap error-page" tabindex="-1"><p class="eyebrow">404 / Page not found</p><h1>This page isn't in the record.</h1><p>The address may have changed, or the page may never have existed.</p><div class="actions"><a class="button" href="/">Back to the overview</a><a href="/how.html">How it works</a><a href="/status.html">Status</a></div></main>
''')
STUBS = {"earlier.html": ("/", "the overview"), "docs.html": ("/how.html", "How it works"), "glossary.html": ("/how.html", "How it works"),
         "tuft.html": ("/how.html#research", "Retrieval with Tuft, on How it works"),
         "splicery.html": ("/how.html#execute", "Edits with Splicery, on How it works"),
         "weft.html": ("/how.html#plan", "Plan verification (planned), on How it works")}
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
