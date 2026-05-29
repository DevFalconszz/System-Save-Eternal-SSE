import tkinter as tk
import threading, os

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY,
)
from src.ui.components import make_button, make_label, HoverCard


class PlayScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        hdr = tk.Frame(self, bg=MANTLE, height=44)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        make_label(hdr, "\U0001F3AE  Jogar Minecraft com Sincronizac\u00e3o",
                   fg=FG_YELLOW, bg=MANTLE, font_size=12, bold=True
                   ).pack(side=tk.LEFT, padx=16)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        # Info card
        info_card = HoverCard(body)
        info_card.pack(fill=tk.X, pady=(0, 6))
        info_inner = info_card.body()
        make_label(info_inner,
                   "\U0001F504  Ciclo completo: detecta launcher, "
                   "puxa saves do GitHub, abre o jogo, monitora e salva ao fechar",
                   fg=FG_DIM, bg=SURFACE0, font_size=9
                   ).pack(fill=tk.X)

        self.terminal = TerminalOutput(body, height=14)
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=4)

        prog = tk.Frame(body, bg=BG_DARK)
        prog.pack(fill=tk.X, pady=(2, 4))
        make_label(prog, "Progresso:", fg=FG_CYAN, font_size=9
                   ).pack(side=tk.LEFT, padx=(0, 8))
        self.progress = ProgressBar(prog, width=280, height=12)
        self.progress.pack(side=tk.LEFT)

        btn_row = tk.Frame(body, bg=BG_DARK)
        btn_row.pack(pady=4)

        self.start_btn = make_button(
            btn_row, "\u25B6  Iniciar Ciclo Completo",
            fg=FG_GREEN, bg=SURFACE0, font_size=11, bold=True,
            padx=18, pady=6, command=self.start_play_cycle
        )

        make_button(btn_row, "\u2190  Voltar", fg=FG_DIM, bg=SURFACE0,
                    font_size=10, bold=True, padx=10, pady=4,
                    command=on_back, side=tk.LEFT)

    def start_play_cycle(self):
        self.terminal.clear()
        self.progress.set_progress(0)
        self.start_btn.configure(state=tk.DISABLED, text="\u25B6  Em andamento...")

        def cycle():
            try:
                self._do_cycle()
            except Exception as e:
                self.terminal.write((f"Erro: {e}\n", "error"))
            finally:
                self.start_btn.configure(state=tk.NORMAL, text="\u25B6  Iniciar Ciclo Completo")

        threading.Thread(target=cycle, daemon=True).start()

    def _do_cycle(self):
        from src.utils import config as cfg
        repo_path = cfg.get("save_repo_path", "")
        if not repo_path:
            self.terminal.write(("ERRO: Repositorio nao configurado.\n", "error"))
            return
        if not os.path.isdir(repo_path):
            self.terminal.write((f"ERRO: Diretorio nao encontrado: {repo_path}\n", "error"))
            return

        self.terminal.write(("Detectando launcher Minecraft...\n", "info"))
        from src.launcher.minecraft_launcher import detect_launchers
        launchers = detect_launchers()
        if not launchers:
            self.terminal.write(("Nenhum launcher encontrado.\n", "error"))
            return
        launcher_info = {
            "launcher": launchers[0],
            "name": launchers[0].name,
            "binary": launchers[0].binary_path,
            "game_dir": launchers[0].game_dir,
        }
        self.terminal.write((f"Launcher: {launcher_info['name']}\n", "ok"))
        self.progress.set_progress(15)

        self.terminal.write(("\nSincronizando saves do GitHub...\n", "info"))
        has_github = bool(cfg.get("github.repo_url") and cfg.get("github.token"))
        if has_github:
            from src.savers.github_saver import GitHubSaver
            GitHubSaver().pull(repo_path)
        self.progress.set_progress(30)

        self.terminal.write(("Copiando saves para o launcher...\n", "info"))
        from src.console.menu import sync_worlds_to_launcher
        sync_worlds_to_launcher(launcher_info, repo_path)
        self.progress.set_progress(45)

        from src.launcher.minecraft_launcher import launch_and_monitor
        self.terminal.write(("\n" + "=" * 50 + "\n", "dim"))
        self.terminal.write((f"Iniciando {launcher_info['name']}...\n", "warn"))
        self.terminal.write(("Jogue normalmente. Quando fechar, os saves serao salvos.\n", "info"))
        self.terminal.write(("=" * 50 + "\n", "dim"))
        self.progress.set_progress(60)

        launch_and_monitor(
            launcher_info["launcher"],
            pre_launch_callback=None,
            post_exit_callback=lambda: self._after_game_exit(launcher_info, repo_path, has_github),
        )

        self.terminal.write(("\nCiclo concluido! Seus saves estao seguros.\n", "ok"))
        self.progress.set_progress(100)

    def _after_game_exit(self, launcher_info, repo_path, has_github):
        self.terminal.write(("\nSincronizando saves apos o jogo...\n", "info"))
        from src.console.menu import sync_worlds_to_repo, get_timestamp
        from src.utils import config as cfg

        sync_worlds_to_repo(launcher_info, repo_path)
        self.progress.set_progress(75)

        if has_github:
            self.terminal.write(("Enviando para GitHub...\n", "info"))
            from src.savers.github_saver import GitHubSaver
            gh = GitHubSaver()
            gh.save([os.path.join(repo_path, "Minecraft", "saves")], {
                "repo_path": repo_path, "save_dir": "Minecraft",
                "game": "Minecraft", "timestamp": get_timestamp(),
            })

        self.progress.set_progress(90)

        for dest, saver_cls in (
            ("Google Drive", "GoogleDriveSaver"),
            ("Telegram", "TelegramSaver"),
        ):
            key = "google_drive.client_id" if dest == "Google Drive" else "telegram.api_id"
            if not cfg.get(key):
                continue
            self.terminal.write((f"Enviando para {dest}...\n", "info"))
            mod = __import__(f"src.savers.{saver_cls.lower().replace('saver', '_saver')}", fromlist=[saver_cls])
            s = getattr(mod, saver_cls)()
            s.save([os.path.join(repo_path, "Minecraft")], {
                "repo_path": repo_path, "save_dir": "Minecraft",
                "game": "Minecraft", "timestamp": get_timestamp(),
            })

        self.progress.set_progress(100)
