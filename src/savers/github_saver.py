import os
import shutil
import subprocess
from typing import List

from src.savers.base import Saver
from src.utils import config


class GitHubSaver(Saver):
    def __init__(self):
        self.token = config.get("github.token", "")
        self.repo_url = config.get("github.repo_url", "")
        self.remote_name = config.get("github.remote_name", "origin")

    def name(self) -> str:
        return "GitHub"

    def configure(self, cfg: dict) -> bool:
        self.token = cfg.get("token", self.token)
        self.repo_url = cfg.get("repo_url", self.repo_url)
        self.remote_name = cfg.get("remote_name", self.remote_name)
        config.set_key("github.token", self.token)
        config.set_key("github.repo_url", self.repo_url)
        config.set_key("github.remote_name", self.remote_name)
        return True

    def save(self, file_paths: List[str], metadata: dict) -> bool:
        repo_path = metadata.get("repo_path", "")
        if not repo_path or not os.path.isdir(repo_path):
            print(f"  [GitHub] Erro: Caminho do repositório inválido: {repo_path}")
            return False

        save_dir = metadata.get("save_dir", "")
        if save_dir:
            dest_dir = os.path.join(repo_path, save_dir)
            os.makedirs(dest_dir, exist_ok=True)
            for src_path in file_paths:
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_dir)
                elif os.path.isdir(src_path):
                    dest_path = os.path.join(dest_dir, os.path.basename(src_path))
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    shutil.copytree(src_path, dest_path)

        timestamp = metadata.get("timestamp", "")
        game_name = metadata.get("game", "Unknown")

        try:
            result = subprocess.run(
                ["git", "add", "-A"],
                cwd=repo_path, capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"  [GitHub] Erro no git add: {result.stderr.strip()}")
                return False

            commit_msg = f"save: {timestamp} -- {game_name}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=repo_path, capture_output=True, text=True, timeout=60
            )

            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                print(f"  [GitHub] Erro no git commit: {result.stderr.strip()}")
                return False

            remote_url = self._build_remote_url()
            if remote_url:
                result = subprocess.run(
                    ["git", "remote", "set-url", self.remote_name, remote_url],
                    cwd=repo_path, capture_output=True, text=True, timeout=30
                )

            result = subprocess.run(
                ["git", "push", self.remote_name, self._get_current_branch(repo_path)],
                cwd=repo_path, capture_output=True, text=True, timeout=120
            )

            if result.returncode != 0:
                print(f"  [GitHub] Erro no git push: {result.stderr.strip()}")
                return False

            print(f"  [GitHub] Commit: {commit_msg}")
            print(f"  [GitHub] Push realizado com sucesso!")
            return True

        except subprocess.TimeoutExpired:
            print(f"  [GitHub] Erro: Operação excedeu o tempo limite")
            return False
        except Exception as e:
            print(f"  [GitHub] Erro inesperado: {e}")
            return False

    def pull(self, repo_path: str) -> bool:
        if not repo_path or not os.path.isdir(repo_path):
            print(f"  [GitHub] Erro: Caminho do repositório inválido: {repo_path}")
            return False

        print(f"  [GitHub] Sincronizando saves mais recentes...")
        try:
            remote_url = self._build_remote_url()
            if remote_url:
                subprocess.run(
                    ["git", "remote", "set-url", self.remote_name, remote_url],
                    cwd=repo_path, capture_output=True, text=True, timeout=30
                )

            result = subprocess.run(
                ["git", "pull", "--rebase", self.remote_name, self._get_current_branch(repo_path)],
                cwd=repo_path, capture_output=True, text=True, timeout=120
            )

            if result.returncode != 0:
                print(f"  [GitHub] Erro no git pull: {result.stderr.strip()}")
                return False

            print(f"  [GitHub] Sincronizado com sucesso!")
            return True

        except subprocess.TimeoutExpired:
            print(f"  [GitHub] Erro: Pull excedeu o tempo limite")
            return False
        except Exception as e:
            print(f"  [GitHub] Erro inesperado no pull: {e}")
            return False

    def _build_remote_url(self) -> str:
        if self.token and self.repo_url:
            repo_path_part = self.repo_url.replace("https://github.com/", "").replace(".git", "")
            return f"https://DevFalconszz:{self.token}@github.com/{repo_path_part}.git"
        return ""

    @staticmethod
    def _get_current_branch(repo_path: str) -> str:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path, capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() or "main"
        except Exception:
            return "main"
