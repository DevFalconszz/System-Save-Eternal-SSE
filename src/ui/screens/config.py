import tkinter as tk
from src.ui.terminal import TerminalOutput
from src.ui.styles import (
    BG_DARK, FG_GREEN, FG_YELLOW, FG_CYAN, FG_RED,
    FONT_FAMILY, FONT_SIZE, apply_theme
)


class ConfigScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        header = tk.Label(self, text="Configuração de Destinos",
                          font=("Courier", 14, "bold"),
                          fg=FG_YELLOW, bg=BG_DARK)
        header.pack(pady=(10, 5))

        self.terminal = TerminalOutput(self, height=10)
        self.terminal.pack(fill=tk.X, padx=10, pady=5)

        notebook_frame = tk.Frame(self, bg=BG_DARK)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = tk.Frame(notebook_frame, bg=BG_DARK)
        btn_frame.pack(pady=5)

        self._current_dest = tk.StringVar(value="github")

        for i, (dest, label) in enumerate([
            ("github", "GitHub"),
            ("google_drive", "Google Drive"),
            ("telegram", "Telegram"),
        ], 1):
            btn = tk.Radiobutton(
                btn_frame, text=f"[{i}] {label}",
                variable=self._current_dest,
                value=dest,
                font=(FONT_FAMILY, FONT_SIZE),
                command=self._show_config_help
            )
            apply_theme(btn)
            btn.pack(side=tk.LEFT, padx=10)

        self._show_config_help()

        form_frame = tk.Frame(self, bg=BG_DARK)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Campo:",
                 font=(FONT_FAMILY, FONT_SIZE), fg=FG_CYAN,
                 bg=BG_DARK).pack(side=tk.LEFT)

        self.field_entry = tk.Entry(form_frame, width=50)
        apply_theme(self.field_entry)
        self.field_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        tk.Label(form_frame, text="Valor:",
                 font=(FONT_FAMILY, FONT_SIZE), fg=FG_CYAN,
                 bg=BG_DARK).pack(side=tk.LEFT)

        self.value_entry = tk.Entry(form_frame, width=50)
        apply_theme(self.value_entry)
        self.value_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        action_frame = tk.Frame(self, bg=BG_DARK)
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="Salvar",
                  command=self._save_field,
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=5)

        tk.Button(action_frame, text="Voltar", command=on_back,
                  font=("Courier", 11)).pack(side=tk.LEFT, padx=20)

    def _show_config_help(self):
        self.terminal.clear()
        dest = self._current_dest.get()
        helps = {
            "github": (
                "GitHub — Configuração\n\n"
                "Campos disponíveis:\n"
                "  repo_url  → URL do repositório (ex: https://github.com/user/repo.git)\n"
                "  token     → Personal Access Token (escopo: repo)\n\n"
                "Como criar um token:\n"
                "  1. Acesse github.com/settings/tokens\n"
                "  2. Generate new token (classic)\n"
                "  3. Marque escopo 'repo'\n"
                "  4. Copie o token gerado"
            ),
            "google_drive": (
                "Google Drive — Configuração\n\n"
                "Campos disponíveis:\n"
                "  client_id     → Client ID do OAuth 2.0\n"
                "  client_secret → Client Secret\n"
                "  folder_id     → ID da pasta (opcional)\n\n"
                "Como obter:\n"
                "  1. Acesse console.cloud.google.com\n"
                "  2. Crie projeto → Google Drive API\n"
                "  3. Credenciais → OAuth 2.0 → Desktop app\n"
                "  4. Baixe o JSON com as credenciais"
            ),
            "telegram": (
                "Telegram — Configuração\n\n"
                "Campos disponíveis:\n"
                "  api_id    → API ID do Telegram\n"
                "  api_hash  → API Hash\n"
                "  phone     → Telefone (+5511999999999)\n"
                "  chat_id   → Chat ID (opcional, padrão: Saved Messages)\n\n"
                "Como obter:\n"
                "  1. Acesse my.telegram.org\n"
                "  2. Login → API Development Tools\n"
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
        self.terminal.write((f"\n✓ {key} salvo com sucesso!\n", "ok"))
        self.field_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
