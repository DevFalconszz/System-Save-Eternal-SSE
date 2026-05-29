import os
import platform
import sys


class PlatformInfo:
    _system = platform.system().lower()

    @classmethod
    def is_linux(cls) -> bool:
        return cls._system == "linux"

    @classmethod
    def is_windows(cls) -> bool:
        return cls._system == "windows"

    @classmethod
    def is_macos(cls) -> bool:
        return cls._system == "darwin"

    @classmethod
    def is_termux(cls) -> bool:
        return cls.is_linux() and "com.termux" in (os.environ.get("PREFIX", ""))

    @classmethod
    def name(cls) -> str:
        if cls.is_windows():
            return "windows"
        if cls.is_termux():
            return "android"
        if cls.is_linux():
            return "linux"
        if cls.is_macos():
            return "macos"
        return cls._system

    @classmethod
    def icon(cls) -> str:
        icons = {
            "linux": "\U0001F427",
            "windows": "\U0001FA9F",
            "android": "\U0001F4F1",
            "macos": "\U0001F5A5",
        }
        return icons.get(cls.name(), "\U0001F310")

    @classmethod
    def home(cls) -> str:
        return os.path.expanduser("~")

    @classmethod
    def config_dir(cls) -> str:
        if cls.is_windows():
            return os.path.join(os.environ.get("APPDATA", cls.home()), "sse")
        return os.path.join(cls.home(), ".config", "sse")

    @classmethod
    def data_dir(cls) -> str:
        if cls.is_windows():
            return os.path.join(os.environ.get("LOCALAPPDATA", cls.home()), "sse")
        return os.path.join(cls.home(), ".local", "share", "sse")

    @classmethod
    def separator(cls) -> str:
        return os.sep

    @classmethod
    def python_path(cls) -> str:
        return sys.executable

    @classmethod
    def is_executable_build(cls) -> bool:
        return getattr(sys, "frozen", False)


def ensure_dirs():
    from src.utils.config import ensure_config_dir
    ensure_config_dir()
    os.makedirs(PlatformInfo.data_dir(), exist_ok=True)
