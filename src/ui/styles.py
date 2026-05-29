import tkinter as tk

BG_DARK = "#0a0a0a"
BG_TERMINAL = "#0d1117"
FG_GREEN = "#00ff41"
FG_CYAN = "#00bfff"
FG_YELLOW = "#ffd700"
FG_RED = "#ff3333"
FG_WHITE = "#c9d1d9"
FG_DIM = "#484f58"

FONT_FAMILY = "Courier"
FONT_SIZE = 11

BTN_BG = "#1a1a2e"
BTN_FG = FG_GREEN
BTN_HOVER = "#2a2a4e"

PROGRESS_BG = "#161b22"
PROGRESS_FILL = FG_GREEN


def apply_theme(widget, font_size=None):
    if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
        widget.configure(bg=BG_DARK)
    elif isinstance(widget, tk.Frame):
        widget.configure(bg=BG_DARK)
    elif isinstance(widget, tk.Label):
        widget.configure(bg=BG_DARK, fg=FG_WHITE,
                         font=(FONT_FAMILY, font_size or FONT_SIZE))
    elif isinstance(widget, tk.Button):
        widget.configure(bg=BTN_BG, fg=BTN_FG, activebackground=BTN_HOVER,
                         activeforeground=FG_WHITE, relief=tk.FLAT,
                         font=(FONT_FAMILY, font_size or FONT_SIZE),
                         cursor="hand2", bd=0, padx=16, pady=8)
    elif isinstance(widget, tk.Text):
        widget.configure(bg=BG_TERMINAL, fg=FG_GREEN,
                         insertbackground=FG_GREEN,
                         font=(FONT_FAMILY, font_size or FONT_SIZE),
                         relief=tk.FLAT, bd=0, highlightthickness=0)
    elif isinstance(widget, tk.Entry):
        widget.configure(bg=BG_TERMINAL, fg=FG_GREEN,
                         insertbackground=FG_GREEN,
                         font=(FONT_FAMILY, font_size or FONT_SIZE),
                         relief=tk.FLAT, bd=0, highlightthickness=1,
                         highlightbackground=FG_DIM, highlightcolor=FG_GREEN)
    elif isinstance(widget, tk.Checkbutton):
        widget.configure(bg=BG_DARK, fg=FG_WHITE,
                         selectcolor=BG_TERMINAL,
                         activebackground=BG_DARK,
                         activeforeground=FG_GREEN,
                         font=(FONT_FAMILY, font_size or FONT_SIZE))
    return widget
