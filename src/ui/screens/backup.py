import tkinter as tk
import threading, os, importlib

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY,
)
from src.ui.components import HoverCard, make_button, make_label


class BackupScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        hdr = tk.Frame(self, bg=MANTLE, height=44)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        make_label(hdr, "\U0001F4E6  Backup de Saves",
                   fg=FG_GREEN, bg=MANTLE, font_size=12, bold=True
                   ).pack(side=tk.LEFT, padx=16)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        # Game cards
        for emoji, label, game in (
            ("\u26CF", "Minecraft  \u2014  Detecta mundos do Minecraft", "minecraft"),
            ("\U0001F409", "Pok\u00e9mon  \u2014  Varre emuladores Nintendo DS", "pokemon"),
        ):
            card = HoverCard(body, command=lambda g=game: self.start_backup(g))
            card.pack(fill=tk.X, pady=3)
            inner = card.body()

            make_label(inner, emoji, fg=FG_GREEN, bg=SURFACE0,
                       font_size=16).pack(side=tk.LEFT, padx=(0, 10))

            make_label(inner, label, fg=TEXT, bg=SURFACE0,
                       font_size=11, bold=True, anchor="w"
                       ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            make_button(inner, "\u25B6", fg=FG_GREEN, bg=SURFACE1,
                        font_size=11, bold=True, padx=8, pady=4,
                        command=lambda g=game: self.start_backup(g)
                        ).pack(side=tk.RIGHT)

        self.terminal = TerminalOutput(body, height=12)
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=(6, 2))

        prog = tk.Frame(body, bg=BG_DARK)
        prog.pack(fill=tk.X, pady=(2, 4))
        make_label(prog, "Progresso:", fg=FG_CYAN, font_size=9
                   ).pack(side=tk.LEFT, padx=(0, 8))
        self.progress = ProgressBar(prog, width=280, height=12)
        self.progress.pack(side=tk.LEFT)

        btn_row = tk.Frame(body, bg=BG_DARK)
        btn_row.pack(fill=tk.X, pady=(4, 0))

        back_btn = tk.Button(
            btn_row, text="\u2190  Voltar",
            font=(FONT_FAMILY, 10, "bold"),
            fg=FG_DIM, bg=SURFACE0,
            activeforeground=TEXT, activebackground=SURFACE1,
            relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
            command=on_back,
        )
        back_btn.pack(side=tk.LEFT)
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            highlightthickness=2, highlightbackground=FG_CYAN))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            highlightthickness=0))

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
            self.terminal.write(("Va em Configuracao primeiro.\n", "warn"))
            return
        if not os.path.isdir(repo_path):
            self.terminal.write((f"ERRO: Diretorio nao encontrado: {repo_path}\n", "error"))
            return

        self.progress.set_progress(10)
        finder_cls = ("src.games.minecraft", "MinecraftFinder") if game == "minecraft" else ("src.games.pokemon", "PokemonFinder")
        self.terminal.write((f"Buscando saves de {game.title()}...\n", "info"))
        mod = importlib.import_module(finder_cls[0])
        finder = getattr(mod, finder_cls[1])(system_wide_search=(game != "minecraft")) if game != "minecraft" else getattr(mod, finder_cls[1])()
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
            self.terminal.write(("Configure em Configuracao primeiro.\n", "dim"))
            self.progress.set_progress(100)
            return

        per_dest = 30.0 / len(configured)
        saver_map = {
            "github": ("src.savers.github_saver", "GitHubSaver"),
            "google_drive": ("src.savers.googledrive_saver", "GoogleDriveSaver"),
            "telegram": ("src.savers.telegram_saver", "TelegramSaver"),
        }

        for i, dest_name in enumerate(configured):
            self.terminal.write((f"\n[{dest_name.title()}] Enviando...\n", "warn"))
            self.progress.set_progress(60 + int(i * per_dest))
            configure_destination(dest_name.title())

            mod_path, cls_name = saver_map[dest_name]
            saver = getattr(importlib.import_module(mod_path), cls_name)()
            all_files = [s.path for s in saves]
            metadata = {"repo_path": repo_path, "save_dir": game,
                        "game": saves[0].game, "timestamp": timestamp}
            if saver.save(all_files, metadata):
                self.terminal.write((f"OK  Backup para {saver.name()} concluido!\n", "ok"))
            else:
                self.terminal.write((f"Falha  Backup para {saver.name()} falhou.\n", "error"))

        self.progress.set_progress(100)
        self.terminal.write(("\nProcesso finalizado! Seus saves estao seguros.\n", "ok"))
