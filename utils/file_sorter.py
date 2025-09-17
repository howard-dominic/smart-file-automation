# helper utilities (safe_move)
import os, shutil

def safe_move(src, dst_folder, rename_on_conflict=True):
    os.makedirs(dst_folder, exist_ok=True)
    basename = os.path.basename(src)
    dst = os.path.join(dst_folder, basename)
    if not os.path.exists(dst):
        shutil.move(src, dst)
        return dst
    if not rename_on_conflict:
        os.remove(dst)
        shutil.move(src, dst)
        return dst
    base, ext = os.path.splitext(basename)
    counter = 1
    while True:
        candidate = f"{base}_{counter}{ext}"
        dst_candidate = os.path.join(dst_folder, candidate)
        if not os.path.exists(dst_candidate):
            shutil.move(src, dst_candidate)
            return dst_candidate
        counter += 1
