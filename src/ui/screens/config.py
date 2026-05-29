import tkinter as tk
from src.ui.terminal import TerminalOutput
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_RED, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE,
)
from src.ui.components import make_button, make_label, HoverCard


class ConfigScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        hdr = tk.Frame(self, bg=MANTLE, height=44)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        make_label(hdr, "\u2699  Configurac\u00e3o de Destinos",
                   fg=FG_YELLOW, bg=MANTLE, font_size=12, bold=True
                   ).pack(side=tk.LEFT, padx=16)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        self.terminal = TerminalOutput(body, height=8)
        self.terminal.pack(fill=tk.X, pady=(0, 6))

        self._current_dest = tk.StringVar(value="github")

        tabs = tk.Frame(body, bg=BG_DARK)
        tabs.pack(fill=tk.X, pady=(0, 6))

        for dest, label in (
            ("github", "GitHub"),
            ("google_drive", "Google Drive"),
            ("telegram", "Telegram"),
        ):
            btn = tk.Button(tabs, text=label,
                            font=(FONT_FAMILY, FONT_SIZE, "bold"),
                            fg=FG_GREEN, bg=SURFACE0,
                            activeforeground=FG_GREEN, activebackground=SURFACE1,
                            relief=tk.FLAT, bd=0, padx=12, pady=4, cursor="hand2",
                            command=lambda d=dest: self._switch_dest(d))
            btn.pack(side=tk.LEFT, padx=3)
            if dest == "github":
                btn.configure(bg=SURFACE1)

        form = tk.Frame(body, bg=BG_DARK)
        form.pack(fill=tk.X, pady=(0, 6))

        tk.Label(form, text="Campo:", font=(FONT_FAMILY, FONT_SIZE),
                 fg=FG_CYAN, bg=BG_DARK).pack(side=tk.LEFT)

        self.field_entry = tk.Entry(form, width=30, bg=BG_DARK, fg=FG_GREEN,
                                     insertbackground=FG_GREEN,
                                     font=(FONT_FAMILY, FONT_SIZE),
                                     relief=tk.FLAT, bd=0, highlightthickness=1,
                                     highlightbackground=SURFACE1, highlightcolor=FG_GREEN)
        self.field_entry.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)

        tk.Label(form, text="Valor:", font=(FONT_FAMILY, FONT_SIZE),
                 fg=FG_CYAN, bg=BG_DARK).pack(side=tk.LEFT, padx=(6, 0))

        self.value_entry = tk.Entry(form, width=30, bg=BG_DARK, fg=FG_GREEN,
                                     insertbackground=FG_GREEN,
                                     font=(FONT_FAMILY, FONT_SIZE),
                                     relief=tk.FLAT, bd=0, highlightthickness=1,
                                     highlightbackground=SURFACE1, highlightcolor=FG_GREEN)
        self.value_entry.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)

        actions = tk.Frame(body, bg=BG_DARK)
        actions.pack(fill=tk.X)

        make_button(actions, "Salvar", fg=FG_GREEN, bg=SURFACE0,
                    font_size=11, bold=True, padx=14, pady=4,
                    command=self._save_field
                    ).pack(side=tk.LEFT, padx=(0, 8))

        make_button(actions, "\u2190 Voltar", fg=FG_CYAN, bg=SURFACE2,
                    font_size=10, bold=True, padx=14, pady=4,
                    command=on_back, side=tk.LEFT)

        self._show_config_help()

    def _switch_dest(self, dest):
        self._current_dest.set(dest)
        for w in self.winfo_children():
            if hasattr(w, "winfo_children"):
                pass
        # Find and update tab buttons
        tabs = self.winfo_children()[2]  # body -> tabs
        for i, (d, _) in enumerate([("github", ""), ("google_drive", ""), ("telegram", "")]):
            btn = tabs.winfo_children()[i] if i < len(tabs.winfo_children()) else None
            if btn:
                btn.configure(bg=SURFACE1 if d == dest else SURFACE0)
        self._show_config_help()

    def _show_config_help(self):
        self.terminal.clear()
        dest = self._current_dest.get()
        helps = {
            "github": (
                "GitHub \u2014 Configurac\u00e3o\n\n"
                "Campos disponiveis:\n"
                "  repo_url  \u2192 URL do repositorio (ex: https://github.com/user/repo.git)\n"
                "  token     \u2192 Personal Access Token (escopo: repo)\n\n"
                "Como criar um token:\n"
                "  1. Acesse github.com/settings/tokens\n"
                "  2. Generate new token (classic)\n"
                "  3. Marque escopo 'repo'\n"
                "  4. Copie o token gerado"
            ),
            "google_drive": (
                "Google Drive \u2014 Configurac\u00e3o\n\n"
                "Campos disponiveis:\n"
                "  client_id     \u2192 Client ID do OAuth 2.0\n"
                "  client_secret \u2192 Client Secret\n"
                "  folder_id     \u2192 ID da pasta (opcional)\n\n"
                "Como obter:\n"
                "  1. Acesse console.cloud.google.com\n"
                "  2. Crie projeto \u2192 Google Drive API\n"
                "  3. Credenciais \u2192 OAuth 2.0 \u2192 Desktop app\n"
                "  4. Baixe o JSON com as credenciais"
            ),
            "telegram": (
                "Telegram \u2014 Configurac\u00e3o\n\n"
                "Campos disponiveis:\n"
                "  api_id    \u2192 API ID do Telegram\n"
                "  api_hash  \u2192 API Hash\n"
                "  phone     \u2192 Telefone (+5511999999999)\n"
                "  chat_id   \u2192 Chat ID (opcional, padrao: Saved Messages)\n\n"
                "Como obter:\n"
                "  1. Acesse my.telegram.org\n"
                "  2. Login \u2192 API Development Tools\n"
                "  3. Crie um app para obter api_id e api_hash"
            ),
        }
        self.terminal.write((helps.get(dest, ""), "info"))

    def _save_field(self):
        from src.utils import config as cfg
        dest = self._current_dest.get()
        field = self.field_entry.get().strip()
        value = self.value_entry.get().strip()

        if not field or not value:
            self.terminal.write(("\n! Preencha ambos os campos.\n", "error"))
            return

        key = f"{dest}.{field}"
        cfg.set_key(key, value)
        self.terminal.write((f"\n{key} salvo com sucesso!\n", "ok"))
        self.field_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
