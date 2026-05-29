import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.ui.styles import (
    BG_DARK, CRUST, SURFACE0, SURFACE1,
    FG_GREEN, FG_RED, FG_DIM, TEXT,
    FONT_FAMILY, apply_theme
)
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

        self.geometry("800x650")
        self.minsize(700, 550)

        try:
            self.iconbitmap(default=os.path.join(
                os.path.dirname(__file__), "..", "..", "assets", "icons", "sse-icon.ico"
            ))
        except Exception:
            pass

        self._current_frame = None
        self._build_title_bar()
        self._content = tk.Frame(self, bg=BG_DARK)
        self._content.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
        self._build_status_bar()
        self._show_welcome()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_title_bar(self):
        bar = tk.Frame(self, bg=BG_DARK, height=36)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        inner = tk.Frame(bar, bg=BG_DARK)
        inner.pack(fill=tk.X, padx=12)

        title = tk.Label(
            inner, text="◆  SSE  —  System Save Eternal",
            font=(FONT_FAMILY, 11, "bold"),
            fg=FG_GREEN, bg=BG_DARK
        )
        title.pack(side=tk.LEFT)

        sep = tk.Label(inner, text="|", font=(FONT_FAMILY, 9), fg=FG_DIM, bg=BG_DARK)
        sep.pack(side=tk.LEFT, padx=8)

        subtitle = tk.Label(
            inner, text="backup inteligente de saves",
            font=(FONT_FAMILY, 10), fg=FG_DIM, bg=BG_DARK
        )
        subtitle.pack(side=tk.LEFT)

        controls = tk.Frame(inner, bg=BG_DARK)
        controls.pack(side=tk.RIGHT)

        for btn_data in (
            ("[─]", FG_DIM, lambda: self.iconify()),
            ("[✕]", FG_RED, self._on_close),
        ):
            btn = tk.Button(
                controls, text=btn_data[0],
                font=(FONT_FAMILY, 10, "bold"),
                fg=btn_data[1], bg=SURFACE0,
                activeforeground=btn_data[1],
                activebackground=SURFACE1,
                relief=tk.FLAT, bd=0, padx=8, cursor="hand2",
                command=btn_data[2]
            )
            btn.pack(side=tk.LEFT, padx=2)

    def _build_status_bar(self):
        bar = tk.Frame(self, bg=CRUST, height=28)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        inner = tk.Frame(bar, bg=CRUST)
        inner.pack(fill=tk.X, padx=12)

        info = tk.Label(
            inner, text="SSE v2.0  •  Linux  •  Windows  •  Android",
            font=(FONT_FAMILY, 9), fg=FG_DIM, bg=CRUST
        )
        info.pack(side=tk.LEFT)

        close_btn = tk.Button(
            inner, text="Sair",
            font=(FONT_FAMILY, 9, "bold"),
            fg=FG_RED, bg=SURFACE0,
            activeforeground=FG_RED, activebackground=SURFACE1,
            relief=tk.FLAT, bd=0, padx=10, cursor="hand2",
            command=self._on_close
        )
        close_btn.pack(side=tk.RIGHT, padx=2, pady=2)

    def _clear(self):
        if self._current_frame:
            self._current_frame.pack_forget()
            self._current_frame.destroy()
            self._current_frame = None

    def _show_welcome(self):
        self._clear()
        self._current_frame = WelcomeScreen(
            self._content,
            on_backup=self._show_backup,
            on_play=self._show_play,
            on_config=self._show_config,
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_backup(self):
        self._clear()
        self._current_frame = BackupScreen(
            self._content, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_play(self):
        self._clear()
        self._current_frame = PlayScreen(
            self._content, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_config(self):
        self._clear()
        self._current_frame = ConfigScreen(
            self._content, on_back=self._show_welcome
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _on_close(self):
        import tkinter.messagebox as mb
        if mb.askokcancel("SSE", "Deseja realmente sair?"):
            self.destroy()


def run_gui():
    app = SSEApp()
    app.mainloop()
