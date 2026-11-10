#!/usr/bin/env python3
"""Copy the .py code files in this repo's src/ into The Farmer Was Replaced's Save0, overwriting existing files.

Run as ethan (dev can't read/write the Steam compatdata tree).
Files in the save dir that aren't in src/ are left alone. Files in src/ that aren't
in the save dir abort the deploy: create them in game first.
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
	# Code only: save.json and other game state never get deployed.
	files = [p.relative_to(REPO_SRC) for p in REPO_SRC.rglob("*.py") if p.is_file()]
	missing = [rel for rel in files if not (SAVE_DIR / rel).is_file()]
	if missing:
		print("These files don't exist in the save yet:", file=sys.stderr)
		for rel in missing:
			print(f"  {rel}", file=sys.stderr)
		print(
			"Create each one manually in game first (same name), save the game, then re-run deploy.",
			file=sys.stderr,
		)
		return 1
	for rel in files:
		shutil.copy2(REPO_SRC / rel, SAVE_DIR / rel)
	print(f"copied {len(files)} file(s) -> {SAVE_DIR}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
