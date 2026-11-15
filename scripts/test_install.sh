#!/usr/bin/env bash
# Offline tests for install.sh. Serves a fake release from a local HTTP
# server and runs the installer in an emptied environment (its own HOME,
# its own PATH of symlinked tools, a fake `claude` that logs its arguments).
# Nothing here touches the real ~/.claude or ~/.local/bin.
#
#   bash scripts/test_install.sh            # all shells found among: dash bash busybox
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../install.sh"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/writfold-install-test.XXXXXX")"
SERVER_PID=""
finish() {
    [ -z "$SERVER_PID" ] || kill "$SERVER_PID" 2>/dev/null
    chmod -R u+w "$WORK" 2>/dev/null
    rm -rf "$WORK"
}
trap finish EXIT

PASS=0
FAIL=0
ok() { PASS=$((PASS + 1)); }
bad() { FAIL=$((FAIL + 1)); printf 'FAIL [%s] %s\n' "$SH_NAME" "$*"; [ ! -f "$OUT" ] || sed 's/^/    | /' "$OUT"; }
check() { # check DESCRIPTION COMMAND...
    local what="$1"; shift
    if "$@"; then ok; else bad "$what"; fi
}
out_has() { grep -qF -- "$1" "$OUT"; }
out_lacks() { ! grep -qF -- "$1" "$OUT"; }
requests() { wc -l <"$WORK/http.log" | tr -d ' '; }
claude_calls() { if [ -f "$HOME_T/claude.log" ]; then wc -l <"$HOME_T/claude.log" | tr -d ' '; else echo 0; fi; }

# ---- Fake release ---------------------------------------------------------

ASSET=writfold-x86_64-linux-musl
mkrelease() { # mkrelease VERSION BODY [bad-checksum]
    local d="$WORK/www/v$1"
    mkdir -p "$d"
    printf '#!/bin/sh\n%s\n' "$2" >"$d/$ASSET"
    if [ "${3:-}" = bad-checksum ]; then
        printf '%064d  %s\n' 0 "$ASSET" >"$d/$ASSET.sha256"
    else
        printf '%s  %s\n' "$(sha256sum "$d/$ASSET" | cut -d' ' -f1)" "$ASSET" >"$d/$ASSET.sha256"
    fi
}
mkrelease 9.9.9 'echo "writfold 9.9.9"; echo "profile=test"'
mkrelease 9.9.8 'echo "writfold 9.9.8"'
mkrelease 6.6.6 'echo "writfold 6.6.6"' bad-checksum
mkrelease 5.5.5 'exit 1'
NEW_SHA="$(cut -d' ' -f1 "$WORK/www/v9.9.9/$ASSET.sha256")"

PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1])')"
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$WORK/www" >/dev/null 2>"$WORK/http.log" &
SERVER_PID=$!
for _ in $(seq 50); do
    curl -fsS -o /dev/null "http://127.0.0.1:$PORT/v9.9.9/$ASSET.sha256" 2>/dev/null && break
    sleep 0.1
done
BASE="http://127.0.0.1:$PORT"

# ---- The installer under test: install.sh stamped the way a release does --

stamp() { # stamp VERSION SHA256 <install.sh >stamped
    sed -e "s/^WRITFOLD_DEFAULT_VERSION=.*/WRITFOLD_DEFAULT_VERSION=\"$1\"/" \
        -e "s/^WRITFOLD_DEFAULT_SHA256=.*/WRITFOLD_DEFAULT_SHA256=\"$2\"/"
}
INSTALLER="$WORK/install.sh"
stamp 9.9.9 "$NEW_SHA" <"$SRC" >"$INSTALLER"
BADPIN="$WORK/install-badpin.sh"
stamp 9.9.9 "$(printf '%064d' 1)" <"$SRC" >"$BADPIN"
SH_NAME=setup; OUT=/nonexistent
check "stamping changes exactly the two pin lines" \
    [ "$(diff "$SRC" "$INSTALLER" | grep -c '^>')" = 2 ]

# ---- Emptied environment: PATH holds only symlinks to the tools needed ----

mkbin() { # mkbin DIR TOOL...
    local d="$1" t p; shift
    mkdir -p "$d"
    for t in "$@"; do
        p="$(command -v "$t")" || { echo "test.sh: missing tool $t" >&2; exit 2; }
        ln -s "$p" "$d/$t"
    done
}
COMMON="sh cat awk sed tr wc chmod mv mkdir mktemp rm uname id grep env"
# shellcheck disable=SC2086
{
    mkbin "$WORK/bin-all" $COMMON curl wget sha256sum
    mkbin "$WORK/bin-wget" $COMMON wget sha256sum
    mkbin "$WORK/bin-shasum" $COMMON curl shasum perl
    mkbin "$WORK/bin-nohash" $COMMON curl
}
mkdir -p "$WORK/claude-ok" "$WORK/claude-fail" "$WORK/uname-arm" "$WORK/uname-mac"
printf '#!/bin/sh\necho "$*" >>"$HOME/claude.log"\n' >"$WORK/claude-ok/claude"
printf '#!/bin/sh\necho "$*" >>"$HOME/claude.log"\nexit 1\n' >"$WORK/claude-fail/claude"
printf '#!/bin/sh\ncase "$1" in -m) echo aarch64 ;; *) echo Linux ;; esac\n' >"$WORK/uname-arm/uname"
printf '#!/bin/sh\ncase "$1" in -m) echo arm64 ;; *) echo Darwin ;; esac\n' >"$WORK/uname-mac/uname"
chmod 755 "$WORK"/claude-*/claude "$WORK"/uname-*/uname

# Settings for the next run; reset by fresh().
fresh() {
    N=$((${N:-0} + 1))
    HOME_T="$WORK/home.$N"; TMP_T="$WORK/tmp.$N"; OUT="$WORK/out.$N"
    mkdir -p "$HOME_T" "$TMP_T"
    PREFIX="$HOME_T/.local/bin"
    PATH_T="$WORK/claude-ok:$WORK/bin-all"
    SCRIPT="$INSTALLER"
    EXTRA_ENV=()
}
# run ARGS...: no controlling terminal, stdin at /dev/null.
run() {
    setsid -w env -i HOME="$HOME_T" PATH="$PATH_T" TMPDIR="$TMP_T" \
        WRITFOLD_DOWNLOAD_BASE="$BASE" "${EXTRA_ENV[@]}" \
        "$SH_PATH" "$SCRIPT" "$@" </dev/null >"$OUT" 2>&1
    RC=$?
}
# run_piped ARGS...: the script arrives on stdin, as under `curl | sh`.
run_piped() {
    setsid -w env -i HOME="$HOME_T" PATH="$PATH_T" TMPDIR="$TMP_T" \
        WRITFOLD_DOWNLOAD_BASE="$BASE" "${EXTRA_ENV[@]}" \
        "$SH_PATH" -s -- "$@" <"$SCRIPT" >"$OUT" 2>&1
    RC=$?
}
# run_tty ANSWERS ARGS...: with a controlling terminal; ANSWERS are typed on it.
run_tty() {
    local answers="$1" cmd; shift
    printf -v cmd '%q ' env -i HOME="$HOME_T" PATH="$PATH_T" TMPDIR="$TMP_T" \
        WRITFOLD_DOWNLOAD_BASE="$BASE" "$SH_PATH" "$SCRIPT" "$@"
    { printf '%b' "$answers"; sleep 2; } | script -qec "$cmd" /dev/null >"$OUT" 2>&1
    RC=$?
}
nothing_written() { [ ! -e "$HOME_T/.local" ] && [ -z "$(ls -A "$TMP_T")" ] && [ ! -e "$HOME_T/.claude" ]; }
tmp_clean() { [ -z "$(ls -A "$TMP_T")" ] && [ -z "$(ls -A "$PREFIX" | grep -v '^writfold$')" ]; }

suite() {
    # Happy path, default (stamped) version, script piped on stdin.
    fresh; run_piped
    check "happy: exit 0" [ "$RC" = 0 ]
    check "happy: binary installed" [ -f "$PREFIX/writfold" ]
    check "happy: mode 755" [ "$(stat -c %a "$PREFIX/writfold" 2>/dev/null)" = 755 ]
    check "happy: bytes are the release's" [ "$(sha256sum "$PREFIX/writfold" | cut -d' ' -f1)" = "$NEW_SHA" ]
    check "happy: version printed" out_has "installed: writfold 9.9.9"
    check "happy: plan names the binary URL" out_has "$BASE/v9.9.9/$ASSET"
    check "happy: plan names the checksum URL" out_has "$BASE/v9.9.9/$ASSET.sha256"
    check "happy: plan names the destination" out_has "$PREFIX/writfold (mode 755)"
    check "happy: plan names ~/.claude" out_has "$HOME_T/.claude"
    check "happy: verified checksum printed" out_has "downloaded file  $NEW_SHA"
    check "happy: non-HTTPS base is called out" out_has "it is not HTTPS"
    check "happy: temp dir and staging file removed" tmp_clean
    # No tty: the plugin step is not run, and the output says how to run it.
    check "no tty: claude never called" [ "$(claude_calls)" = 0 ]
    check "no tty: says why" out_has "no terminal to ask on"
    check "no tty: prints command 1" out_has "claude plugin marketplace add writfold-dev/writfold"
    check "no tty: prints command 2" out_has "claude plugin install writfold@writfold"
    check "no tty: prints the opt-in" out_has "sh -s -- --plugin"
    check "PATH advice when the directory is not on PATH" out_has "is not on your PATH"
    check "PATH advice does not touch rc files" [ -z "$(ls -A "$HOME_T" | grep -v -e '^\.local$')" ]

    # No PATH advice when the directory is on PATH.
    fresh; PATH_T="$PREFIX:$PATH_T"; run --no-plugin
    check "on PATH: exit 0" [ "$RC" = 0 ]
    check "on PATH: no advice" out_lacks "not on your PATH"

    # Checksum mismatch: refuses, installs nothing, keeps an older binary.
    fresh; run --version 6.6.6
    check "mismatch: non-zero exit" [ "$RC" != 0 ]
    check "mismatch: says so" out_has "checksum mismatch"
    check "mismatch: nothing installed" [ ! -e "$PREFIX" ]
    check "mismatch: temp dir removed" [ -z "$(ls -A "$TMP_T")" ]
    fresh; run --version 9.9.8; run --version 6.6.6
    check "mismatch over old: non-zero exit" [ "$RC" != 0 ]
    check "mismatch over old: old binary kept" [ "$("$PREFIX/writfold" --version)" = "writfold 9.9.8" ]
    check "mismatch over old: no leftovers" tmp_clean

    # The release's own .sha256 agrees but the installer's pin does not.
    fresh; SCRIPT="$BADPIN"; run
    check "pin mismatch: non-zero exit" [ "$RC" != 0 ]
    check "pin mismatch: says so" out_has "not the one this installer pins"
    check "pin mismatch: nothing installed" [ ! -e "$PREFIX" ]

    # A verified binary that does not run is not put in place.
    fresh; run --version 9.9.8; run --version 5.5.5
    check "broken binary: non-zero exit" [ "$RC" != 0 ]
    check "broken binary: old binary kept" [ "$("$PREFIX/writfold" --version)" = "writfold 9.9.8" ]
    check "broken binary: no leftovers" tmp_clean

    # Missing release.
    fresh; run --version 1.2.3
    check "missing release: non-zero exit" [ "$RC" != 0 ]
    check "missing release: nothing installed" [ ! -e "$PREFIX" ]

    # --dry-run: prints the plan, fetches nothing, writes nothing.
    fresh; before="$(requests)"; run --dry-run --plugin
    check "dry-run: exit 0" [ "$RC" = 0 ]
    check "dry-run: plan printed" out_has "Plan"
    check "dry-run: says so" out_has "Dry run: nothing was downloaded"
    check "dry-run: nothing written" nothing_written
    check "dry-run: no requests" [ "$(requests)" = "$before" ]
    check "dry-run: claude never called" [ "$(claude_calls)" = 0 ]

    # --no-plugin never calls claude, even with a terminal.
    fresh; run_tty '\n' --no-plugin
    check "--no-plugin: exit 0" [ "$RC" = 0 ]
    check "--no-plugin: installed" [ -x "$PREFIX/writfold" ]
    check "--no-plugin: claude never called" [ "$(claude_calls)" = 0 ]
    check "--no-plugin: prints the commands" out_has "claude plugin install writfold@writfold"
    check "--no-plugin: no plugin question" out_lacks "Run these two commands now?"

    # --plugin runs exactly the two commands.
    fresh; run --plugin
    check "--plugin: exit 0" [ "$RC" = 0 ]
    check "--plugin: exactly the two commands" \
        [ "$(cat "$HOME_T/claude.log" 2>/dev/null)" = "plugin marketplace add writfold-dev/writfold
plugin install writfold@writfold" ]
    check "--plugin: announces each before running" out_has "running: claude plugin marketplace add writfold-dev/writfold"

    # --plugin when claude fails: binary stays installed, exit is non-zero.
    fresh; PATH_T="$WORK/claude-fail:$WORK/bin-all"; run --plugin
    check "plugin failure: non-zero exit" [ "$RC" != 0 ]
    check "plugin failure: binary installed" [ -x "$PREFIX/writfold" ]
    check "plugin failure: says so" out_has "the plugin was not installed"

    # claude absent: skip and print the commands, even with --plugin.
    fresh; PATH_T="$WORK/bin-all"; run --plugin
    check "claude absent: exit 0" [ "$RC" = 0 ]
    check "claude absent: installed" [ -x "$PREFIX/writfold" ]
    check "claude absent: says why" out_has "the claude CLI is not on PATH"
    check "claude absent: prints command 1" out_has "claude plugin marketplace add writfold-dev/writfold"
    check "claude absent: prints command 2" out_has "claude plugin install writfold@writfold"

    # --yes: no prompt, binary only.
    fresh; run_tty '' --yes
    check "--yes: exit 0" [ "$RC" = 0 ]
    check "--yes: no prompts" out_lacks "[Y/n]"
    check "--yes: installed" [ -x "$PREFIX/writfold" ]
    check "--yes: claude never called" [ "$(claude_calls)" = 0 ]

    # With a terminal: decline the install.
    fresh; run_tty 'n\n'
    check "tty decline: asked" out_has "Proceed with the download and install? [Y/n]"
    check "tty decline: non-zero exit" [ "$RC" != 0 ]
    check "tty decline: nothing written" nothing_written
    # Accept the install, take the default (no) for the plugin.
    fresh; run_tty '\n\n'
    check "tty default: exit 0" [ "$RC" = 0 ]
    check "tty default: installed" [ -x "$PREFIX/writfold" ]
    check "tty default: plugin question asked" out_has "Run these two commands now? [y/N]"
    check "tty default: claude never called" [ "$(claude_calls)" = 0 ]
    # Accept both.
    fresh; run_tty 'y\ny\n'
    check "tty yes: exit 0" [ "$RC" = 0 ]
    check "tty yes: claude called twice" [ "$(claude_calls)" = 2 ]

    # Upgrade in place, then an identical re-run.
    fresh; run --version v9.9.8 --no-plugin
    check "upgrade: first install" out_has "installed: writfold 9.9.8"
    run --no-plugin
    check "upgrade: exit 0" [ "$RC" = 0 ]
    check "upgrade: plan says what is replaced" out_has "replaces: writfold 9.9.8"
    check "upgrade: old -> new" out_has "installed: writfold 9.9.8 -> writfold 9.9.9"
    check "upgrade: new binary in place" [ "$("$PREFIX/writfold" --version | sed -n 1p)" = "writfold 9.9.9" ]
    inode="$(stat -c %i "$PREFIX/writfold")"
    run --no-plugin
    check "re-run: exit 0" [ "$RC" = 0 ]
    check "re-run: says identical" out_has "identical"
    check "re-run: file not rewritten" [ "$(stat -c %i "$PREFIX/writfold")" = "$inode" ]
    check "re-run: no leftovers" tmp_clean

    # --prefix and the environment variables.
    fresh; run --prefix "$HOME_T/opt/tools" --no-plugin
    check "--prefix: installed there" [ -x "$HOME_T/opt/tools/writfold" ]
    check "--prefix: default location untouched" [ ! -e "$HOME_T/.local" ]
    fresh; EXTRA_ENV=(WRITFOLD_INSTALL_DIR="$HOME_T/envdir" WRITFOLD_VERSION=9.9.8); run
    check "env: WRITFOLD_INSTALL_DIR and WRITFOLD_VERSION" \
        [ "$("$HOME_T/envdir/writfold" --version 2>/dev/null)" = "writfold 9.9.8" ]

    # Refusals that touch nothing.
    fresh; PATH_T="$WORK/uname-arm:$PATH_T"; run
    check "aarch64: non-zero exit" [ "$RC" != 0 ]
    check "aarch64: says so" out_has "unsupported architecture: aarch64"
    check "aarch64: nothing written" nothing_written
    fresh; PATH_T="$WORK/uname-mac:$PATH_T"; run
    check "macOS: non-zero exit" [ "$RC" != 0 ]
    check "macOS: says so" out_has "macOS is not supported"
    check "macOS: nothing written" nothing_written
    fresh; run --frobnicate
    check "unknown option: non-zero exit" [ "$RC" != 0 ]
    check "unknown option: nothing written" nothing_written
    fresh; run --version '../../etc'
    check "bad version: non-zero exit" [ "$RC" != 0 ]
    check "bad version: nothing written" nothing_written
    fresh; PATH_T="$WORK/bin-nohash"; run
    check "no sha256 tool: non-zero exit" [ "$RC" != 0 ]
    check "no sha256 tool: nothing written" nothing_written
    if [ "$(id -u)" != 0 ]; then
        fresh; mkdir -p "$HOME_T/ro"; chmod 555 "$HOME_T/ro"; run --prefix "$HOME_T/ro"
        check "read-only dir: non-zero exit" [ "$RC" != 0 ]
        check "read-only dir: mentions no sudo" out_has "never uses sudo"
        check "read-only dir: nothing fetched into tmp" [ -z "$(ls -A "$TMP_T")" ]
    fi

    # wget instead of curl; shasum instead of sha256sum.
    fresh; PATH_T="$WORK/bin-wget"; run
    check "wget: exit 0" [ "$RC" = 0 ]
    check "wget: plan says wget" out_has "with wget"
    check "wget: installed" [ -x "$PREFIX/writfold" ]
    fresh; PATH_T="$WORK/bin-shasum"; run
    check "shasum: exit 0" [ "$RC" = 0 ]
    check "shasum: plan says shasum" out_has "(shasum)"
    check "shasum: installed" [ -x "$PREFIX/writfold" ]
    fresh; PATH_T="$WORK/bin-wget"; run --version 6.6.6
    check "wget mismatch: refused" [ "$RC" != 0 ] 
    check "wget mismatch: nothing installed" [ ! -e "$PREFIX" ]

    # A download cut short runs nothing: every whole-line prefix, and every
    # byte prefix of the last line.
    fresh
    local total last_len n before cut ran=0
    total="$(wc -l <"$INSTALLER")"
    last_len="$(tail -n 1 "$INSTALLER" | wc -c)"
    before="$(requests)"
    cut="$WORK/cut.sh"
    : >"$WORK/cut.out"
    for n in $(seq 1 $((total - 1))); do
        head -n "$n" "$INSTALLER" >"$cut"
        SCRIPT="$cut"; run_piped --plugin; cat "$OUT" >>"$WORK/cut.out"; ran=$((ran + 1))
    done
    for n in $(seq 2 "$last_len"); do   # n=1 would drop only the final newline
        head -c "-$n" "$INSTALLER" >"$cut"
        SCRIPT="$cut"; run_piped --plugin; cat "$OUT" >>"$WORK/cut.out"; ran=$((ran + 1))
    done
    OUT="$WORK/cut.out"
    check "truncated ($ran cuts): nothing written" nothing_written
    check "truncated: no requests" [ "$(requests)" = "$before" ]
    check "truncated: claude never called" [ "$(claude_calls)" = 0 ]
    check "truncated: no plan printed" out_lacks "Plan"
    OUT=/nonexistent
    # And the whole file without its final newline still works.
    fresh; head -c -1 "$INSTALLER" >"$cut"; SCRIPT="$cut"; run_piped --no-plugin
    check "no final newline: installs" [ -x "$PREFIX/writfold" ]
}

# ---- Static checks, then the suite under each shell ------------------------

SH_NAME=static; OUT=/nonexistent
check "dash -n" dash -n "$SRC"
check "bash -n" bash -n "$SRC"
check "no sudo invocation in the script" bash -c '! grep -nE "(^|[;&|[:space:]])sudo[[:space:]]+[a-z-]" "$1" | grep -v "^[0-9]*:#"' _ "$SRC"
check "last line is the guarded call" [ "$(tail -n 1 "$SRC")" = '{ main "$@"; }' ]
if command -v shellcheck >/dev/null 2>&1; then
    check "shellcheck -s sh" shellcheck -s sh "$SRC"
else
    echo "note: shellcheck is not installed; skipped"
fi
if command -v checkbashisms >/dev/null 2>&1; then
    check "checkbashisms" checkbashisms "$SRC"
fi

for SH_NAME in dash bash "bash --posix" busybox; do
    case "$SH_NAME" in
        "bash --posix")
            printf '#!/bin/sh\nexec %s --posix "$@"\n' "$(command -v bash)" >"$WORK/bash-posix"
            chmod 755 "$WORK/bash-posix"; SH_PATH="$WORK/bash-posix" ;;
        busybox)
            command -v busybox >/dev/null 2>&1 || { echo "note: busybox is not installed; skipped"; continue; }
            printf '#!/bin/sh\nexec %s sh "$@"\n' "$(command -v busybox)" >"$WORK/busybox-sh"
            chmod 755 "$WORK/busybox-sh"; SH_PATH="$WORK/busybox-sh" ;;
        *) SH_PATH="$(command -v "$SH_NAME")" ;;
    esac
    p=$PASS; f=$FAIL
    suite
    printf '%-13s %d passed, %d failed\n' "$SH_NAME" $((PASS - p)) $((FAIL - f))
done

printf 'total         %d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" = 0 ]
