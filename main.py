#!/usr/bin/env python3
"""
smart-file-automation main CLI
- reads config.yml (fallback to config.example.yml)
- organizes files by extension
- writes sorting_report.csv with original -> new path
- supports --dry-run and --yes
"""
import os
import shutil
import argparse
import csv
import datetime
from pathlib import Path

try:
    import yaml
except Exception:
    print("Missing dependency 'PyYAML'. Install with: pip install pyyaml")
    raise

DEFAULT_CONFIG_FILES = ["config.yml", "config.example.yml"]

def load_config():
    for fname in DEFAULT_CONFIG_FILES:
        if os.path.exists(fname):
            with open(fname, "r") as fh:
                return yaml.safe_load(fh) or {}
    return {}

def safe_move(src, dst_folder, rename_on_conflict=True):
    os.makedirs(dst_folder, exist_ok=True)
    basename = os.path.basename(src)
    dst = os.path.join(dst_folder, basename)
    if not os.path.exists(dst):
        shutil.move(src, dst)
        return dst
    if not rename_on_conflict:
        # overwrite
        os.remove(dst)
        shutil.move(src, dst)
        return dst
    # else rename
    base, ext = os.path.splitext(basename)
    counter = 1
    while True:
        candidate = f"{base}_{counter}{ext}"
        dst_candidate = os.path.join(dst_folder, candidate)
        if not os.path.exists(dst_candidate):
            shutil.move(src, dst_candidate)
            return dst_candidate
        counter += 1

def matches_exclude(path, exclude_patterns):
    from fnmatch import fnmatch
    for pat in exclude_patterns or []:
        if fnmatch(path, pat) or fnmatch(os.path.basename(path), pat):
            return True
    return False

def build_extension_map(mappings):
    ext_map = {}
    for folder, exts in (mappings or {}).items():
        for e in exts:
            ext_map[e.lower()] = folder
    return ext_map

def write_report(report_path, rows):
    header = ["timestamp", "src", "dst", "size_bytes"]
    with open(report_path, "w", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)

def organize(folder, cfg, dry_run=False, yes=False):
    mappings = cfg.get("mappings", {})
    ext_map = build_extension_map(mappings)
    rename_on_conflict = cfg.get("rename_on_conflict", True)
    exclude = cfg.get("exclude_patterns", [])
    report_path = cfg.get("report_path", "sorting_report.csv")

    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        return

    all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    if not all_files:
        print("No files to organize in folder:", folder)
        return

    print(f"Organizing {len(all_files)} files in: {folder}")
    moved = []
    for f in all_files:
        full = os.path.join(folder, f)
        if matches_exclude(full, exclude):
            print("Skipping (excluded):", f)
            continue
        ext = os.path.splitext(f)[1].lower()
        target_folder_name = ext_map.get(ext, "Others")
        target_folder = os.path.join(folder, target_folder_name)
        if dry_run:
            print(f"[dry-run] Would move {f} -> {target_folder_name}/")
            dst = os.path.join(target_folder, f)
        else:
            dst = safe_move(full, target_folder, rename_on_conflict=rename_on_conflict)
            print(f"Moved {f} -> {os.path.relpath(dst)}")
        size = os.path.getsize(dst) if os.path.exists(dst) else 0
        moved.append([datetime.datetime.utcnow().isoformat(), full, dst, size])

    # write report
    if dry_run:
        print("[dry-run] Skipping report write")
    else:
        write_report(report_path, moved)
        print(f"Report generated: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Smart File Automation - configurable file organizer")
    parser.add_argument("folder", nargs="?", default=".", help="folder to organize (default: current folder)")
    parser.add_argument("--config", "-c", help="path to config.yml (optional)")
    parser.add_argument("--dry-run", action="store_true", help="show actions but don't move files")
    parser.add_argument("--yes", "-y", action="store_true", help="answer yes to prompts")
    parser.add_argument("--init-config", action="store_true", help="create a config.yml from example")
    args = parser.parse_args()

    if args.init_config:
        if not os.path.exists("config.example.yml"):
            print("No config.example.yml found to initialize from.")
        else:
            if os.path.exists("config.yml"):
                print("config.yml already exists, not overwriting.")
            else:
                shutil.copy("config.example.yml", "config.yml")
                print("Created config.yml from config.example.yml")
        return

    if args.config:
        cfg_file = args.config
    else:
        # load default config
        cfg_file = None

    cfg = load_config()
    # parse override: use cfg_file if given
    if args.config and os.path.exists(args.config):
        with open(args.config,"r") as fh:
            cfg = yaml.safe_load(fh) or {}

    organize(args.folder, cfg, dry_run=args.dry_run, yes=args.yes)

if __name__ == "__main__":
    main()
