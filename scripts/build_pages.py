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

def flow_figure(pfx, caption):
    return (f'<figure class="diagram-figure">{diagrams.LEGEND}{diagrams.flow(pfx)}'
            f'<figcaption class="fine-print">{caption}</figcaption></figure>')

# ---------------------------------------------------------------- index
GUIDE = "https://github.com/writfold-dev/writfold/blob/main/docs/guide/"

def guide(page, label):
    return f'<a href="{GUIDE}{page}.md">{label}</a>'

def more(*links):
    """The one link out of a section: the matching guide in the Writfold repository."""
    return f'<p class="guide-link"><span aria-hidden="true">→</span> Full skeleton: {" and ".join(links)}</p>'

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
      <div class="section-heading"><p class="eyebrow">The flow</p><h2 id="flow-title">Research, plan, execute, deliver. Each stage writes back.</h2><p>The agent keeps its own loop and model. What it finds, checks or drafts at each stage goes back into the knowledge base, so the next session starts from more than this one did.</p></div>
      {flow_figure("hf", "Planned: the run graph, required steps that backfill the knowledge base and close every run with a reflection, and your own delivery modes.")}
      <p class="boundary">The knowledge base is plain Markdown and JSON in Git. Writes are left uncommitted for you to review and commit. The index refreshes itself on every read; <code>kb stale</code>, <code>kb index verify</code> and <code>gate status</code> re-check citations, the index and gate evidence on demand. <a href="/how.html">Walk through the stages</a>.</p>
    </section>

    <section id="runs" class="section" aria-labelledby="runs-title">
      <div class="section-heading"><p class="eyebrow">Inside a run</p><h2 id="runs-title">Gates, evidence, and what is still owed</h2><p>A gate is one small check: a command and the paths it covers, or a statement someone must make. <code>gate run</code> keeps a receipt for the exact bytes checked, and when those bytes change the gate is owed again. <code>resume</code> lists what is met and what is owed, with the next command.</p></div>
      {board('One run, drawn from what <code>resume</code> prints for a demo repository.')}
      <p class="boundary">Gates report; they block nothing. Draft PR comments and Slack summaries carry their own checks, and nothing is sent.</p>
      {more(guide("gates", "the gates guide"))}
    </section>

    <section id="try" class="section" aria-labelledby="try-title">
      <div class="section-heading"><p class="eyebrow">Try it</p><h2 id="try-title">Download, verify, install the plugin</h2><p>Linux x86_64 or WSL2. The plugin adds a project brief at session start and keeps local checkpoint drafts.</p></div>
      {pre("Download and install commands", INSTALL, "shell")}
      <p class="fine-print">Single user, cooperating agents, local clones only; nothing is fetched. Setup is in the <a href="https://github.com/writfold-dev/writfold#readme">README</a>.</p>
    </section>

    <section id="first" class="section" aria-labelledby="first-title">
      <div class="section-heading"><p class="eyebrow">Built</p><h2 id="first-title">What the preview runs</h2></div>
      <dl class="verbs">
        <div><dt>Read</dt><dd><code>brief</code> <code>why</code> <code>status</code> <code>find</code> <code>impact</code> <code>resume</code>: {guide("kb-layout", "layout")}</dd></div>
        <div><dt>Write</dt><dd><code>checkpoint</code> <code>record</code> <code>cite make</code>: {guide("feeding-back", "feeding back")}</dd></div>
        <div><dt>Check</dt><dd><code>stale</code> <code>index verify</code>: {guide("validation", "validation")}</dd></div>
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
    --evidence harbor-api@4be03f7897b691715114a229ab1acc307f5de90f:src/ledger.rs:3-5'''
NEWRUN = '''$ writfold kb checkpoint --new-run --project harbor --task "Retry ledger connections" \\
    --note "Plan: wrap every open(url()) in with_retry; gate unit; PR comment for harbor#42."'''
EXECUTE = '''$ writfold kb edit apply retry.spl --dry-run      # the preview diff; nothing written
$ writfold kb edit apply retry.spl                # every file or none, with an edit receipt
$ writfold kb gate run unit                       # run the command, keep a receipt
$ writfold kb gate attest wording --statement "README unchanged" --by agent
$ writfold kb checkpoint --note "Retry applied; next: commit and post."'''
CHECK = '''$ writfold kb stale            # which cited sources moved, changed or expired
$ writfold kb index verify     # the index equals a fresh rebuild
$ writfold kb gate status      # which gates are met, and which are owed again'''

how = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="how-title">
      <p class="eyebrow">How it works</p>
      <h1 id="how-title">Four stages.<br><span>A record of each.</span></h1>
      <p class="lede">Each part below is two sentences, one example and a link to the full guide. The commands are real; what is planned is marked.</p>
      <nav class="actions" aria-label="Page sections"><a href="#kb">Knowledge base</a><a href="#research">1 Research</a><a href="#plan">2 Plan</a><a href="#execute">3 Execute</a><a href="#deliver">4 Deliver</a><a href="#gates">Gates</a><a href="#check">Checking</a><a href="#plugin">Plugin</a></nav>
    </section>

    <section id="kb" class="section" aria-labelledby="kb-title">
      <div class="section-heading"><p class="eyebrow">The base</p><h2 id="kb-title">Records in Git, an index you can rebuild</h2><p>The knowledge base is a Git repository of plain Markdown and JSON: decisions, tickets, assets, the links between them and one folder per run. Every row of an answer ends in its source, and the last line says what was examined and how many sources are stale.</p></div>
      {panel("kb why output", WHY, REAL)}
      {more(guide("kb-layout", "the knowledge base layout"))}
    </section>

    <section id="research" class="section" aria-labelledby="research-title">
      <div class="section-heading"><p class="eyebrow">Stage 1 / Research</p><h2 id="research-title">Ask the knowledge base, or search the code</h2><p>The <code>kb</code> verbs answer from what the project already knows, and a short Tuft program finds exact text in code at one pinned commit. With <code>--cite</code> each row carries a citation, and what the agent concludes it writes down with <code>record</code>.</p></div>
      {panel("Research commands", RESEARCH)}
      <p class="fine-print"><span class="chip chip-planned">Planned</span> A required step whose check is met only when research wrote something back.</p>
      {more(guide("feeding-back", "what each stage writes back"))}
    </section>

    <section id="plan" class="section" aria-labelledby="plan-title">
      <div class="section-heading"><p class="eyebrow">Stage 2 / Plan</p><h2 id="plan-title">Start a run</h2><p>A run records the task, the repository, branch, worktree and base commit, and today the plan is its first checkpoint note. <code>kb resume</code> shows it to any later session.</p></div>
      {panel("Starting a run", NEWRUN)}
      <div class="planned-panel"><p><span class="chip chip-planned">Planned</span> <strong>The run graph.</strong> A plan becomes an ordered list of steps, each naming the gates it owes; <code>plan advance</code> moves on only when they are met, and a skill can add its own steps. Writfold records the steps and the agent walks them. Required steps, such as a closing reflection, are part of every run, and a step can ask for a Weft assessment.</p></div>
      {more(guide("run-graph", "the run graph (planned)"))}
    </section>

    <section id="execute" class="section" aria-labelledby="execute-title">
      <div class="section-heading"><p class="eyebrow">Stage 3 / Execute</p><h2 id="execute-title">Edit, check, checkpoint</h2><p>The agent edits the run&rsquo;s worktree with Splicery recipes for repeated or structural edits, or with ordinary tools for one small change. Either way the result is an uncommitted Git change, and any gate whose scope covers it is owed again.</p></div>
      {panel("Execute commands", EXECUTE)}
      {more(guide("gates", "gate definitions, receipts and standing"))}
    </section>

    <section id="deliver" class="section" aria-labelledby="deliver-title">
      <div class="section-heading"><p class="eyebrow">Stage 4 / Deliver</p><h2 id="deliver-title">Drafts, checked. Nothing sent.</h2><p><code>kb deliver prepare</code> copies a PR comment or Slack summary into the run as the exact text that would be posted, and <code>deliver check</code> runs three checks on those bytes: paragraph length, references the audience must not see, and whether every citation is still fresh. Writfold has no network code, so posting stays with you or your agent.</p></div>
      {drafts()}
      <p class="fine-print">The checks are mechanical: they do not judge tone or truth. An optional Claude Code hook, off unless configured, can deny a listed publishing command until a ready draft holds the exact bytes: a guard, not enforcement.</p>
      {more(guide("delivery-modes", "delivery modes, deny lists and the guard"))}
    </section>

    <section id="gates" class="section" aria-labelledby="gates-title">
      <div class="section-heading"><p class="eyebrow">The thread</p><h2 id="gates-title">Who owes a gate, and what meets it</h2><p>Runs and delivery drafts owe gates, and evidence that Writfold records meets them. Gates report and block nothing; receipts resist mistakes, such as a forgotten check or a stale &ldquo;tests pass&rdquo;, and they are tracked files, not signatures.</p></div>
      <figure class="diagram-figure">{diagrams.LEGEND}{diagrams.gates("wg")}<figcaption class="fine-print">Evidence is tied to exact bytes. When they change, the gate is owed again.</figcaption></figure>
      {more(guide("assurance", "what is proved, tested and trusted"))}
    </section>

    <section id="check" class="section" aria-labelledby="check-title">
      <div class="section-heading"><p class="eyebrow">Any time</p><h2 id="check-title">Check that it still holds</h2><p>The index refreshes itself on every read, so there is no sync step. Three commands re-check the rest on demand: cited sources, the index against a rebuild, and gate evidence.</p></div>
      {panel("Validation commands", CHECK)}
      <p class="fine-print"><span class="chip chip-planned">Planned</span> <code>kb check</code>, one command for all three.</p>
      {more(guide("validation", "validation, flag by flag"))}
    </section>

    <section id="plugin" class="section" aria-labelledby="plugin-title">
      <div class="section-heading"><p class="eyebrow">In Claude Code</p><h2 id="plugin-title">A brief at session start, drafts at the end</h2><p>The plugin puts <code>brief</code> and <code>resume</code> into a new session with no tool call, and keeps a local checkpoint draft at compaction and stop. One skill teaches the verbs; the hooks run no model, and a missing binary or knowledge base makes them do nothing.</p></div>
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
    row(GUIDE + "kb-layout.md", "Read verbs", "<code>brief | context | why | status | find | match | impact | uses | timeline | resume | runs</code>. Every row names its source; every answer ends with what was examined and omitted"),
    row(GUIDE + "feeding-back.md", "Write verbs", "<code>checkpoint</code>, <code>record ticket | decision | link</code>, <code>status --set</code>, <code>cite make</code>. Plain files, written atomically, left uncommitted"),
    row(GUIDE + "validation.md", "Citations and the index", "<code>stale</code> reports each pinned citation as fresh, moved, changed or gone; <code>index verify</code> checks the index equals a rebuild"),
    row(GUIDE + "gates.md", "Gates", "<code>gate run | status | verify | lines | attest | waive</code>. Receipts pinned to exact bytes; a timeout or crash is never a pass"),
    row(GUIDE + "delivery-modes.md", "Delivery drafts", "<code>deliver prepare | check | status | attest | waive</code> for PR comments and Slack summaries. Nothing is sent"),
    row(GUIDE + "feeding-back.md", "Tuft and Splicery in a run", "<code>tuft run --cite</code> adds citations and a retrieval receipt; <code>edit apply | recover</code> replays recipes and keeps an edit receipt"),
    row(GUIDE + "hooks.md", "Claude Code plugin", "A brief at session start, local checkpoint drafts, one skill, and an optional guard hook"),
    row("/how.html#execute", "<code>writfold watch</code>", "A read-only terminal view of runs, gates, receipts and drafts"),
])
def step(title, text, chip):
    cls = {"Done": "chip-today", "Next": "chip-progress", "Planned": "chip-planned"}[chip]
    return f'<li><div><h3>{title}</h3><p>{text} <span class="chip {cls}">{chip}</span></p></div></li>'
ROAD = "".join([
    step("The four questions", "Read and write verbs, the index, pinned citations and the Claude Code plugin.", "Done"),
    step("Runs with gates, edits and drafts", "Receipts, statements, Splicery edits, Tuft citations, delivery drafts and <code>watch</code>.", "Done"),
    step("Instruction gates and your own delivery modes", "A gate can point to written instructions; a mode such as a commit message lists its gates.", "Next"),
    step("The run graph", "<code>plan set | status | advance</code>: ordered steps, each owing gates.", "Planned"),
    step("Splicing and required steps", "A skill adds its steps to the plan. Every run includes required steps, checked against the run&rsquo;s own records: research wrote back, the run ended with a reflection.", "Planned"),
    step("Hooks that show the plan", "The plan position at session start and after compaction. No model in a hook.", "Planned"),
    step("One week of real use", "Count what the checks caught before adding more.", "Planned"),
    step("Then", "Proofs of the plan and gate kernels, a model of two sessions on one run, <code>kb check</code>, proposals, an evaluation skill, and Weft assessments of plan steps.", "Planned"),
])
LOG = "".join(f"<li><time>{d}</time><p>{t}</p></li>" for d, t in [
    ("12 Nov 2026", f'The site is shorter. Full file layouts, configuration and output moved to the <a href="{GUIDE}README.md">guides</a> in the Writfold repository. Direction set: the run graph, required steps and model-free hooks, all planned.'),
    ("12 Nov 2026", f'Preview <a href="{REL}">v0.3.0-dev.1</a>: gates, Splicery edits in a run, <code>writfold watch</code>, delivery drafts and an optional guard hook.'),
    ("12 Nov 2026", 'Preview <a href="https://github.com/writfold-dev/writfold/releases/tag/v0.2.0-dev.1">v0.2.0-dev.1</a>: the <code>kb</code> read and write verbs, the index, citations checked for staleness, and the Claude Code plugin.'),
    ("11 Nov 2026", "Mission set: Git-native project continuity for coding agents."),
])
def faq(q, a): return f"<details><summary>{q}</summary><p>{a}</p></details>"
FAQ = "".join([
    faq("Can I use Writfold today?", 'Yes, as a preview: <a href="/#try">download the binary and install the plugin</a>. Single user, cooperating agents, local clones only, Linux x86_64 or WSL2.'),
    faq("Does it need a server or a database?", "No. One static binary, records in Git, and a local index that Writfold derives and can always rebuild."),
    faq("Can an agent skip a gate?", "Yes. Gates record what was checked and report whether it still holds; they block nothing. A skipped gate shows as open. The optional hook is a guard, not enforcement."),
    faq("What is proved?", f'For the knowledge base, nothing yet: its write protocol is model-checked and kill-tested, and its decision kernels are tested. Proofs of the gate and plan kernels are planned. Details are in {guide("assurance", "the assurance guide")}.'),
    faq("Does Writfold post PR comments or Slack messages?", "No. <code>kb deliver</code> keeps drafts with their checks in the run. Nothing is sent."),
    faq("Other harnesses?", "The CLI works wherever an agent has a shell. An MCP server is deferred until a harness without a shell needs one."),
    faq("Is the source available?", 'Yes: <a href="https://github.com/writfold-dev/writfold">Writfold</a>, <a href="https://github.com/writfold-dev/weft">Weft</a> and <a href="https://github.com/writfold-dev/splicery">Splicery</a> are public, and this website is under the MIT license.'),
])
status = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="status-title">
      <p class="eyebrow">Status</p>
      <h1 id="status-title">What runs today.<br><span>What comes next.</span></h1>
      <p class="lede">Writfold is <a href="/">Git-native project continuity for coding agents</a>. The preview covers research, execution and delivery drafts. The run graph is planned.</p>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">v0.3.0-dev.1</a> · Updated 12 November 2026</span></p>
      <nav class="actions" aria-label="Page sections"><a href="#today">Runs today</a><a href="#next">Roadmap</a><a href="#changelog">Changelog</a><a href="#faq">FAQ</a></nav>
    </section>
    <section id="today" class="section" aria-labelledby="today-title">
      <div class="section-heading"><p class="eyebrow">01 / Runs today</p><h2 id="today-title">In the preview</h2><p>Each entry links to its guide. <a href="/#try">Try it</a>, or read the <a href="{README}">README</a>.</p></div>
      <div class="doc-links">{TODAY}</div>
      <p class="fine-print">Measured: reads at most 45&nbsp;ms on 4,130 records; writes about 120&ndash;130&nbsp;ms. A write killed at any step leaves the old or the new complete file.</p>
      <p class="fine-print">Limits: single user with cooperating agents; local clones only. No real PR comment or Slack summary has gone through the delivery checks yet.</p>
    </section>
    <section id="next" class="section" aria-labelledby="next-title">
      <div class="section-heading"><p class="eyebrow">02 / Roadmap</p><h2 id="next-title">In order</h2><p>The planned model is in {guide("run-graph", "the run graph guide")}.</p></div>
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
