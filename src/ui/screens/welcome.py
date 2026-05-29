import tkinter as tk
from src.ui.styles import (
    BG_DARK, FG_GREEN, FG_CYAN, FG_YELLOW, FG_DIM,
    FONT_FAMILY, FONT_SIZE, apply_theme
)


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, on_backup, on_play, on_config, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        banner_lines = [
            ("╔══════════════════════════════════════════════════╗", "green"),
            ("║          SYSTEM SAVE ETERNAL - SSE              ║", "green"),
            ("║     Backup Inteligente de Saves de Jogos        ║", "cyan"),
            ("╚══════════════════════════════════════════════════╝", "green"),
            ("", None),
            ("  Sistema unificado  |  Linux  |  Windows  |  Android", "dim"),
            ("", None),
        ]

        for i, (text, color) in enumerate(banner_lines):
            lbl = tk.Label(
                self, text=text,
                font=(FONT_FAMILY, FONT_SIZE),
                anchor="w"
            )
            if color == "green":
                lbl.configure(fg=FG_GREEN)
            elif color == "cyan":
                lbl.configure(fg=FG_CYAN)
            elif color == "dim":
                lbl.configure(fg=FG_DIM)
            else:
                lbl.configure(fg=FG_GREEN)
            apply_theme(lbl)
            lbl.pack(pady=0 if text else 4)

        self.details = tk.Label(
            self,
            text="",
            font=(FONT_FAMILY, 10),
            fg=FG_YELLOW, bg=BG_DARK,
            wraplength=500, justify="center"
        )
        self.details.pack(pady=(20, 5))

        btn_frame = tk.Frame(self, bg=BG_DARK)
        btn_frame.pack(pady=20)

        btn_backup = tk.Button(
            btn_frame, text="[1] Fazer Backup de Saves",
            font=(FONT_FAMILY, FONT_SIZE + 2),
            command=lambda: self._confirm(on_backup, "Backup de Saves",
                                          "• Detecta automaticamente saves de Minecraft e Pokémon\n"
                                          "• Envia para GitHub, Google Drive e/ou Telegram\n"
                                          "• Mantém versionamento completo dos seus saves")
        )
        apply_theme(btn_backup)
        btn_backup.pack(pady=6, ipadx=24, ipady=6)

        btn_play = tk.Button(
            btn_frame, text="[2] Jogar Minecraft com Sincronização",
            font=(FONT_FAMILY, FONT_SIZE + 2),
            command=lambda: self._confirm(on_play, "Modo Jogar Minecraft",
                                          "• Detecta seu launcher automaticamente\n"
                                          "• Sincroniza saves antes de jogar\n"
                                          "• Monitora o jogo e salva ao fechar\n"
                                          "• Push automático para GitHub")
        )
        apply_theme(btn_play)
        btn_play.pack(pady=6, ipadx=24, ipady=6)

        btn_config = tk.Button(
            btn_frame, text="[3] Configurar Destinos",
            font=(FONT_FAMILY, FONT_SIZE + 2),
            command=on_config
        )
        apply_theme(btn_config)
        btn_config.pack(pady=6, ipadx=24, ipady=6)

        footer = tk.Label(
            self,
            text="Feito com 💾 para preservar o que importa.",
            font=(FONT_FAMILY, 9),
            fg=FG_DIM, bg=BG_DARK
        )
        footer.pack(side=tk.BOTTOM, pady=10)

    def _confirm(self, callback, title, details):
        import tkinter.messagebox as mb
        result = mb.askyesno(
            title=f"SSE — {title}",
            message=f"{details}\n\nDeseja continuar?",
            icon="question"
        )
        if result:
            callback()
