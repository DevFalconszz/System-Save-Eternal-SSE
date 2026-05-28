import os
import glob
import platform
from typing import List


def search_files(root_dirs: List[str], patterns: List[str], max_depth: int = 10) -> List[str]:
    results = []
    for root in root_dirs:
        if not os.path.exists(root):
            continue
        for pattern in patterns:
            full_pattern = os.path.join(root, pattern)
            matches = glob.glob(full_pattern, recursive=True)
            for match in matches:
                rel_depth = match[len(root):].count(os.sep)
                if rel_depth <= max_depth:
                    results.append(match)
    return sorted(set(results))


def search_saves_by_name(name_hints: List[str]) -> List[str]:
    candidates = []

    if platform.system().lower() == "windows":
        search_roots = []
        for var in ["USERPROFILE", "SYSTEMDRIVE", "HOMEDRIVE"]:
            val = os.environ.get(var, "")
            if val and os.path.exists(val):
                search_roots.append(val)
        search_roots.extend(["C:/Users", "D:/", "E:/"])
    else:
        search_roots = ["/home", "/mnt", "/media"]

    for root in search_roots:
        if not os.path.exists(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                name_lower = f.lower()
                if any(hint in name_lower for hint in name_hints):
                    candidates.append(os.path.join(dirpath, f))
    return candidates


def get_dir_size(path: str) -> int:
    total = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def human_size(bytes_val: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"
