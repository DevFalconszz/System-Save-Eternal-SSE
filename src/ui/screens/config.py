import tkinter as tk
from src.ui.terminal import TerminalOutput
from src.ui.styles import (
    BG_DARK, MANTLE, SURFACE0, SURFACE1, SURFACE2,
    FG_GREEN, FG_YELLOW, FG_CYAN, FG_RED, FG_DIM, TEXT,
    FONT_FAMILY, FONT_SIZE,
)
from src.ui.components import make_button, make_label


DEST_FIELDS = {
    "github": [
        ("repo_url", "URL do Reposit\u00f3rio"),
        ("token", "Token de Acesso"),
    ],
    "google_drive": [
        ("client_id", "Client ID"),
        ("client_secret", "Client Secret"),
        ("folder_id", "ID da Pasta (opcional)"),
    ],
    "telegram": [
        ("api_id", "API ID"),
        ("api_hash", "API Hash"),
        ("phone", "Telefone"),
        ("chat_id", "Chat ID (opcional)"),
    ],
}

DEST_LABELS = {
    "github": "GitHub",
    "google_drive": "Google Drive",
    "telegram": "Telegram",
}


SEP = "\u2500" * 50

HELP_TEXTS = {
    "github": (
        "COMO CONFIGURAR O GITHUB\n"
        + SEP + "\n\n"
        + "1. CRIE UM REPOSIT\u00d3RIO NO GITHUB\n\n"
        + "   a. Acesse github.com e fa\u00e7a login na sua conta\n"
        + "   b. Clique no bot\u00e3o verde \"New\" (ou + no canto superior direito \u2192 New repository)\n"
        + "   c. Escolha um nome para o reposit\u00f3rio (ex: meus-saves)\n"
        + "   d. Deixe como p\u00fablico ou privado (recomendado: privado)\n"
        + "   e. N\u00c3O marque \"Initialize this repository with a README\"\n"
        + "   f. Clique em \"Create repository\"\n"
        + "   g. Na p\u00e1gina seguinte, copie a URL do reposit\u00f3rio\n"
        + "      (ex: https://github.com/seuusuario/meus-saves.git)\n\n"
        + "2. CRIE UM TOKEN DE ACESSO PESSOAL\n\n"
        + "   a. Acesse github.com/settings/tokens\n"
        + "   b. Clique em \"Generate new token (classic)\"\n"
        + "   c. D\u00ea um nome para o token (ex: SSE-Backup)\n"
        + "   d. Em Expiration, escolha \"No expiration\" ou um per\u00edodo longo\n"
        + "   e. Em Scopes, marque APENAS a op\u00e7\u00e3o:\n"
        + "      \u2502  repo (controle total de reposit\u00f3rios privados)\n"
        + "   f. Role at\u00e9 o final e clique em \"Generate token\"\n"
        + "   g. COPIE O TOKEN GERADO IMEDIATAMENTE\n"
        + "      (ele s\u00f3 aparece uma vez! Se perder, ter\u00e1 que criar outro)\n"
        + "   h. Cole no campo \"Token de Acesso\" ao lado\n\n"
        + "3. PREENCHENDO OS CAMPOS\n\n"
        + "   \u2022 URL do Reposit\u00f3rio: a URL completa copiada no passo 1g\n"
        + "   \u2022 Token de Acesso: o token copiado no passo 2g\n"
        + "   \u2022 Clique em \"Salvar\" para finalizar\n\n"
        + "PRONTO! Agora o SSE pode fazer backup dos seus saves no GitHub."
    ),
    "google_drive": (
        "COMO CONFIGURAR O GOOGLE DRIVE\n"
        + SEP + "\n\n"
        + "1. CRIE UM PROJETO NO GOOGLE CLOUD\n\n"
        + "   a. Acesse console.cloud.google.com\n"
        + "   b. Fa\u00e7a login com sua conta Google\n"
        + "   c. Se for o primeiro acesso, aceite os termos de servi\u00e7o\n"
        + "   d. No topo ao lado do logotipo, clique no seletor de projetos\n"
        + "   e. Clique em \"NOVO PROJETO\"\n"
        + "   f. D\u00ea um nome (ex: SSE-Backup) e clique em \"Criar\"\n"
        + "   g. Com o projeto selecionado, prossiga para o pr\u00f3ximo passo\n\n"
        + "2. ATIVE A GOOGLE DRIVE API\n\n"
        + "   a. No menu lateral, v\u00e1 em \"APIs e servi\u00e7os\" > \"Biblioteca\"\n"
        + "   b. Pesquise por \"Google Drive API\"\n"
        + "   c. Clique no resultado e depois em \"ATIVAR\"\n"
        + "   d. Aguarde alguns segundos at\u00e9 a API ser ativada\n\n"
        + "3. CRIE AS CREDENCIAIS OAuth 2.0\n\n"
        + "   a. No menu lateral, v\u00e1 em \"APIs e servi\u00e7os\" > \"Credenciais\"\n"
        + "   b. Clique em \"+ CRIAR CREDENCIAIS\" > \"ID do cliente OAuth\"\n"
        + "   c. Se aparecer uma tela de consentimento:\n"
        + "      \u2502  1. Selecione \"Externo\" e clique em \"Criar\"\n"
        + "      \u2502  2. Preencha:\n"
        + "      \u2502     - Nome do app: SSE-Backup\n"
        + "      \u2502     - E-mail de suporte: seu e-mail\n"
        + "      \u2502     - E-mail do desenvolvedor: seu e-mail\n"
        + "      \u2502  3. Clique em \"Salvar e continuar\" at\u00e9 o final\n"
        + "      \u2502  4. Em \"Test users\", clique em \"ADD USERS\"\n"
        + "      \u2502     e adicione seu e-mail pessoal\n"
        + "      \u2502  5. Volte para \"Credenciais\" e tente novamente\n"
        + "   d. Em \"Tipo de aplicativo\", selecione \"App para desktop\"\n"
        + "   e. D\u00ea um nome (ex: SSE-Desktop)\n"
        + "   f. Clique em \"Criar\"\n"
        + "   g. Uma janela aparecer\u00e1 com:\n"
        + "      \u2502  Client ID:一串 caracteres\n"
        + "      \u2502  Client Secret:一串 caracteres\n"
        + "   h. Copie AMBOS e cole nos campos ao lado\n"
        + "   i. Clique em \"BAIXAR JSON\" para ter uma c\u00f3pia de seguran\u00e7a\n\n"
        + "4. OBTER O ID DA PASTA (OPCIONAL)\n\n"
        + "   Se quiser que os saves sejam enviados para uma pasta espec\u00edfica:\n"
        + "   a. Acesse drive.google.com\n"
        + "   b. Crie uma pasta para os backups\n"
        + "   c. Abra a pasta\n"
        + "   d. A URL ser\u00e1 algo como:\n"
        + "      https://drive.google.com/drive/folders/ABC123def456GHI\n"
        + "   e. O ID da pasta \u00e9 a parte ap\u00f3s \"folders/\": ABC123def456GHI\n"
        + "   f. Cole no campo \"ID da Pasta\" (deixe vazio para usar a pasta raiz)\n\n"
        + "5. PRIMEIRO USO\n\n"
        + "   Na primeira vez que o backup rodar:\n"
        + "   a. Seu navegador abrir\u00e1 automaticamente\n"
        + "   b. Fa\u00e7a login na sua conta Google\n"
        + "   c. Aparecer\u00e1 um aviso \"O app n\u00e3o foi verificado\"\n"
        + "      \u2192 Clique em \"Avan\u00e7ado\" > \"Acessar SSE-Backup\"\n"
        + "   d. Permita as permiss\u00f5es solicitadas\n"
        + "   e. Pronto! O token ser\u00e1 salvo automaticamente\n\n"
        + "PRONTO! Agora o SSE pode fazer backup dos seus saves no Google Drive."
    ),
    "telegram": (
        "COMO CONFIGURAR O TELEGRAM\n"
        + SEP + "\n\n"
        + "1. OBTENHA O API ID E API HASH\n\n"
        + "   a. Acesse my.telegram.org\n"
        + "   b. Fa\u00e7a login com seu n\u00famero de telefone\n"
        + "   c. Voc\u00ea receber\u00e1 um c\u00f3digo de verifica\u00e7\u00e3o no Telegram\n"
        + "   d. Ap\u00f3s login, clique em \"API Development Tools\"\n"
        + "   e. Se for a primeira vez:\n"
        + "      \u2502  Preencha:\n"
        + "      \u2502  - App title: SSE-Backup\n"
        + "      \u2502  - Short name: SSEBackup\n"
        + "      \u2502  - URL: (deixe em branco)\n"
        + "      \u2502  - Platform: Desktop\n"
        + "      \u2502  - Description: Backup de saves de jogos\n"
        + "      \u2502  Clique em \"Create application\"\n"
        + "   f. Voc\u00ea ver\u00e1:\n"
        + "      \u2502  App api_id: 1234567 (n\u00famero)\n"
        + "      \u2502  App api_hash: abcdef1234567890abcdef (texto)\n"
        + "   g. COPIE AMBOS e cole nos campos ao lado\n\n"
        + "2. PREENCHA O TELEFONE\n\n"
        + "   a. Use o formato internacional: +55 (Brasil) + DDD + n\u00famero\n"
        + "   b. Exemplos:\n"
        + "      \u2502  +5511999999999 (SP - celular)\n"
        + "      \u2502  +5521988887777 (RJ - celular)\n"
        + "      \u2502  +5541999998888 (PR - celular)\n"
        + "   c. N\u00c3O use espa\u00e7os, tra\u00e7os ou par\u00eanteses\n"
        + "   d. N\u00e3o esque\u00e7a do sinal de + antes do c\u00f3digo do pa\u00eds\n\n"
        + "3. OBTER O CHAT ID (OPCIONAL)\n\n"
        + "   Se quiser enviar para um grupo ou chat espec\u00edfico:\n"
        + "   a. Abra o Telegram e pesquise por @userinfobot\n"
        + "   b. Inicie o bot e envie qualquer mensagem\n"
        + "   c. Ele responder\u00e1 com seu Chat ID (n\u00famero)\n"
        + "   d. Para grupo: adicione o bot ao grupo e envie /start\n"
        + "   e. Se deixar vazio, o backup ser\u00e1 enviado para \"Saved Messages\"\n\n"
        + "4. PRIMEIRO USO\n\n"
        + "   Na primeira vez que o backup rodar:\n"
        + "   a. O programa pedir\u00e1 um c\u00f3digo de verifica\u00e7\u00e3o\n"
        + "   b. Voc\u00ea receber\u00e1 o c\u00f3digo no Telegram\n"
        + "   c. Digite o c\u00f3digo quando solicitado\n"
        + "   d. Se tiver verifica\u00e7\u00e3o em duas etapas, digite a senha\n"
        + "   e. Pronto! A sess\u00e3o ser\u00e1 salva para pr\u00f3ximos usos\n\n"
        + "PRONTO! Agora o SSE pode enviar seus saves pelo Telegram."
    ),
}


class HelpDialog(tk.Toplevel):
    def __init__(self, parent, dest_key):
        super().__init__(parent)
        self.title(f"Ajuda - {DEST_LABELS[dest_key]}")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        title_bar = tk.Frame(self, bg=MANTLE, height=36)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(title_bar, text=f"Ajuda: {DEST_LABELS[dest_key]}",
                 font=(FONT_FAMILY, 11, "bold"),
                 fg=FG_YELLOW, bg=MANTLE).pack(side=tk.LEFT, padx=12)

        tk.Button(title_bar, text="[✕]", font=(FONT_FAMILY, 9, "bold"),
                  fg=FG_RED, bg=MANTLE, activeforeground=FG_RED,
                  activebackground=SURFACE0, relief=tk.FLAT, bd=0, padx=8,
                  cursor="hand2", command=self.destroy).pack(side=tk.RIGHT)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        inner = tk.Frame(body, bg=SURFACE0)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        canvas = tk.Canvas(inner, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(inner, orient=tk.VERTICAL,
                                 bg=SURFACE1, troughcolor=BG_DARK,
                                 activebackground=FG_GREEN,
                                 elementborderwidth=0,
                                 width=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.configure(command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        text_frame = tk.Frame(canvas, bg=BG_DARK)
        canvas_window = canvas.create_window((0, 0), window=text_frame, anchor="nw")

        lines = HELP_TEXTS[dest_key].split("\n")
        for line in lines:
            if not line.strip():
                tk.Label(text_frame, text=" ",
                         font=(FONT_FAMILY, 9),
                         fg=TEXT, bg=BG_DARK).pack(fill=tk.X)
                continue

            is_header = line.startswith("COMO")
            is_section = line.startswith(tuple(str(i) + "." for i in range(1, 10)))
            is_substep = line.strip().startswith("\u2502")
            is_bullet = line.strip().startswith("\u2022")
            is_separator = line.startswith("\u2500")

            if is_header:
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 13, "bold"),
                         fg=FG_YELLOW, bg=BG_DARK,
                         anchor="w").pack(fill=tk.X, pady=(8, 2))
            elif is_separator:
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 9),
                         fg=FG_DIM, bg=BG_DARK).pack(fill=tk.X)
            elif is_section:
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 10, "bold"),
                         fg=FG_CYAN, bg=BG_DARK,
                         anchor="w").pack(fill=tk.X, pady=(4, 0))
            elif is_substep:
                fg_color = FG_GREEN if "\u2502" in line else TEXT
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 9),
                         fg=fg_color,
                         bg=BG_DARK, anchor="w").pack(fill=tk.X, padx=(16, 0))
            elif is_bullet:
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 9),
                         fg=FG_GREEN, bg=BG_DARK,
                         anchor="w").pack(fill=tk.X, padx=(8, 0))
            else:
                tk.Label(text_frame, text=line,
                         font=(FONT_FAMILY, 9),
                         fg=TEXT, bg=BG_DARK,
                         anchor="w").pack(fill=tk.X, padx=(4, 0))

        tk.Label(text_frame, text=" ",
                 font=(FONT_FAMILY, 9),
                 fg=TEXT, bg=BG_DARK).pack(fill=tk.X)

        def _configure_text_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        text_frame.bind("<Configure>", _configure_text_frame)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=canvas.winfo_width()))

        _on_mousewheel = lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.protocol("WM_DELETE_WINDOW", lambda: (canvas.unbind_all("<MouseWheel>"), self.destroy()))
        self.bind("<Escape>", lambda e: (canvas.unbind_all("<MouseWheel>"), self.destroy()))

        self.update_idletasks()
        pw = parent.winfo_rootx()
        ph = parent.winfo_rooty()
        pww = parent.winfo_width()
        phh = parent.winfo_height()
        w = min(600, pww - 40)
        h = min(520, phh - 40)
        self.geometry(f"{w}x{h}+{pw + (pww - w) // 2}+{ph + (phh - h) // 2}")

    def destroy(self):
        try:
            self.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()


class ConfigScreen(tk.Frame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        hdr = tk.Frame(self, bg=MANTLE, height=44)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        make_label(hdr, "\u2699  Configura\u00e7\u00e3o de Destinos",
                   fg=FG_YELLOW, bg=MANTLE, font_size=12, bold=True
                   ).pack(side=tk.LEFT, padx=16)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        self.terminal = TerminalOutput(body, height=5)
        self.terminal.pack(fill=tk.X, pady=(0, 6))

        self._current_dest = tk.StringVar(value="github")

        tabs = tk.Frame(body, bg=BG_DARK)
        tabs.pack(fill=tk.X, pady=(0, 6))

        self._tab_btns = {}
        for dest, label in (
            ("github", "GitHub"),
            ("google_drive", "Google Drive"),
            ("telegram", "Telegram"),
        ):
            row = tk.Frame(tabs, bg=BG_DARK)
            row.pack(side=tk.LEFT, padx=3)

            btn = tk.Button(row, text=label,
                            font=(FONT_FAMILY, FONT_SIZE, "bold"),
                            fg=FG_GREEN, bg=SURFACE0,
                            activeforeground=FG_GREEN, activebackground=SURFACE1,
                            relief=tk.FLAT, bd=0, padx=12, pady=4, cursor="hand2",
                            command=lambda d=dest: self._switch_dest(d))
            btn.pack(side=tk.LEFT)
            self._tab_btns[dest] = btn

            help_btn = tk.Button(row, text="?",
                                 font=(FONT_FAMILY, FONT_SIZE, "bold"),
                                 fg=FG_YELLOW, bg=SURFACE2,
                                 activeforeground=FG_YELLOW, activebackground=SURFACE1,
                                 relief=tk.FLAT, bd=0, padx=6, pady=4, cursor="hand2",
                                 command=lambda d=dest: HelpDialog(self, d))
            help_btn.pack(side=tk.LEFT, padx=(2, 0))

        self._form_container = tk.Frame(body, bg=BG_DARK)
        self._form_container.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self._field_widgets = {}

        actions = tk.Frame(body, bg=BG_DARK)
        actions.pack(fill=tk.X, side=tk.BOTTOM)

        make_button(actions, "Salvar", fg=FG_GREEN, bg=SURFACE0,
                    font_size=11, bold=True, padx=14, pady=4,
                    command=self._save_config
                    ).pack(side=tk.LEFT, padx=(0, 8))

        make_button(actions, "Limpar", fg=FG_RED, bg=SURFACE0,
                    font_size=11, bold=True, padx=14, pady=4,
                    command=self._clear_dest
                    ).pack(side=tk.LEFT, padx=(0, 8))

        make_button(actions, "Ajuda Completa", fg=FG_YELLOW, bg=SURFACE0,
                    font_size=11, bold=True, padx=14, pady=4,
                    command=lambda: HelpDialog(self, self._current_dest.get())
                    ).pack(side=tk.LEFT, padx=(0, 8))

        back_btn = tk.Button(
            actions, text="\u2190  Voltar",
            font=(FONT_FAMILY, 10, "bold"),
            fg=FG_DIM, bg=SURFACE0,
            activeforeground=TEXT, activebackground=SURFACE1,
            relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
            command=on_back,
        )
        back_btn.pack(side=tk.LEFT)
        back_btn.bind("<Enter>", lambda e: back_btn.configure(
            highlightthickness=2, highlightbackground=FG_CYAN))
        back_btn.bind("<Leave>", lambda e: back_btn.configure(
            highlightthickness=0))

        self._build_form("github")

    def _switch_dest(self, dest):
        self._current_dest.set(dest)
        for d, btn in self._tab_btns.items():
            btn.configure(bg=SURFACE1 if d == dest else SURFACE0)
        self._build_form(dest)

    def _build_form(self, dest):
        for w in self._form_container.winfo_children():
            w.destroy()
        self._field_widgets.clear()

        from src.utils import config as cfg
        saved = cfg.load_config().get(dest, {})

        fields = DEST_FIELDS[dest]
        configured = any(v for v in saved.values() if v)

        status_text = "Configurado" if configured else "N\u00e3o configurado"
        status_color = FG_GREEN if configured else FG_RED

        status_frame = tk.Frame(self._form_container, bg=BG_DARK)
        status_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(status_frame, text="Status:",
                 font=(FONT_FAMILY, FONT_SIZE, "bold"),
                 fg=TEXT, bg=BG_DARK).pack(side=tk.LEFT)
        tk.Label(status_frame, text=status_text,
                 font=(FONT_FAMILY, FONT_SIZE, "bold"),
                 fg=status_color, bg=BG_DARK).pack(side=tk.LEFT, padx=(6, 0))

        for key, label in fields:
            row = tk.Frame(self._form_container, bg=BG_DARK)
            row.pack(fill=tk.X, pady=3)

            tk.Label(row, text=label,
                     font=(FONT_FAMILY, FONT_SIZE),
                     fg=FG_CYAN, bg=BG_DARK, width=22, anchor="w"
                     ).pack(side=tk.LEFT)

            current_value = saved.get(key, "")
            display_value = str(current_value) if current_value else ""

            if "token" in key or "secret" in key or "hash" in key:
                entry = tk.Entry(row, width=40, bg=BG_DARK,
                                 fg=FG_GREEN, insertbackground=FG_GREEN,
                                 font=(FONT_FAMILY, FONT_SIZE),
                                 relief=tk.FLAT, bd=0, highlightthickness=1,
                                 highlightbackground=SURFACE1, highlightcolor=FG_GREEN,
                                 show="*")
            else:
                entry = tk.Entry(row, width=40, bg=BG_DARK,
                                 fg=FG_GREEN, insertbackground=FG_GREEN,
                                 font=(FONT_FAMILY, FONT_SIZE),
                                 relief=tk.FLAT, bd=0, highlightthickness=1,
                                 highlightbackground=SURFACE1, highlightcolor=FG_GREEN)

            entry.insert(0, display_value)
            entry.pack(side=tk.LEFT, padx=(0, 6), fill=tk.X, expand=True)

            if display_value and ("token" in key or "secret" in key or "hash" in key):
                show_btn = tk.Button(row, text="Mostrar",
                                     font=(FONT_FAMILY, 9),
                                     fg=FG_DIM, bg=SURFACE0,
                                     activeforeground=TEXT, activebackground=SURFACE1,
                                     relief=tk.FLAT, bd=0, padx=6, pady=1,
                                     cursor="hand2",
                                     command=lambda e=entry, b=None: self._toggle_show(e, b))
                show_btn.pack(side=tk.LEFT)

            help_btn = tk.Button(row, text="?",
                                 font=(FONT_FAMILY, 9, "bold"),
                                 fg=FG_YELLOW, bg=SURFACE2,
                                 activeforeground=FG_YELLOW, activebackground=SURFACE1,
                                 relief=tk.FLAT, bd=0, padx=5, pady=0,
                                 cursor="hand2",
                                 command=lambda d=dest: HelpDialog(self, d))
            help_btn.pack(side=tk.LEFT)

            entry.takefocus = True
            self._field_widgets[key] = entry

        if self._field_widgets:
            first = next(iter(self._field_widgets.values()))
            first.focus_set()

        self.terminal.clear()
        self.terminal.write((f"Status: {status_text}\n", "info" if not configured else "ok"))

    def _toggle_show(self, entry, btn):
        if entry.cget("show") == "*":
            entry.configure(show="")
            if btn:
                btn.configure(text="Ocultar")
        else:
            entry.configure(show="*")
            if btn:
                btn.configure(text="Mostrar")

    def _save_config(self):
        from src.utils import config as cfg
        dest = self._current_dest.get()
        saved = cfg.load_config().get(dest, {})
        has_existing = any(v for v in saved.values() if v)

        updated = {}
        for key, _ in DEST_FIELDS[dest]:
            val = self._field_widgets[key].get().strip()
            if key == "api_id" and val:
                updated[key] = int(val)
            else:
                updated[key] = val

        filled = any(v for v in updated.values() if v)
        if not filled:
            self.terminal.write(("\n! Preencha pelo menos um campo antes de salvar.\n", "error"))
            return

        if has_existing and updated == saved:
            self.terminal.write(("\nNenhuma altera\u00e7\u00e3o detectada.\n", "info"))
            return

        full_cfg = cfg.load_config()
        full_cfg[dest] = updated
        cfg.save_config(full_cfg)

        action = "atualizadas" if has_existing else "salvas"
        self.terminal.write((f"\nConfigura\u00e7\u00f5es de {DEST_LABELS[dest]} {action} com sucesso!\n", "ok"))

        self._build_form(dest)

    def _clear_dest(self):
        from src.ui.dialog import SSEDialog
        from src.utils import config as cfg

        dest = self._current_dest.get()
        saved = cfg.load_config().get(dest, {})
        if not any(v for v in saved.values() if v):
            self.terminal.write((f"\n{DEST_LABELS[dest]} j\u00e1 est\u00e1 vazio.\n", "info"))
            return

        if not SSEDialog.confirm(self, "Limpar",
                                  f"Limpar todos os dados de {DEST_LABELS[dest]}?"):
            return

        full_cfg = cfg.load_config()
        full_cfg[dest] = {k: (0 if k == "api_id" else "") for k, _ in DEST_FIELDS[dest]}
        cfg.save_config(full_cfg)

        self.terminal.write((f"\nConfigura\u00e7\u00f5es de {DEST_LABELS[dest]} removidas.\n", "warn"))
        self._build_form(dest)
