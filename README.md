<p align="center">
  <img src="icoico.png" width="140" alt="SSE Logo">
</p>

<p align="center">
  <img src="SYSTEM-SAVE-ETERNAL-SSE.png" width="427" alt="SYSTEM SAVE ETERNAL">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Plataforma-Linux%20%7C%20Windows%20%7C%20Android-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square">
</p>

---

**System Save Eternal (SSE)** é um sistema inteligente de backup e versionamento de saves de jogos. Funciona em **Linux**, **Windows** e **Android** (Termux) com uma única base de código. Ele detecta automaticamente seu sistema operacional, localiza saves de Minecraft e Pokémon DS, e envia para **múltiplos destinos simultaneamente** — GitHub, Google Drive e Telegram.

O SSE oferece **duas interfaces**:

| Interface | Descrição |
|-----------|-----------|
| 🖥️ **GUI Terminal-like** | Interface gráfica Tkinter que imita um terminal retrô (verde neon / fundo preto) |
| ⌨️ **CLI clássica** | Terminal tradicional com menus, cores e checkboxes |

> A interface GUI é a padrão. Se o Tkinter não estiver disponível, o SSE cai automaticamente para o modo CLI.

---

## 🔥 Destaques

| Recurso | Detalhes |
|---------|----------|
| 🎮 **Minecraft** | Detecta todos os mundos em qualquer launcher |
| 🐉 **Pokémon DS** | Varre emuladores e o sistema atrás de saves |
| 🚀 **Modo Jogar** | Abre o launcher, monitora, sincroniza antes/depois |
| ☁️ **3 Destinos Simultâneos** | GitHub + Google Drive + Telegram |
| 🔐 **Configuração Guiada** | Passo a passo para cada destino |
| 🧩 **Multi-plataforma** | Código único que se adapta ao SO |
| 📱 **Android (Termux)** | Scripts e documentação para celular |
| ⚡ **Executável Standalone** | PyInstaller gera .exe / binário único |
| 🔒 **Transparência Total** | Explica cada ação antes de executar |

---

## 📦 Instalação

### 🐧 Linux

#### Opção 1: Executável Standalone (recomendado)

```bash
# Baixe o executável da página de releases
chmod +x SSE
./SSE
```

> Não requer Python nem dependências — arquivo único.

#### Opção 2: Via Python

```bash
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE

# Instalação automática
chmod +x scripts/install.sh
./scripts/install.sh

# Ou manualmente:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

**Atalho:** `./sse.sh`

### 🪟 Windows

#### Opção 1: Executável Standalone (recomendado)

```powershell
# Baixe o SSE.exe da página de releases
# Apenas execute o arquivo — sem instalação necessária
```

#### Opção 2: Via Python

```powershell
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE

# Instalação automática (PowerShell como Admin)
powershell -ExecutionPolicy Bypass .\scripts\install.ps1

# Ou manualmente:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src\main.py
```

**Atalho:** duplo clique em `sse.bat`

### 📱 Android (Termux)

> SSE pode rodar no Android via [Termux](https://termux.dev). Consulte [`docs/ANDROID.md`](docs/ANDROID.md) para o guia completo.

```bash
pkg install python git
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE
pip install -r requirements.txt
python src/main.py
```

---

## 🎮 Modos de Uso

### Opção 1: Backup de Saves

Fluxo completo: escolhe o jogo, seleciona os saves, escolhe os destinos e faz o backup.

```
[1] Fazer backup de saves
    │
    ├─ Minecraft → lista mundos de ~/.minecraft/saves/
    │              (ou %APPDATA%\.minecraft\saves\ no Windows)
    │
    └─ Pokémon  → varre emuladores (DeSmuME, MelonDS, RetroArch, mGBA, No$GBA)
                   + varredura no sistema inteiro
```

### Opção 2: Jogar Minecraft com Sincronização Automática

Fluxo completo: detecta o launcher, puxa saves do GitHub, abre o jogo, monitora e salva ao fechar.

```
[2] Jogar Minecraft com sincronização automática
    │
    ├─ 1. Detecta launcher instalado
    │     (SKLauncher, Prism, MultiMC, Vanilla, ATLauncher...)
    │
    ├─ 2. Pull dos saves do GitHub
    ├─ 3. Rsync saves → launcher
    ├─ 4. Abre o jogo 🎮
    ├─ 5. Monitora o processo
    ├─ 6. Quando fecha → rsync → repositório local
    ├─ 7. Git push para GitHub
    └─ 8. Opcional: backup extra (Drive / Telegram)
```

---

## 🎮 Games Suportados

### ⛏ Minecraft

| Sistema | Localizações buscadas |
|---------|----------------------|
| **Linux** | `~/.minecraft/saves/`, `~/.local/share/minecraft/saves/`, `~/snap/minecraft/common/.minecraft/saves/` |
| **Windows** | `%APPDATA%\.minecraft\saves\`, `%USERPROFILE%\.minecraft\saves\` |

#### Launchers

| Launcher | Linux | Windows |
|----------|-------|---------|
| **SKLauncher** | ✅ | ✅ |
| **Prism Launcher** | ✅ | ✅ |
| **MultiMC** | ✅ | ✅ |
| **Minecraft Launcher** | ✅ | ✅ |
| **ATLauncher** | ✅ | ✅ |
| **GDLauncher** | ✅ | ✅ |
| **CurseForge** | ✅ | ✅ |

### 🐉 Pokémon (Black & White / DS)

| Emulador | Extensões | Linux | Windows |
|----------|-----------|-------|---------|
| **DeSmuME** | `.dsv`, `.sav` | ✅ | ✅ |
| **MelonDS** | `.sav`, `.dsv` | ✅ | ✅ |
| **RetroArch** | `.sav`, `.dsv`, `.state` | ✅ | ✅ |
| **No$GBA** | `.sav` | — | ✅ |
| **mGBA** | `.sav` | ✅ | ✅ |

---

## ☁️ Destinos de Backup

### GitHub

`git add + commit + push` para seu repositório privado de saves.

**Requisitos:** Token de acesso pessoal (escopo: `repo`)

### Google Drive

Upload via `pydrive2` com autenticação OAuth 2.0.

**Requisitos:** Credenciais da Google Cloud Console (Desktop app)

### Telegram

Upload para **Saved Messages** via API MTProto (Telethon).

**Requisitos:** `api_id` e `api_hash` do [my.telegram.org](https://my.telegram.org)

---

## 🏗️ Arquitetura

```
┌──────────────────────────────────────────────────────┐
│  📦 System-Save-Eternal-SSE (PÚBLICO)                 │
│  ├── src/           → Código do sistema              │
│  │   ├── ui/        → Interface gráfica (Tkinter)    │
│  │   ├── console/   → Interface de terminal (CLI)    │
│  │   ├── games/     → Detectores de saves            │
│  │   ├── savers/    → Destinos de backup             │
│  │   ├── launcher/  → Detectores de launcher         │
│  │   └── utils/     → Utilitários                    │
│  ├── scripts/       → Instaladores e build           │
│  ├── docs/          → Documentação adicional          │
│  └── README.md      → Esta documentação              │
│  Função: Gerenciar os backups                        │
└──────────────┬───────────────────────────────────────┘
               │ git push / Google Drive / Telegram
               ▼
┌──────────────────────────────────────────────────────┐
│  🔒 System-Save-Eternal (PRIVADO)                     │
│  ├── Minecraft/     → Saves, mods, config            │
│  ├── Pokemon-Black-White/ → Saves, ROM               │
│  └── .git/          → Histórico versionado           │
│  Função: Armazenar os saves                          │
└──────────────────────────────────────────────────────┘
```

> 📖 Consulte [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) para documentação técnica detalhada.

---

## 📁 Estrutura do Projeto

```
System-Save-Eternal-SSE/
├── src/
│   ├── main.py                  # Entry point (GUI + CLI dispatch)
│   ├── ui/                      # Interface gráfica Tkinter
│   │   ├── app.py               # App principal
│   │   ├── terminal.py          # Widget terminal customizado
│   │   ├── styles.py            # Tema retrô (cores, fontes)
│   │   └── screens/             # Telas da aplicação
│   │       ├── welcome.py       # Tela inicial
│   │       ├── backup.py        # Fluxo de backup
│   │       ├── play.py          # Modo jogar
│   │       └── config.py        # Configuração
│   ├── console/                 # Modo CLI
│   │   └── menu.py              # Interface de terminal
│   ├── games/
│   │   ├── base.py              # Classe abstrata GameFinder
│   │   ├── minecraft.py         # Detecção Minecraft
│   │   └── pokemon.py           # Detecção Pokémon
│   ├── launcher/
│   │   └── minecraft_launcher.py # Detecção + monitoramento
│   ├── savers/
│   │   ├── base.py              # Classe abstrata Saver
│   │   ├── github_saver.py      # Backup via GitHub
│   │   ├── googledrive_saver.py # Backup via Google Drive
│   │   └── telegram_saver.py    # Backup via Telegram
│   └── utils/
│       ├── config.py            # Gerenciamento de config
│       ├── file_utils.py        # Utilitários de busca
│       └── platform.py          # Utilitários de SO
├── scripts/
│   ├── install.sh               # Instalador Linux 🐧
│   ├── install.ps1              # Instalador Windows 🪟
│   └── build.sh                 # Build PyInstaller
├── docs/
│   ├── ARCHITECTURE.md          # Documentação da arquitetura
│   ├── ANDROID.md               # Guia Android 📱
│   └── ICONS.md                 # Guia de ícones
├── sse.bat                      # Atalho Windows
├── sse.sh                       # Atalho Linux
├── setup.py                     # Instalação via pip
├── pyproject.toml               # Build config
├── config.example.json          # Template de configuração
├── requirements.txt             # Dependências
├── requirements-build.txt       # Dependências de build
└── README.md                    # Esta documentação
```

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| Tkinter | padrão | Interface gráfica |
| Colorama | 0.4+ | Cores no terminal |
| GitPython | 3.1+ | Operações Git |
| PyDrive2 | 1.19+ | Google Drive API |
| Telethon | 1.35+ | Telegram MTProto |
| PyInstaller | 6.0+ | Executável standalone |

---

## 🔒 Transparência

O SSE prioriza a transparência com o usuário. Antes de cada ação, uma tela de confirmação explica:

```
⚠  SSE — Cópia de Saves
════════════════════════════════════════════════════
  • 3 save(s) serão copiados para: /mnt/saves/repo
  • Tamanho total: 124.5 MB
  • Os saves originais NÃO serão modificados
  • Apenas uma cópia será feita para o repositório local
════════════════════════════════════════════════════
Deseja continuar? (s/N):
```

---

## 🤝 Contribuição

```bash
git checkout -b feature/nova-feature
git commit -m "feat: descrição clara"
git push origin feature/nova-feature
```

Abra um **Pull Request** para a branch `main`.

---

## 📄 Licença

MIT

---

<p align="center">
  <img src="icoico.png" width="60" alt="SSE">
</p>
<p align="center">
  <sub>Feito com 💾 para preservar o que importa.</sub>
</p>
