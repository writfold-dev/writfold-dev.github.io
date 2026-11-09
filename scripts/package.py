#!/usr/bin/env python3
"""Package already-rendered static files; never fetch or render product docs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    ".nojekyll", "404.html", "CNAME", "LICENSE.txt", "index.html", "docs.html",
    "weft.html", "splicery.html", "status.html", "glossary.html",
    "examples/review.weft", "examples/client.rs", "examples/add-retry.spl",
    "assets/favicon.svg", "assets/og-image.png", "assets/site.css", "assets/theme.js",
    "assets/writfold-icon-dark.svg", "assets/writfold-icon.svg",
)
MANIFEST = ROOT / "content-manifest.json"


def digest(path):
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"Not a regular publication file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-manifest", action="store_true",
                        help="Locally approve updated bytes before review and commit")
    parser.add_argument("--output", type=Path, default=ROOT / "_site",
                        help="New artifact directory; existing destinations are never replaced")
    args = parser.parse_args()
    actual = {name: digest(ROOT / name) for name in FILES}
    if args.refresh_manifest:
        manifest = {
            "schema_version": 1,
            "canonical_origin": "https://writfold.dev",
            "product_source_base_commit": "fcf7fcd1471821712e16e5cb2b569bc9b3a597e9",
            "product_source_visibility": "public",
            "architecture_revision": 5,
            "component_evidence": {
                "scope": "Control and local artifact regressions only; not owner data/effect services or alpha readiness",
                "campaign_sha256": "f2f3bec8b7d5954a751a4c1d229c13ec7bbbc6feb4b7b04d881b5af7b19efef2",
                "writfold_binary_sha256": "12fdaad21cb62f0d0371efd73a8febda38d0b13ba58e15c80079bf155502f65c",
            },
            "language_example_evidence": {
                "scope": "Actual local symbolic assessment and read-only preview; no grounding or effect authority",
                "receipt_sha256": "285fd6059365b01958da732a08e7606e041bab8b3c3c7d33ed5aba44f3ba355b",
            },
            "splicery_rust_example_evidence": {
                "scope": "Offline Splicery preview and three refusal runs on the Rust example; no Writfold effect",
                "receipt_sha256": "ddf716c5716559671f1a321125fa1684e5b58e8cf11a4cb9bde78de1c6924b98",
            },
            "files": actual,
        }
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("canonical_origin") != "https://writfold.dev":
        raise SystemExit("Unrecognized publication manifest")
    if manifest.get("files") != actual:
        raise SystemExit("Publication bytes differ from the approved content manifest")
    if (ROOT / "CNAME").read_text(encoding="utf-8") != "writfold.dev\n":
        raise SystemExit("Unexpected custom domain")
    destination = args.output.absolute()
    if destination.exists() or destination.is_symlink():
        raise SystemExit("Artifact directory already exists; select a new --output")
    destination.mkdir()
    for name in FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    shutil.copyfile(MANIFEST, destination / MANIFEST.name)
    print(f"Packaged manifest-matched static files into {destination}/")


if __name__ == "__main__":
    main()
