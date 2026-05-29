import os
import platform
from typing import List

from src.games.base import GameFinder, SaveEntry


EMULATOR_PATTERNS = {
    "desmume": {
        "linux": ["~/.config/desmume", "~/.desmume"],
        "windows": ["%APPDATA%/DeSmuME", "%USERPROFILE%/.config/desmume"],
        "extensions": [".dsv", ".sav"],
    },
    "melonds": {
        "linux": ["~/.local/share/melonDS", "~/.config/melonDS"],
        "windows": ["%APPDATA%/melonDS", "%USERPROFILE%/AppData/Local/melonDS"],
        "extensions": [".sav", ".dsv"],
    },
    "retroarch": {
        "linux": ["~/.config/retroarch/saves", "~/.local/share/retroarch/saves"],
        "windows": ["%APPDATA%/RetroArch/saves", "%USERPROFILE%/RetroArch/saves"],
        "extensions": [".sav", ".dsv", ".state"],
    },
    "nogba": {
        "linux": [],
        "windows": ["%USERPROFILE%/.no$gba"],
        "extensions": [".sav"],
    },
    "mgba": {
        "linux": ["~/.config/mgba", "~/.local/share/mgba"],
        "windows": ["%APPDATA%/mgba"],
        "extensions": [".sav"],
    }
}


class PokemonFinder(GameFinder):
    def __init__(self, system_wide_search: bool = True):
        self.system_wide_search = system_wide_search
        self._system = platform.system().lower()

    def name(self) -> str:
        return "Pokémon"

    def find_saves(self) -> List[SaveEntry]:
        saves = []

        for emulator, cfg in EMULATOR_PATTERNS.items():
            dirs = cfg.get(self._system, []) if self._system in ("linux", "windows") else cfg.get("linux", [])
            for dir_template in dirs:
                emu_dir = self._resolve_path(dir_template)
                if not emu_dir or not os.path.isdir(emu_dir):
                    continue
                for fname in os.listdir(emu_dir):
                    fpath = os.path.join(emu_dir, fname)
                    if not os.path.isfile(fpath):
                        continue
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in cfg["extensions"] and self._is_pokemon_save(fname):
                        saves.append(SaveEntry(
                            name=fname,
                            path=fpath,
                            game=self._detect_pokemon_game(fname),
                            platform=f"DS ({emulator})",
                            size_bytes=os.path.getsize(fpath),
                            files=[fpath]
                        ))

        if self.system_wide_search:
            saves.extend(self._system_wide_search())

        saves.sort(key=lambda s: s.name)
        return saves

    def _system_wide_search(self) -> List[SaveEntry]:
        results = []

        if self._system == "windows":
            search_roots = []
            for var in ["USERPROFILE", "HOMEDRIVE", "HOMEPATH", "SYSTEMDRIVE"]:
                val = os.environ.get(var, "")
                if val and os.path.exists(val):
                    search_roots.append(val)
            search_roots.extend(["C:/Users", "D:/", "E:/"])
        else:
            search_roots = ["/home", "/mnt", "/media"]

        for root in search_roots:
            if not os.path.exists(root):
                continue
            try:
                for dirpath, _, filenames in os.walk(root):
                    for fname in filenames:
                        if self._is_pokemon_save(fname) and self._is_save_ext(fname):
                            fpath = os.path.join(dirpath, fname)
                            results.append(SaveEntry(
                                name=fname,
                                path=fpath,
                                game=self._detect_pokemon_game(fname),
                                platform="Unknown (system scan)",
                                size_bytes=os.path.getsize(fpath),
                                files=[fpath]
                            ))
            except PermissionError:
                continue

        return results

    @staticmethod
    def _resolve_path(path_template: str) -> str:
        env_map = {
            "%APPDATA%": os.environ.get("APPDATA", ""),
            "%USERPROFILE%": os.environ.get("USERPROFILE", os.path.expanduser("~")),
            "%HOMEDRIVE%": os.environ.get("HOMEDRIVE", "C:"),
            "%HOMEPATH%": os.environ.get("HOMEPATH", "\\Users\\Default"),
            "%LOCALAPPDATA%": os.environ.get("LOCALAPPDATA", ""),
        }
        result = path_template
        for key, val in env_map.items():
            if val:
                result = result.replace(key, val)
        result = os.path.normpath(os.path.expanduser(result))
        return result if os.path.isdir(os.path.dirname(result)) else ""

    @staticmethod
    def _is_pokemon_save(fname: str) -> bool:
        name = fname.lower()
        hints = ["pokemon", "pokémon", "pkmn", "black", "white",
                 "platinum", "heartgold", "soulsilver", "emerald",
                 "ruby", "sapphire", "fire red", "leaf green",
                 "diamond", "pearl", "nintendo ds"]
        return any(hint in name for hint in hints)

    @staticmethod
    def _is_save_ext(fname: str) -> bool:
        ext = os.path.splitext(fname)[1].lower()
        return ext in [".dsv", ".sav", ".dst", ".ms0", ".state"]

    @staticmethod
    def _detect_pokemon_game(fname: str) -> str:
        name = fname.lower()
        if "black" in name and "white" not in name:
            return "Pokémon Black"
        if "white" in name and "black" not in name:
            return "Pokémon White"
        if "black" in name and "white" in name:
            return "Pokémon Black & White"
        if "platinum" in name:
            return "Pokémon Platinum"
        if "heartgold" in name:
            return "Pokémon HeartGold"
        if "soulsilver" in name:
            return "Pokémon SoulSilver"
        if "emerald" in name:
            return "Pokémon Emerald"
        if "fire" in name and "red" in name:
            return "Pokémon Fire Red"
        if "leaf" in name and "green" in name:
            return "Pokémon Leaf Green"
        if "diamond" in name:
            return "Pokémon Diamond"
        if "pearl" in name:
            return "Pokémon Pearl"
        if "ruby" in name and "sapphire" not in name:
            return "Pokémon Ruby"
        if "sapphire" in name:
            return "Pokémon Sapphire"
        if "pokemon" in name or "pokémon" in name or "pkmn" in name:
            return "Pokémon (unidentified)"
        return "Pokémon (unidentified)"
