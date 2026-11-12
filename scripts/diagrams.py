"""Generate the two diagrams, each as a wide and a tall inline SVG."""
from html import escape as e

def marker(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="fd-head" d="M0 0 10 5 0 10z"/></marker></defs>')

def text(x, y, cls, s, anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" class="{cls}"{a}>{e(s)}</text>'

STAGES = [
    ("01", "Research", ["kb find · why · context", "kb impact · stale", "or tuft run --cite"], [],
     ["required: backfill the KB"],
     ["citations,", "receipts, records"], "Citations, retrieval receipts and the records you write."),
    ("02", "Plan", ["checkpoint --new-run"], ["today the plan is a note"],
     ["the run graph:", "plan set · plan status"],
     ["a run: its task,", "place and plan note"], "A run with its task, worktree and plan note."),
    ("03", "Execute", ["kb edit apply (Splicery)", "or Edit · grep · sed", "gate run · gate status", "checkpoint · watch"], [],
     ["plan advance"],
     ["checkpoints, edit and", "gate receipts, statements"], "Checkpoints, edit receipts, gate receipts and statements."),
    ("04", "Deliver", ["deliver prepare · check", "deliver status"], ["checked; nothing is sent"],
     ["your own modes", "required: reflect at end"],
     ["the exact draft and", "a receipt per check"], "The exact draft and one receipt per check."),
]
FLOW_TITLE = "The Writfold flow: four stages, each writing back to the knowledge base"
FLOW_DESC = ("Four stages left to right. 1 Research: kb find, why, context, impact and stale, or tuft run --cite; planned: a required step that backfills the knowledge base. "
             "2 Plan: checkpoint --new-run starts a run and today the plan is a note; planned: the run graph, with plan set and plan status. "
             "3 Execute: kb edit apply with Splicery, or ordinary Edit, grep and sed; gate run and gate status; checkpoint and watch; planned: plan advance. "
             "4 Deliver: deliver prepare, check and status; drafts are checked and nothing is sent; planned: your own delivery modes, and a required reflection at the end of every run. "
             "Every stage writes to the knowledge base, plain records in Git: citations, receipts, records, runs, checkpoints, statements and drafts. "
             "The knowledge base answers the next session's questions, with sources. "
             "Check on demand with kb stale, kb index verify and gate status; the index refreshes itself on every read.")

def flow_wide(pfx):
    W, bw, gap, bh = 960, 225, 20, 236
    o = [f'<svg class="fd fd-wide" viewBox="0 0 {W} 458" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="{pfx}-t">{e(FLOW_TITLE)}</title><desc id="{pfx}-d">{e(FLOW_DESC)}</desc>', marker(pfx + "-m")]
    for i, (num, title, cmds, notes, planned, feed, _) in enumerate(STAGES):
        x = i * (bw + gap)
        o.append(f'<rect class="fd-box" x="{x+.75}" y=".75" width="{bw-1.5}" height="{bh-1.5}" rx="7"/>')
        o.append(text(x + 16, 28, "fd-num", num)); o.append(text(x + 16, 54, "fd-title", title))
        y = 84
        for c in cmds: o.append(text(x + 16, y, "fd-cmd", c)); y += 20
        for n in notes: o.append(text(x + 16, y, "fd-note", n)); y += 20
        ph = 26 + 20 * len(planned); py = bh - 12 - ph
        o.append(f'<rect class="fd-planned-box" x="{x+10}" y="{py}" width="{bw-20}" height="{ph}" rx="5"/>')
        o.append(text(x + 18, py + 16, "fd-tag", "PLANNED"))
        for j, p in enumerate(planned): o.append(text(x + 18, py + 35 + 20 * j, "fd-planned", p))
        if i < 3:
            o.append(f'<path class="fd-arrow" d="M{x+bw+3} 54H{x+bw+gap-3}" marker-end="url(#{pfx}-m)"/>')
        ax = x + (132 if i == 0 else 28)
        o.append(f'<path class="fd-arrow" d="M{ax} {bh+6}V314" marker-end="url(#{pfx}-m)"/>')
        o.append(text(ax + 10, bh + 22, "fd-lane", "WRITES BACK"))
        for j, f in enumerate(feed): o.append(text(ax + 10, bh + 42 + 16 * j, "fd-note", f))
    o.append(f'<path class="fd-arrow fd-arrow-read" d="M28 314V{bh+8}" marker-end="url(#{pfx}-m)"/>')
    o.append(text(38, bh + 22, "fd-lane fd-lane-read", "READS"))
    o.append(text(38, bh + 42, "fd-read", "answers,")); o.append(text(38, bh + 58, "fd-read", "with sources"))
    o.append(f'<rect class="fd-kb" x="1" y="320" width="{W-2}" height="90" rx="7"/>')
    o.append(text(20, 350, "fd-title", "Knowledge base: plain records in Git"))
    o.append(text(20, 374, "fd-cmd", "decisions · tickets · links · runs/<id>/ checkpoints, receipts, drafts · .writfold/ gates and delivery rules"))
    o.append(text(20, 396, "fd-note", "A local index is derived from it and can always be rebuilt. A new machine needs git clone and the binary."))
    o.append(f'<rect class="fd-box" x=".75" y="420.75" width="{W-1.5}" height="36.5" rx="7"/>')
    o.append(text(20, 444, "fd-num", "CHECK ON DEMAND"))
    o.append(text(170, 444, "fd-cmd", "kb stale · kb index verify · gate status"))
    o.append(text(W - 20, 444, "fd-note", "The index refreshes itself on every read.", "end"))
    o.append('</svg>')
    return "".join(o)

def flow_tall(pfx):
    W = 328
    body = []; y = 0
    for i, (num, title, cmds, notes, planned, _, feed) in enumerate(STAGES):
        h = 62 + 20 * (len(cmds) + len(notes)) + 8 + 26 + 20 * len(planned) + 12 + 52
        body.append(f'<rect class="fd-box" x=".75" y="{y+.75}" width="{W-1.5}" height="{h-1.5}" rx="7"/>')
        body.append(text(16, y + 28, "fd-num", num)); body.append(text(16, y + 54, "fd-title", title))
        ty = y + 82
        for c in cmds: body.append(text(16, ty, "fd-cmd", c)); ty += 20
        for n in notes: body.append(text(16, ty, "fd-note", n)); ty += 20
        py = ty - 6; ph = 26 + 20 * len(planned)
        body.append(f'<rect class="fd-planned-box" x="10" y="{py}" width="{W-20}" height="{ph}" rx="5"/>')
        body.append(text(18, py + 16, "fd-tag", "PLANNED"))
        for j, p in enumerate(planned): body.append(text(18, py + 35 + 20 * j, "fd-planned", p))
        fy = py + ph + 12
        body.append(f'<path class="fd-rule" d="M10 {fy}H{W-10}"/>')
        words = ("Writes back: " + feed).split(); lines = [""]
        for w in words:
            if len(lines[-1]) + len(w) + 1 > 46: lines.append("")
            lines[-1] = (lines[-1] + " " + w).strip()
        for j, l in enumerate(lines[:2]): body.append(text(16, fy + 18 + 16 * j, "fd-note", l))
        y += h
        body.append(f'<path class="fd-arrow" d="M{W/2} {y+4}V{y+24}" marker-end="url(#{pfx}-m)"/>')
        y += 30
    body.append(f'<rect class="fd-kb" x="1" y="{y}" width="{W-2}" height="166" rx="7"/>')
    body.append(text(16, y + 28, "fd-title", "Knowledge base"))
    body.append(text(16, y + 50, "fd-note", "Plain records in Git: decisions, tickets, links,"))
    body.append(text(16, y + 66, "fd-note", "runs with checkpoints, receipts and drafts,"))
    body.append(text(16, y + 82, "fd-note", "and .writfold/ gates and delivery rules."))
    body.append(text(16, y + 104, "fd-read", "It answers the next session, with sources."))
    body.append(text(16, y + 130, "fd-num", "CHECK ON DEMAND"))
    body.append(text(16, y + 150, "fd-cmd", "kb stale · kb index verify · gate status"))
    y += 168
    head = [f'<svg class="fd fd-tall" viewBox="0 0 {W} {y}" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{pfx}-t">{e(FLOW_TITLE)}</title><desc id="{pfx}-d">{e(FLOW_DESC)}</desc>', marker(pfx + "-m")]
    return "".join(head + body) + '</svg>'

T, P = "today", "planned"
COLS = [
    ("WHO OWES GATES", [
        ("A run", "every gate defined for its repository", T),
        ("A delivery draft", "PR comment or Slack summary: 3 checks", T),
        ("Your own delivery modes", "a commit message, say, listing its gates", P),
        ("A plan step", "required steps are in every run", P)]),
    ("A GATE: ONE ATOMIC CHECK", [
        ("Command gate", "a command and the paths it covers", T),
        ("Attested gate", "a statement someone must make", T),
        ("Instruction gate", "an .md to read, with its own scripts", P),
        ("Run-record check", "did the run backfill, and reflect?", P)]),
    ("EVIDENCE WRITFOLD RECORDS", [
        ("Receipt", "the command, run on these bytes", T),
        ("Statement", "attested or waived; never a pass", T),
        ("Stale when the bytes move", "derived on each read, never stored", T),
        ("Assessed receipt", "Weft's result on a plan step", P)]),
]
GATE_TITLE = "Gates, the evidence that meets them, and what follows"
GATE_DESC = ("Three columns. Who owes gates: today a run owes every gate defined for its repository, and a delivery draft (PR comment or Slack summary) owes its built-in checks; "
             "planned: your own delivery modes listing their gates, and plan steps, with required steps included in every run. "
             "A gate is one atomic check: today a command gate (a command and the paths it covers) or an attested gate (a statement someone must make); "
             "planned: an instruction gate with an .md to read and its own scripts, and a run-record check over the run's own records, such as whether it backfilled the knowledge base and ended with a reflection. "
             "Evidence Writfold records: today a receipt, written after Writfold ran the command on the exact bytes, or a statement, attested or waived by name and never shown as a pass; both go stale when the bytes move; "
             "planned: an assessed receipt from Weft on a plan step. "
             "When every gate is met, today gate status and deliver status exit 0; planned: plan advance records the step and moves to the next.")

def item(o, x, y, w, t, s, st):
    cls = "fd-box" if st == T else "fd-planned-box"
    o.append(f'<rect class="{cls}" x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="56.5" rx="6"/>')
    o.append(text(x + 14, y + 24, "fd-item", t)); o.append(text(x + 14, y + 44, "fd-note", s))
    if st == P: o.append(text(x + w - 12, y + 22, "fd-tag", "PLANNED", "end"))

def gates_wide(pfx):
    W, cw, gap = 960, 280, 60
    o = [f'<svg class="fd fd-wide" viewBox="0 0 {W} 418" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="{pfx}-t">{e(GATE_TITLE)}</title><desc id="{pfx}-d">{e(GATE_DESC)}</desc>', marker(pfx + "-m")]
    for i, (head, items) in enumerate(COLS):
        x = i * (cw + gap)
        o.append(text(x, 14, "fd-num", head))
        for j, (t, s, st) in enumerate(items): item(o, x, 28 + 68 * j, cw, t, s, st)
    for i, lab in enumerate(["owes", "met by"]):
        x = cw + i * (cw + gap)
        o.append(f'<path class="fd-arrow" d="M{x+4} 160H{x+gap-4}" marker-end="url(#{pfx}-m)"/>')
        o.append(text(x + gap / 2, 150, "fd-note", lab, "middle"))
    o.append(f'<path class="fd-arrow" d="M480 300V330" marker-end="url(#{pfx}-m)"/>')
    o.append(f'<rect class="fd-kb" x="1" y="336" width="{W-2}" height="80" rx="7"/>')
    o.append(text(20, 364, "fd-item", "When every gate is met: satisfied, attested or waived"))
    o.append(text(20, 388, "fd-note", "Today: gate status and deliver status exit 0, and gate lines prints the receipt lines for a commit message."))
    o.append(text(20, 406, "fd-planned-note", "Planned: plan advance records what met each gate and moves to the next step."))
    o.append('</svg>'); return "".join(o)

def gates_tall(pfx):
    W = 328; body = []; y = 0
    labels = ["owes", "met by"]
    for i, (head, items) in enumerate(COLS):
        body.append(text(0, y + 14, "fd-num", head)); y += 26
        for (t, s, st) in items: item(body, 0, y, W, t, s, st); y += 66
        if i < 2:
            body.append(f'<path class="fd-arrow" d="M24 {y-4}V{y+20}" marker-end="url(#{pfx}-m)"/>')
            body.append(text(36, y + 14, "fd-note", labels[i])); y += 34
    body.append(f'<path class="fd-arrow" d="M24 {y-4}V{y+20}" marker-end="url(#{pfx}-m)"/>'); y += 26
    body.append(f'<rect class="fd-kb" x="1" y="{y}" width="{W-2}" height="150" rx="7"/>')
    for j, (c, l) in enumerate([("fd-item", "When every gate is met"), ("fd-note", "(satisfied, attested or waived)"),
                                ("fd-note", "Today: gate status and deliver status exit 0;"), ("fd-note", "gate lines prints the receipt lines."),
                                ("fd-planned-note", "Planned: plan advance records what met"), ("fd-planned-note", "each gate and moves to the next step.")]):
        body.append(text(16, y + 28 + j * 20 + (6 if j > 1 else 0) + (6 if j > 3 else 0), c, l))
    y += 152
    head = [f'<svg class="fd fd-tall" viewBox="0 0 {W} {y}" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{pfx}-t">{e(GATE_TITLE)}</title><desc id="{pfx}-d">{e(GATE_DESC)}</desc>', marker(pfx + "-m")]
    return "".join(head + body) + '</svg>'

LEGEND = ('<p class="legend"><span><span class="chip chip-today">solid</span> runs today</span>'
          '<span><span class="chip chip-planned">dashed</span> planned, not built</span></p>')
def flow(pfx): return flow_wide(pfx + "w") + flow_tall(pfx + "n")
def gates(pfx): return gates_wide(pfx + "w") + gates_tall(pfx + "n")
