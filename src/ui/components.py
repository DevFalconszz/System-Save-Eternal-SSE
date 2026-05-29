import tkinter as tk
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_RED, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE,
)


def make_button(parent, text, fg=FG_GREEN, bg=SURFACE0,
                font_size=None, bold=False, padx=14, pady=6,
                command=None, side=None, fill=None, expand=False,
                **kwargs):
    weight = "bold" if bold else "normal"
    btn = tk.Button(
        parent, text=text,
        font=(FONT_FAMILY, font_size or FONT_SIZE, weight),
        fg=fg, bg=bg,
        activeforeground=fg, activebackground=SURFACE1,
        relief=tk.FLAT, bd=0, padx=padx, pady=pady,
        cursor="hand2", command=command, **kwargs
    )
    btn.pack(side=side, fill=fill, expand=expand)
    return btn


def make_label(parent, text, fg=TEXT, bg=None, font_size=None,
               bold=False, **kwargs):
    return tk.Label(
        parent, text=text,
        font=(FONT_FAMILY, font_size or FONT_SIZE, "bold" if bold else "normal"),
        fg=fg, bg=bg or BG_DARK, **kwargs
    )


class HoverCard(tk.Frame):
    def __init__(self, parent, command=None, bg=SURFACE0,
                 hover_bg=SURFACE1, padx=14, pady=10,
                 no_hover=False, **kwargs):
        super().__init__(parent, bg=bg, cursor="hand2", **kwargs)
        self._normal_bg = bg
        self._hover_bg = hover_bg
        self._command = command
        self._no_hover = no_hover
        self._inner = tk.Frame(self, bg=bg)
        self._inner.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)

        if not no_hover:
            self._bind_widget(self)
            self._bind_widget(self._inner)
            self.after(0, self._bind_children)
        self.bind("<Button-1>", self._on_click, add="+")

    def _bind_widget(self, w):
        w.bind("<Enter>", self._on_enter, add="+")
        w.bind("<Leave>", self._on_leave, add="+")
        w.bind("<Button-1>", self._on_click, add="+")

    def _bind_children(self):
        def rec(w):
            for c in w.winfo_children():
                self._bind_widget(c)
                rec(c)
        rec(self)

    def body(self):
        return self._inner

    def _set_bg(self, bg):
        self.configure(bg=bg)
        self._inner.configure(bg=bg)
        for w in self._inner.winfo_children():
            try:
                w.configure(bg=bg)
            except Exception:
                pass

    def _on_enter(self, event=None):
        self._set_bg(self._hover_bg)

    def _on_leave(self, event=None):
        if event and event.x_root > 0:
            rx = self.winfo_rootx()
            ry = self.winfo_rooty()
            if rx <= event.x_root <= rx + self.winfo_width() and \
               ry <= event.y_root <= ry + self.winfo_height():
                return
        self._set_bg(self._normal_bg)

    def _on_click(self, event=None):
        if self._command:
            self._command()


class NavButton(tk.Frame):
    def __init__(self, parent, icon, label, fg=FG_DIM, activefg=FG_GREEN,
                 command=None, **kwargs):
        super().__init__(parent, bg=MANTLE)
        self._normal_fg = fg
        self._active_fg = activefg
        self._is_active = False

        self._indicator = tk.Frame(self, width=3, bg=MANTLE)
        self._indicator.pack(side=tk.LEFT, fill=tk.Y)

        self._btn = tk.Button(
            self, text=f"  {icon}   {label}",
            font=(FONT_FAMILY, 10),
            anchor="w", relief=tk.FLAT, bd=0,
            padx=8, pady=10, cursor="hand2",
            bg=MANTLE, fg=fg,
            activebackground=SURFACE0, activeforeground=fg,
            command=command
        )
        self._btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._btn.bind("<Enter>", lambda e: self._on_hover(True), add="+")
        self._btn.bind("<Leave>", lambda e: self._on_hover(False), add="+")

    def _on_hover(self, on):
        if self._is_active:
            return
        self._btn.configure(
            bg=SURFACE1 if on else MANTLE,
            fg=TEXT if on else self._normal_fg
        )

    def set_active(self, active):
        self._is_active = active
        if active:
            self._btn.configure(bg=SURFACE0, fg=self._active_fg)
            self._indicator.configure(bg=self._active_fg)
        else:
            self._btn.configure(bg=MANTLE, fg=self._normal_fg)
            self._indicator.configure(bg=MANTLE)
