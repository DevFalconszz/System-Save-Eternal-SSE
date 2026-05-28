import os
from typing import List

from src.savers.base import Saver
from src.utils import config


class TelegramSaver(Saver):
    def __init__(self):
        self.api_id = config.get("telegram.api_id", 0)
        self.api_hash = config.get("telegram.api_hash", "")
        self.phone = config.get("telegram.phone", "")
        self.chat_id = config.get("telegram.chat_id", "")

    def name(self) -> str:
        return "Telegram"

    def configure(self, cfg: dict) -> bool:
        self.api_id = cfg.get("api_id", self.api_id)
        self.api_hash = cfg.get("api_hash", self.api_hash)
        self.phone = cfg.get("phone", self.phone)
        self.chat_id = cfg.get("chat_id", self.chat_id)
        config.set_key("telegram.api_id", self.api_id)
        config.set_key("telegram.api_hash", self.api_hash)
        config.set_key("telegram.phone", self.phone)
        config.set_key("telegram.chat_id", self.chat_id)
        return True

    def save(self, file_paths: List[str], metadata: dict) -> bool:
        if not self._check_credentials():
            print("  [Telegram] Credenciais não configuradas.")
            return False

        try:
            from telethon import TelegramClient
            from telethon.errors import SessionPasswordNeededError
        except ImportError:
            print("  [Telegram] Biblioteca Telethon não instalada. pip install telethon")
            return False

        try:
            session_file = os.path.expanduser("~/.config/sse/telegram.session")
            client = TelegramClient(session_file, self.api_id, self.api_hash)
            await_client = None

            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                async def do_upload():
                    await client.start(phone=self.phone or None)

                    if not await client.is_user_authorized():
                        print("  [Telegram] Envie o código de verificação enviado para seu Telegram.")
                        await client.send_code_request(self.phone)
                        code = input("  [Telegram] Código de verificação: ").strip()
                        try:
                            await client.sign_in(phone=self.phone, code=code)
                        except SessionPasswordNeededError:
                            pwd = input("  [Telegram] Senha de verificação em duas etapas: ").strip()
                            await client.sign_in(password=pwd)

                    peer = self.chat_id if self.chat_id else "me"
                    entity = await client.get_entity(peer)
                    game_name = metadata.get("game", "Unknown")
                    timestamp = metadata.get("timestamp", "")
                    caption = f"Backup: {game_name} - {timestamp}"

                    for file_path in file_paths:
                        if not os.path.exists(file_path):
                            continue
                        if os.path.isfile(file_path):
                            await client.send_file(entity, file_path, caption=caption)
                            print(f"  [Telegram] Enviado: {os.path.basename(file_path)}")
                        elif os.path.isdir(file_path):
                            for root, _, files in os.walk(file_path):
                                for f in files:
                                    fpath = os.path.join(root, f)
                                    await client.send_file(entity, fpath, caption=caption)
                                    print(f"  [Telegram] Enviado: {f}")

                    return True

                await_client = do_upload()
                result = loop.run_until_complete(await_client)

                if result:
                    print(f"  [Telegram] Backup enviado com sucesso!")
                return result

            finally:
                if await_client and not await_client.done():
                    await_client.close()
                loop.close()

        except Exception as e:
            print(f"  [Telegram] Erro: {e}")
            return False

    def _check_credentials(self) -> bool:
        return bool(self.api_id and self.api_hash)
