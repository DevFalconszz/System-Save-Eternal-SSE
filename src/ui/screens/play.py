import tkinter as tk
import threading
import os

from src.ui.terminal import TerminalOutput, ProgressBar
from src.ui.styles import BG_DARK, FG_YELLOW, FG_CYAN, FG_GREEN, FG_RED, apply_theme


class PlayScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        header = tk.Label(self, text="Jogar Minecraft com Sincronização",
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

        self.start_btn = tk.Button(
            btn_frame, text="▶ Iniciar Ciclo Completo",
            command=self.start_play_cycle,
            font=("Courier", 11)
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Voltar", command=on_back,
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=20)

    def start_play_cycle(self):
        self.terminal.clear()
        self.progress.set_progress(0)
        self.start_btn.configure(state=tk.DISABLED, text="▶ Em andamento...")

        def cycle():
            try:
                self._do_cycle()
            except Exception as e:
                self.terminal.write((f"Erro: {e}\n", "error"))
            finally:
                self.start_btn.configure(state=tk.NORMAL, text="▶ Iniciar Ciclo Completo")

        threading.Thread(target=cycle, daemon=True).start()

    def _do_cycle(self):
        from src.utils import config as cfg
        repo_path = cfg.get("save_repo_path", "")
        if not repo_path:
            self.terminal.write(("ERRO: Repositório não configurado.\n", "error"))
            return
        if not os.path.isdir(repo_path):
            self.terminal.write((f"ERRO: Diretório não encontrado: {repo_path}\n", "error"))
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
            gh_saver = GitHubSaver()
            gh_saver.pull(repo_path)
        self.progress.set_progress(30)

        self.terminal.write(("Copiando saves para o launcher...\n", "info"))
        from src.console.menu import sync_worlds_to_launcher
        sync_worlds_to_launcher(launcher_info, repo_path)
        self.progress.set_progress(45)

        from src.launcher.minecraft_launcher import launch_and_monitor
        self.terminal.write(("\n" + "=" * 50 + "\n", "dim"))
        self.terminal.write((f"Iniciando {launcher_info['name']}...\n", "warn"))
        self.terminal.write(("Jogue normalmente. Quando fechar, os saves serão salvos.\n", "info"))
        self.terminal.write(("=" * 50 + "\n", "dim"))
        self.progress.set_progress(60)

        launched = launch_and_monitor(
            launcher_info["launcher"],
            pre_launch_callback=None,
            post_exit_callback=lambda: self._after_game_exit(
                launcher_info, repo_path, has_github
            ),
        )

        if launched:
            self.terminal.write(("\n✔ Ciclo concluído! Seus saves estão seguros.\n", "ok"))
            self.progress.set_progress(100)

    def _after_game_exit(self, launcher_info, repo_path, has_github):
        self.terminal.write(("\nSincronizando saves após o jogo...\n", "info"))
        from src.console.menu import sync_worlds_to_repo, get_timestamp
        from src.utils import config as cfg

        sync_worlds_to_repo(launcher_info, repo_path)
        self.progress.set_progress(75)

        if has_github:
            self.terminal.write(("Enviando para GitHub...\n", "info"))
            from src.savers.github_saver import GitHubSaver
            gh = GitHubSaver()
            all_files = [os.path.join(repo_path, "Minecraft", "saves")]
            metadata = {
                "repo_path": repo_path,
                "save_dir": "Minecraft",
                "game": "Minecraft",
                "timestamp": get_timestamp(),
            }
            gh.save(all_files, metadata)

        self.progress.set_progress(90)

        dests = []
        if cfg.get("google_drive.client_id"):
            dests.append("Google Drive")
        if cfg.get("telegram.api_id"):
            dests.append("Telegram")

        for dest in dests:
            self.terminal.write((f"Enviando para {dest}...\n", "info"))
            if dest == "Google Drive":
                from src.savers.googledrive_saver import GoogleDriveSaver
                s = GoogleDriveSaver()
            else:
                from src.savers.telegram_saver import TelegramSaver
                s = TelegramSaver()
            files = [os.path.join(repo_path, "Minecraft")]
            meta = {
                "repo_path": repo_path,
                "save_dir": "Minecraft",
                "game": "Minecraft",
                "timestamp": get_timestamp(),
            }
            s.save(files, meta)

        self.progress.set_progress(100)
