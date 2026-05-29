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
    hover_bg = kwargs.pop("hover_bg", SURFACE1)
    btn = tk.Button(
        parent, text=text,
        font=(FONT_FAMILY, font_size or FONT_SIZE, weight),
        fg=fg, bg=bg,
        activeforeground=fg, activebackground=hover_bg,
        relief=tk.FLAT, bd=0, padx=padx, pady=pady,
        cursor="hand2", command=command, **kwargs
    )
    def on_enter(e):
        btn.configure(bg=hover_bg)
    def on_leave(e):
        btn.configure(bg=bg)
    btn.bind("<Enter>", on_enter, add="+")
    btn.bind("<Leave>", on_leave, add="+")
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
        self._hovering = False

        self._inner = tk.Frame(self, bg=bg)
        self._inner.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)

        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")
        self.bind("<Button-1>", self._on_click, add="+")
        self._inner.bind("<Button-1>", self._on_click, add="+")

    def body(self):
        return self._inner

    def _paint(self, bg):
        self.configure(bg=bg)
        self._inner.configure(bg=bg)
        for w in self._inner.winfo_children():
            try:
                w.configure(bg=bg)
            except Exception:
                pass

    def _mouse_over_card(self):
        try:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            rx = self.winfo_rootx()
            ry = self.winfo_rooty()
            return (rx <= x <= rx + self.winfo_width() and
                    ry <= y <= ry + self.winfo_height())
        except Exception:
            return False

    def _on_enter(self, event=None):
        self._hovering = True
        self._paint(self._hover_bg)

    def _on_leave(self, event=None):
        self._hovering = False
        self.after(30, self._resolve_leave)

    def _resolve_leave(self):
        if not self._hovering and not self._mouse_over_card():
            self._paint(self._normal_bg)

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
        self._hovering = False

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

        for w in (self, self._icon_lbl, self._text_lbl):
            w.bind("<Enter>", lambda e: self._on_enter(), add="+")
            w.bind("<Leave>", lambda e: self._on_leave(), add="+")
            w.bind("<Button-1>", lambda e: self._click(), add="+")

    def _on_enter(self):
        if self._is_active:
            return
        self._hovering = True
        self._paint(SURFACE1, TEXT)

    def _on_leave(self):
        self._hovering = False
        self.after(30, self._resolve_leave)

    def _resolve_leave(self):
        if self._is_active or self._hovering:
            return
        try:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            rx = self.winfo_rootx()
            ry = self.winfo_rooty()
            inside = (rx <= x <= rx + self.winfo_width() and
                      ry <= y <= ry + self.winfo_height())
            if not inside:
                self._paint(MANTLE, self._normal_fg)
        except Exception:
            self._paint(MANTLE, self._normal_fg)

    def _paint(self, bg, fg=None):
        self.configure(bg=bg)
        self._icon_lbl.configure(bg=bg, fg=fg or self._normal_fg)
        self._text_lbl.configure(bg=bg, fg=fg or self._normal_fg)

    def set_active(self, active):
        self._is_active = active
        if active:
            self._paint(self._active_bg, self._active_fg)
        else:
            self._paint(MANTLE, self._normal_fg)

    def _click(self):
        if self._command:
            self._command()
