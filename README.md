<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Plataforma-Linux%20%7C%20Windows-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Licença-MIT-green?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square">
</p>

---

## System Save Eternal — CLI

**System Save Eternal (SSE)** é um sistema inteligente de backup e versionamento de saves de jogos, rodando diretamente no terminal. Ele localiza automaticamente seus saves, oferece opções interativas de seleção, e envia para os destinos que você escolher.

### Arquitetura

O SSE-CLI é a ferramenta pública que gerencia os backups. Seus saves ficam em um **repositório privado separado**:

```
┌─────────────────────────────────────────────┐
│  System-Save-Eternal-SSE (PÚBLICO)          │
│  ├── src/   → Código do sistema de backup   │
│  ├── config.json → Suas configurações       │
│  └── README.md    → Documentação            │
│  Função: Gerenciar os backups               │
└─────────────────────────────────────────────┘
         │ git push / Google Drive / Telegram
         ▼
┌─────────────────────────────────────────────┐
│  System-Save-Eternal (PRIVADO)              │
│  ├── Minecraft/   → Saves, mods, config     │
│  ├── Pokemon-Black-White/ → Saves, ROM      │
│  └── .git/   → Histórico versionado         │
│  Função: Armazenar os saves                 │
└─────────────────────────────────────────────┘
```

**Suporta 3 destinos de backup simultâneos:**
- **GitHub** → `git add + commit + push` para seu repositório privado
- **Google Drive** → Upload via API do Google Drive (pydrive2)
- **Telegram** → Upload via MTProto (Telethon) para Saved Messages

---

## Índice

- [Instalação](#instalação)
- [Uso](#uso)
- [Games Suportados](#games-suportados)
  - [Minecraft](#-minecraft)
  - [Pokémon](#-pokémon)
- [Destinos de Backup](#destinos-de-backup)
  - [GitHub](#github)
  - [Google Drive](#google-drive)
  - [Telegram](#telegram)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Branches](#branches)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Instalação

### Pré-requisitos

- Python 3.8+
- Git
- Pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE

# 2. (Opcional) Crie um virtualenv
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute
python3 src/main.py
```

---

## Uso

O SSE-CLI é totalmente interativo pelo terminal:

```bash
python3 src/main.py
```

Ou, se preferir instalar como comando global:

```bash
# Crie um link simbólico
chmod +x src/main.py
ln -s "$(pwd)/src/main.py" ~/.local/bin/sse

# Agora pode chamar de qualquer lugar
sse
```

### Primeira execução

Na primeira execução, o SSE vai perguntar:

1. **Caminho do repositório de saves** — Onde seus saves serão armazenados localmente
2. **Qual jogo** — Minecraft ou Pokémon
3. **Qual(is) save(s)** — Selecione um ou mais mundos/arquivos
4. **Destino(s)** — Marque GitHub, Google Drive e/ou Telegram
5. **Configuração** — Token, credenciais, etc. (só na primeira vez, salvo em `~/.config/sse/config.json`)

---

## Games Suportados

### ⛏ Minecraft

O SSE varre automaticamente os diretórios padrão do Minecraft:

| Sistema | Localização |
|---------|-------------|
| Linux   | `~/.minecraft/saves/` |
| Linux (Snap) | `~/snap/minecraft/common/.minecraft/saves/` |
| Linux (XDG)  | `~/.local/share/minecraft/saves/` |

Para cada mundo encontrado (identificado por `level.dat`), exibe o nome, tamanho e caminho. Você pode selecionar quantos mundos quiser.

### 🐉 Pokémon (Black & White / DS)

O SSE busca inteligentemente por saves de emuladores Nintendo DS no sistema:

| Emulador | Extensões | Localização típica (Linux) |
|----------|-----------|---------------------------|
| **DeSmuME** | `.dsv`, `.sav` | `~/.config/desmume/` |
| **MelonDS** | `.sav`, `.dsv` | `~/.local/share/melonDS/` |
| **RetroArch** | `.sav`, `.dsv`, `.state` | `~/.config/retroarch/saves/` |
| **mGBA** | `.sav` | `~/.config/mgba/` |

Se nenhum save for encontrado nos diretórios padrão, o SSE faz uma varredura em `/home`, `/mnt`, e `/media` procurando por arquivos com padrões como `pokemon`, `black`, `white`, `pkmn`, etc.

---

## Destinos de Backup

### GitHub

O SSE usa `git push` para enviar seus saves para um repositório no GitHub.

**Setup interativo:**

Na primeira vez, o SSE pergunta:

1. **Você já tem um repositório?** → Se sim, informe a URL. Se não, um guia passo a passo é exibido para criar um repositório **privado** no GitHub.
2. **Personal Access Token** → Necessário para autenticar. O SSE guia para criar em:  
   `Settings → Developer Settings → Personal Access Tokens → Tokens (classic)`  
   Escopo mínimo: `repo` (controle total de repositórios privados).
3. Salva as credenciais em `~/.config/sse/config.json`.

### Google Drive

O SSE usa `pydrive2` para fazer upload para o Google Drive.

**Setup:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto e habilite a **Google Drive API**
3. Crie credenciais OAuth 2.0 do tipo "Desktop app"
4. Informe Client ID e Client Secret quando o SSE pedir
5. Na primeira execução, o navegador abrirá para autenticação OAuth (salva em `~/.config/sse/gdrive_settings.yaml`)

### Telegram

O SSE usa [Telethon](https://github.com/LonamiWebs/Telethon) para enviar arquivos via MTProto.

**Setup:**
1. Acesse [my.telegram.org](https://my.telegram.org)
2. Crie um aplicativo em "API Development Tools"
3. Informe `api_id` e `api_hash` quando solicitado
4. Na primeira execução, o SSE pedirá seu número de telefone + código de verificação
5. Os saves são enviados para **Saved Messages** (ou um chat específico se configurado)

---

## Estrutura do Projeto

```
System-Save-Eternal-SSE/
├── src/
│   ├── main.py                  # Entry point
│   ├── console/
│   │   └── menu.py              # Interface de terminal interativa
│   ├── games/
│   │   ├── base.py              # Classe abstrata GameFinder
│   │   ├── minecraft.py         # Detecção de saves do Minecraft
│   │   └── pokemon.py           # Detecção de saves de Pokémon
│   ├── savers/
│   │   ├── base.py              # Classe abstrata Saver
│   │   ├── github_saver.py      # Backup via Git/GitHub
│   │   ├── googledrive_saver.py # Backup via Google Drive API
│   │   └── telegram_saver.py    # Backup via Telegram MTProto
│   └── utils/
│       ├── file_utils.py        # Utilitários de busca de arquivos
│       └── config.py            # Gerenciamento de configuração
├── config.json                  # Configurações (template)
├── requirements.txt             # Dependências Python
└── README.md                   # Documentação
```

---

## Branches

| Branch | Descrição |
|--------|-----------|
| `main` | Documentação geral, README |
| `linux` | Implementação para Linux (paths, emuladores) |
| `windows` | Implementação para Windows (paths, emuladores) |

---

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

---

<p align="center">
  <sub>Feito com 💾 para preservar o que importa.</sub>
</p>
