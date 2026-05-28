<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Plataforma-Windows-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square">
</p>

# System Save Eternal — Windows

Esta branch contém documentação específica para Windows. **O código principal está na branch `main`.**

## Uso Rápido

```powershell
git checkout main
python src\main.py
```
Ou use `sse.bat` (duplo clique).

## Launcher no Windows

O SSE detecta automaticamente estes launchers no Windows:

| Launcher | Binário |
|----------|---------|
| SKLauncher | `SKLauncher.exe` |
| Prism Launcher | `PrismLauncher.exe` |
| MultiMC | `MultiMC.exe` |
| Vanilla | `MinecraftLauncher.exe` |
| ATLauncher | `ATLauncher.exe` |

### Localização dos Saves

| Jogo | Diretório |
|------|-----------|
| Minecraft | `%APPDATA%\.minecraft\saves\` |
| Pokémon (DeSmuME) | `%APPDATA%\DeSmuME\` |
| Pokémon (MelonDS) | `%APPDATA%\melonDS\` |
| Pokémon (RetroArch) | `%APPDATA%\RetroArch\saves\` |
| Pokémon (No\$GBA) | `%USERPROFILE%\.no$gba\` |

## Instalação

```powershell
git clone https://github.com/DevFalconszz/System-Save-Eternal-SSE.git
cd System-Save-Eternal-SSE
git checkout main

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src\main.py
```

## Atalho

Use `sse.bat` incluso no projeto.
