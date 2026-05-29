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
                 hover_bg=SURFACE1, padx=14, pady=10, **kwargs):
        super().__init__(parent, bg=bg, cursor="hand2", **kwargs)
        self._normal_bg = bg
        self._hover_bg = hover_bg
        self._command = command
        self._inner = tk.Frame(self, bg=bg)
        self._inner.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)

        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")
        self.bind("<Button-1>", self._on_click, add="+")
        self._inner.bind("<Enter>", self._on_enter, add="+")
        self._inner.bind("<Leave>", self._on_leave, add="+")
        self._inner.bind("<Button-1>", self._on_click, add="+")

        self._children_bind = []

    def _bind_all_children(self):
        def bind_rec(w):
            try:
                w.bind("<Enter>", self._on_enter, add="+")
                w.bind("<Leave>", self._on_leave, add="+")
                w.bind("<Button-1>", self._on_click, add="+")
                self._children_bind.append(w)
            except Exception:
                pass
            for c in w.winfo_children():
                bind_rec(c)
        for c in self.winfo_children():
            bind_rec(c)
        self.after(100, bind_rec, self._inner)

    def body(self):
        return self._inner

    def _on_enter(self, event=None):
        self.configure(bg=self._hover_bg)
        self._inner.configure(bg=self._hover_bg)
        for w in self._inner.winfo_children():
            try:
                w.configure(bg=self._hover_bg)
            except Exception:
                pass

    def _on_leave(self, event=None):
        self.configure(bg=self._normal_bg)
        self._inner.configure(bg=self._normal_bg)
        for w in self._inner.winfo_children():
            try:
                w.configure(bg=self._normal_bg)
            except Exception:
                pass

    def _on_click(self, event=None):
        if self._command:
            self._command()


class NavButton(tk.Frame):
    def __init__(self, parent, icon, label, fg=FG_DIM, activefg=FG_GREEN,
                 command=None, **kwargs):
        super().__init__(parent, bg=MANTLE, cursor="hand2")
        self._normal_bg = MANTLE
        self._active_bg = SURFACE0
        self._normal_fg = fg
        self._active_fg = activefg
        self._command = command
        self._is_active = False

        self._icon_lbl = tk.Label(
            self, text=icon, font=(FONT_FAMILY, 12),
            fg=fg, bg=MANTLE, width=3, anchor="center"
        )
        self._icon_lbl.pack(side=tk.LEFT, padx=(12, 4), pady=8)

        self._text_lbl = tk.Label(
            self, text=label, font=(FONT_FAMILY, 10),
            fg=fg, bg=MANTLE, anchor="w"
        )
        self._text_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=8)

        self._bind_hover()

    def _bind_hover(self):
        for w in (self, self._icon_lbl, self._text_lbl):
            w.bind("<Enter>", lambda e: self._set_hover(True), add="+")
            w.bind("<Leave>", lambda e: self._set_hover(False), add="+")
            w.bind("<Button-1>", lambda e: self._click(), add="+")

    def _set_hover(self, on):
        if self._is_active:
            return
        bg = SURFACE1 if on else MANTLE
        fg = TEXT if on else self._normal_fg
        self._set_theme(bg, fg)

    def _set_theme(self, bg, fg):
        self.configure(bg=bg)
        self._icon_lbl.configure(bg=bg, fg=fg)
        self._text_lbl.configure(bg=bg, fg=fg)

    def set_active(self, active):
        self._is_active = active
        if active:
            self._set_theme(self._active_bg, self._active_fg)
        else:
            self._set_theme(self._normal_bg, self._normal_fg)

    def _click(self):
        if self._command:
            self._command()
