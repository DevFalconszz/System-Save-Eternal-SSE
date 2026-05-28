import os
from typing import List

from src.savers.base import Saver
from src.utils import config


class GoogleDriveSaver(Saver):
    def __init__(self):
        self.client_id = config.get("google_drive.client_id", "")
        self.client_secret = config.get("google_drive.client_secret", "")
        self.folder_id = config.get("google_drive.folder_id", "")

    def name(self) -> str:
        return "Google Drive"

    def configure(self, cfg: dict) -> bool:
        self.client_id = cfg.get("client_id", self.client_id)
        self.client_secret = cfg.get("client_secret", self.client_secret)
        self.folder_id = cfg.get("folder_id", self.folder_id)
        config.set_key("google_drive.client_id", self.client_id)
        config.set_key("google_drive.client_secret", self.client_secret)
        config.set_key("google_drive.folder_id", self.folder_id)
        return True

    def save(self, file_paths: List[str], metadata: dict) -> bool:
        if not self._check_credentials():
            print("  [Google Drive] Credenciais não configuradas. Execute 'sse configure' primeiro.")
            return False

        try:
            from pydrive2.auth import GoogleAuth
            from pydrive2.drive import GoogleDrive
        except ImportError:
            print("  [Google Drive] Biblioteca pydrive2 não instalada. pip install pydrive2")
            return False

        try:
            gauth = GoogleAuth()
            settings_file = os.path.expanduser("~/.config/sse/gdrive_settings.yaml")
            if os.path.exists(settings_file):
                gauth.LoadCredentialsFile(settings_file)
            if gauth.credentials is None:
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            gauth.SaveCredentialsFile(settings_file)

            drive = GoogleDrive(gauth)

            game_name = metadata.get("game", "Unknown")
            timestamp = metadata.get("timestamp", "")
            folder_id = self._ensure_game_folder(drive, game_name)

            for file_path in file_paths:
                if not os.path.exists(file_path):
                    continue
                if os.path.isfile(file_path):
                    self._upload_file(drive, folder_id, file_path, timestamp)
                elif os.path.isdir(file_path):
                    self._upload_dir(drive, folder_id, file_path, timestamp)

            print(f"  [Google Drive] Upload concluído com sucesso!")
            return True

        except Exception as e:
            print(f"  [Google Drive] Erro: {e}")
            return False

    def _check_credentials(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def _ensure_game_folder(self, drive, game_name: str) -> str:
        if self.folder_id:
            return self.folder_id
        query = f"title='{game_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = drive.ListFile({"q": query}).GetList()
        if file_list:
            return file_list[0]["id"]
        folder = drive.CreateFile({
            "title": game_name,
            "mimeType": "application/vnd.google-apps.folder"
        })
        folder.Upload()
        return folder["id"]

    def _upload_file(self, drive, folder_id: str, file_path: str, timestamp: str):
        fname = os.path.basename(file_path)
        if timestamp:
            name_parts = os.path.splitext(fname)
            fname = f"{name_parts[0]}_{timestamp}{name_parts[1]}"
        gfile = drive.CreateFile({
            "title": fname,
            "parents": [{"id": folder_id}]
        })
        gfile.SetContentFile(file_path)
        gfile.Upload()
        print(f"  [Google Drive] Upload: {fname}")

    def _upload_dir(self, drive, folder_id: str, dir_path: str, timestamp: str):
        dir_name = os.path.basename(dir_path)
        if timestamp:
            dir_name = f"{dir_name}_{timestamp}"
        gdir = drive.CreateFile({
            "title": dir_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"id": folder_id}]
        })
        gdir.Upload()
        for root, _, files in os.walk(dir_path):
            for f in files:
                fpath = os.path.join(root, f)
                self._upload_file(drive, gdir["id"], fpath, "")
