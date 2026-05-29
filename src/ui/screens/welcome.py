import tkinter as tk
from src.ui.styles import (
    BG_DARK, CRUST, SURFACE0, SURFACE1,
    FG_GREEN, FG_CYAN, FG_YELLOW, FG_DIM, TEXT, FG_BLUE,
    FONT_FAMILY, FONT_SIZE, rounded_rect,
)


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, on_backup, on_play, on_config, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        # ── Banner ──
        banner_frame = tk.Frame(self, bg=BG_DARK)
        banner_frame.pack(pady=(30, 10))

        lines = [
            ("╭─────────────────────────────────────────────╮", FG_GREEN),
            ("│           SYSTEM SAVE ETERNAL               │", FG_GREEN),
            ("│               ~  SSE  ~                     │", FG_CYAN),
            ("╰─────────────────────────────────────────────╯", FG_GREEN),
        ]
        for text, color in lines:
            lbl = tk.Label(banner_frame, text=text, font=(FONT_FAMILY, FONT_SIZE),
                           fg=color, bg=BG_DARK)
            lbl.pack()

        # ── Subtitle ──
        tk.Label(
            banner_frame,
            text="Backup inteligente de saves  •  Linux  🐧  Windows  🪟  Android  📱",
            font=(FONT_FAMILY, 10),
            fg=FG_DIM, bg=BG_DARK
        ).pack(pady=(6, 0))

        # ── Center content ──
        center = tk.Frame(self, bg=BG_DARK)
        center.pack(expand=True)

        btns = [
            ("[1]  Fazer Backup de Saves", FG_GREEN,
             lambda: self._confirm(on_backup, "Backup de Saves",
                                   " Detecta automaticamente saves de Minecraft e Pokemon\n"
                                   " Envia para GitHub, Google Drive e/ou Telegram\n"
                                   " Mantem versionamento completo dos seus saves")),
            ("[2]  Jogar Minecraft c/ Sincronizacao", FG_CYAN,
             lambda: self._confirm(on_play, "Modo Jogar Minecraft",
                                   " Detecta seu launcher automaticamente\n"
                                   " Sincroniza saves antes de jogar\n"
                                   " Monitora o jogo e salva ao fechar\n"
                                   " Push automatico para GitHub")),
            ("[3]  Configurar Destinos", FG_YELLOW, on_config),
        ]

        for text, color, cmd in btns:
            btn = tk.Button(
                center, text=text,
                font=(FONT_FAMILY, 12, "bold"),
                fg=color, bg=SURFACE0,
                activeforeground=color, activebackground=SURFACE1,
                relief=tk.FLAT, bd=0, padx=28, pady=10, cursor="hand2",
                command=cmd
            )
            btn.pack(pady=6, ipadx=20)

        # ── Footer ──
        tk.Label(
            self, text="Feito com 💾  para preservar o que importa.",
            font=(FONT_FAMILY, 9), fg=FG_DIM, bg=BG_DARK
        ).pack(side=tk.BOTTOM, pady=12)

    def _confirm(self, callback, title, details):
        import tkinter.messagebox as mb
        result = mb.askyesno(
            title=f"SSE — {title}",
            message=f"{details}\n\nDeseja continuar?",
            icon="question"
        )
        if result:
            callback()
