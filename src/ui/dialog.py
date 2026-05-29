import tkinter as tk
from src.ui.styles import (
    BG_DARK, CRUST, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_RED, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE, rounded_rect,
)


class SSEDialog(tk.Toplevel):
    def __init__(self, parent, title="", message="",
                 confirm_text="Confirmar", cancel_text="Cancelar",
                 icon_color=FG_YELLOW, icon_symbol="?"):
        super().__init__(parent)
        self.withdraw()
        self.title("SSE")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)
        self.attributes("-type", "dialog")
        self.transient(parent)
        self.grab_set()

        self._result = False

        inner = tk.Frame(self, bg=BG_DARK, padx=0, pady=0)
        inner.pack(fill=tk.BOTH, expand=True)

        bb = tk.Frame(inner, bg=SURFACE0, bd=0)
        bb.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        content = tk.Frame(bb, bg=BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        top = tk.Frame(content, bg=BG_DARK)
        top.pack(fill=tk.X, pady=(0, 12))

        tk.Label(top, text=icon_symbol,
                 font=(FONT_FAMILY, 20, "bold"),
                 fg=icon_color, bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(top, text=title,
                 font=(FONT_FAMILY, 13, "bold"),
                 fg=icon_color, bg=BG_DARK).pack(side=tk.LEFT)

        msg = tk.Label(content, text=message,
                       font=(FONT_FAMILY, FONT_SIZE),
                       fg=TEXT, bg=BG_DARK,
                       justify=tk.LEFT, wraplength=380)
        msg.pack(fill=tk.X, pady=(0, 16))

        btn_frame = tk.Frame(content, bg=BG_DARK)
        btn_frame.pack(fill=tk.X)

        spacer = tk.Frame(btn_frame, bg=BG_DARK)
        spacer.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        if cancel_text:
            btn_cancel = tk.Button(
                btn_frame, text=cancel_text,
                font=(FONT_FAMILY, FONT_SIZE, "bold"),
                fg=FG_DIM, bg=SURFACE0,
                activeforeground=TEXT, activebackground=SURFACE1,
                relief=tk.FLAT, bd=0, padx=14, pady=6, cursor="hand2",
                command=self._cancel
            )
            btn_cancel.pack(side=tk.RIGHT, padx=(4, 4))

        btn_confirm = tk.Button(
            btn_frame, text=confirm_text,
            font=(FONT_FAMILY, FONT_SIZE, "bold"),
            fg=FG_GREEN, bg=SURFACE0,
            activeforeground=FG_GREEN, activebackground=SURFACE1,
            relief=tk.FLAT, bd=0, padx=14, pady=6, cursor="hand2",
            command=self._confirm
        )
        btn_confirm.pack(side=tk.RIGHT, padx=(0, 4))

        self.bind("<Escape>", lambda e: self._cancel())
        self.bind("<Return>", lambda e: self._confirm())

        self.update_idletasks()
        pw = parent.winfo_rootx()
        ph = parent.winfo_rooty()
        pww = parent.winfo_width()
        phh = parent.winfo_height()
        w = self.winfo_reqwidth() + 4
        h = self.winfo_reqheight() + 4
        self.geometry(f"{w}x{h}+{pw + (pww - w) // 2}+{ph + (phh - h) // 2}")

        self.deiconify()
        self.wait_window()

    def _confirm(self):
        self._result = True
        self.destroy()

    def _cancel(self):
        self._result = False
        self.destroy()

    @classmethod
    def ask(cls, parent, title, message,
            confirm="Confirmar", cancel="Cancelar",
            icon_color=FG_YELLOW, icon_symbol="?"):
        return cls(parent, title, message, confirm, cancel,
                   icon_color, icon_symbol)._result

    @classmethod
    def confirm(cls, parent, title, message):
        return cls.ask(parent, title, message,
                       confirm="Sim", cancel="Nao",
                       icon_color=FG_YELLOW, icon_symbol="?")

    @classmethod
    def delete(cls, parent, title, message):
        return cls.ask(parent, title, message,
                       confirm="Sim, excluir", cancel="Cancelar",
                       icon_color=FG_RED, icon_symbol="!")
