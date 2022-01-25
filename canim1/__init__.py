import argparse
from pathlib import Path

from tomlkit import parse


parser = argparse.ArgumentParser()
parser.add_argument("pyversion")
parser.add_argument("path")


def main():
    args = parser.parse_args()
    lockfiles = Path(args.path).rglob("poetry.lock")
    print(f"\nthe following packages do not have wheels available for Apple Silicon on {args.pyversion}")
    for l in lockfiles:
        print(f"\n# {l}\n")
        any = False
        lock_data = parse(l.read_text())
        for package, files in lock_data["metadata"]["files"].items():
            for f in files:
                if args.pyversion in f["file"] or "py3" in f["file"]:
                    if "macosx" in f["file"]:
                        if "arm64" in f["file"] or "universal2" in f["file"]:
                            break
                    elif "-none-any" in f["file"]:
                        break
            else:
                any = True
                package_version = [p for p in lock_data["package"] if p["name"] == package][0]["version"]
                print(f"- {package} {package_version}")
        if not any:
            print("(none)")
