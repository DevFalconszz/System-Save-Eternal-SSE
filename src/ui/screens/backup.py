import tkinter as tk
import threading
import sys, os, importlib

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY,
)


class BackupScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        # ── Header ──
        hdr = tk.Frame(self, bg=MANTLE, height=44)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📦  Backup de Saves",
                 font=(FONT_FAMILY, 12, "bold"),
                 fg=FG_GREEN, bg=MANTLE).pack(side=tk.LEFT, padx=16)

        # ── Body ──
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        # Game selection cards
        cards = tk.Frame(body, bg=BG_DARK)
        cards.pack(fill=tk.X, pady=(0, 6))

        for emoji, label, game in (
            ("⛏", "Minecraft  —  Detecta mundos do Minecraft", "minecraft"),
            ("🐉", "Pokemon  —  Varre emuladores Nintendo DS", "pokemon"),
        ):
            card = tk.Frame(cards, bg=SURFACE0, cursor="hand2")
            card.pack(fill=tk.X, pady=3)
            inner = tk.Frame(card, bg=SURFACE0, padx=14, pady=10)
            inner.pack(fill=tk.X)

            tk.Label(inner, text=emoji, font=(FONT_FAMILY, 18),
                     fg=FG_GREEN, bg=SURFACE0).pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(inner, text=label, font=(FONT_FAMILY, 11, "bold"),
                     fg=TEXT, bg=SURFACE0, anchor="w"
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Button(inner, text="▶", font=(FONT_FAMILY, 11, "bold"),
                      fg=FG_GREEN, bg=SURFACE1, relief=tk.FLAT,
                      bd=0, padx=8, cursor="hand2",
                      command=lambda g=game: self.start_backup(g)
                      ).pack(side=tk.RIGHT)

            for w in (card, inner):
                w.bind("<Enter>", lambda e, f=SURFACE1: (card.configure(bg=f), inner.configure(bg=f)))
                w.bind("<Leave>", lambda e, f=SURFACE0: (card.configure(bg=f), inner.configure(bg=f)))

        # Terminal
        self.terminal = TerminalOutput(body, height=12)
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=4)

        # Progress
        prog = tk.Frame(body, bg=BG_DARK)
        prog.pack(fill=tk.X, pady=(2, 4))
        tk.Label(prog, text="Progresso:", font=(FONT_FAMILY, 9),
                 fg=FG_CYAN, bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 8))
        self.progress = ProgressBar(prog, width=280, height=12)
        self.progress.pack(side=tk.LEFT)

        # Voltar
        tk.Button(body, text="←  Voltar",
                  font=(FONT_FAMILY, 10, "bold"),
                  fg=FG_DIM, bg=SURFACE0, relief=tk.FLAT,
                  bd=0, padx=12, pady=4, cursor="hand2",
                  activeforeground=TEXT, activebackground=SURFACE1,
                  command=on_back
                  ).pack(pady=(2, 0))

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
            self.terminal.write(("Configure em Configuracao primeiro.\n", "dim"))
            self.progress.set_progress(100)
            return

        per_dest = 30.0 / len(configured)
        for i, dest_name in enumerate(configured):
            self.terminal.write((f"\n[{dest_name.title()}] Enviando...\n", "warn"))
            self.progress.set_progress(60 + int(i * per_dest))
            configure_destination(dest_name.title())

            mod = importlib.import_module(f"src.savers.{dest_name}_saver")
            cls_name = {"github": "GitHubSaver", "google_drive": "GoogleDriveSaver", "telegram": "TelegramSaver"}[dest_name]
            saver = getattr(mod, cls_name)()
            if not saver:
                continue

            all_files = [s.path for s in saves]
            metadata = {
                "repo_path": repo_path, "save_dir": game,
                "game": saves[0].game, "timestamp": timestamp,
            }
            if saver.save(all_files, metadata):
                self.terminal.write((f"OK  Backup para {saver.name()} concluido!\n", "ok"))
            else:
                self.terminal.write((f"Falha  Backup para {saver.name()} falhou.\n", "error"))

        self.progress.set_progress(100)
        self.terminal.write(("\nProcesso finalizado! Seus saves estao seguros.\n", "ok"))
