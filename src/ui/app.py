import tkinter as tk
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1,
    FG_GREEN, FG_RED, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY, apply_theme,
)
from src.ui.components import make_button, NavButton
from src.ui.screens.welcome import WelcomeScreen
from src.ui.screens.backup import BackupScreen
from src.ui.screens.play import PlayScreen
from src.ui.screens.config import ConfigScreen


class SSEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSE Launcher")
        self.configure(bg=BG_DARK)
        apply_theme(self)

        self.geometry("960x660")
        self.minsize(800, 580)

        PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        try:
            icon_path = os.path.join(PROJECT_DIR, "assets", "icons", "sse-icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
        except Exception:
            pass

        self._current_frame = None
        self._current_nav = "home"

        self._build_title_bar()
        self._build_main_area()
        self._show_welcome()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_title_bar(self):
        bar = tk.Frame(self, bg=MANTLE, height=32)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        tk.Label(bar, text="SSE Launcher",
                 font=(FONT_FAMILY, 10, "bold"),
                 fg=FG_GREEN, bg=MANTLE).pack(side=tk.LEFT, padx=12)

        ctrl = tk.Frame(bar, bg=MANTLE)
        ctrl.pack(side=tk.RIGHT)

        for txt, fg, cmd in (
            ("[─]", FG_DIM, lambda: self.iconify()),
            ("[□]", FG_CYAN, self._toggle_maximize),
            ("[✕]", FG_RED, self._on_close),
        ):
            tk.Button(ctrl, text=txt, font=(FONT_FAMILY, 9, "bold"),
                      fg=fg, bg=MANTLE, activeforeground=fg,
                      activebackground=SURFACE0, relief=tk.FLAT,
                      bd=0, padx=8, cursor="hand2",
                      command=cmd).pack(side=tk.LEFT, padx=1)

    def _build_main_area(self):
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True)

        self._side = tk.Frame(body, bg=MANTLE, width=180)
        self._side.pack(side=tk.LEFT, fill=tk.Y)
        self._side.pack_propagate(False)

        # canvas decorativo sobre a sidebar
        self._side_cv = tk.Canvas(self._side, bg=MANTLE, highlightthickness=0)
        self._side_cv.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Logo ---
        logo_frame = tk.Frame(self._side, bg=MANTLE)
        logo_frame.pack(fill=tk.X, pady=(18, 6))
        tk.Label(logo_frame, text="SSE",
                 font=(FONT_FAMILY, 16, "bold"),
                 fg=FG_GREEN, bg=MANTLE).pack()
        tk.Label(logo_frame, text="Launcher",
                 font=(FONT_FAMILY, 8),
                 fg=FG_DIM, bg=MANTLE).pack()

        # --- Nav ---
        self._nav_btns = {}
        for nav_id, icon, label in (
            ("home", "⬡", "In\u00edcio"),
            ("backup", "\U0001F4E6", "Backup"),
            ("play", "\U0001F3AE", "Jogar"),
            ("config", "\u2699", "Config"),
        ):
            nb = NavButton(self._side, icon, label,
                           command=lambda n=nav_id: self._nav_go(n))
            nb.pack(fill=tk.X, padx=4, pady=1)
            self._nav_btns[nav_id] = nb

        spacer = tk.Frame(self._side, bg=MANTLE)
        spacer.pack(expand=True)

        NavButton(self._side, "\u2715", "Sair",
                  fg=FG_DIM, activefg=FG_RED,
                  command=self._on_close).pack(fill=tk.X, padx=4, pady=1)

        tk.Label(self._side, text="v2.0",
                 font=(FONT_FAMILY, 7),
                 fg=FG_DIM, bg=MANTLE).pack(side=tk.BOTTOM, pady=(2, 6))

        self._content = tk.Frame(body, bg=BG_DARK)
        self._content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._side.bind("<Configure>", lambda e: self._draw_side_border())

    def _draw_side_border(self):
        w = self._side.winfo_width()
        h = self._side.winfo_height()
        if w < 10 or h < 10:
            return
        cv = self._side_cv
        cv.delete("all")
        cv.create_line(w - 1, 0, w - 1, h, fill=SURFACE1, width=1)

    def _nav_go(self, nav_id):
        self._current_nav = nav_id
        for nid, btn in self._nav_btns.items():
            btn.set_active(nid == nav_id)
        target = {
            "home": self._show_welcome,
            "backup": self._show_backup,
            "play": self._show_play,
            "config": self._show_config,
        }.get(nav_id, self._show_welcome)
        target()

    def _clear(self):
        if self._current_frame:
            self._current_frame.pack_forget()
            self._current_frame.destroy()
            self._current_frame = None

    def _show_welcome(self):
        self._clear()
        self._current_frame = WelcomeScreen(
            self._content,
            on_backup=lambda: self._nav_go("backup"),
            on_play=lambda: self._nav_go("play"),
            on_config=lambda: self._nav_go("config"),
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_backup(self):
        self._clear()
        self._current_frame = BackupScreen(
            self._content, on_back=lambda: self._nav_go("home")
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_play(self):
        self._clear()
        self._current_frame = PlayScreen(
            self._content, on_back=lambda: self._nav_go("home")
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_config(self):
        self._clear()
        self._current_frame = ConfigScreen(
            self._content, on_back=lambda: self._nav_go("home")
        )
        self._current_frame.pack(fill=tk.BOTH, expand=True)

    def _toggle_maximize(self):
        import platform
        if platform.system() == "Windows":
            self.state("normal" if self.state() == "zoomed" else "zoomed")
        else:
            self.attributes("-zoomed", not self.attributes("-zoomed"))

    def _on_close(self):
        from src.ui.dialog import SSEDialog
        if SSEDialog.confirm(self, "Sair", "Deseja realmente sair do SSE Launcher?"):
            self.destroy()


def run_gui():
    app = SSEApp()
    app.mainloop()
