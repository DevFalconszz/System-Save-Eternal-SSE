import os
import platform
from typing import List

from src.games.base import GameFinder, SaveEntry


class MinecraftFinder(GameFinder):
    def name(self) -> str:
        return "Minecraft"

    def find_saves(self) -> List[SaveEntry]:
        saves = []
        candidates = self._get_save_dirs()

        for mc_dir in candidates:
            saves_dir = os.path.join(mc_dir, "saves")
            if not os.path.isdir(saves_dir):
                continue
            for entry in sorted(os.listdir(saves_dir)):
                world_path = os.path.join(saves_dir, entry)
                if not os.path.isdir(world_path):
                    continue
                level_dat = os.path.join(world_path, "level.dat")
                if not os.path.isfile(level_dat):
                    continue

                saves.append(SaveEntry(
                    name=entry,
                    path=world_path,
                    game="Minecraft",
                    platform="PC",
                    size_bytes=self._get_world_size(world_path),
                    files=[level_dat]
                ))
        return saves

    def _get_save_dirs(self) -> List[str]:
        dirs = []
        system = platform.system().lower()

        if system == "windows":
            return self._get_save_dirs_windows()
        return self._get_save_dirs_linux()

    def _get_save_dirs_linux(self) -> List[str]:
        dirs = []
        home = os.path.expanduser("~")

        candidates = [
            os.path.join(home, ".minecraft"),
            os.path.join(home, ".local", "share", "minecraft"),
            os.path.join(home, "snap", "minecraft", "common", ".minecraft"),
        ]

        xdg_data = os.environ.get("XDG_DATA_HOME", os.path.join(home, ".local", "share"))
        candidates.append(os.path.join(xdg_data, "minecraft"))

        game_dir = os.environ.get("GAME_DIR")
        if game_dir:
            candidates.append(game_dir)

        for d in candidates:
            if os.path.isdir(d):
                dirs.append(d)

        return dirs

    def _get_save_dirs_windows(self) -> List[str]:
        dirs = []
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            dirs.append(os.path.join(appdata, ".minecraft"))

        home = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        candidates = [
            os.path.join(home, ".minecraft"),
            os.path.join(home, "AppData", "Roaming", ".minecraft"),
        ]
        for d in candidates:
            if os.path.isdir(d):
                dirs.append(d)

        game_dir = os.environ.get("GAME_DIR")
        if game_dir:
            dirs.append(game_dir)

        return list(set(dirs))

    @staticmethod
    def _get_world_size(world_path: str) -> int:
        total = 0
        for dirpath, _, filenames in os.walk(world_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
        return total
