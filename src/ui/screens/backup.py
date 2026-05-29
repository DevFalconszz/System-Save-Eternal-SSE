import tkinter as tk
import threading
import sys
import os

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import BG_DARK, FG_YELLOW, FG_CYAN, FG_GREEN, apply_theme

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))


class BackupScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        header = tk.Label(self, text="Backup de Saves",
                          font=("Courier", 14, "bold"),
                          fg=FG_YELLOW, bg=BG_DARK)
        header.pack(pady=(10, 5))

        self.terminal = TerminalOutput(self, height=18)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        progress_frame = tk.Frame(self, bg=BG_DARK)
        progress_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        tk.Label(progress_frame, text="Progresso:",
                 font=("Courier", 10), fg=FG_CYAN,
                 bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 10))
        self.progress = ProgressBar(progress_frame, width=300, height=18)
        self.progress.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self, bg=BG_DARK)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="[1] Minecraft",
                  command=lambda: self.start_backup("minecraft"),
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="[2] Pokémon",
                  command=lambda: self.start_backup("pokemon"),
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Voltar", command=on_back,
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=20)

    def start_backup(self, game):
        self.terminal.clear()
        self.progress.set_progress(0)
        self.terminal.write(("Iniciando backup...\n", "warn"))
        self.terminal.write((f"Jogo: {game}\n", "info"))

        def run():
            try:
                self._do_backup(game)
            except Exception as e:
                self.terminal.write((f"Erro: {e}\n", "error"))

        threading.Thread(target=run, daemon=True).start()

    def _do_backup(self, game):
        self.terminal.write(("Verificando configurações...\n", "info"))

        from src.utils import config as cfg
        repo_path = cfg.get("save_repo_path", "")
        if not repo_path:
            self.terminal.write(("ERRO: Caminho do repositório não configurado.\n", "error"))
            self.terminal.write(("Volte e configure em 'Configurar Destinos'.\n", "warn"))
            return

        if not os.path.isdir(repo_path):
            self.terminal.write((f"ERRO: Diretório não encontrado: {repo_path}\n", "error"))
            return

        self.progress.set_progress(10)

        if game == "minecraft":
            from src.games.minecraft import MinecraftFinder
            finder = MinecraftFinder()
            self.terminal.write(("Buscando saves do Minecraft...\n", "info"))
        else:
            from src.games.pokemon import PokemonFinder
            finder = PokemonFinder(system_wide_search=True)
            self.terminal.write(("Buscando saves de Pokémon...\n", "info"))

        saves = finder.find_saves()
        if not saves:
            self.terminal.write(("Nenhum save encontrado para este jogo.\n", "error"))
            return

        self.progress.set_progress(30)
        self.terminal.write((f"\n{len(saves)} save(s) encontrado(s):\n", "ok"))
        for s in saves:
            self.terminal.write((f"  [{s.name}]  ({s.game})\n", "dim"))

        self.terminal.write(("\nCopiando saves para o repositório local...\n", "info"))
        from src.console.menu import sync_to_repo
        if not sync_to_repo(saves, repo_path):
            self.terminal.write(("Falha ao sincronizar saves.\n", "error"))
            return

        self.progress.set_progress(60)

        from src.console.menu import get_timestamp, configure_destination
        timestamp = get_timestamp()

        dests = ["github", "google_drive", "telegram"]
        configured = []
        for d in dests:
            key_map = {
                "github": ("github.repo_url", "github.token"),
                "google_drive": ("google_drive.client_id", "google_drive.client_secret"),
                "telegram": ("telegram.api_id", "telegram.api_hash"),
            }
            keys = key_map[d]
            if all(cfg.get(k) for k in keys):
                configured.append(d)

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

            saver = None
            if dest_name == "github":
                from src.savers.github_saver import GitHubSaver
                saver = GitHubSaver()
            elif dest_name == "google_drive":
                from src.savers.googledrive_saver import GoogleDriveSaver
                saver = GoogleDriveSaver()
            elif dest_name == "telegram":
                from src.savers.telegram_saver import TelegramSaver
                saver = TelegramSaver()

            if not saver:
                continue

            all_files = []
            for save in saves:
                if os.path.isdir(save.path):
                    all_files.append(save.path)
                else:
                    all_files.append(save.path)

            metadata = {
                "repo_path": repo_path,
                "save_dir": game,
                "game": saves[0].game,
                "timestamp": timestamp,
            }

            success = saver.save(all_files, metadata)
            if success:
                self.terminal.write((f"✓ Backup para {saver.name()} concluído!\n", "ok"))
            else:
                self.terminal.write((f"✗ Backup para {saver.name()} falhou.\n", "error"))

        self.progress.set_progress(100)
        self.terminal.write(("\n✔ Processo finalizado! Seus saves estão seguros.\n", "ok"))
