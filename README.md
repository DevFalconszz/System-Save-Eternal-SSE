<p align="center">
  <img src="icoico.png" width="140" alt="SSE Logo">
</p>

<p align="center">
  <img src="SYSTEM-SAVE-ETERNAL-SSE.png" width="427" alt="SYSTEM SAVE ETERNAL">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Plataforma-Linux%20%7C%20Windows-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Licença-MIT-green?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square">
</p>

---

**System Save Eternal (SSE)** é um sistema inteligente de backup e versionamento de saves de jogos que roda diretamente no terminal. Localiza automaticamente seus saves do Minecraft e Pokémon Nintendo DS, oferece seleção interativa com checkboxes, e envia para **múltiplos destinos simultaneamente** — GitHub, Google Drive e Telegram.

![SSE Demo](assets/workflow.svg)

---

## 🔥 Destaques

- 🎮 **Minecraft** — Detecta automaticamente todos os mundos em `~/.minecraft/saves/`
- 🐉 **Pokémon DS** — Varre emuladores (DeSmuME, MelonDS, RetroArch, mGBA) e o sistema inteiro
- ☁️ **3 Destinos Simultâneos** — GitHub, Google Drive e Telegram de uma só vez
- 🔐 **GitHub guiado** — Pergunta se já tem repo ou guia passo a passo para criar um **privado**
- 🧩 **Modular** — Arquitetura limpa e extensível para adicionar novos jogos e destinos
- 🖥️ **Terminal interativo** — Menus, checkboxes e feedback visual com cores

---

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE

# Crie um virtualenv (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute!
python3 src/main.py
```

> 💡 **Dica:** Você pode criar um atalho `sse` no sistema:
> ```bash
> chmod +x src/main.py
> ln -s "$(pwd)/src/main.py" ~/.local/bin/sse
> sse
> ```

---

## 🎮 Games Suportados

### ⛏ Minecraft

O SSE varre automaticamente os diretórios padrão do Minecraft e lista todos os mundos disponíveis:

| Sistema | Localização detectada |
|---------|----------------------|
| **Linux** | `~/.minecraft/saves/` |
| **Linux (Snap)** | `~/snap/minecraft/common/.minecraft/saves/` |
| **Linux (XDG)** | `~/.local/share/minecraft/saves/` |
| **Windows** | `%APPDATA%\.minecraft\saves\` |

**Funcionamento:**
1. Detecta mundos via arquivo `level.dat`
2. Exibe nome, tamanho e caminho de cada mundo
3. Você seleciona quantos mundos quiser (1, 2 ou todos)

### 🐉 Pokémon (Black & White / DS)

Busca inteligente por saves de emuladores Nintendo DS:

| Emulador | Extensões | Linux | Windows |
|----------|-----------|-------|---------|
| **DeSmuME** | `.dsv`, `.sav` | `~/.config/desmume/` | `%APPDATA%\DeSmuME\` |
| **MelonDS** | `.sav`, `.dsv` | `~/.local/share/melonDS/` | `%APPDATA%\melonDS\` |
| **RetroArch** | `.sav`, `.dsv`, `.state` | `~/.config/retroarch/saves/` | `%APPDATA%\RetroArch\saves\` |
| **mGBA** | `.sav` | `~/.config/mgba/` | `%APPDATA%\mgba\` |

Se nenhum save for encontrado nos diretórios padrão, o SSE faz uma **varredura inteligente** em todo o sistema (`/home`, `/mnt`, `/media` no Linux / `C:\Users` no Windows) procurando por arquivos com nomes contendo *pokemon, black, white, pkmn*.

---

## ☁️ Destinos de Backup

Você pode selecionar **múltiplos destinos ao mesmo tempo** usando checkboxes:

```
[✓] GitHub
[✓] Google Drive
[ ] Telegram
```

### <img src="icoico.png" width="20" height="20"> GitHub

O sistema faz `git add + commit + push` para seu repositório **privado** de saves.

**Na primeira configuração, o SSE pergunta:**
1. **Já tem um repositório?** → Se sim, informe a URL
2. **Não tem?** → Guia passo a passo exibido no terminal:
   - Acesse `https://github.com/new`
   - Crie um repositório **PRIVADO**
   - NÃO marque "Add README"
   - Cole a URL gerada
3. **Token de acesso** → Guia para criar Personal Access Token em:
   `Settings → Developer Settings → Personal Access Tokens → Tokens (classic)`
   Escopo mínimo: **`repo`** (controle total)
4. Salva tudo em `~/.config/sse/config.json`

### <img src="icoico.png" width="20" height="20"> Google Drive

Upload via Google Drive API usando `pydrive2`.

**Setup:** 1. Google Cloud Console → 2. Criar projeto → 3. Habilitar Google Drive API → 4. Credenciais OAuth 2.0 (Desktop app) → 5. Informar Client ID e Secret

### <img src="icoico.png" width="20" height="20"> Telegram

Upload via [Telethon](https://github.com/LonamiWebs/Telethon) (MTProto) para **Saved Messages**.

**Setup:** 1. Acesse [my.telegram.org](https://my.telegram.org) → 2. API Development Tools → 3. Informar `api_id`, `api_hash` e telefone

---

## 🏗️ Arquitetura

A arquitetura é dividida em **2 repositórios**:

```
┌──────────────────────────────────────────────────┐
│  📦 System-Save-Eternal-SSE (PÚBLICO)             │
│  ├── src/           → Código do sistema          │
│  ├── config.json    → Suas configurações          │
│  └── README.md      → Documentação               │
│  Função: Gerenciar os backups                    │
└──────────────┬───────────────────────────────────┘
               │ git push / Google Drive / Telegram
               ▼
┌──────────────────────────────────────────────────┐
│  🔒 System-Save-Eternal (PRIVADO)                 │
│  ├── Minecraft/   → Saves, mods, config          │
│  ├── Pokemon-Black-White/ → Saves, ROM           │
│  └── .git/        → Histórico versionado         │
│  Função: Armazenar os saves                      │
└──────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
System-Save-Eternal-SSE/
├── src/
│   ├── main.py                  # Entry point
│   ├── console/
│   │   └── menu.py              # Interface de terminal
│   ├── games/
│   │   ├── base.py              # Classe abstrata GameFinder
│   │   ├── minecraft.py         # Detecção de saves Minecraft
│   │   └── pokemon.py           # Detecção de saves Pokémon
│   ├── savers/
│   │   ├── base.py              # Classe abstrata Saver
│   │   ├── github_saver.py      # Backup via GitHub
│   │   ├── googledrive_saver.py # Backup via Google Drive
│   │   └── telegram_saver.py    # Backup via Telegram
│   └── utils/
│       ├── file_utils.py        # Utilitários de busca
│       └── config.py            # Gerenciamento de config
├── config.example.json          # Template de configuração
├── requirements.txt             # Dependências
├── icoico.png                   # Ícone do projeto
├── SYSTEM-SAVE-ETERNAL-SSE.png  # Banner do projeto
└── README.md                   # Documentação
```

---

## 🧪 Fluxo de Uso

```
┌─────────────────────────────────────────────────────┐
│  python3 src/main.py                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Informar caminho do repositório de saves        │
│     (ex: /mnt/dados/System-Save-Eternal)            │
│                                                     │
│  2. Escolher o jogo:                                │
│     (1) Minecraft                                   │
│     (2) Pokémon                                     │
│                                                     │
│  3. Selecionar saves (checkboxes):                  │
│     [✓] Mundo Eterno                                │
│     [ ] Outro Mundo                                 │
│                                                     │
│  4. Escolher destino(s):                            │
│     [✓] GitHub                                      │
│     [ ] Google Drive                                │
│     [✓] Telegram                                    │
│                                                     │
│  5. Configurar cada destino (primeira vez)          │
│                                                     │
│  6. ✅ Backup concluído!                            │
└─────────────────────────────────────────────────────┘
```

---

## 🌿 Branches

| Branch | Descrição | Status |
|--------|-----------|--------|
| `main` | Documentação geral e visão do projeto | ✅ |
| `linux` | Implementação completa para Linux | ✅ |
| `windows` | Implementação adaptada para Windows | ✅ |

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| Colorama | 0.4+ | Cores no terminal |
| GitPython | 3.1+ | Operações Git |
| PyDrive2 | 1.19+ | Google Drive API |
| Telethon | 1.35+ | Telegram MTProto |
| Cryptg | 0.4+ | Aceleração cripto do Telegram |

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga o padrão:

```bash
git checkout -b feature/minha-feature
git commit -m "feat: descrição clara do que foi feito"
git push origin feature/minha-feature
```

Abra um **Pull Request** para a branch `main`.

---

## 📄 Licença

Distribuído sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

<p align="center">
  <img src="icoico.png" width="60" alt="SSE">
</p>
<p align="center">
  <sub>Feito com 💾 para preservar o que importa.</sub>
</p>
