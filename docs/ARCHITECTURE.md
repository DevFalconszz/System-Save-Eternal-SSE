# 🏗️ Arquitetura do SSE

> Documentação técnica da arquitetura do System Save Eternal

---

## Visão Geral

O SSE é um sistema modular com 4 camadas principais: **Interface**, **Detectores**, **Savers** e **Utilitários**. Cada camada é independente e pode ser estendida sem afetar as demais.

```
┌─────────────────────────────────────────────────────┐
│                   INTERFACE                          │
│  ┌─────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │  GUI    │  │   CLI    │  │  Terminal Widget   │  │
│  │(Tkinter)│  │(colorama)│  │  (Tkinter custom)  │  │
│  └────┬────┘  └────┬─────┘  └─────────┬──────────┘  │
│       └────────────┼──────────────────┘              │
│                    ▼                                 │
│              ┌──────────┐                            │
│              │  main.py │  ← dispatch                │
│              └────┬─────┘                            │
├───────────────────┼─────────────────────────────────┤
│                   ▼                                  │
│  ┌──────────────────────────────────────────────┐   │
│  │              CORE (LÓGICA)                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │ Games    │  │ Launcher │  │  Savers    │  │   │
│  │  │ Finder   │  │ Detector │  │ (Git/Drive/│  │   │
│  │  │          │  │          │  │  Telegram) │  │   │
│  │  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │   │
│  │       └─────────────┼──────────────┘          │   │
│  │                     ▼                          │   │
│  │              ┌──────────┐                      │   │
│  │              │  Utils   │                      │   │
│  │              │ (Config, │                      │   │
│  │              │  Files,  │                      │   │
│  │              │ Platform)│                      │   │
│  │              └──────────┘                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Módulos

### 1. Interface (`src/ui/` e `src/console/`)

| Módulo | Função |
|--------|--------|
| `src/ui/app.py` | App Tkinter principal (loop de eventos) |
| `src/ui/terminal.py` | Widget customizado que imita terminal (texto, barra de progresso, input) |
| `src/ui/styles.py` | Tema retrô: cores verde neon, fundo preto, fonte monospace |
| `src/ui/screens/welcome.py` | Tela inicial com menu de opções |
| `src/ui/screens/backup.py` | Fluxo completo de backup com progresso |
| `src/ui/screens/play.py` | Modo jogar Minecraft com monitoramento |
| `src/ui/screens/config.py` | Configuração dos destinos de backup |
| `src/console/menu.py` | Interface CLI tradicional com colorama |

**Fluxo de dispatch em `src/main.py`:**

```python
def main():
    try:
        import tkinter
        from src.ui.app import run_gui  # Tenta GUI
        run_gui()
    except ImportError:
        cli_main()  # Fallback para CLI
```

### 2. Games (`src/games/`)

```
GameFinder (ABC)
  ├── MinecraftFinder
  │   ├── find_saves() → List[SaveEntry]
  │   ├── _get_save_dirs_linux()
  │   └── _get_save_dirs_windows()
  └── PokemonFinder
      ├── find_saves() → List[SaveEntry]
      ├── _system_wide_search()
      └── _detect_pokemon_game()
```

**Como adicionar um novo jogo:**

1. Crie `src/games/novo_jogo.py`
2. Estenda `GameFinder`
3. Implemente `find_saves()` e `name()`
4. Registre no menu em `src/console/menu.py`

### 3. Launcher (`src/launcher/`)

```
LauncherInfo (dataclass)
  ├── name: str
  ├── binary_path: str
  ├── game_dir: str
  └── icon: str

detect_launchers() → List[LauncherInfo]
  ├── SKLAUNCHER
  ├── Prism Launcher
  ├── MultiMC
  ├── Minecraft Launcher
  ├── ATLauncher
  ├── GDLauncher
  └── CurseForge

launch_and_monitor(launcher, pre_cb, post_cb) → bool
find_instance_dirs(launcher) → List[str]
```

### 4. Savers (`src/savers/`)

```
Saver (ABC)
  ├── GitHubSaver
  │   ├── save() → git add + commit + push
  │   └── pull() → git pull --rebase
  ├── GoogleDriveSaver
  │   └── save() → upload via pydrive2
  └── TelegramSaver
      └── save() → upload via Telethon
```

**Como adicionar um novo destino:**

1. Crie `src/savers/novo_saver.py`
2. Estenda `Saver`
3. Implemente `save()`, `name()`, `configure()`
4. Registre em `src/console/menu.py` e/ou `src/ui/screens/config.py`

### 5. Utilitários (`src/utils/`)

| Módulo | Função |
|--------|--------|
| `config.py` | Gerenciamento de config.json (load/save/get/set) |
| `file_utils.py` | Busca de arquivos, tamanho, formatação |
| `platform.py` | Detecção de SO (Linux/Windows/Android), paths |

---

## 🔄 Fluxo de Dados

### Backup de Saves

```
Usuário → seleciona jogo e saves
         → GameFinder.find_saves()
         → List[SaveEntry] retornada
         → Usuário confirma seleção
         → sync_to_repo() copia saves para repositório local
         → Para cada destino configurado:
             → Saver.save(files, metadata)
```

### Modo Jogar Minecraft

```
Usuário → "Jogar Minecraft"
         → detect_launchers()
         → LauncherInfo encontrado
         → GitHubSaver.pull() (se configurado)
         → sync_worlds_to_launcher() (rsync repo → launcher)
         → launch_and_monitor()
             → abre o jogo
             → aguarda fechar (ou Ctrl+C)
             → callback post_exit → sync_worlds_to_repo()
             → GitHubSaver.save() (se configurado)
             → Savers extras (Drive/Telegram)
```

---

## 🔒 Segurança

| Prática | Detalhes |
|---------|----------|
| **Tokens** | Armazenados apenas localmente em `~/.config/sse/config.json` |
| **.gitignore** | `config.json` não é versionado |
| **Escopo mínimo** | GitHub: só escopo `repo`; Telegram: só Saved Messages |
| **Transparência** | Toda ação que modifica o sistema requer confirmação explícita |
| **Sessões** | Sessão do Telegram salva em `~/.config/sse/telegram.session` |

---

## 🧪 Extensibilidade

### Adicionar novo jogo

```python
from src.games.base import GameFinder, SaveEntry

class MeuJogoFinder(GameFinder):
    def name(self) -> str:
        return "Meu Jogo"

    def find_saves(self) -> List[SaveEntry]:
        # Lógica de detecção aqui
        return []
```

### Adicionar novo destino

```python
from src.savers.base import Saver

class MeuSaver(Saver):
    def name(self) -> str:
        return "Meu Serviço"

    def configure(self, cfg: dict) -> bool:
        # Configuração
        return True

    def save(self, file_paths: List[str], metadata: dict) -> bool:
        # Lógica de upload aqui
        return True
```

---

## 📦 Build e Distribuição

### PyInstaller (Standalone)

```
requirements-build.txt
  ├── pyinstaller>=6.0.0
  └── -r requirements.txt

scripts/build.sh
  ├── pyinstaller --onefile
  ├── --collect-all colorama, telethon, pydrive2
  └── Gera dist/SSE (Linux) ou dist/SSE.exe (Windows)
```

### Distribuição

| Método | Prós | Contras |
|--------|------|---------|
| Executável (PyInstaller) | Zero dependências | Arquivo grande (~25MB) |
| Via Python + pip | Mais leve | Requer Python |
| Script de instalação | Automático | Depende de shell |

---

## 📱 Android

O SSE pode rodar no Android via Termux. Consulte o guia completo em [`ANDROID.md`](ANDROID.md).

**Limitações no Android:**
- Não suporta Modo Jogar (Minecraft) — apenas backup de saves
- Detecta saves de RetroArch, Drastic, Pizza Boy e outros emuladores
- GitHub e Google Drive funcionam normalmente
- Telegram funciona via Termux
