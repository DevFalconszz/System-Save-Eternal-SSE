import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.ui.styles import BG_DARK, FONT_FAMILY, apply_theme
from src.ui.screens.welcome import WelcomeScreen
from src.ui.screens.backup import BackupScreen
from src.ui.screens.play import PlayScreen
from src.ui.screens.config import ConfigScreen


class SSEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Save Eternal — SSE")
        self.configure(bg=BG_DARK)
        apply_theme(self)

        self.geometry("750x600")
        self.minsize(650, 500)

        try:
            self.iconbitmap(default=os.path.join(
                os.path.dirname(__file__), "..", "..", "assets", "icons", "sse-icon.ico"
            ))
        except Exception:
            pass

        self._current_frame = None
        self._show_welcome()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _clear(self):
        if self._current_frame:
            self._current_frame.pack_forget()
            self._current_frame.destroy()
            self._current_frame = None

    def _show_welcome(self):
        self._clear()
        self._current_frame = WelcomeScreen(
            self,
            on_backup=self._show_backup,
            on_play=self._show_play,
            on_config=self._show_config,
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_backup(self):
        self._clear()
        self._current_frame = BackupScreen(
            self, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_play(self):
        self._clear()
        self._current_frame = PlayScreen(
            self, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_config(self):
        self._clear()
        self._current_frame = ConfigScreen(
            self, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _on_close(self):
        import tkinter.messagebox as mb
        if mb.askokcancel("SSE", "Deseja realmente sair?"):
            self.destroy()


def run_gui():
    app = SSEApp()
    app.mainloop()
