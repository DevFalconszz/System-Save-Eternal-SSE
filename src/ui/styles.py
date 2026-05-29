import tkinter as tk

# ── Catppuccin Mocha Palette ──
BASE     = "#1e1e2e"
MANTLE   = "#181825"
CRUST    = "#11111b"
SURFACE0 = "#313244"
SURFACE1 = "#45475a"
SURFACE2 = "#585b70"
OVERLAY0 = "#6c7086"
OVERLAY1 = "#7f849c"
SUBTEXT0 = "#a6adc8"
SUBTEXT1 = "#bac2de"
TEXT     = "#cdd6f4"
LAVENDER = "#b4befe"
BLUE     = "#89b4fa"
SAPPHIRE = "#74c7ec"
SKY      = "#89dceb"
TEAL     = "#94e2d5"
GREEN    = "#a6e3a1"
YELLOW   = "#f9e2af"
PEACH    = "#fab387"
MAROON   = "#eba0ac"
RED      = "#f38ba8"
MAUVE    = "#cba6f7"
PINK     = "#f5c2e7"
FLAMINGO = "#f2cdcd"
ROSEWATER= "#f5e0dc"

# ── Semantic Aliases ──
BG_DARK      = BASE
BG_TERMINAL  = CRUST
FG_GREEN     = GREEN
FG_CYAN      = SKY
FG_YELLOW    = YELLOW
FG_RED       = RED
FG_WHITE     = TEXT
FG_DIM       = OVERLAY0
FG_BLUE      = BLUE
FG_LAVENDER  = LAVENDER
FG_PEACH     = PEACH

FONT_FAMILY = "Courier"
FONT_SIZE = 11

BTN_BG       = SURFACE0
BTN_FG       = GREEN
BTN_HOVER    = SURFACE1

PROGRESS_BG  = SURFACE0
PROGRESS_FILL = GREEN

BORDER_RADIUS = 12


def apply_theme(widget, font_size=None):
    fs = font_size or FONT_SIZE
    if isinstance(widget, (tk.Tk, tk.Toplevel)):
        widget.configure(bg=BG_DARK)
    elif isinstance(widget, tk.Frame):
        widget.configure(bg=BG_DARK)
    elif isinstance(widget, tk.Label):
        widget.configure(bg=BG_DARK, fg=FG_WHITE, font=(FONT_FAMILY, fs))
    elif isinstance(widget, tk.Button):
        widget.configure(
            bg=BTN_BG, fg=BTN_FG, activebackground=BTN_HOVER,
            activeforeground=FG_WHITE, relief=tk.FLAT,
            font=(FONT_FAMILY, fs),
            cursor="hand2", bd=0, padx=16, pady=8
        )
    elif isinstance(widget, tk.Text):
        widget.configure(
            bg=BG_TERMINAL, fg=FG_GREEN,
            insertbackground=FG_GREEN,
            font=(FONT_FAMILY, fs),
            relief=tk.FLAT, bd=0, highlightthickness=0
        )
    elif isinstance(widget, tk.Entry):
        widget.configure(
            bg=BG_TERMINAL, fg=FG_GREEN,
            insertbackground=FG_GREEN,
            font=(FONT_FAMILY, fs),
            relief=tk.FLAT, bd=0, highlightthickness=1,
            highlightbackground=SURFACE1, highlightcolor=FG_GREEN
        )
    elif isinstance(widget, tk.Checkbutton):
        widget.configure(
            bg=BG_DARK, fg=FG_WHITE, selectcolor=BG_TERMINAL,
            activebackground=BG_DARK, activeforeground=FG_GREEN,
            font=(FONT_FAMILY, fs)
        )
    return widget


def rounded_rect(canvas, x1, y1, x2, y2, radius=12, fill=BASE, outline=None):
    points = []
    for coord in [
        (x1 + radius, y1, x2 - radius, y1),
        (x2, y1 + radius, x2, y2 - radius),
        (x2 - radius, y2, x1 + radius, y2),
        (x1, y2 - radius, x1, y1 + radius),
    ]:
        points.extend(coord)
    return canvas.create_polygon(
        points, smooth=True, fill=fill,
        outline=outline or fill, width=1
    )
