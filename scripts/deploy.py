#!/usr/bin/env python3
"""Mirror the .py code files in this repo's src/ into The Farmer Was Replaced's Save0.

Run as ethan (dev can't read/write the Steam compatdata tree).
- Files in src/ overwrite their copies in the save dir.
- The save's .py files must match src/ exactly (ignoring the game-generated
  __builtins__.py), otherwise the deploy aborts before anything is changed:
  - in src/ but not the save: create them in game first.
  - in the save but not src/ (removed from the repo): delete them in game first.
  The game doesn't cope with files being added or removed behind its back.
Non-code files (save.json etc.) are never touched.
"""
import shutil
import sys
from pathlib import Path

REPO_SRC = Path(__file__).resolve().parent.parent / "src"
SAVE_DIR = Path(
	"/home/ethan/.steam/debian-installation/steamapps/compatdata/2060160/pfx/drive_c/"
	"users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Save0"
)
# Game-owned files that may exist in the save without being in src/.
IGNORED_IN_SAVE = {Path("__builtins__.py")}


def code_files(root: Path) -> set[Path]:
	return {p.relative_to(root) for p in root.rglob("*.py") if p.is_file()}


def main() -> int:
	if not REPO_SRC.is_dir():
		print(f"missing source dir: {REPO_SRC}", file=sys.stderr)
		return 1
	if not SAVE_DIR.is_dir():
		print(f"missing save dir: {SAVE_DIR}", file=sys.stderr)
		return 1
	# Code only: save.json and other game state never get deployed.
	files = sorted(code_files(REPO_SRC))
	save_files = code_files(SAVE_DIR)
	missing = [rel for rel in files if rel not in save_files]
	removed = sorted(save_files - set(files) - IGNORED_IN_SAVE)
	if missing:
		print("These files don't exist in the save yet:", file=sys.stderr)
		for rel in missing:
			print(f"  {rel}", file=sys.stderr)
		print("Create each one manually in game first (same name).", file=sys.stderr)
	if removed:
		print("These files are in the save but were removed from src/:", file=sys.stderr)
		for rel in removed:
			print(f"  {rel}", file=sys.stderr)
		print("Delete each one manually in game first.", file=sys.stderr)
	if missing or removed:
		print("Then save the game and re-run deploy.", file=sys.stderr)
		return 1
	for rel in files:
		shutil.copy2(REPO_SRC / rel, SAVE_DIR / rel)
	print(f"copied {len(files)} file(s) -> {SAVE_DIR}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
