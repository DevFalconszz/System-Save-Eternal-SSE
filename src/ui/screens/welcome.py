import tkinter as tk
import os

from src.ui.styles import (
    BG_DARK, CRUST, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_CYAN, FG_YELLOW, FG_DIM, TEXT,
    FONT_FAMILY, rounded_rect,
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, on_backup, on_play, on_config, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        # ── Hero Banner ──
        hero = tk.Frame(self, bg=MANTLE, height=180)
        hero.pack(fill=tk.X)
        hero.pack_propagate(False)

        # Try to load SSE banner image
        self._banner_img = None
        banner_path = os.path.join(PROJECT_DIR, "SYSTEM-SAVE-ETERNAL-SSE.png")
        if os.path.exists(banner_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(banner_path)
                img = img.resize((480, 100), Image.LANCZOS)
                self._banner_img = ImageTk.PhotoImage(img)
                tk.Label(hero, image=self._banner_img,
                         bg=MANTLE).pack(expand=True)
            except Exception:
                self._fallback_banner(hero)
        else:
            self._fallback_banner(hero)

        # ── Info bar ──
        info = tk.Frame(self, bg=BG_DARK)
        info.pack(fill=tk.X, padx=30, pady=(14, 6))

        for icon, text in (
            ("🐧", "Linux"),
            ("🪟", "Windows"),
            ("📱", "Android"),
            ("☁", "GitHub / Drive / Telegram"),
            ("🔄", "Auto-sync"),
        ):
            tag = tk.Label(info, text=f" {icon} {text} ",
                           font=(FONT_FAMILY, 9),
                           fg=FG_DIM, bg=SURFACE0, padx=6, pady=2)
            tag.pack(side=tk.LEFT, padx=3)

        # ── Cards ──
        cards = tk.Frame(self, bg=BG_DARK)
        cards.pack(expand=True, pady=(10, 0))

        card_data = [
            ("📦", "BACKUP", "de Saves", FG_GREEN,
             "Detecta Minecraft e Pokemon\ne envia para a nuvem",
             on_backup),
            ("🎮", "JOGAR", "Minecraft", FG_CYAN,
             "Launcher + sync automatico\nantes e depois de jogar",
             on_play),
            ("⚙", "CONFIG", "Destinos", FG_YELLOW,
             "GitHub, Google Drive e Telegram\nconfigure suas chaves",
             on_config),
        ]

        for emoji, title, subtitle, color, desc, cmd in card_data:
            self._build_card(cards, emoji, title, subtitle, color, desc, cmd)

        # ── Footer ──
        tk.Label(self, text="Feito com 💾  para preservar o que importa.",
                 font=(FONT_FAMILY, 9), fg=FG_DIM, bg=BG_DARK
                 ).pack(side=tk.BOTTOM, pady=8)

    def _fallback_banner(self, parent):
        lines = [
            ("╔══════════════════════════════════════╗", FG_GREEN),
            ("║     SYSTEM SAVE ETERNAL  ~  SSE     ║", FG_GREEN),
            ("║    Backup Inteligente de Saves      ║", FG_CYAN),
            ("╚══════════════════════════════════════╝", FG_GREEN),
        ]
        for text, color in lines:
            tk.Label(parent, text=text, font=(FONT_FAMILY, 11, "bold"),
                     fg=color, bg=MANTLE).pack()

    def _build_card(self, parent, emoji, title, subtitle, color, desc, command):
        card = tk.Frame(parent, bg=SURFACE0, bd=0, cursor="hand2")
        card.pack(pady=5, padx=24, fill=tk.X)

        inner = tk.Frame(card, bg=SURFACE0, padx=18, pady=14)
        inner.pack(fill=tk.X)

        # Emoji + Title
        tk.Label(inner, text=emoji, font=(FONT_FAMILY, 22),
                 fg=color, bg=SURFACE0).pack(side=tk.LEFT, padx=(0, 14))

        txt_block = tk.Frame(inner, bg=SURFACE0)
        txt_block.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(txt_block, text=f"{title}  {subtitle}",
                 font=(FONT_FAMILY, 13, "bold"),
                 fg=color, bg=SURFACE0, anchor="w"
                 ).pack(fill=tk.X)

        tk.Label(txt_block, text=desc,
                 font=(FONT_FAMILY, 9),
                 fg=FG_DIM, bg=SURFACE0, anchor="w"
                 ).pack(fill=tk.X, pady=(2, 0))

        # Arrow button
        tk.Button(inner, text="▶", font=(FONT_FAMILY, 12, "bold"),
                  fg=color, bg=SURFACE1,
                  activeforeground=color, activebackground=SURFACE2,
                  relief=tk.FLAT, bd=0, padx=10, cursor="hand2",
                  command=command).pack(side=tk.RIGHT, padx=(10, 0))

        # Hover effect
        def on_enter(e, f=SURFACE1): card.configure(bg=f); inner.configure(bg=f)
        for w in (card, inner):
            for c in w.winfo_children():
                try:
                    c.bind("<Enter>", lambda e, f=SURFACE1: on_enter(e, f), add="+")
                    c.bind("<Leave>", lambda e: on_enter(e, SURFACE0), add="+")
                except Exception:
                    pass
            w.bind("<Enter>", lambda e, f=SURFACE1: on_enter(e, f))
            w.bind("<Leave>", lambda e: on_enter(e, SURFACE0))
        for c in inner.winfo_children():
            try:
                c.bind("<Enter>", lambda e, f=SURFACE1: on_enter(e, f), add="+")
                c.bind("<Leave>", lambda e: on_enter(e, SURFACE0), add="+")
            except Exception:
                pass
