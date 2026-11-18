"""Inline SVG diagrams for How it works, drawn with the site's .fd classes so they
follow the theme. Each has a wide drawing and a stacked one for narrow screens.
They are drawings of how the product decides, not captured output."""


def _arrow(x1, y1, x2, y2, read=False):
    cls = "fd-arrow fd-arrow-read" if read else "fd-arrow"
    return f'<path class="{cls}" d="M{x1} {y1} L{x2} {y2}" marker-end="url(#MARKER)"/>'


def _defs(marker):
    return (f'<defs><marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse"><path class="fd-head" d="M0 0 L10 5 L0 10 z"/></marker></defs>')


def _box(x, y, w, h, title, lines=(), cls="fd-box", note_cls="fd-note"):
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>',
           f'<text class="fd-item" x="{x + 14}" y="{y + 24}">{title}</text>']
    for n, (text, c) in enumerate(lines):
        out.append(f'<text class="{c or note_cls}" x="{x + 14}" y="{y + 46 + n * 19}">{text}</text>')
    return "".join(out)


def _svg(name, cls, w, h, label, body):
    marker = f"fd-head-{name}-{cls}"
    return (f'<svg class="fd {cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'{_defs(marker)}{body.replace("MARKER", marker)}</svg>')


SESSIONS_LABEL = ("Two agent sessions on one machine, in two repositories, each reading its own current run "
                  "from the knowledge base clone's local pointers: its session's pointer first, then its work "
                  "tree's, then the clone's shared one.")


def sessions():
    wide = "".join([
        _box(16, 30, 214, 74, "Session A", [("in ~/src/api", None)]),
        _box(16, 176, 214, 74, "Session B", [("in ~/src/web", None)]),
        _box(296, 16, 300, 248, "KB clone: local pointers", [
            ("1  session A      → run-1", "fd-cmd"),
            ("2  tree ~/src/api → run-1", "fd-cmd"),
            ("", None),
            ("1  session B      → run-2", "fd-cmd"),
            ("2  tree ~/src/web → run-2", "fd-cmd"),
            ("", None),
            ("3  shared         → run-2", "fd-cmd"),
            ("last made current; read only", "fd-note"),
            ("when 1 and 2 are not set", "fd-note"),
        ], cls="fd-kb"),
        _box(660, 30, 204, 74, "run-1", [("gates A owes", None)]),
        _box(660, 176, 204, 74, "run-2", [("gates B owes", None)]),
        _arrow(230, 67, 294, 60, read=True), _arrow(598, 60, 658, 67, read=True),
        _arrow(230, 213, 294, 135, read=True), _arrow(598, 135, 658, 213, read=True),
        '<text class="fd-read" x="16" y="292">A&#8217;s git commit is judged against run-1, whatever B starts.</text>',
    ])
    tall = "".join([
        _box(10, 10, 190, 64, "Session A", [("in ~/src/api", None)]),
        _box(220, 10, 190, 64, "Session B", [("in ~/src/web", None)]),
        _box(10, 104, 400, 196, "KB clone: local pointers", [], cls="fd-kb"),
        '<text class="fd-cmd" x="24" y="150">1 session A → run-1</text>',
        '<text class="fd-cmd" x="24" y="169">2 ~/src/api → run-1</text>',
        '<text class="fd-cmd" x="224" y="150">1 session B → run-2</text>',
        '<text class="fd-cmd" x="224" y="169">2 ~/src/web → run-2</text>',
        '<text class="fd-cmd" x="24" y="196">3 shared → run-2</text>',
        '<text class="fd-note" x="24" y="230">The most specific pointer that is set</text>',
        '<text class="fd-note" x="24" y="249">decides, even when its run is closed.</text>',
        '<text class="fd-read" x="24" y="272">Proved in Lean.</text>',
        _box(10, 330, 190, 64, "run-1", [("gates A owes", None)]),
        _box(220, 330, 190, 64, "run-2", [("gates B owes", None)]),
        _arrow(105, 76, 105, 102, read=True), _arrow(315, 76, 315, 102, read=True),
        _arrow(105, 302, 105, 328, read=True), _arrow(315, 302, 315, 328, read=True),
    ])
    return (_svg("sessions", "fd-wide", 880, 304, SESSIONS_LABEL, wide)
            + _svg("sessions", "fd-tall", 420, 404, SESSIONS_LABEL, tall))


STORE_LABEL = ("A decision in the knowledge base cites a reproducer in an attached store at the commit where it "
               "was written. The store was tidied later and the file moved; the citation is still judged at its "
               "pinned commit, so it stays fresh. The store's declaration says where every machine finds the clone.")


def store():
    wide = "".join([
        _box(16, 20, 300, 112, "Decision: batch size 250", [
            ("cites repo=scratch rev=a1b2…", "fd-cmd"),
            ("path=work/fuzz/repro.py blob=…", "fd-cmd"),
            ("in the KB, tracked", None),
        ], cls="fd-kb"),
        _box(16, 168, 300, 112, ".writfold/stores/scratch.toml", [
            ("url = git@host:me/scratch.git", "fd-cmd"),
            ("role = attached (pinned)", "fd-cmd"),
            ("committed once, read on every machine", None),
        ]),
        _box(392, 20, 472, 260, "scratch: an attached store", [], cls="fd-box"),
        _box(412, 60, 432, 74, "commit a1b2", [("work/fuzz/repro.py  ← the cited bytes", "fd-cmd")], cls="fd-new-box"),
        _box(412, 156, 432, 74, "head, tidied later", [("archive/fuzz/repro.py  (moved)", "fd-cmd")]),
        '<text class="fd-read" x="412" y="262">judged at a1b2: fresh. The head is never read.</text>',
        _arrow(318, 76, 410, 97, read=True),
        _arrow(318, 224, 390, 224),
        '<text class="fd-note" x="16" y="312">Each machine finds the clone: its own map, then a search root or path hint whose origin is the declared URL.</text>',
    ])
    tall = "".join([
        _box(10, 10, 400, 100, "Decision: batch size 250", [
            ("cites repo=scratch rev=a1b2…", "fd-cmd"),
            ("path=work/fuzz/repro.py", "fd-cmd"),
        ], cls="fd-kb"),
        _box(10, 140, 400, 210, "scratch: an attached store", []),
        _box(26, 178, 368, 70, "commit a1b2", [("work/fuzz/repro.py", "fd-cmd")], cls="fd-new-box"),
        _box(26, 262, 368, 70, "head, tidied later", [("archive/fuzz/repro.py", "fd-cmd")]),
        _arrow(210, 112, 210, 176, read=True),
        '<text class="fd-read" x="10" y="378">Judged at a1b2: fresh.</text>',
        _box(10, 396, 400, 82, ".writfold/stores/scratch.toml", [("url, role = attached (pinned)", "fd-cmd")]),
    ])
    return (_svg("store", "fd-wide", 880, 324, STORE_LABEL, wide)
            + _svg("store", "fd-tall", 420, 488, STORE_LABEL, tall))
