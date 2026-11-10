#!/usr/bin/env python3
"""Copy this repo's src/ into The Farmer Was Replaced's Save0, overwriting existing files.

Run as ethan (dev can't read/write the Steam compatdata tree).
Files in the save dir that aren't in src/ are left alone.
"""
import shutil
import sys
from pathlib import Path

REPO_SRC = Path(__file__).resolve().parent.parent / "src"
SAVE_DIR = Path(
    "/home/ethan/.steam/debian-installation/steamapps/compatdata/2060160/pfx/drive_c/"
    "users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Save0"
)


def main() -> int:
    if not REPO_SRC.is_dir():
        print(f"missing source dir: {REPO_SRC}", file=sys.stderr)
        return 1
    if not SAVE_DIR.is_dir():
        print(f"missing save dir: {SAVE_DIR}", file=sys.stderr)
        return 1
    count = 0
    for src in REPO_SRC.rglob("*"):
        if src.is_file():
            dst = SAVE_DIR / src.relative_to(REPO_SRC)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            count += 1
    print(f"copied {count} file(s) -> {SAVE_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
