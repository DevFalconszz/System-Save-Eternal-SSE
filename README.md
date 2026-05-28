<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Plataforma-Linux-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square">
</p>

# System Save Eternal — Linux

Esta branch contém documentação específica para Linux. **O código principal está na branch `main`.**

## Uso Rápido

```bash
git checkout main
python3 src/main.py
```

## Launcher no Linux

O SSE detecta automaticamente estes launchers no Linux:

| Launcher | Binário |
|----------|---------|
| SKLauncher | `sklauncher`, `~/SKLauncher/SKLauncher.jar` |
| Prism Launcher | `prismlauncher` |
| MultiMC | `multimc` |
| Vanilla | `minecraft-launcher` |
| ATLauncher | `ATLauncher` |

### Localização dos Saves

| Jogo | Diretório |
|------|-----------|
| Minecraft | `~/.minecraft/saves/` |
| Pokémon (DeSmuME) | `~/.config/desmume/` |
| Pokémon (MelonDS) | `~/.local/share/melonDS/` |
| Pokémon (RetroArch) | `~/.config/retroarch/saves/` |

## Instalação

```bash
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE
git checkout main

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

## Atalho

```bash
chmod +x src/main.py
ln -s "$(pwd)/src/main.py" ~/.local/bin/sse
sse
```