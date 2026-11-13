"""Authoring-time syntax highlighting: text in, HTML spans out. No runtime script."""
import re
from html import escape

def _scan(text, rules):
    """Leftmost match of the combined rules wins; unmatched text stays plain."""
    pattern = re.compile("|".join(f"(?P<g{i}>{rx})" for i, (rx, _) in enumerate(rules)), re.M)
    out, at = [], 0
    for m in pattern.finditer(text):
        out.append(escape(text[at:m.start()], quote=False))
        cls = rules[int(m.lastgroup[1:])][1]
        if callable(cls):
            cls = cls(m.group())
        body = escape(m.group(), quote=False)
        out.append(f'<span class="syntax-{cls}">{body}</span>' if cls else body)
        at = m.end()
    out.append(escape(text[at:], quote=False))
    return "".join(out)

STRING = r'"(?:[^"\\\n]|\\.)*"' + r"|'[^'\n]*'"
OK = {"satisfied", "accepted", "ready", "applied", "active", "done", "fresh", "confirmed", "ok", "clean"}
WARN = {"stale", "moved", "changed", "gone", "blocked", "failed", "unknown", "open", "draft", "in-progress", "unverifiable", "attention", "pending"}

def _badge(text):
    word = text.strip("[]")
    return "ok" if word in OK else "warn" if word in WARN else "badge"

OUTPUT = [
    (r"^#.*$", "comment"),
    (r"⟦[^⟧]*⟧", "string"),
    (r"\[(?:[a-z][a-z-]*)\](?!\()", _badge),
    (r"(?<=\s)![a-z][\w=→./:-]*", "stale"),
    (r"(?<=\s)@[\w.…<>/:#-]+", "path"),
    (r"^(?:decision|asset|ticket|gate|edit|delivery|run|checkpoint|retrieval|relationship|investigation|project|cite|step|plan|proposal|check)\b", "keyword"),
    (r"^ +[a-z-]+:(?= )", "function"),
    (r"^==.*==$", "comment"),
    (r"^> ", "operator"),
]
SHELL = [
    (r"(?<=\s)#.*$", "comment"),
    (STRING, "string"),
    (r"(?<=\s)--?[A-Za-z][\w-]*", "flag"),
    (r"(?:^|(?<=\| )|(?<=&& ))(?:writfold|claude|curl|install|echo|cut|sha256sum|cat|git)\b", "function"),
    (r"\$\(?[A-Za-z_]\w*\)?|\$\(", "variable"),
    (r"\\$|\||&&|=", "operator"),
]
TOML = [
    (r"#.*$", "comment"),
    (STRING, "string"),
    (r"^[A-Za-z_][\w-]*(?= *=)", "keyword"),
    (r"\b\d+\b", "number"),
    (r"[\[\],=]", "punctuation"),
]
SPL = [
    (r'(?:rx)?"(?:[^"\\\n]|\\.)*"', "string"),
    (r"@[\w.]+", "variable"),
    (r"\b(?:edit|each|in|line_matches|expect|replace|with|keep|one|text|within|delete)\b", "keyword"),
    (r"\b\d+\b", "number"),
    (r":=", "operator"),
    (r"[{}\[\](),]", "punctuation"),
]
TUFT = [
    (STRING, "string"),
    (r"@\w+", "variable"),
    (r"\b(?:find|text|in|at|retain|around|lines|project|emit|budget_tokens|sort|asc|desc)\b", "keyword"),
    (r"\b(?:path|line|excerpt|max_chars)\b", "function"),
    (r"\b\d+\b", "number"),
    (r":=", "operator"),
    (r"[\[\](),;:]", "punctuation"),
]
LANGS = {"output": OUTPUT, "toml": TOML, "spl": SPL, "tuft": TUFT}

def highlight(text, lang="session"):
    """`session`: `$ ` lines are commands (with `\\` continuations), the rest is
    output; `%lang` on a line of its own switches the following lines to that language until
    the next command."""
    if lang in LANGS:
        return _scan(text, LANGS[lang])
    if lang == "shell":
        return "\n".join(_scan(line, SHELL) for line in text.split("\n"))
    out, mode, continued = [], "output", False
    for line in text.split("\n"):
        if line.startswith("%"):
            mode = line[1:]
            continue
        if line.startswith("$ ") or continued:
            body = line[2:] if not continued else line
            prompt = "" if continued else '<span class="syntax-prompt">$ </span>'
            out.append(prompt + _scan(body, SHELL))
            continued = line.endswith("\\")
            mode = "output"
        elif line == "…":
            out.append('<span class="syntax-comment">…</span>')
        else:
            out.append(_scan(line, LANGS[mode]))
    return "\n".join(out)
