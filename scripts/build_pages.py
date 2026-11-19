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
from highlight import highlight
from term_glyphs import uncovered
import diagrams

SITE = Path(__file__).resolve().parent.parent
VERSION = "v0.6.0-dev.10"
RELEASED = "19 November 2026"
RELEASES = "https://github.com/writfold-dev/writfold/releases/"
REL = RELEASES + "tag/" + VERSION
ALT = ("The folded-W Writfold mark on navy with the headline: Deterministic agent work that resumes where it stopped. "
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
  <script src="/assets/copy.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
'''

def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''  <header class="site-header wrap">
    <a class="wordmark" href="/" aria-label="Writfold home"><picture><source srcset="/assets/writfold-icon.svg" media="(prefers-color-scheme: light)"><img src="/assets/writfold-icon-dark.svg" width="40" height="40" alt=""></picture><span>writfold</span></a>
    <nav aria-label="Main navigation">{links}<a href="https://github.com/writfold-dev/writfold">GitHub</a></nav>
    <label class="theme-control" hidden>Theme <select id="theme" aria-describedby="theme-note"><option value="system">System</option><option value="light">Light</option><option value="paper-dark">Paper Dark</option></select><span id="theme-note" class="visually-hidden">Your choice is remembered in this browser.</span></label>
  </header>
'''

FOOTER = '''  <footer class="site-footer wrap">
    <div class="footer-line">
      <span class="footer-credit"><span class="footer-mark" aria-hidden="true"></span> © 2026 <a href="https://tknawara.dev">Tarek Nawara</a></span>
      <a href="/how.html">How it works</a><a href="/status.html">Status</a><a href="/LICENSE.txt">MIT license</a><a href="https://github.com/writfold-dev/writfold">GitHub</a><a href="https://github.com/writfold-dev/writfold-dev.github.io">Website source</a>
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
    return (f'<pre class="code-panel lang-{lang}" tabindex="0" aria-label="{label}"><code>'
            f'{highlight(text.strip(chr(10)), lang)}</code></pre>')

def pill(text, kind):
    return f'<span class="pill pill-{kind}">{text}</span>'

ANSWER = f'''<figure id="example" class="visual">
        <figcaption><span class="chip chip-parts">Illustration</span> Invented content, in the shape <code>kb why</code> prints. The evidence is code pinned at a commit, flagged because those lines have moved.</figcaption>
        <div class="card answer">
          <p class="card-cmd"><code><span class="syntax-prompt">$ </span>writfold kb why "batch writes"</code></p>
          <p class="answer-head">{pill("accepted", "ok")} <strong>Batch ledger writes</strong> <span class="src">proposals/decision/2026-11-02-batch-writes/proposal.md:5</span></p>
          <dl class="answer-rows">
            <div><dt>Decided</dt><dd>by api-review on 2026-11-05 <span class="src">:11</span></dd></div>
            <div><dt>Why</dt><dd>One transaction per 500 rows keeps replay under a minute. <span class="src">:25</span></dd></div>
            <div><dt>Evidence</dt><dd><code>demo-api src/ledger.rs:40-72</code> {pill("moved → 44-76", "warn")} <span class="src">:31</span></dd></div>
          </dl>
          <ul class="card-foot"><li>31 of 31 records examined</li><li>nothing omitted</li><li class="warn">1 source stale</li></ul>
        </div>
      </figure>'''

# Captured terminal frames. Each is the <span> fragment the capture tool wrote, kept in
# scripts/frames/<name>.html. To publish a new capture, replace the file, adjust its label
# here if the picture changed, and run this script again.
FRAMES = Path(__file__).parent / "frames"
FRAME_LABELS = {
    "home": "writfold watch in its calm default frame: the runs, the plan map of the selected run, and the inspector for its next step",
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

GUIDE = "https://github.com/writfold-dev/writfold/blob/main/docs/guide/"

def guide(page, label):
    return f'<a href="{GUIDE}{page}.md">{label}</a>'

def more(*links, lead="More"):
    '''The one link out of a section.'''
    return f'<p class="guide-link"><span aria-hidden="true">→</span> {lead}: {" and ".join(links)}</p>'

# ---------------------------------------------------------------- the installer
# install.sh at the site root is served as https://writfold.dev/install.sh. Its two pin
# lines are stamped at release (README, "Releasing the installer"); the pages must name
# the same release, so a mismatch stops the build.
ONE_LINER = "curl -fsSL https://writfold.dev/install.sh | sh"
DRY_RUN = ONE_LINER + " -s -- --dry-run"
_pin = re.search(r'^WRITFOLD_DEFAULT_VERSION="([^"]+)"$', (SITE / "install.sh").read_text(encoding="utf-8"), re.M)
if not _pin or "v" + _pin.group(1) != VERSION:
    raise SystemExit(f"install.sh pins {_pin.group(1) if _pin else 'nothing'}; the pages describe {VERSION}")

def copy_line(command, label):
    '''A command with a Copy button. The button is hidden until assets/copy.js shows it,
    so without JavaScript the command is plain selectable text.'''
    return (f'<div class="copy-line"><code aria-label="{label}"><span class="syntax-prompt">$ </span>{escape(command)}</code>'
            f'<button type="button" class="copy" data-copy="{escape(command)}" hidden>Copy</button></div>')

MANUAL = f'''base={RELEASES}download/{VERSION}
curl -LO "$base/writfold-x86_64-linux-musl" -LO "$base/writfold-x86_64-linux-musl.sha256"
echo "$(cut -d' ' -f1 writfold-x86_64-linux-musl.sha256)  writfold-x86_64-linux-musl" | sha256sum -c
install -m 755 writfold-x86_64-linux-musl ~/.local/bin/writfold
claude plugin marketplace add writfold-dev/writfold
claude plugin install writfold@writfold'''

# ---------------------------------------------------------------- index
DESC_HOME = ("Writfold keeps a coding agent's plan, checks and decisions as plain files in Git, "
             f"so the work can be checked and picked up where it stopped. Preview: {VERSION}.")
index = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="hero-title">
      <p class="eyebrow">Git-native project continuity for coding agents</p>
      <h1 id="hero-title">Deterministic agent work<br><span>that resumes where it stopped.</span></h1>
      <p class="lede">Writfold keeps a coding agent&rsquo;s plan, checks and decisions as plain files in Git.</p>
      <div class="two-up">
        <div class="capability"><h2>Deterministic</h2><p>Not the model: the process around it. The agent follows a plan; each check leaves a receipt tied to the exact bytes it checked; and what is done, what is owed and whether a step may close are computed from files in Git, the same on every machine.</p></div>
        <div class="capability"><h2>Resumable</h2><p>A new session reads a short brief and the last checkpoint, not the whole project. Commit and push the run&rsquo;s files, and it resumes on any machine.</p></div>
      </div>
      <div class="hero-install">
        {copy_line(ONE_LINER, "Install command")}
        <p class="fine-print">Prints its plan first; asks before touching <code>~/.claude</code>. <a href="#try">What it does <span aria-hidden="true">→</span></a></p>
      </div>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">{VERSION}</a>, {RELEASED}. Linux x86_64 or WSL2. <a href="/how.html">How it works</a> · <a href="/status.html">Status</a></span></p>
    </section>

    <section id="deterministic" class="section" aria-labelledby="deterministic-title">
      <div class="section-heading"><p class="eyebrow">Deterministic</p><h2 id="deterministic-title">A plan the agent walks, with checks that leave receipts</h2><p>What the agent writes is its own; what Writfold says about it is derived from the records, never from a model.</p><p>Each task is a run with a plan. Each step names its gates: checks you define, such as your tests. <code>writfold watch</code> shows the plan in your terminal.</p></div>
      <figure class="example"><figcaption><span class="chip chip-today">Captured</span> <code>writfold watch</code> on a demo project.</figcaption>{frame("home")}</figure>
      <dl class="callouts">
        <div><dt><code>✓</code> Done, and its checks still hold</dt><dd>A step is recorded done only when every gate it owes is met. A gate met by a statement or a waiver is shown as attested or waived, never as passed, and a step whose checked bytes have since changed is flagged stale.</dd></div>
        <div><dt><code>!</code> Done, but something moved</dt><dd>A later edit changed the bytes a gate checked.</dd></div>
        <div><dt><code>▶</code> Next</dt><dd>The step to pick up.</dd></div>
      </dl>
      <p>A finished plan says how it finished: <code>complete</code>, <code>complete-with-exceptions</code>, <code>policy-moved</code>.</p>
      <p class="fine-print">Gates report; they block nothing by themselves. A guard rule you add can deny a command such as <code>git commit</code> until they are met, and <a href="/how.html#policy">your policy</a> says which outcomes meet a gate.</p>
      {more('<a href="/how.html">a short example, and the files and commands behind this</a>')}
    </section>

    <section id="resumable" class="section" aria-labelledby="resumable-title">
      <div class="section-heading"><p class="eyebrow">Resumable</p><h2 id="resumable-title">A new session reads a brief, not the project</h2><p>Three commands carry work from one session to the next.</p></div>
      <dl class="callouts">
        <div><dt><code>kb checkpoint</code></dt><dd>Writes a note into the run for the next session.</dd></div>
        <div><dt><code>kb resume</code></dt><dd>Shows where the run stopped: its last notes, plan step and owed gates.</dd></div>
        <div><dt><code>kb brief</code></dt><dd>Shows where the project stands. The Claude Code plugin adds it at session start.</dd></div>
      </dl>
      <p>The agent can also ask why something was decided. Every line of the answer names its source, and says so when that source has moved.</p>
      {ANSWER}
    </section>

    <section id="git" class="section" aria-labelledby="git-title">
      <div class="section-heading"><p class="eyebrow">No server</p><h2 id="git-title">Plain files in Git, and one binary</h2></div>
      <div class="three-up">
        <div class="capability"><h3>Git is the source of truth</h3><p>Decisions, tickets, runs and receipts are Markdown and JSON files. Writfold writes them and leaves the commit to you.</p></div>
        <div class="capability"><h3>Nothing else to run</h3><p>No server and no account. A new machine needs <code>git clone</code> and the binary.</p></div>
        <div class="capability"><h3>Your agent stays yours</h3><p>It keeps its own loop and model. Writfold records and reports; it runs no model and sends nothing.</p></div>
      </div>
    </section>

    <section id="try" class="section" aria-labelledby="try-title">
      <div class="section-heading"><p class="eyebrow">Try it</p><h2 id="try-title">Install</h2><p>Linux x86_64 or WSL2.</p></div>
      {copy_line(ONE_LINER, "Install command")}
      <p>The installer prints its plan first, with every path it will touch. Then it:</p>
      <ul class="steps">
        <li>downloads <code>writfold-x86_64-linux-musl</code> and its <code>.sha256</code> from the GitHub release into a temporary directory;</li>
        <li>checks the SHA-256 before installing anything;</li>
        <li>writes one file, <code>~/.local/bin/writfold</code>;</li>
        <li>asks before adding the Claude Code plugin. That step runs the <code>claude</code> CLI, which writes under <code>~/.claude</code>. With no terminal to ask on, it is skipped and the two commands are printed.</li>
      </ul>
      <p>It does not use sudo and does not edit your shell startup files. <a href="/install.sh">Read the script</a>, or see the plan without installing:</p>
      {copy_line(DRY_RUN, "Dry-run command")}
      <p class="fine-print">Options: <code>--no-plugin</code>, <code>--plugin</code>, <code>--yes</code>, <code>--prefix DIR</code>, <code>--version V</code>.</p>
      <details class="manual"><summary>Prefer to do it by hand?</summary>
        {pre("Manual download and install commands", MANUAL, "shell")}
        <p class="fine-print">These are the same steps the installer performs.</p>
      </details>
      <p class="boundary">Pre-release, for one person and their agents: formats and commands may still change. Setup is in the <a href="https://github.com/writfold-dev/writfold#readme">README</a>; see <a href="/status.html#today">what runs today</a> and <a href="/status.html#next">what is next</a>.</p>
    </section>
  </main>
'''
page("index.html", "Writfold — Git-native project continuity for coding agents", DESC_HOME, "/", index)

# ---------------------------------------------------------------- how
# Each section shows one real file beside the commands that use it. The files are kept
# in scripts/examples/ so they can be copied into a demo knowledge base and run with the
# release binary before the page is published (README, "Writing pages").
EXAMPLES = Path(__file__).parent / "examples"

def file_panel(path, name, lang):
    text = (EXAMPLES / name).read_text(encoding="utf-8")
    return (f'<figure class="file"><figcaption>{path}</figcaption>{pre("The file " + path, text, lang)}</figure>')

def commands(*items):
    return '<ol class="cmds">' + "".join(
        f'<li><p>{caption}</p>{pre("Command", "$ " + command)}</li>' for caption, command in items) + "</ol>"

def sessions(*items):
    '''Commands with the output they printed, trimmed as the README allows.'''
    return '<ol class="cmds wrap">' + "".join(
        f'<li><p>{caption}</p>{pre("Command and its output", text)}</li>' for caption, text in items) + "</ol>"

def pair(sid, eyebrow, title, text, files, cmds, link):
    return f'''
    <section id="{sid}" class="section" aria-labelledby="{sid}-title">
      <div class="section-heading"><p class="eyebrow">{eyebrow}</p><h2 id="{sid}-title">{title}</h2><p>{text}</p></div>
      <div class="pair"><div class="pair-files">{"".join(files)}</div>{cmds}</div>
      {link}
    </section>
'''

def drawn(sid, eyebrow, title, text, figure, caption, files, cmds, link):
    """A section led by a drawing of how the product decides, then files and commands."""
    files_html = f'<div class="pair-files">{"".join(files)}</div>' if files else ""
    return f'''
    <section id="{sid}" class="section" aria-labelledby="{sid}-title">
      <div class="section-heading"><p class="eyebrow">{eyebrow}</p><h2 id="{sid}-title">{title}</h2><p>{text}</p></div>
      <figure class="diagram-figure">{figure}<figcaption><span class="chip chip-parts">Drawing</span> {caption}</figcaption></figure>
      <div class="pair">{files_html}{cmds}</div>
      {link}
    </section>
'''

HOW = "".join([
    pair("gates", "A gate", "A gate is a check that leaves a receipt",
         "This gate runs the unit tests. Its receipt is tied to the files in <code>scope</code>: edit one of them, and the gate is owed again.",
         [file_panel(".writfold/gates/unit.toml", "unit.toml", "toml")],
         commands(("Run the check and keep a receipt.", "writfold kb gate run unit"),
                  ("See where every gate stands.", "writfold kb gate status"),
                  ("Some gates are a statement, not a command. Make one.", 'writfold kb gate attest wording \\\n    --statement "README unchanged" --by agent')),
         more(guide("gates", "the gates guide"), lead="Every key and gate kind")),
    pair("plan", "A plan", "A plan is a list of steps and the gates each one owes",
         "Each line is a step name, then its gates. Writfold records the steps. The agent does the work.",
         [file_panel(".writfold/plans/fix.toml", "fix.toml", "toml")],
         commands(("Give the current run this plan.", "writfold kb plan set fix"),
                  ("See each step and what it owes.", "writfold kb plan status"),
                  ("Record the current step as done. Refused while a gate is owed.", "writfold kb plan advance")),
         more(guide("run-graph", "the plan guide"), lead="Templates, skipping and required steps")),
    pair("policy", "Your policy", "Your policy says what counts",
         "You decide what adequate work means; Writfold holds no opinion of its own. Here the research gate takes a statement and no waiver, and every plan starts with a research step that cannot be skipped.",
         [file_panel(".writfold/gates/research.toml", "research.toml", "toml"), file_panel(".writfold/plans/required.toml", "required.toml", "toml")],
         sessions(("A waiver is refused.", """$ writfold kb gate waive research \\
    --reason "no time" --by agent
writfold kb: refused: gate research does not accept a waiver (accept = ["attested"] @.writfold/gates/research.toml:7); meet it: writfold kb gate attest research --statement TEXT --by WHO"""),
                  ("So is skipping the step.", """$ writfold kb plan skip \\
    --reason "no time" --by agent
step research#1/research [current] owes: research [open] @runs/run-…/plan/splice-research.1.json:1 !locked
  next: writfold kb gate attest research --statement TEXT --by WHO
# note: not skipped: research#1/research is a required step this run cannot skip (unskippable = ["research"] @.writfold/plans/required.toml:3, pinned @runs/run-…/policy/pin-1-….json:1); nothing written
…"""),
                  ("A finished plan says how it finished. This one closed its research on a statement and skipped two steps.", """$ writfold kb plan status
…
plan complete-with-exceptions 4 steps: 1 passed, 1 attested, 0 waived, 2 skipped; policy=same @runs/run-…/plan/
…""")),
         more(guide("policy", "the policy guide"), lead="Checklists, pinned policy and an example to start from")),
    pair("skill", "A skill", "A skill adds its own steps",
         "A Claude Code skill can carry one line that adds steps to the plan when the skill loads. The steps come from a template of their own.",
         [file_panel(".claude/skills/review/SKILL.md", "SKILL.md", "md"), file_panel(".writfold/plans/review.toml", "review.toml", "toml")],
         commands(("The skill&rsquo;s line. It adds the review steps before the current step; running it twice adds them once. The agent then walks them like any other step.", "writfold kb plan use review")),
         more(guide("skills", "the skills guide"), lead="Writing a skill")),
    pair("guard", "A guard rule", "A guard rule holds a command until the gates are met",
         "With the Claude Code plugin, this rule denies <code>git commit</code> and <code>git push</code> while the run owes a gate. It only sees the commands Claude Code shows it, so it is a guard, not a lock.",
         [file_panel(".writfold/guards/commit-needs-gates.toml", "commit-needs-gates.toml", "toml")],
         commands(("Ask what each rule would decide right now.", "writfold kb guard status"),
                  ("A denial names what is owed and the command that meets it. For example:", "writfold kb gate run unit")),
         more(guide("hooks", "the hooks guide"), lead="Every key and requirement")),
    drawn("sessions", "Several sessions", "Each agent session works in its own run",
          "Run two agents on one machine, in two repositories, and each one&rsquo;s commits are judged against its own run. A session reads its own pointer first, then its work tree&rsquo;s, then the clone&rsquo;s shared one. Nothing to set up: the plugin hands the session its ID.",
          diagrams.sessions(),
          "How the current run is found. Which pointer decides is proved in Lean: a session with its own pointer reads the same whatever other sessions start, and a run that was closed is reported, never swapped for another session&rsquo;s.",
          [],
          commands(("Start a run. It becomes current for this session and this work tree, and for nobody else.", 'writfold kb checkpoint --new-run --task "batch writes" \\\n    --note "start"'),
                   ("Hand a run to a reviewer or a second session: make it current here too.", "writfold kb resume run-… --here"),
                   ("Several lookups in one call, for a hook that runs before each search.", 'writfold kb find --each "batch writes" ledger replay')),
          more(guide("hooks", "the hooks guide"), guide("adopting", "adopting Writfold in an existing workflow"), lead="Sessions, worktrees and hand-overs")),
    drawn("store", "An attached store", "Disposable evidence, cited for good",
          "Probe scripts, reproducers, data pulls and review notes are worth citing and not worth curating. Keep them in a Git repository of their own and declare it once. A citation into it is judged at the commit it names, so tidying the store never makes evidence stale.",
          diagrams.store(),
          "How a citation into a store is judged. The rule is proved in Lean: fresh exactly when the cited commit is still reachable and holds the cited bytes; a clone that is only behind is never read as a loss.",
          [file_panel(".writfold/stores/scratch.toml", "scratch.toml", "toml")],
          commands(("See where each machine finds the store, or the command to clone it.", "writfold kb repos"),
                   ("Record what the run made in the store on its checkpoint. Refused unless it would read fresh: committed, reachable, a file.", 'writfold kb checkpoint --note "reproducer saved" \\\n    --artifact scratch@4f0c…:work/fuzz-parser/crash-01.bin'),
                   ("Check every citation. Ones into the store are judged at their pin.", "writfold kb stale")),
          more(guide("stores", "the stores guide"), lead="Declaring a store and laying it out")),
    pair("deliver", "A delivery mode", "A delivery mode checks a draft before you send it",
         "This mode checks a commit message. Writfold checks the exact text and sends nothing: posting stays with you or your agent.",
         [file_panel(".writfold/deliveries/commit-message.toml", "commit-message.toml", "toml")],
         commands(("Keep the exact text as a draft in the run.", "writfold kb deliver prepare \\\n    --mode commit-message \\\n    --audience external --from msg.txt"),
                  ("Run the mode&rsquo;s checks on that text. The draft is ready only when every check is met.", "writfold kb deliver check"),
                  ("A plan step can owe this mode: <code>commit: deliver:commit-message</code>. It advances only once the draft is ready.", "writfold kb plan advance")),
         more(guide("delivery-modes", "the delivery guide"), lead="PR comments, Slack summaries and your own modes")),
    pair("resume", "A checkpoint", "A checkpoint is a note for the next session",
         "Each run keeps its notes in one Markdown file. The next session reads the last ones instead of the whole history.",
         [file_panel("runs/&lt;run&gt;/checkpoint.md", "checkpoint.md", "md")],
         commands(("Write a note into the current run.", 'writfold kb checkpoint --note \\\n    "unit passes. Next: attest wording, then commit."'),
                  ("See where the run stopped: its last notes, plan step and owed gates.", "writfold kb resume"),
                  ("See where the project stands. The plugin adds this at session start.", "writfold kb brief")),
         more(guide("kb-layout", "the knowledge base layout"), lead="Every record and where it lives")),
])

EXAMPLE = '<ol class="cmds walk">' + "".join(f'<li><p>{caption}</p>{pre("Command and its output", text)}</li>' for caption, text in [
    ("1. Record a decision. It is a file, and the answer names where it is.", """$ writfold kb record decision --title "Batch ledger writes" \\
    --target-source src/ledger.rs \\
    --why "One transaction per 500 rows keeps replay under a minute."
decision proposal/decision/2026-11-17-batch-ledger-writes [draft] Batch ledger writes @proposals/…/proposal.md:6
…"""),
    ("2. Start a run, with a note for the next session.", """$ writfold kb checkpoint --new-run --project demo-api \\
    --task "batch ledger writes" \\
    --note "Batching at 500 rows. Next: tune the batch size."
run run-… [open] batch ledger writes @runs/run-…/manifest.json:8 !current
…
checkpoint 2026-11-17T00:42:26Z entry 1 of 1 @runs/run-…/checkpoint.md:2
  note: Batching at 500 rows. Next: tune the batch size. @runs/run-…/checkpoint.md:4
…"""),
    ("3. Pass a gate. Its receipt names the commit and the bytes it checked.", """$ writfold kb gate run unit
gate unit [satisfied] mechanical pass exit=0 at demo-api@de2997f4dbc4 scope=7ac784bc428b paths=1 @runs/run-…/gates/unit-….json:1
…"""),
    ("4. Stop. Commit and push the run&rsquo;s files.", """$ git add -A && git commit -qm "batch writes: decision, checkpoint, receipt" && git push -q"""),
    ("5. Later, a commit changes a file in the gate&rsquo;s scope.", """$ sed -i 's/500/250/' src/ledger.rs && git commit -qam "try 250 rows" && git push -q"""),
    ("6. On another machine, clone and resume. The gate is stale, and the <code>next:</code> line names the command that meets it again.", """$ git clone -q …/demo-api.git && cd demo-api && writfold kb resume
run run-… [open] batch ledger writes @runs/run-…/manifest.json:8
…
gate unit [stale] mechanical pass exit=0 at demo-api@de2997f4dbc4 scope=7ac784bc428b paths=1 @runs/run-…/gates/unit-….json:1 !stale
  why: changed in scope: src/ledger.rs
  next: writfold kb gate run unit
checkpoint 2026-11-17T00:42:26Z entry 1 of 1 @runs/run-…/checkpoint.md:2
  note: Batching at 500 rows. Next: tune the batch size. @runs/run-…/checkpoint.md:4
…"""),
]) + "</ol>"

how = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="how-title">
      <p class="eyebrow">How it works</p>
      <h1 id="how-title">Small files.<br><span>A few commands.</span></h1>
      <p class="lede">You describe your checks, plans and rules in small files, kept in Git. The agent runs a few commands against them. Here is one short example, then the files, each beside the commands that use it.</p>
      <nav class="actions" aria-label="Page sections"><a href="#example">Example</a><a href="#gates">Gate</a><a href="#plan">Plan</a><a href="#policy">Policy</a><a href="#skill">Skill</a><a href="#guard">Guard rule</a><a href="#sessions">Sessions</a><a href="#store">Store</a><a href="#deliver">Delivery mode</a><a href="#resume">Checkpoint</a></nav>
    </section>
    <section id="example" class="section" aria-labelledby="example-title">
      <div class="section-heading"><p class="eyebrow">An example</p><h2 id="example-title">Stop on one machine, resume on another</h2><p>Six commands, run on a demo repository whose <code>unit</code> gate covers <code>src/**</code>. The output is real and trimmed: <code>…</code> stands for a run ID, a path or lines left out.</p></div>
      {EXAMPLE}
    </section>
{HOW}
    <section class="section" aria-labelledby="next-title">
      <div class="section-heading"><h2 id="next-title">Try it</h2><p><a href="/#try">Install the preview</a>, read the <a href="{GUIDE}README.md">guides</a>, or see <a href="/status.html">what runs today and what is next</a>.</p></div>
    </section>
  </main>
'''
page("how.html", "How it works — Writfold",
     "How Writfold works: one short example of stopping and resuming, then seven small files (a gate, a plan, a policy, a skill, a guard rule, a delivery mode, a checkpoint), each beside the commands that use it.",
     "/how.html", how)

# ---------------------------------------------------------------- status
README = "https://github.com/writfold-dev/writfold#readme"
def row(href, title, text):
    return f'<a href="{href}"><span><strong>{title}</strong><small>{text}</small></span><span aria-hidden="true">→</span></a>'
# The one list of what runs; the overview and How it works link here.
TODAY = "".join([
    row(GUIDE + "kb-layout.md", "Questions with sourced answers", "<code>brief | context | why | status | find | match | impact | uses | timeline | resume | runs | repos</code>. Every row names its source"),
    row(GUIDE + "hooks.md#the-current-run-per-session-and-per-work-tree", "Several agent sessions at once", "Each session and each work tree has its own current run, so two agents on one machine never judge each other&rsquo;s commits. <code>resume &lt;run&gt; --here</code> hands a run to a reviewer or a second session; <code>find --each</code> answers several lookups in one call"),
    row(GUIDE + "feeding-back.md", "Writing records", "<code>checkpoint</code>, <code>record</code>, <code>status --set</code>, <code>cite make</code>, <code>observe</code>. <code>propose</code> queues a record until you accept or drop it"),
    row(GUIDE + "validation.md", "Citations that say when they moved", "<code>stale</code> reports each citation as fresh, moved, changed or gone. <code>check</code> adds the index, gates, plan and guard rules in one summary"),
    row(GUIDE + "stores.md", "Attached stores", "A Git repository of probes, reproducers and review notes, declared once and found on every machine. Citations into it are judged at the commit they name, so tidying it never makes evidence stale. <code>checkpoint --artifact</code> records what a run made there; <code>resume</code> shows each with its standing. A store directory that names a record in its README is listed by <code>context</code> and <code>uses</code>, and <code>observe --snapshot</code> keeps the bytes an agent looked at"),
    row(GUIDE + "gates.md", "Gates", "<code>gate run | status | verify | lines | attest | waive | cover</code>. Receipts tied to exact bytes; a timeout or crash is never a pass. A scope can name paths in another repository (<code>repo:docs/adr/**</code>), and a gate about outside state can age (<code>ages_as</code>)"),
    row(GUIDE + "gates.md#which-item-the-evidence-was-for-built-in-v060-dev9", "Evidence that answers its item", "A checklist item can require evidence of its own (<code>own_evidence</code>) or from named gates (<code>evidence_from</code>); <code>gate status</code> notes a look made for another item and evidence shared across items. A look that found nothing ages and can pin what it searched"),
    row(GUIDE + "run-graph.md", "Plans", "<code>plan set | use | status | advance | skip | repin</code>. Templates, skills that add steps, steps you require in every plan, and a recorded way to adopt a gate edited mid-run"),
    row(GUIDE + "policy.md", "Your policy", "A gate&rsquo;s <code>accept</code> says which outcomes meet it; a checklist says which items may be <code>not-applicable</code> or <code>none-found</code>; a required step can be <code>unskippable</code>. Each run pins the policy it started under and says when it moved. <code>init</code> starts a knowledge base; <code>policy</code> shows the policy"),
    row(GUIDE + "hooks.md#guard-rules", "Guard rules", "A rule denies or asks about a command or tool until the run&rsquo;s gates are met. A guard, not a lock"),
    row(GUIDE + "run-graph.md#a-delivery-as-a-steps-gate", "A draft as a step&rsquo;s gate", "A step that owes <code>deliver:&lt;mode&gt;</code> advances only once a draft of that mode is ready: every check met"),
    row(GUIDE + "delivery-modes.md", "Delivery drafts", "<code>deliver prepare | check | status | payload | posted | withdraw</code>. PR comments, Slack summaries, commit messages and your own modes, checked before posting; the guard holds the posting command until the exact text is ready. Nothing is sent"),
    row(GUIDE + "errors.md", "Errors that point at the line", "Every file you write reports the file, line and column, the line itself and a suggested fix. <code>kb lint</code> checks them all, for CI"),
    row(GUIDE + "checkers.md", "External checkers", "Programs on your <code>PATH</code> that <code>kb stale</code> asks about citation kinds Git cannot check. <code>--record</code> writes their answers to tracked files for you to commit, so a clone without the checker can read them"),
    row(GUIDE + "hooks.md", "Claude Code plugin", "The brief and the plan position at session start and after compaction, checkpoint drafts, and two skills"),
    row(GUIDE + "watch.md", "<code>writfold watch</code>", "A read-only terminal view of the run&rsquo;s plan, gates and guard rules, and of the project&rsquo;s decisions, tracker and stale citations"),
])
def step(title, text, chip):
    cls = {"Done": "chip-today", "Next": "chip-progress", "Planned": "chip-planned", "Not planned": "chip-parts"}[chip]
    return f'<li><div><h3>{title}</h3><p>{text} <span class="chip {cls}">{chip}</span></p></div></li>'
ROAD = "".join([
    step("Questions, records and citations", "The read and write commands, pinned citations, external checkers and the Claude Code plugin.", "Done"),
    step("Gates and delivery drafts", "Receipts tied to exact bytes, statements, checklists and checked drafts.", "Done"),
    step("Plans and guard rules", "Plan templates, skills that add steps, required steps and guard rules.", "Done"),
    step("<code>writfold watch</code>", "The plan and the project&rsquo;s records in one terminal view.", "Done"),
    step("A delivery mode as a step&rsquo;s gate", "A plan step that owes a checked draft.", "Done"),
    step("Your policy", "Which outcomes meet a gate, steps that cannot be skipped, policy pinned per run, and a plan that says how it finished.", "Done"),
    step("Delivery modes for agents", "A mode says which checks may be waived; the guard reads the exact text being posted; citations are stripped from outward text; posts are recorded.", "Done"),
    step("Re-pinning", "<code>plan repin</code> to accept an edited policy mid-run, on the record.", "Done"),
    step("Several agent sessions at once", "A current run per session and per work tree, and hand-overs with <code>resume --here</code>.", "Done"),
    step("Attached stores", "A companion repository of evidence, declared once and cited at its pinned commit.", "Done"),
    step("Run artifacts", "<code>checkpoint --artifact</code>: a run keeps pinned pointers to what it made in a store, shown by <code>resume</code>.", "Done"),
    step("Evidence that answers its item", "Checklist items that need their own evidence, gates that age, scopes across repositories, and looks that found nothing pinned to what they searched. Proved in Lean.", "Done"),
    step("Stores that point back", "A store directory names the record it serves, and <code>kb context</code> and <code>kb uses</code> list it.", "Done"),
    step("Snapshots of a look", "<code>observe --snapshot</code> keeps the bytes an agent saw in a store, so a record shows what it relied on. Proved in Lean.", "Done"),
    step("Store evidence on another machine", "A committed record of pinned store verdicts, so a clone without the store can still read them.", "Next"),
    step("Citations as links", "Posted text with each citation rendered as a pinned link, instead of removed.", "Planned"),
    step("Finding records by what people call them", "Stemming, aliases on every record, acronyms and faster lookups for session-start hooks.", "Next"),
    step("Links from commits and trackers, and <code>--at</code>", "Links read from commit trailers and tracker references, and answers as of a given commit.", "Planned"),
    step("Access control and signing", "Writfold stays a tool for one person and their agents.", "Not planned"),
])
def rel(version):
    return f'Preview <a href="{RELEASES}tag/{version}">{version}</a>'
LOG = "".join(f"<li><time>{d}</time><p>{t}</p></li>" for d, t in [
    ("19 Nov 2026", f'{rel(VERSION)}: stores that point back and snapshots. A store directory whose README names a record in <code>subject:</code> is listed by <code>kb context</code> and <code>kb uses</code> on that record, marked as the store&rsquo;s claim. <code>observe --snapshot</code> keeps the bytes an agent looked at in a pinned store, committed by you, and the look counts as evidence only while that snapshot holds. Both rules are proved in Lean.'),
    ("19 Nov 2026", f'{rel("v0.6.0-dev.9")}: evidence that answers its item. A checklist item can require evidence recorded for it, or a receipt of a named gate; <code>gate status</code> notes evidence shared across items. A gate&rsquo;s scope can include paths in another repository, so a docs change there makes it stale; a gate about outside state can age by a catalog kind; a look that found nothing ages and can pin what it searched. The decisions are proved in Lean.'),
    ("18 Nov 2026", f'{rel("v0.6.0-dev.8")}: run artifacts: <code>checkpoint --artifact</code> records what a run made in an attached store (a test suite, a fuzz reproducer, review notes) as pinned citations, and <code>resume</code> shows each with its standing.'),
    ("18 Nov 2026", f'{rel("v0.6.0-dev.7")}: attached stores: a Git repository of disposable evidence, declared once, found on every machine and cited at its pinned commit, so tidying it never makes evidence stale.'),
    ("18 Nov 2026", f'{rel("v0.6.0-dev.6")}: several agent sessions on one machine, each with its own current run; <code>resume --here</code> for hand-overs; <code>plan repin</code>; <code>find --each</code>; a guide for adopting Writfold in an existing workflow, and a page of behaviour changes by release.'),
    ("17 Nov 2026", f'{rel("v0.6.0-dev.5")}: <code>deliver match</code> shows the same draft on every run when several hold the same text.'),
    ("17 Nov 2026", f'{rel("v0.6.0-dev.4")}: delivery modes other agents can rely on: the guard reads the exact text being posted, a mode says which checks may be waived, citations never leave in outward text, and posts are recorded. More of the core proved in Lean, a fix for a wrong result across two clones, and faster lookups.'),
    ("17 Nov 2026", f'{rel("v0.6.0-dev.3")}: your policy, applied the same way every time. A gate can say which outcomes meet it, a required step can refuse a skip, each run pins the policy it started under and says when it moved, and a finished plan says how it finished. <code>kb init</code> starts a knowledge base. More of the core is proved in Lean.'),
    ("16 Nov 2026", f'{rel("v0.6.0-dev.2")}: errors point at the exact place: every file you write reports the file, line and column, shows the line, and suggests a fix; <code>kb lint</code> checks them all at once.'),
    ("16 Nov 2026", f'{rel("v0.6.0-dev.1")}: guard rules read the command as the shell does; a plan step can owe a checked draft (<code>deliver:&lt;mode&gt;</code>); lookups find the right record first more often; <code>writfold watch</code> speaks plain words; and a smaller binary, now just <code>kb</code> and <code>watch</code>.'),
    ("15 Nov 2026", f'{rel("v0.5.0-dev.9")}: <code>kb stale --record</code> writes what a checker found to a tracked file you commit, so a clone without that checker can read it, for citation kinds that set a <code>max_age</code>. <code>record investigation</code> opens an investigation record.'),
    ("15 Nov 2026", f'{rel("v0.5.0-dev.8")}: <code>writfold watch</code> shows the project&rsquo;s records too: decisions, tracker, an impact tree and stale citations. <code>find --kind</code> lists records by kind.'),
    ("15 Nov 2026", f'{rel("v0.5.0-dev.7")}: <code>writfold watch</code> opens on a calm frame; <code>d</code> shows every detail.'),
    ("15 Nov 2026", f'{rel("v0.5.0-dev.6")}: the plan map in <code>writfold watch</code>, with an inspector for the selected step.'),
    ("14 Nov 2026", f'{rel("v0.5.0-dev.5")}: run progress in <code>writfold watch</code>: plan steps with their gates, the inbox, guard rules and a timeline.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.3")}: <code>kb observe</code>, <code>kb repos</code>, and guard rules scoped to paths.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.2")}: external checkers for citation kinds Git cannot check, and citations followed through renames.'),
    ("13 Nov 2026", f'{rel("v0.5.0-dev.1")}: guard rules and checklist gates.'),
    ("13 Nov 2026", f'{rel("v0.4.0-dev.1")}: plans, skills that add steps, your own delivery modes, proposals and <code>kb check</code>.'),
    ("12 Nov 2026", f'{rel("v0.3.0-dev.1")}: gates, <code>writfold watch</code> and delivery drafts.'),
    ("12 Nov 2026", f'{rel("v0.2.0-dev.1")}: the <code>kb</code> read and write commands, citations checked for staleness, and the Claude Code plugin.'),
])
def faq(q, a): return f"<details><summary>{q}</summary><p>{a}</p></details>"
FAQ = "".join([
    faq("Can I use Writfold today?", 'Yes, as a preview: <a href="/#try">install it</a> on Linux x86_64 or WSL2. It is built for one person and their agents, working on local clones.'),
    faq("Does it need a server or a database?", "No. One static binary and files in Git. Writfold keeps a local index for speed and can always rebuild it from Git."),
    faq("Does Writfold run or schedule my agent?", "No. It records the plan and what met each gate. The agent reads the current step, does the work its own way and asks to advance. Writfold runs no model and posts nothing."),
    faq("Can an agent skip a gate or a step?", "Yes, and it shows. A gate never run shows as open; a skipped step shows as skipped, with a reason and a name. Your policy can narrow this: a gate can refuse a waiver, and a required step can refuse a skip. A guard rule you add can deny a command such as <code>git commit</code> until the gates are met. It is a guard, not a lock: it only sees the commands Claude Code shows it."),
    faq("Is it formally verified?", f'In part. The decisions about plans, gates, checklists, delivery drafts, guard rules, your policy, which run is current for a session, how a store&rsquo;s citations are judged and whether a checklist item&rsquo;s evidence answers it and still holds, such as whether a step may be recorded as done and whether a receipt is still about the present bytes, are proved in Lean for every input, against the Rust that ships. The code that reads files into those decisions is tested, not proved. {guide("assurance", "The assurance guide")} has the details and the limits.'),
    faq("Other harnesses?", "The CLI works wherever an agent has a shell. The session-start brief and the guard rules come with the Claude Code plugin."),
    faq("Is the source available?", 'Yes: <a href="https://github.com/writfold-dev/writfold">Writfold</a> is public, and this website is under the MIT license.'),
])
status = f'''  <main id="main" class="wrap" tabindex="-1">
    <section class="hero" aria-labelledby="status-title">
      <p class="eyebrow">Status</p>
      <h1 id="status-title">What runs today.<br><span>What comes next.</span></h1>
      <p class="lede">Writfold is a pre-release. This page lists what the preview runs, what is planned and what is not.</p>
      <p class="maturity"><span class="badge badge-today">Preview</span> <span><a href="{REL}">{VERSION}</a> · Updated {RELEASED}</span></p>
      <nav class="actions" aria-label="Page sections"><a href="#today">Runs today</a><a href="#next">Roadmap</a><a href="#changelog">Changelog</a><a href="#faq">FAQ</a></nav>
    </section>
    <section id="today" class="section" aria-labelledby="today-title">
      <div class="section-heading"><p class="eyebrow">01 / Runs today</p><h2 id="today-title">In the preview</h2><p>Each entry links to its guide. <a href="/#try">Install it</a>, or read the <a href="{README}">README</a>.</p></div>
      <div class="doc-links">{TODAY}</div>
      <p class="fine-print">Limits: one person and their agents, on local clones. Plans, policy, guard rules and external checkers are new: built and tested, with little real use behind them yet.</p>
    </section>
    <section id="next" class="section" aria-labelledby="next-title">
      <div class="section-heading"><p class="eyebrow">02 / Roadmap</p><h2 id="next-title">Done, planned, and not planned</h2></div>
      <ol class="workflow">{ROAD}</ol>
    </section>
    <section id="changelog" class="section" aria-labelledby="changelog-title">
      <div class="section-heading"><p class="eyebrow">03 / Changelog</p><h2 id="changelog-title">What changed</h2><p>One line per release; the <a href="{RELEASES}">release notes</a> carry the detail.</p></div>
      <ol class="changelog">{LOG}</ol>
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
STUBS = {"earlier.html": ("/", "the overview"), **{name: ("/how.html", "How it works") for name in
         ("docs.html", "glossary.html", "tuft.html", "splicery.html", "weft.html")}}
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
