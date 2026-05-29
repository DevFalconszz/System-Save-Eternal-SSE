# 🎨 Guia de Ícones do SSE

> Este documento lista todos os ícones utilizados no projeto e seus significados.

---

## Ícones de Interface

| Ícone | Significado | Onde aparece |
|-------|-------------|-------------|
| ⚠ | Aviso / Transparência | Telas de confirmação, antes de ações |
| ✔ | Operação concluída com sucesso | Logs, terminal, GUI |
| ✗ | Operação falhou | Logs, terminal, GUI |
| ℹ | Informação | Logs, terminal |
| ▶ | Iniciar / Play | Tela do modo Jogar |
| 📦 | Repositório de saves | README, arquitetura |
| 🔒 | Repositório privado | README, arquitetura |
| 💾 | Disquete (salvar) | Footer do README, branding |
| 🎮 | Jogos | README, documentação |
| ⛏ | Minecraft | README |
| 🐉 | Pokémon | README |
| 🚀 | Modo Jogar / Play | README |
| ☁️ | Destinos de nuvem | Documentação |
| 🧩 | Multi-plataforma | README |
| 🔐 | Segurança / Configuração | README |
| ⚡ | Executável rápido | README |

## Ícones de Plataforma

| Ícone | Plataforma | Código | Onde usar |
|-------|-----------|--------|-----------|
| 🐧 | Linux | `\U0001F427` | README, scripts, docs |
| 🪟 | Windows | `\U0001FA9F` | README, scripts, docs |
| 📱 | Android | `\U0001F4F1` | README, docs/ANDROID.md |
| 🖥️ | Desktop genérico | `\U0001F5A5` | Documentação geral |
| ⌨️ | Modo CLI | | Documentação |

## Ícones de Launcher

| Ícone | Launcher | Código no código |
|-------|----------|-----------------|
| | SKLauncher | (vazio — launcher padrão) |
| 🔮 | Prism Launcher | `icon` field |
| 📦 | MultiMC | `icon` field |
| 🟢 | Minecraft Launcher | `icon` field |
| 🔧 | ATLauncher | `icon` field |
| 💎 | GDLauncher | `icon` field |
| 🔥 | CurseForge | `icon` field |
| ⚙️ | Configuração manual | `_manual_launcher_config` |

## Ícones de Status

| Ícone | Significado | Cor no terminal |
|-------|-------------|----------------|
| ✓ | Sucesso | Verde (`Fore.GREEN`) |
| ✗ | Falha | Vermelho (`Fore.RED`) |
| i | Informação | Ciano (`Fore.CYAN`) |
| › | Prompt de input | Ciano (`Fore.CYAN`) |
| ⚠ | Atenção | Amarelo (`Fore.YELLOW`) |

## Ícones de Destinos

| Ícone | Destino | Código |
|-------|---------|--------|
| | GitHub | `GitHubSaver.name()` |
| 📂 | Google Drive | `GoogleDriveSaver.name()` |
| ✈️ | Telegram | `TelegramSaver.name()` |

## Emojis vs Unicode

Para máxima compatibilidade entre terminais, o SSE usa:

- **Emojis**: em documentação (README, markdown)
- **Unicode/ASCII**: em logs de terminal (✓, ✗, i, ›)
- **Caracteres Unicode**: para ícones de plataforma (🐧 🪟 📱)

### Fallback em terminais sem suporte a emoji

O módulo `src/utils/platform.py` usa caracteres Unicode padrão:

```python
icons = {
    "linux": "\U0001F427",   # 🐧
    "windows": "\U0001FA9F", # 🪟
    "android": "\U0001F4F1", # 📱
    "macos": "\U0001F5A5",   # 🖥️
}
```

## Cores do Tema (Interface Tkinter)

| Elemento | Cor | Código | Uso |
|----------|-----|--------|-----|
| Fundo escuro | `#0a0a0a` | `BG_DARK` | Janela principal |
| Fundo terminal | `#0d1117` | `BG_TERMINAL` | Área de output |
| Verde neon | `#00ff41` | `FG_GREEN` | Texto principal, sucesso, prompt |
| Azul ciano | `#00bfff` | `FG_CYAN` | Informação, dicas |
| Amarelo ouro | `#ffd700` | `FG_YELLOW` | Títulos, avisos |
| Vermelho | `#ff3333` | `FG_RED` | Erros, falhas |
| Branco suave | `#c9d1d9` | `FG_WHITE` | Texto secundário |
| Cinza escuro | `#484f58` | `FG_DIM` | Metadados, detalhes |

## Arquivos de Imagem

| Arquivo | Uso |
|---------|-----|
| `icoico.png` | Logo principal (ícone) |
| `SYSTEM-SAVE-ETERNAL-SSE.png` | Banner do projeto |
| `assets/workflow.svg` | Diagrama de fluxo |
| `assets/icons/sse-icon-256.png` | Ícone para Linux (256x256) |
| `assets/icons/sse-icon.ico` | Ícone para Windows (.ico) |

---

> Para adicionar novos ícones, edite este arquivo e atualize os assets em `assets/icons/`.
