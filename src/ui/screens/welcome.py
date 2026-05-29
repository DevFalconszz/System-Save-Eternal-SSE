import tkinter as tk
import os

from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_CYAN, FG_YELLOW, FG_DIM, TEXT,
    FONT_FAMILY,
)
from src.ui.components import HoverCard, make_label


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, on_backup, on_play, on_config, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # ── Hero ──
        hero = tk.Frame(self, bg=MANTLE, height=170)
        hero.pack(fill=tk.X)
        hero.pack_propagate(False)

        banner_path = os.path.join(PROJECT_DIR, "SYSTEM-SAVE-ETERNAL-SSE.png")
        if os.path.exists(banner_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(banner_path)
                img = img.resize((460, 96), Image.LANCZOS)
                self._banner_img = ImageTk.PhotoImage(img)
                tk.Label(hero, image=self._banner_img, bg=MANTLE).pack(expand=True)
            except Exception:
                self._fallback_banner(hero)
        else:
            self._fallback_banner(hero)

        # ── Tags ──
        tags = tk.Frame(self, bg=BG_DARK)
        tags.pack(fill=tk.X, padx=28, pady=(12, 4))

        for icon, text in (
            ("\U0001F427", "Linux"),
            ("\U0001FA9F", "Windows"),
            ("\U0001F4F1", "Android"),
            ("\u2601", "GitHub / Drive / TG"),
            ("\U0001F504", "Auto-sync"),
        ):
            tag = tk.Label(tags, text=f" {icon} {text} ",
                           font=(FONT_FAMILY, 9),
                           fg=FG_DIM, bg=SURFACE0, padx=6, pady=2)
            tag.pack(side=tk.LEFT, padx=3)

        # ── Cards ──
        cards_frame = tk.Frame(self, bg=BG_DARK)
        cards_frame.pack(expand=True, pady=(8, 0), fill=tk.BOTH)

        card_configs = [
            ("\U0001F4E6", "BACKUP  de Saves", FG_GREEN,
             "Detecta Minecraft e Pok\u00e9mon\ne envia para a nuvem",
             on_backup),
            ("\U0001F3AE", "JOGAR  Minecraft", FG_CYAN,
             "Launcher + sync autom\u00e1tico\nantes e depois de jogar",
             on_play),
            ("\u2699", "CONFIG  Destinos", FG_YELLOW,
             "GitHub, Google Drive e Telegram\nconfigure suas chaves",
             on_config),
        ]

        for emoji, title, color, desc, cmd in card_configs:
            self._build_card(cards_frame, emoji, title, color, desc, cmd)

        # ── Footer ──
        make_label(self, "Feito com \U0001F4BE  para preservar o que importa.",
                   fg=FG_DIM, font_size=9
                   ).pack(side=tk.BOTTOM, pady=8)

    def _fallback_banner(self, parent):
        lines = [
            ("\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557", FG_GREEN),
            ("\u2551     SYSTEM SAVE ETERNAL  ~  SSE     \u2551", FG_GREEN),
            ("\u2551    Backup Inteligente de Saves      \u2551", FG_CYAN),
            ("\u2559\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255C", FG_GREEN),
        ]
        for text, color in lines:
            tk.Label(parent, text=text, font=(FONT_FAMILY, 11, "bold"),
                     fg=color, bg=MANTLE).pack()

    def _build_card(self, parent, emoji, title, color, desc, command):
        card = HoverCard(parent, command=command)
        card.pack(pady=4, padx=22, fill=tk.X)

        body = card.body()

        emoji_lbl = tk.Label(body, text=emoji, font=(FONT_FAMILY, 20),
                             fg=color, bg=SURFACE0)
        emoji_lbl.pack(side=tk.LEFT, padx=(0, 12))

        txt_block = tk.Frame(body, bg=SURFACE0)
        txt_block.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(txt_block, text=title,
                 font=(FONT_FAMILY, 12, "bold"),
                 fg=color, bg=SURFACE0, anchor="w"
                 ).pack(fill=tk.X)

        tk.Label(txt_block, text=desc,
                 font=(FONT_FAMILY, 9),
                 fg=FG_DIM, bg=SURFACE0, anchor="w"
                 ).pack(fill=tk.X, pady=(2, 0))

        tk.Button(body, text="\u25B6", font=(FONT_FAMILY, 11, "bold"),
                  fg=color, bg=SURFACE1,
                  activeforeground=color, activebackground=SURFACE2,
                  relief=tk.FLAT, bd=0, padx=8, cursor="hand2",
                  command=command
                  ).pack(side=tk.RIGHT, padx=(8, 0))
