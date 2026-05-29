import tkinter as tk
from tkinter import ttk
import queue
import threading

from src.ui.styles import (
    BG_TERMINAL, FG_GREEN, FG_RED, FG_YELLOW, FG_CYAN,
    FG_DIM, FONT_FAMILY, FONT_SIZE, PROGRESS_BG, PROGRESS_FILL, apply_theme
)


class TerminalOutput(tk.Frame):
    def __init__(self, parent, height=20, **kwargs):
        super().__init__(parent, bg=BG_TERMINAL, **kwargs)
        self.text = tk.Text(
            self, height=height,
            wrap=tk.WORD, state=tk.DISABLED,
            padx=12, pady=8
        )
        apply_theme(self.text)
        self.text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            self.text, command=self.text.yview,
            bg=BG_TERMINAL, troughcolor="#161b22",
            activebackground=FG_GREEN
        )
        self.text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._tag_colors = {
            "ok": FG_GREEN,
            "info": FG_CYAN,
            "warn": FG_YELLOW,
            "error": FG_RED,
            "dim": FG_DIM,
        }
        for tag, color in self._tag_colors.items():
            self.text.tag_configure(tag, foreground=color)

        self.tag_configure("bold", font=(FONT_FAMILY, FONT_SIZE, "bold"))

        self.write_queue = queue.Queue()
        self._poll_queue()

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

    def clear(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.configure(state=tk.DISABLED)


class ProgressBar(tk.Canvas):
    def __init__(self, parent, width=400, height=20, **kwargs):
        super().__init__(
            parent, width=width, height=height,
            bg=PROGRESS_BG, highlightthickness=0, **kwargs
        )
        self._bar_width = width - 4
        self._bar = self.create_rectangle(
            2, 2, 2, height - 2,
            fill=PROGRESS_FILL, outline=""
        )
        self._label = self.create_text(
            width // 2, height // 2,
            text="0%", fill=BG_TERMINAL,
            font=(FONT_FAMILY, 9, "bold")
        )

    def set_progress(self, percent):
        w = max(2, int(self._bar_width * percent / 100))
        self.coords(self._bar, 2, 2, 2 + w, int(self.cget("height")) - 2)
        self.itemconfig(self._label, text=f"{percent}%")
        self.update_idletasks()


class InputBar(tk.Frame):
    def __init__(self, parent, on_submit=None, prompt=">>>", **kwargs):
        super().__init__(parent, bg=BG_TERMINAL, **kwargs)
        self.prompt_label = tk.Label(self, text=f" {prompt} ", fg=FG_GREEN,
                                     bg=BG_TERMINAL,
                                     font=(FONT_FAMILY, FONT_SIZE))
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self, bg=BG_TERMINAL, fg=FG_GREEN,
                              insertbackground=FG_GREEN,
                              font=(FONT_FAMILY, FONT_SIZE),
                              relief=tk.FLAT, bd=0, highlightthickness=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self._submit())

        self._on_submit = on_submit

    def _submit(self):
        if self._on_submit:
            self._on_submit(self.entry.get())

    def focus(self):
        self.entry.focus_set()

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tk.END)
