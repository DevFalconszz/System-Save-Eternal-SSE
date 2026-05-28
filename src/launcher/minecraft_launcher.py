import os
import platform
import shutil
import stat
import subprocess
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LauncherInfo:
    name: str
    binary_path: str
    game_dir: str
    icon: str = ""


SKLAUNCHER = {
    "name": "SKLauncher",
    "linux_bins": [
        "sklauncher", "SKLauncher",
        os.path.expanduser("~/SKLauncher/SKLauncher"),
        os.path.expanduser("~/sklauncher/SKLauncher"),
        os.path.expanduser("~/SKLauncher/sklauncher"),
        os.path.expanduser("~/SKLauncher/SKLauncher.jar"),
        os.path.expanduser("~/sklauncher/SKLauncher.jar"),
        os.path.expanduser("~/.sklauncher/SKLauncher.jar"),
        "/usr/local/bin/sklauncher",
        "/opt/sklauncher/SKLauncher",
        "/opt/SKLauncher/SKLauncher",
    ],
    "windows_bins": ["SKLauncher.exe", "SKLauncherPortable.exe"],
    "linux_dirs": [
        os.path.expanduser("~/.minecraft"),
        os.path.expanduser("~/.sklauncher/minecraft"),
        os.path.expanduser("~/SKLauncher/minecraft"),
        os.path.expanduser("~/sklauncher/minecraft"),
    ],
    "windows_dirs": [
        os.path.expandvars("%APPDATA%/.minecraft"),
        os.path.expandvars("%USERPROFILE%/SKLauncher/minecraft"),
    ],
}

LAUNCHERS = [
    {
        "name": "Prism Launcher",
        "linux_bins": [
            "prismlauncher", "prism-launcher",
            "/usr/bin/prismlauncher",
            "/usr/local/bin/prismlauncher",
            os.path.expanduser("~/.local/bin/prismlauncher"),
            os.path.expanduser("~/Applications/PrismLauncher/prismlauncher"),
            "/opt/prismlauncher/prismlauncher",
        ],
        "windows_bins": ["PrismLauncher.exe", "prismlauncher.exe"],
        "linux_dirs": [
            os.path.expanduser("~/.local/share/PrismLauncher/instances"),
            os.path.expanduser("~/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances"),
        ],
        "windows_dirs": [],
        "icon": "🔮",
    },
    {
        "name": "MultiMC",
        "linux_bins": [
            "multimc", "MultiMC",
            os.path.expanduser("~/MultiMC/MultiMC"),
            "/opt/multimc/MultiMC",
        ],
        "windows_bins": ["MultiMC.exe", "multimc.exe"],
        "linux_dirs": [
            os.path.expanduser("~/.local/share/multimc/instances"),
            os.path.expanduser("~/MultiMC/instances"),
        ],
        "windows_dirs": [],
        "icon": "📦",
    },
    {
        "name": "Minecraft Launcher",
        "linux_bins": [
            "minecraft-launcher",
            "/usr/bin/minecraft-launcher",
            "/snap/bin/minecraft-launcher",
            "/usr/share/minecraft/minecraft-launcher",
        ],
        "windows_bins": ["MinecraftLauncher.exe", "Minecraft.exe"],
        "linux_dirs": [os.path.expanduser("~/.minecraft")],
        "windows_dirs": [],
        "icon": "🟢",
    },
    {
        "name": "ATLauncher",
        "linux_bins": [
            "ATLauncher", "atlauncher",
            os.path.expanduser("~/ATLauncher/ATLauncher"),
            "/opt/atlauncher/ATLauncher",
        ],
        "windows_bins": ["ATLauncher.exe", "atlauncher.exe"],
        "linux_dirs": [
            os.path.expanduser("~/.atlauncher"),
            os.path.expanduser("~/.local/share/atlauncher"),
        ],
        "windows_dirs": [],
        "icon": "🔧",
    },
    {
        "name": "GDLauncher",
        "linux_bins": [
            "gdlauncher", "gdlauncher-appimage", "GDLauncher",
            os.path.expanduser("~/.local/bin/gdlauncher"),
        ],
        "windows_bins": ["GDLauncher.exe", "gdlauncher.exe"],
        "linux_dirs": [
            os.path.expanduser("~/.gdlauncher"),
            os.path.expanduser("~/.config/GDLauncher"),
        ],
        "windows_dirs": [],
        "icon": "💎",
    },
    {
        "name": "CurseForge",
        "linux_bins": [
            "curseforge", "CurseForge",
            os.path.expanduser("~/CurseForge/CurseForge"),
            "/opt/curseforge/CurseForge",
        ],
        "windows_bins": ["CurseForge.exe", "curseforge.exe"],
        "linux_dirs": [
            os.path.expanduser("~/.curseforge/minecraft"),
            os.path.expanduser("~/CurseForge/minecraft"),
        ],
        "windows_dirs": [],
        "icon": "🔥",
    },
]


def detect_launchers() -> List[LauncherInfo]:
    system = platform.system().lower()
    all_candidates = [SKLAUNCHER] + LAUNCHERS
    found = []

    for candidate in all_candidates:
        bins_key = f"{system}_bins" if system in ("linux", "windows") else "linux_bins"
        dirs_key = f"{system}_dirs" if system in ("linux", "windows") else "linux_dirs"
        bins = candidate.get(bins_key, [])
        game_dirs = candidate.get(dirs_key, [])

        binary_path = None
        for b in bins:
            if b.startswith("/") or b.startswith("~"):
                expanded = os.path.expanduser(b)
                if os.path.isfile(expanded):
                    binary_path = expanded
                    break
            else:
                resolved = shutil.which(b)
                if resolved:
                    binary_path = resolved
                    break

        if not binary_path:
            continue

        game_dir = None
        for gd in game_dirs:
            expanded = os.path.expandvars(os.path.expanduser(gd))
            if os.path.isdir(expanded):
                game_dir = expanded
                break

        found.append(LauncherInfo(
            name=candidate["name"],
            binary_path=binary_path,
            game_dir=game_dir or "",
            icon=candidate.get("icon", ""),
        ))

    return found


def find_instance_dirs(launcher: LauncherInfo) -> List[str]:
    instances = []
    if not launcher.game_dir:
        return instances

    if launcher.name in ("Prism Launcher", "MultiMC"):
        if os.path.isdir(launcher.game_dir):
            for entry in os.listdir(launcher.game_dir):
                inst_path = os.path.join(launcher.game_dir, entry)
                if os.path.isdir(inst_path):
                    mc_dir = os.path.join(inst_path, ".minecraft")
                    saves_dir = os.path.join(mc_dir if os.path.isdir(mc_dir) else inst_path, "saves")
                    if os.path.isdir(saves_dir):
                        instances.append(saves_dir)
        return instances

    saves_dir = os.path.join(launcher.game_dir, "saves")
    if os.path.isdir(saves_dir):
        instances.append(saves_dir)

    return instances


def launch_and_monitor(
    launcher: LauncherInfo,
    pre_launch_callback=None,
    post_exit_callback=None,
) -> bool:
    system = platform.system().lower()
    binary = launcher.binary_path

    if not os.path.isfile(binary) and not shutil.which(binary):
        print(f"  [{launcher.icon}] Binário não encontrado: {binary}")
        return False

    print(f"  [{launcher.icon}] Iniciando {launcher.name}...")

    if pre_launch_callback:
        pre_launch_callback()

    try:
        env = os.environ.copy()
        extra_kwargs = {}

        if system == "windows":
            extra_kwargs["creationflags"] = 0x08000000
        else:
            extra_kwargs["start_new_session"] = True

        proc = subprocess.Popen(
            [binary],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            **extra_kwargs,
        )

        print(f"  [{launcher.icon}] Processo iniciado (PID: {proc.pid})")
        print(f"  [{launcher.icon}] Aguardando o jogo fechar...")
        print(f"  [{launcher.icon}] Pressione Ctrl+C para interromper a espera.")

        try:
            proc.wait()
            print(f"  [{launcher.icon}] Processo encerrado (código: {proc.returncode})")
        except KeyboardInterrupt:
            print(f"\n  [{launcher.icon}] Monitoramento interrompido pelo usuário.")
            if proc.poll() is None:
                print(f"  [{launcher.icon}] O jogo ainda está rodando. Os saves serão sincronizados mesmo assim.")

        if post_exit_callback:
            post_exit_callback()

        return True

    except FileNotFoundError:
        print(f"  [{launcher.icon}] Erro: Binário não encontrado: {binary}")
        return False
    except Exception as e:
        print(f"  [{launcher.icon}] Erro ao executar: {e}")
        return False
