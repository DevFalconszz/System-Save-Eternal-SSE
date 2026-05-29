import tkinter as tk
import threading
import sys, os

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import (
    BG_DARK, CRUST, SURFACE0, SURFACE1,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE, apply_theme
)


class BackupScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        # ── Header ──
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill=tk.X, padx=14, pady=(10, 2))
        tk.Label(hdr, text="Backup de Saves",
                 font=(FONT_FAMILY, 13, "bold"),
                 fg=FG_YELLOW, bg=BG_DARK).pack(side=tk.LEFT)
        tk.Label(hdr, text="selecione o jogo abaixo",
                 font=(FONT_FAMILY, 10),
                 fg=FG_DIM, bg=BG_DARK).pack(side=tk.LEFT, padx=10)

        # ── Terminal ──
        self.terminal = TerminalOutput(self, height=16)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        # ── Progress ──
        prog_frame = tk.Frame(self, bg=BG_DARK)
        prog_frame.pack(fill=tk.X, padx=12, pady=(2, 4))
        tk.Label(prog_frame, text="Progresso:", font=(FONT_FAMILY, 10),
                 fg=FG_CYAN, bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 10))
        self.progress = ProgressBar(prog_frame, width=300, height=14)
        self.progress.pack(side=tk.LEFT)

        # ── Buttons ──
        btn_frame = tk.Frame(self, bg=BG_DARK)
        btn_frame.pack(pady=6)

        for text, game in (("[1]  Minecraft", "minecraft"), ("[2]  Pokemon", "pokemon")):
            btn = tk.Button(btn_frame, text=text, font=(FONT_FAMILY, 11, "bold"),
                            fg=FG_GREEN, bg=SURFACE0,
                            activeforeground=FG_GREEN, activebackground=SURFACE1,
                            relief=tk.FLAT, bd=0, padx=16, pady=6, cursor="hand2",
                            command=lambda g=game: self.start_backup(g))
            btn.pack(side=tk.LEFT, padx=4)

        tk.Button(btn_frame, text="Voltar", font=(FONT_FAMILY, 11, "bold"),
                  fg=TEXT, bg=SURFACE0,
                  activeforeground=TEXT, activebackground=SURFACE1,
                  relief=tk.FLAT, bd=0, padx=16, pady=6, cursor="hand2",
                  command=on_back).pack(side=tk.LEFT, padx=20)

    def start_backup(self, game):
        self.terminal.clear()
        self.progress.set_progress(0)
        self.terminal.write(("Preparando backup...\n", "warn"))
        self.terminal.write((f"Jogo: {game}\n", "info"))

        def run():
            try:
                self._do_backup(game)
            except Exception as e:
                self.terminal.write((f"Erro: {e}\n", "error"))
        threading.Thread(target=run, daemon=True).start()

    def _do_backup(self, game):
        from src.utils import config as cfg
        repo_path = cfg.get("save_repo_path", "")
        if not repo_path:
            self.terminal.write(("ERRO: Caminho do repositorio nao configurado.\n", "error"))
            self.terminal.write(("Va em 'Configurar Destinos' primeiro.\n", "warn"))
            return
        if not os.path.isdir(repo_path):
            self.terminal.write((f"ERRO: Diretorio nao encontrado: {repo_path}\n", "error"))
            return

        self.progress.set_progress(10)

        if game == "minecraft":
            from src.games.minecraft import MinecraftFinder
            finder = MinecraftFinder()
            self.terminal.write(("Buscando saves do Minecraft...\n", "info"))
        else:
            from src.games.pokemon import PokemonFinder
            finder = PokemonFinder(system_wide_search=True)
            self.terminal.write(("Buscando saves de Pokemon...\n", "info"))

        saves = finder.find_saves()
        if not saves:
            self.terminal.write(("Nenhum save encontrado.\n", "error"))
            return

        self.progress.set_progress(30)
        self.terminal.write((f"\n{len(saves)} save(s) encontrado(s):\n", "ok"))
        for s in saves:
            self.terminal.write((f"  [{s.name}]  ({s.game})\n", "dim"))

        self.terminal.write(("\nCopiando saves para o repositorio local...\n", "info"))
        from src.console.menu import sync_to_repo
        if not sync_to_repo(saves, repo_path):
            self.terminal.write(("Falha ao sincronizar saves.\n", "error"))
            return

        self.progress.set_progress(60)

        from src.console.menu import get_timestamp, configure_destination
        timestamp = get_timestamp()

        dests_checks = {
            "github": ("github.repo_url", "github.token"),
            "google_drive": ("google_drive.client_id", "google_drive.client_secret"),
            "telegram": ("telegram.api_id", "telegram.api_hash"),
        }
        configured = [d for d, keys in dests_checks.items() if all(cfg.get(k) for k in keys)]

        if not configured:
            self.terminal.write(("\nNenhum destino configurado.\n", "warn"))
            self.terminal.write(("Configure em 'Configurar Destinos' primeiro.\n", "dim"))
            self.progress.set_progress(100)
            return

        per_dest = 30.0 / len(configured)
        for i, dest_name in enumerate(configured):
            self.terminal.write((f"\n[{dest_name.title()}] Enviando...\n", "warn"))
            self.progress.set_progress(60 + int(i * per_dest))
            configure_destination(dest_name.title())

            saver_map = {
                "github": ("src.savers.github_saver", "GitHubSaver"),
                "google_drive": ("src.savers.googledrive_saver", "GoogleDriveSaver"),
                "telegram": ("src.savers.telegram_saver", "TelegramSaver"),
            }
            mod_path, cls_name = saver_map[dest_name]
            import importlib
            mod = importlib.import_module(mod_path)
            saver = getattr(mod, cls_name)()
            if not saver:
                continue

            all_files = [s.path for s in saves]
            metadata = {
                "repo_path": repo_path, "save_dir": game,
                "game": saves[0].game, "timestamp": timestamp,
            }
            success = saver.save(all_files, metadata)
            if success:
                self.terminal.write((f"OK Backup para {saver.name()} concluido!\n", "ok"))
            else:
                self.terminal.write((f"Falha Backup para {saver.name()} falhou.\n", "error"))

        self.progress.set_progress(100)
        self.terminal.write(("\nProcesso finalizado! Seus saves estao seguros.\n", "ok"))
