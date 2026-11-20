#!/bin/sh
# Writfold installer.
#
#   curl -fsSL https://writfold.dev/install.sh | sh
#   curl -fsSL https://writfold.dev/install.sh | sh -s -- --dry-run
#
# It prints a plan naming every path it will touch, then:
#   1. downloads one static binary and its .sha256 file from the GitHub
#      release into a fresh temporary directory;
#   2. verifies the SHA-256 before anything is installed;
#   3. writes the binary to ~/.local/bin/writfold (temporary file in that
#      directory, then an atomic rename);
#   4. optionally registers the Claude Code plugin by running the `claude`
#      CLI, which writes into ~/.claude. This step is never run unless you
#      answer "y" on the terminal or pass --plugin.
#
# It never uses sudo and never edits shell startup files.
# Run with --help for the options. Linux x86_64 (including WSL2) only.
#
# Everything runs from main(), called on the last line, so a download that
# is cut short defines functions and then stops without running anything.

set -eu

# The release installed by default. The website's release step rewrites
# these two lines together (see the release notes for the site).
WRITFOLD_DEFAULT_VERSION="0.6.0-dev.11"
WRITFOLD_DEFAULT_SHA256="8c67505991bb4e845cd380491ce32eca04fcbe3fcb93c4f1c34888acf4370660"

REPO="writfold-dev/writfold"
ASSET="writfold-x86_64-linux-musl"
BIN="writfold"
MARKETPLACE_CMD="claude plugin marketplace add writfold-dev/writfold"
PLUGIN_CMD="claude plugin install writfold@writfold"

TMP_DIR=""
STAGED=""

say() {
    printf '%s\n' "$*"
}

row() {
    printf '  %-10s %s\n' "$1" "$2"
}

detail() {
    printf '      %s\n' "$*"
}

warn() {
    printf 'writfold-install: warning: %s\n' "$*" >&2
}

die() {
    printf 'writfold-install: error: %s\n' "$*" >&2
    exit 1
}

cleanup() {
    [ -z "$STAGED" ] || rm -f "$STAGED"
    [ -z "$TMP_DIR" ] || rm -rf "$TMP_DIR"
}

usage() {
    cat <<EOF
Writfold installer (Linux x86_64, including WSL2)

Usage:
  curl -fsSL https://writfold.dev/install.sh | sh
  curl -fsSL https://writfold.dev/install.sh | sh -s -- [options]
  sh install.sh [options]

Options:
  --dry-run        Print the plan and exit. Downloads and writes nothing.
  --version V      Install release V instead of the default ($WRITFOLD_DEFAULT_VERSION).
  --prefix DIR     Directory to put the binary in; the file is DIR/$BIN.
                   Default: \$HOME/.local/bin
  --plugin         Also register the Claude Code plugin, without asking.
  --no-plugin      Never run the plugin step and never ask about it.
  --yes            Do not prompt. Installs the binary; the plugin step runs
                   only if --plugin is also given.
  --help           Show this help.

Environment:
  WRITFOLD_VERSION        Same as --version.
  WRITFOLD_INSTALL_DIR    Same as --prefix.
  WRITFOLD_DOWNLOAD_BASE  Replace https://github.com/$REPO/releases/download
                          (a mirror, or a local server for testing).

With no terminal to ask on (CI, a pipe with no tty), the binary is installed
and the plugin step is skipped unless --plugin is given.
EOF
}

have() {
    command -v "$1" >/dev/null 2>&1
}

# True when there is a terminal a question can be asked on. Under
# `curl | sh` standard input is the script itself, so prompts use /dev/tty.
have_tty() {
    ( : </dev/tty ) 2>/dev/null
}

# ask QUESTION DEFAULT(y|n): 0 for yes, 1 for no.
ask() {
    printf '%s ' "$1" >/dev/tty
    answer=""
    read -r answer </dev/tty || answer=""
    case "$answer" in
        y|Y|yes|Yes|YES) return 0 ;;
        n|N|no|No|NO) return 1 ;;
        "") [ "$2" = y ] ;;
        *) return 1 ;;
    esac
}

fetch() {
    case "$DOWNLOADER" in
        curl)
            case "$1" in
                https://*)
                    curl --proto '=https' --proto-redir '=https' --tlsv1.2 \
                        -fsSL -o "$2" "$1" ;;
                *)
                    curl -fsSL -o "$2" "$1" ;;
            esac ;;
        wget)
            wget -q -O "$2" "$1" ;;
    esac
}

sha256_of() {
    if [ "$HASHER" = sha256sum ]; then
        sha256sum "$1"
    else
        shasum -a 256 "$1"
    fi | awk '{ print $1 }'
}

is_sha256() {
    case "$1" in
        *[!0-9a-f]*) return 1 ;;
    esac
    [ "${#1}" -eq 64 ]
}

# First line of `FILE --version`, or nothing if it does not run.
version_of() {
    "$1" --version </dev/null 2>/dev/null | sed -n '1p'
}

print_plugin_commands() {
    detail "$MARKETPLACE_CMD"
    detail "$PLUGIN_CMD"
}

main() {
    version="${WRITFOLD_VERSION:-}"
    install_dir="${WRITFOLD_INSTALL_DIR:-}"
    base="${WRITFOLD_DOWNLOAD_BASE:-https://github.com/$REPO/releases/download}"
    plugin=ask
    assume_yes=no
    dry_run=no

    while [ $# -gt 0 ]; do
        case "$1" in
            --dry-run) dry_run=yes ;;
            --yes|-y) assume_yes=yes ;;
            --plugin) plugin=yes ;;
            --no-plugin) plugin=no ;;
            --version)
                [ $# -ge 2 ] || die "--version needs a value"
                version="$2"; shift ;;
            --version=*) version="${1#--version=}" ;;
            --prefix)
                [ $# -ge 2 ] || die "--prefix needs a directory"
                install_dir="$2"; shift ;;
            --prefix=*) install_dir="${1#--prefix=}" ;;
            --help|-h) usage; exit 0 ;;
            *) die "unknown option: $1 (try --help)" ;;
        esac
        shift
    done

    # ---- Checks that touch nothing --------------------------------------

    os="$(uname -s)"
    arch="$(uname -m)"
    case "$os" in
        Linux) ;;
        Darwin)
            die "macOS is not supported. Writfold ships one build: Linux x86_64 (including WSL2)." ;;
        MINGW*|MSYS*|CYGWIN*)
            die "native Windows is not supported. Run this inside WSL2 instead." ;;
        *)
            die "unsupported operating system: $os. Writfold ships one build: Linux x86_64 (including WSL2)." ;;
    esac
    case "$arch" in
        x86_64|amd64) ;;
        *)
            die "unsupported architecture: $arch. Writfold ships one build: Linux x86_64 (including WSL2)." ;;
    esac
    platform="Linux x86_64"
    if grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then
        platform="Linux x86_64 (WSL)"
    fi

    if [ -z "$version" ]; then
        version="$WRITFOLD_DEFAULT_VERSION"
        version_note="the default pinned in this installer"
    else
        version="${version#v}"
        version_note="requested"
    fi
    case "$version" in
        ""|*[!0-9A-Za-z.+-]*) die "not a version: '$version' (expected something like $WRITFOLD_DEFAULT_VERSION)" ;;
    esac
    pinned_sha=""
    if [ "$version" = "$WRITFOLD_DEFAULT_VERSION" ]; then
        pinned_sha="$WRITFOLD_DEFAULT_SHA256"
    fi

    if [ -z "$install_dir" ]; then
        [ -n "${HOME:-}" ] || die "HOME is not set; pass --prefix DIR"
        install_dir="$HOME/.local/bin"
    fi
    case "$install_dir" in
        /*) ;;
        *) install_dir="$(pwd)/$install_dir" ;;
    esac
    install_dir="${install_dir%/}"
    [ -n "$install_dir" ] || die "refusing to install into /"
    dest="$install_dir/$BIN"

    if have curl; then
        DOWNLOADER=curl
    elif have wget; then
        DOWNLOADER=wget
    else
        die "need curl or wget to download the release"
    fi
    if have sha256sum; then
        HASHER=sha256sum
    elif have shasum; then
        HASHER=shasum
    else
        die "need sha256sum or shasum to verify the download; refusing to install unverified"
    fi

    if [ -d "$dest" ]; then
        die "$dest is a directory; choose another --prefix"
    fi
    if [ -e "$install_dir" ] && [ ! -d "$install_dir" ]; then
        die "$install_dir exists and is not a directory"
    fi
    if [ -d "$install_dir" ] && [ ! -w "$install_dir" ]; then
        die "$install_dir is not writable by $(id -un). This installer never uses sudo; pass --prefix DIR for a directory you own."
    fi

    old_version=""
    if [ -f "$dest" ]; then
        old_version="$(version_of "$dest" || true)"
        [ -n "$old_version" ] || old_version="an existing file that does not report a version"
    fi

    claude_dir="${CLAUDE_CONFIG_DIR:-${HOME:-}/.claude}"
    claude_path="$(command -v claude 2>/dev/null || true)"
    tty=no
    if have_tty; then
        tty=yes
    fi
    # What the plugin step will do: run, ask, or skip (with the reason).
    if [ "$plugin" = no ]; then
        plugin_action=skip; plugin_why="--no-plugin was given"
    elif [ -z "$claude_path" ]; then
        plugin_action=skip; plugin_why="the claude CLI is not on PATH"
    elif [ "$plugin" = yes ]; then
        plugin_action=run; plugin_why="--plugin was given"
    elif [ "$assume_yes" = yes ]; then
        plugin_action=skip; plugin_why="--yes installs the binary only; add --plugin to include it"
    elif [ "$tty" = yes ]; then
        plugin_action=ask; plugin_why=""
    else
        plugin_action=skip; plugin_why="there is no terminal to ask on, and it is not run unasked"
    fi

    url_bin="$base/v$version/$ASSET"
    url_sum="$url_bin.sha256"

    # ---- The plan --------------------------------------------------------

    say "Writfold installer"
    say ""
    say "Plan"
    row "version" "$version ($version_note)"
    row "platform" "$platform"
    row "download" "$url_bin"
    row "" "$url_sum"
    row "" "with $DOWNLOADER, into a fresh temporary directory under ${TMPDIR:-/tmp}"
    row "" "(removed when the installer exits)"
    case "$base" in
        https://github.com/*) row "" "GitHub redirects these to its release-asset host; HTTPS only" ;;
        https://*) row "" "note: download base set by WRITFOLD_DOWNLOAD_BASE" ;;
        *) row "" "note: download base set by WRITFOLD_DOWNLOAD_BASE, and it is not HTTPS" ;;
    esac
    row "verify" "SHA-256 of the binary against the release's .sha256 file ($HASHER)"
    if [ -n "$pinned_sha" ]; then
        row "" "and against the checksum pinned in this installer:"
        row "" "$pinned_sha"
    fi
    row "" "nothing is installed unless it matches"
    row "install" "$dest (mode 755)"
    if [ -n "$old_version" ]; then
        row "" "replaces: $old_version"
    else
        row "" "new file; nothing is there now"
    fi
    if [ ! -d "$install_dir" ]; then
        row "" "creates the directory $install_dir"
    fi
    row "" "written as $install_dir/.writfold-install.* first, then renamed into place"
    case "$plugin_action" in
        run) row "plugin" "will run, because $plugin_why:" ;;
        ask) row "plugin" "will ask you first (default: no). If you say yes, runs:" ;;
        skip) row "plugin" "skipped, because $plugin_why. The commands, for later:" ;;
    esac
    row "" "$MARKETPLACE_CMD"
    row "" "$PLUGIN_CMD"
    row "" "these make Claude Code write its marketplace and plugin records under"
    row "" "$claude_dir; this installer writes nothing there itself"
    row "untouched" "shell startup files, PATH, and every path not listed above. No sudo."
    say ""

    if [ "$dry_run" = yes ]; then
        say "Dry run: nothing was downloaded and nothing was written."
        exit 0
    fi

    if [ "$assume_yes" = no ] && [ "$tty" = yes ]; then
        if ! ask "Proceed with the download and install? [Y/n]" y; then
            say "Stopped. Nothing was downloaded and nothing was written."
            exit 1
        fi
        say ""
    fi

    # ---- 1. Download -----------------------------------------------------

    trap cleanup EXIT
    trap 'exit 130' INT
    trap 'exit 143' HUP TERM
    TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/writfold-install.XXXXXX")" \
        || die "could not create a temporary directory"

    say "[1/4] Downloading into $TMP_DIR"
    detail "$url_sum"
    fetch "$url_sum" "$TMP_DIR/$ASSET.sha256" \
        || die "could not download $url_sum (is $version a published release?). Nothing was installed."
    detail "$url_bin"
    fetch "$url_bin" "$TMP_DIR/$ASSET" \
        || die "could not download $url_bin. Nothing was installed."
    [ -s "$TMP_DIR/$ASSET" ] || die "the downloaded binary is empty. Nothing was installed."
    detail "received $(wc -c <"$TMP_DIR/$ASSET" | tr -d ' ') bytes"

    # ---- 2. Verify -------------------------------------------------------

    say "[2/4] Verifying SHA-256 before anything is installed"
    expected="$(awk 'NR == 1 { print $1 }' "$TMP_DIR/$ASSET.sha256" | tr 'A-F' 'a-f')"
    is_sha256 "$expected" \
        || die "the .sha256 file does not start with a SHA-256 checksum. Nothing was installed."
    actual="$(sha256_of "$TMP_DIR/$ASSET")"
    is_sha256 "$actual" || die "could not compute the SHA-256 of the download. Nothing was installed."
    detail "release .sha256  $expected"
    detail "downloaded file  $actual"
    [ "$actual" = "$expected" ] \
        || die "checksum mismatch: the binary is not the one the release's .sha256 file describes. Nothing was installed."
    if [ -n "$pinned_sha" ]; then
        detail "installer's pin  $pinned_sha"
        [ "$actual" = "$pinned_sha" ] \
            || die "checksum mismatch: the binary is not the one this installer pins for $version. Nothing was installed."
    fi
    detail "match"

    # ---- 3. Install ------------------------------------------------------

    say "[3/4] Installing $dest"
    if [ -f "$dest" ] && [ "$(sha256_of "$dest")" = "$actual" ]; then
        detail "the file already there is identical (same SHA-256); left as it is"
        new_version="$(version_of "$dest" || true)"
    else
        if [ ! -d "$install_dir" ]; then
            detail "creating $install_dir"
            mkdir -p "$install_dir" || die "could not create $install_dir. Nothing was installed."
        fi
        STAGED="$(mktemp "$install_dir/.writfold-install.XXXXXX")" \
            || die "could not write in $install_dir. Nothing was installed."
        detail "writing $STAGED"
        cat "$TMP_DIR/$ASSET" >"$STAGED" || die "could not write $STAGED. Nothing was installed."
        chmod 755 "$STAGED"
        [ "$(sha256_of "$STAGED")" = "$actual" ] \
            || die "the copy in $install_dir does not match the verified download. Nothing was installed."
        new_version="$(version_of "$STAGED" || true)"
        [ -n "$new_version" ] \
            || die "the verified binary does not run here ($STAGED --version failed). $dest was left as it was."
        detail "it runs and reports: $new_version"
        detail "renaming it to $dest"
        mv -f "$STAGED" "$dest" || die "could not rename into $dest; it was left as it was."
        STAGED=""
    fi
    if [ -z "$old_version" ]; then
        detail "installed: $new_version"
    elif [ "$old_version" = "$new_version" ]; then
        detail "installed: $new_version (same version as before)"
    else
        detail "installed: $old_version -> $new_version"
    fi
    case "$new_version" in
        *"$version"*) ;;
        *) warn "asked for $version, but $dest --version reports '$new_version'" ;;
    esac

    # ---- 4. Claude Code plugin -------------------------------------------

    say "[4/4] Claude Code plugin"
    plugin_failed=no
    if [ "$plugin_action" = ask ]; then
        detail "This would run, with $claude_path:"
        print_plugin_commands
        detail "Claude Code then writes its marketplace and plugin records under $claude_dir."
        if ask "      Run these two commands now? [y/N]" n; then
            plugin_action=run
        else
            plugin_action=skip; plugin_why="you answered no"
        fi
    fi
    if [ "$plugin_action" = run ]; then
        detail "running: $MARKETPLACE_CMD"
        detail "(Claude Code writes under $claude_dir)"
        # Both arguments are fixed strings; nothing downloaded is passed on.
        if ! claude plugin marketplace add writfold-dev/writfold </dev/null; then
            warn "that command failed (it can, when the marketplace was added before); trying the next one anyway"
        fi
        detail "running: $PLUGIN_CMD"
        if claude plugin install writfold@writfold </dev/null; then
            detail "plugin step finished"
        else
            plugin_failed=yes
            warn "the plugin was not installed. The binary is installed; run these yourself to see the error:"
            print_plugin_commands >&2
        fi
    else
        detail "skipped, because $plugin_why."
        detail "Nothing was written under $claude_dir. To add the plugin later, run:"
        print_plugin_commands
        if [ "$plugin" = ask ] && [ -n "$claude_path" ] && [ "$plugin_why" != "you answered no" ]; then
            detail "or re-run this installer with --plugin:"
            detail "curl -fsSL https://writfold.dev/install.sh | sh -s -- --plugin"
        fi
    fi

    # ---- Summary ---------------------------------------------------------

    say ""
    say "Done. $new_version is at $dest"
    case ":${PATH:-}:" in
        *":$install_dir:"*)
            on_path="$(command -v "$BIN" 2>/dev/null || true)"
            if [ -n "$on_path" ] && [ "$on_path" != "$dest" ]; then
                say "Note: another $BIN comes first on your PATH: $on_path"
            fi
            ;;
        *)
            say "Note: $install_dir is not on your PATH, and this installer does not edit"
            say "shell startup files. To use it in this shell:"
            say "    export PATH=\"$install_dir:\$PATH\""
            say "Add that line to your shell's startup file yourself to keep it"
            say "(fish: fish_add_path $install_dir)."
            ;;
    esac
    if [ "$plugin_failed" = yes ]; then
        exit 1
    fi
}

{ main "$@"; }
