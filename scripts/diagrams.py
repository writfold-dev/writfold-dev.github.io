"""Generate the three diagrams, each as a wide and a tall inline SVG."""
from html import escape as e

def marker(mid):
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="fd-head" d="M0 0 10 5 0 10z"/></marker></defs>')

def text(x, y, cls, s, anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" class="{cls}"{a}>{e(s)}</text>'

STAGES = [
    ("01", "Research", ["kb find · why · context", "kb impact · stale", "or tuft run --cite"], [],
     ["required step: research", "gate: research.backfilled"],
     ["citations,", "receipts, records"], "Citations, retrieval receipts and the records you write."),
    ("02", "Plan", ["checkpoint --new-run"], ["templates in .writfold/plans/"],
     ["the run graph:", "plan set · use · status"],
     ["a run: its task,", "place and plan steps"], "A run with its task, worktree and plan steps."),
    ("03", "Execute", ["kb edit apply (Splicery)", "or Edit · grep · sed", "gate run · gate status", "checkpoint · watch"], [],
     ["plan advance · skip"],
     ["checkpoints, receipts,", "statements, done steps"], "Checkpoints, edit and gate receipts, statements and done steps."),
    ("04", "Deliver", ["deliver prepare · check", "deliver status"], ["checked; nothing is sent"],
     ["your own modes (.toml)", "required step: reflect"],
     ["the exact draft, its", "receipts, a reflection"], "The exact draft, one receipt per check, and a reflection."),
]
FLOW_TITLE = "The Writfold flow: four stages, each writing back to the knowledge base"
FLOW_DESC = ("Four stages left to right, all built. 1 Research: kb find, why, context, impact and stale, or tuft run --cite; a required research step owes the research.backfilled check. "
             "2 Plan: checkpoint --new-run starts a run; the run graph: plan set, plan use and plan status, from templates in .writfold/plans/. "
             "3 Execute: kb edit apply with Splicery, or ordinary Edit, grep and sed; gate run and gate status; checkpoint and watch; plan advance and plan skip. "
             "4 Deliver: deliver prepare, check and status; drafts are checked and nothing is sent; your own delivery modes as .toml files, and a required reflect step at the end of the run. "
             "Every stage writes to the knowledge base, plain records in Git: citations, receipts, records, runs with their plan steps, checkpoints, statements, drafts and a reflection. "
             "The knowledge base answers the next session's questions, with sources. "
             "Check on demand with kb check, kb stale, kb index verify and gate status; the index refreshes itself on every read.")

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
        o.append(f'<rect class="fd-new-box" x="{x+10}" y="{py}" width="{bw-20}" height="{ph}" rx="5"/>')
        o.append(text(x + 18, py + 16, "fd-newtag", "NEW IN v0.4"))
        for j, p in enumerate(planned): o.append(text(x + 18, py + 35 + 20 * j, "fd-cmd", p))
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
    o.append(text(20, 374, "fd-cmd", "decisions · tickets · links · runs/<id>/ checkpoints, receipts, drafts · .writfold/ gates, plans and delivery rules"))
    o.append(text(20, 396, "fd-note", "A local index is derived from it and can always be rebuilt. A new machine needs git clone and the binary."))
    o.append(f'<rect class="fd-box" x=".75" y="420.75" width="{W-1.5}" height="36.5" rx="7"/>')
    o.append(text(20, 444, "fd-num", "CHECK ON DEMAND"))
    o.append(text(170, 444, "fd-cmd", "kb check · kb stale · kb index verify · gate status"))
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
        body.append(f'<rect class="fd-new-box" x="10" y="{py}" width="{W-20}" height="{ph}" rx="5"/>')
        body.append(text(18, py + 16, "fd-newtag", "NEW IN v0.4"))
        for j, p in enumerate(planned): body.append(text(18, py + 35 + 20 * j, "fd-cmd", p))
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
    body.append(f'<rect class="fd-kb" x="1" y="{y}" width="{W-2}" height="184" rx="7"/>')
    body.append(text(16, y + 28, "fd-title", "Knowledge base"))
    body.append(text(16, y + 50, "fd-note", "Plain records in Git: decisions, tickets, links,"))
    body.append(text(16, y + 66, "fd-note", "runs with checkpoints, receipts and drafts,"))
    body.append(text(16, y + 82, "fd-note", "and .writfold/ gates, plans and delivery rules."))
    body.append(text(16, y + 104, "fd-read", "It answers the next session, with sources."))
    body.append(text(16, y + 130, "fd-num", "CHECK ON DEMAND"))
    body.append(text(16, y + 150, "fd-cmd", "kb check · kb stale"))
    body.append(text(16, y + 168, "fd-cmd", "kb index verify · gate status"))
    y += 186
    head = [f'<svg class="fd fd-tall" viewBox="0 0 {W} {y}" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{pfx}-t">{e(FLOW_TITLE)}</title><desc id="{pfx}-d">{e(FLOW_DESC)}</desc>', marker(pfx + "-m")]
    return "".join(head + body) + '</svg>'

T, P = "today", "planned"
COLS = [
    ("WHO OWES GATES", [
        ("A run without a plan", "every gate defined for its repository", T),
        ("A plan step", "the gates its template names", T),
        ("A delivery draft", "PR comment or Slack summary: 3 checks", T),
        ("Your own delivery mode", "a commit message, say, listing its gates", T)]),
    ("A GATE: ONE ATOMIC CHECK", [
        ("Command gate", "a command, or a script it ships", T),
        ("Attested gate", "a statement; it can name an .md to read", T),
        ("Run-record check", "did the step backfill, or reflect?", T),
        ("Weft assessed gate", "checks entailed from cited evidence", T)]),
    ("EVIDENCE WRITFOLD RECORDS", [
        ("Receipt", "the command, run on these bytes", T),
        ("Statement", "attested or waived; never a pass", T),
        ("Assessed receipt", "Weft's result and each citation", T),
        ("Stale when the bytes move", "derived on each read, never stored", T)]),
]
GATE_TITLE = "Gates, the evidence that meets them, and what follows"
GATE_DESC = ("Three columns, all built. Who owes gates: a run without a plan owes every gate defined for its repository; a plan step owes the gates its template names; "
             "a delivery draft (PR comment or Slack summary) owes its three checks; your own delivery mode, a commit message say, lists its gates. "
             "A gate is one atomic check: a command gate (a command, or a script the gate ships), an attested gate (a statement someone must make, which can name an .md to read first), "
             "a run-record check over the run's own records (did the step backfill the knowledge base, or reflect), or a Weft assessed gate (checks entailed from cited evidence). "
             "Evidence Writfold records: a receipt, written after Writfold ran the command on the exact bytes; a statement, attested or waived by name and never shown as a pass; "
             "an assessed receipt holding Weft's result and what each citation stood on; all go stale when the bytes move. "
             "When every gate of the current step is met, plan advance records what met each gate and moves to the next step; without a plan, gate status and deliver status exit 0.")

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
    o.append(text(20, 388, "fd-note", "With a plan: plan advance records what met each gate of the current step and moves to the next."))
    o.append(text(20, 406, "fd-note", "Without one: gate status and deliver status exit 0, and gate lines prints the receipt lines for a commit message."))
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
                                ("fd-note", "With a plan: plan advance records what met"), ("fd-note", "each gate and moves to the next step."),
                                ("fd-note", "Without one: gate status and deliver status"), ("fd-note", "exit 0; gate lines prints the receipt lines.")]):
        body.append(text(16, y + 28 + j * 20 + (6 if j > 1 else 0) + (6 if j > 3 else 0), c, l))
    y += 152
    head = [f'<svg class="fd fd-tall" viewBox="0 0 {W} {y}" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{pfx}-t">{e(GATE_TITLE)}</title><desc id="{pfx}-d">{e(GATE_DESC)}</desc>', marker(pfx + "-m")]
    return "".join(head + body) + '</svg>'

# ---------------------------------------------------------------- the run graph spine
# One run's plan, as `plan status` printed it for the demo repository: (step, state, flag, gates, group)
SPINE = [
    ("research", "done", "", [("backfilled", "satisfied")], "req-start"),
    ("implement", "done", "!stale", [("unit", "stale")], "plan"),
    ("read-diff", "done", "", [], "splice"),
    ("findings", "current", "", [("findings", "open")], "splice"),
    ("ship", "later", "", [("wording", "")], "plan"),
    ("reflect", "later", "", [("reflected", ""), ("reflection", "")], "req-end"),
]
SPINE_TITLE = "One run's plan as a spine of six steps"
SPINE_DESC = ("Six steps in order on one line. research, a required start step: done, its gate backfilled satisfied. "
              "implement, from the plan template fix: done, flagged !stale because its gate unit went stale after a later edit; it stays done. "
              "read-diff and findings, spliced before ship by a review skill as review#1: read-diff is done and owes no gates; findings is the current step and owes the gate findings, open. "
              "ship, from the plan template: later, owing wording. reflect, a required end step: later, owing reflected and reflection.")
KIND = {"satisfied": "ok", "stale": "warn", "open": "warn", "": "later"}

def node(o, x, y, state, flag):
    if state == "done":
        o.append(f'<circle class="sp-done{" sp-stale" if flag else ""}" cx="{x}" cy="{y}" r="8"/>')
    elif state == "current":
        o.append(f'<circle class="sp-current" cx="{x}" cy="{y}" r="10"/><circle class="sp-done" cx="{x}" cy="{y}" r="4"/>')
    else:
        o.append(f'<circle class="sp-later" cx="{x}" cy="{y}" r="7"/>')

def chip(o, x, y, gate, st, anchor):
    label = f"{gate} {st}".strip(); w = round(len(label) * 6.7 + 18)
    left = x - w / 2 if anchor == "middle" else x
    o.append(f'<rect class="sp-chip sp-chip-{KIND[st]}" x="{left}" y="{y}" width="{w}" height="22" rx="11"/>')
    tail = f' <tspan class="sp-{KIND[st]}">{e(st)}</tspan>' if st else ""
    o.append(f'<text x="{left + 9}" y="{y + 15}" class="sp-gate">{e(gate)}{tail}</text>')
    return w

def state_text(x, y, state, flag, anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ''
    tail = f' <tspan class="sp-warn">{e(flag)}</tspan>' if flag else ""
    return f'<text x="{x}" y="{y}" class="sp-state"{a}>[{state}]{tail}</text>'

def brace(o, x1, x2, y, label, cls="fd-lane"):
    o.append(f'<path class="sp-brace" d="M{x1} {y+10}V{y+5}H{x2}V{y+10}"/>')
    o.append(text((x1 + x2) / 2, y - 2, cls, label, "middle"))

def spine_wide(pfx):
    W, cw, ry = 960, 160, 84
    o = [f'<svg class="fd fd-wide" viewBox="0 0 {W} 204" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="{pfx}-t">{e(SPINE_TITLE)}</title><desc id="{pfx}-d">{e(SPINE_DESC)}</desc>']
    xs = [cw // 2 + cw * i for i in range(6)]
    brace(o, xs[0] - 62, xs[0] + 62, 14, "REQUIRED · START")
    brace(o, xs[1] - 62, xs[4] + 62, 14, "PLAN TEMPLATE: fix")
    brace(o, xs[2] - 62, xs[3] + 62, 46, "SPLICED BY A SKILL: review#1", "fd-lane fd-lane-read")
    brace(o, xs[5] - 62, xs[5] + 62, 14, "REQUIRED · END")
    o.append(f'<path class="sp-rail sp-rail-done" d="M{xs[0]} {ry}H{xs[3]}"/><path class="sp-rail" d="M{xs[3]} {ry}H{xs[5]}"/>')
    for x, (step, state, flag, gates, _) in zip(xs, SPINE):
        node(o, x, ry, state, flag)
        o.append(text(x, ry + 32, "sp-step", step, "middle"))
        o.append(state_text(x, ry + 50, state, flag, "middle"))
        if not gates: o.append(text(x, ry + 77, "fd-note", "no gates", "middle"))
        for j, (g, st) in enumerate(gates): chip(o, x, ry + 62 + 28 * j, g, st, "middle")
    o.append('</svg>'); return "".join(o)

def spine_tall(pfx):
    W, rx = 328, 16; body = []; y = 0; ys = []
    for step, state, flag, gates, group in SPINE:
        lane = {"req-start": "REQUIRED · START", "req-end": "REQUIRED · END"}.get(group)
        if step == "implement": lane = "PLAN TEMPLATE: fix"
        if step == "read-diff": lane = "SPLICED BY A SKILL: review#1"
        tx = 62 if group == "splice" else 40
        if lane:
            body.append(text(tx, y + 12, "fd-lane fd-lane-read" if group == "splice" else "fd-lane", lane)); y += 20
        cy = y + 12; ys.append((cy, state, flag, group))
        body.append(text(tx, cy + 5, "sp-step", step))
        body.append(state_text(tx + len(step) * 8 + 10, cy + 5, state, flag))
        cx = tx
        if not gates: body.append(text(tx, cy + 30, "fd-note", "no gates"))
        for g, st in gates: cx += chip(body, cx, cy + 15, g, st, None) + 6
        y += 62
    rail = [f'<path class="sp-rail sp-rail-done" d="M{rx} {ys[0][0]}V{ys[3][0]}"/><path class="sp-rail" d="M{rx} {ys[3][0]}V{ys[5][0]}"/>',
            f'<path class="sp-brace" d="M{rx + 14} {ys[2][0]}H48V{ys[3][0] + 26}"/><path class="sp-brace" d="M{rx + 14} {ys[3][0]}H48"/>']
    for cy, state, flag, _ in ys: node(rail, rx, cy, state, flag)
    head = [f'<svg class="fd fd-tall" viewBox="0 0 {W} {y - 10}" role="img" aria-labelledby="{pfx}-t {pfx}-d" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="{pfx}-t">{e(SPINE_TITLE)}</title><desc id="{pfx}-d">{e(SPINE_DESC)}</desc>']
    return "".join(head + rail + body) + '</svg>'

def flow(pfx): return flow_wide(pfx + "w") + flow_tall(pfx + "n")
def gates(pfx): return gates_wide(pfx + "w") + gates_tall(pfx + "n")
def spine(pfx): return spine_wide(pfx + "w") + spine_tall(pfx + "n")
