import tkinter as tk
import queue
import math

from src.ui.styles import (
    BG_TERMINAL, BG_DARK, CRUST, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_RED, FG_YELLOW, FG_CYAN, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE, PROGRESS_FILL,
    rounded_rect,
)


class TerminalOutput(tk.Frame):
    def __init__(self, parent, height=20, **kwargs):
        self._radius = 10
        self._bezel = 3
        self._frame_w = 2
        self._pad = 3
        super().__init__(parent, bg=BG_DARK, **kwargs)

        self._canvas = tk.Canvas(
            self, bg=BG_DARK, highlightthickness=0
        )
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.text = tk.Text(
            self, height=height,
            wrap=tk.WORD, state=tk.DISABLED,
            padx=10, pady=6,
            bg=BG_TERMINAL, fg=FG_GREEN,
            insertbackground=FG_GREEN,
            font=(FONT_FAMILY, FONT_SIZE),
            relief=tk.FLAT, bd=0, highlightthickness=0,
            takefocus=0,
        )
        self.text.place(x=0, y=0)

        self.scrollbar = tk.Canvas(
            self.text, width=10, bg=BG_TERMINAL,
            highlightthickness=0, bd=0
        )
        self.text.bind("<Configure>", self._update_scrollbar)

        self._tag_colors = {
            "ok": FG_GREEN,
            "info": FG_CYAN,
            "warn": FG_YELLOW,
            "error": FG_RED,
            "dim": FG_DIM,
        }
        for tag, color in self._tag_colors.items():
            self.text.tag_configure(tag, foreground=color)

        self.text.tag_configure("bold", font=(FONT_FAMILY, FONT_SIZE, "bold"))

        self.write_queue = queue.Queue()
        self._poll_queue()

        self.bind("<Configure>", lambda e: self._draw_border())

    def _draw_border(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 20 or h < 20:
            return
        self._canvas.delete("all")

        bx = self._bezel
        by = self._bezel
        bw = w - 2 * self._bezel - 1
        bh = h - 2 * self._bezel - 1

        # screen border frame
        rounded_rect(
            self._canvas, bx, by, bx + bw, by + bh,
            radius=self._radius,
            fill=BG_TERMINAL, outline=SURFACE1,
            width=self._frame_w,
        )

        inset = self._bezel + self._frame_w + self._pad
        self.text.place_configure(
            x=inset, y=inset,
            width=w - 2 * inset,
            height=h - 2 * inset
        )

    def _update_scrollbar(self, event=None):
        try:
            total = float(self.text.index("end-1c").split(".")[0])
            visible = self.text.winfo_height() // self.text.dlineinfo("1.0")[1] if self.text.dlineinfo("1.0") else 20
            if total <= visible:
                self.scrollbar.place_forget()
                return
            frac = visible / total
            self.scrollbar.place(relx=1.0, rely=0, anchor=tk.NE, relheight=1)
            self.scrollbar.delete("all")
            h = self.scrollbar.winfo_height() * frac
            self.scrollbar.create_rectangle(
                2, 0, 8, h, fill=SURFACE2, outline=""
            )
        except Exception:
            pass

    def _poll_queue(self):
        try:
            while True:
                parts = self.write_queue.get_nowait()
                self._write_parts(parts)
        except queue.Empty:
            pass
        self.after(50, self._poll_queue)

    def write(self, *parts):
        self.write_queue.put(parts)

    def _write_parts(self, parts):
        self.text.configure(state=tk.NORMAL)
        for content, tag in parts:
            if content:
                self.text.insert(tk.END, content, tag if tag else ())
        self.text.see(tk.END)
        self.text.configure(state=tk.DISABLED)
        self._update_scrollbar()

    def clear(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.configure(state=tk.DISABLED)


class ProgressBar(tk.Frame):
    def __init__(self, parent, width=400, height=16, **kwargs):
        self._width = width
        self._height = height
        super().__init__(
            parent, width=width, height=height,
            bg=BG_DARK, **kwargs
        )
        self.pack_propagate(False)

        self._canvas = tk.Canvas(
            self, width=width, height=height,
            bg=BG_DARK, highlightthickness=0
        )
        self._canvas.pack()

        rounded_rect(self._canvas, 0, 0, width, height, radius=height // 2, fill=SURFACE0)
        self._bar_bg = self._canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            fill=SURFACE0, outline=""
        )

        pw = max(4, int((width - 4) * 2 / 100))
        self._bar = self._canvas.create_rectangle(
            2, 2, pw, height - 2,
            fill=PROGRESS_FILL, outline="",
            stipple="" if False else ""
        )

        self._label = self._canvas.create_text(
            width // 2, height // 2,
            text="0%", fill=BG_TERMINAL,
            font=(FONT_FAMILY, 9, "bold")
        )

    def set_progress(self, percent):
        w = max(4, int((self._width - 4) * percent / 100))
        self._canvas.coords(self._bar, 2, 2, w + 2, self._height - 2)
        self._canvas.itemconfig(self._label, text=f"{percent}%")
        self._canvas.update_idletasks()


class InputBar(tk.Frame):
    def __init__(self, parent, on_submit=None, prompt=">>>", **kwargs):
        self._radius = 8
        super().__init__(parent, bg=BG_DARK, **kwargs)

        self._canvas = tk.Canvas(
            self, height=34, bg=BG_DARK,
            highlightthickness=0
        )
        self._canvas.pack(fill=tk.X)

        self._canvas.bind("<Configure>", self._redraw)

        self.prompt_label = tk.Label(
            self._canvas, text=f" {prompt} ", fg=FG_GREEN,
            bg=BG_TERMINAL, font=(FONT_FAMILY, FONT_SIZE)
        )
        self._canvas.create_window(16, 17, window=self.prompt_label, anchor=tk.W)

        self.entry = tk.Entry(
            self._canvas, bg=BG_TERMINAL, fg=FG_GREEN,
            insertbackground=FG_GREEN,
            font=(FONT_FAMILY, FONT_SIZE),
            relief=tk.FLAT, bd=0, highlightthickness=0
        )
        self.entry.bind("<Return>", lambda e: self._submit())
        self.entry.bind("<FocusIn>", lambda e: self._redraw())

        self._on_submit = on_submit

    def _redraw(self, event=None):
        w = self._canvas.winfo_width()
        h = self._canvas.winfo_height()
        if w < 20:
            return
        self._canvas.delete("bg")
        rounded_rect(self._canvas, 0, 0, w, h, radius=self._radius, fill=BG_TERMINAL, outline=SURFACE1)
        pl = self.prompt_label.winfo_reqwidth()
        ew = w - pl - 30
        if ew > 50:
            self._canvas.coords(
                self._canvas.find_withtag("entry")[0] if self._canvas.find_withtag("entry") else None,
                pl + 20, 17
            )
            try:
                self._canvas.delete("entry")
            except Exception:
                pass
            self._canvas.create_window(pl + 20, 17, window=self.entry, anchor=tk.W, tags="entry", width=ew)

    def _submit(self):
        if self._on_submit:
            self._on_submit(self.entry.get())

    def focus(self):
        self.entry.focus_set()

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tk.END)
