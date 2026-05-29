#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# SSE — Build de Executável Standalone (PyInstaller)
# ═══════════════════════════════════════════════════════════
# Gera um único executável que não requer Python instalado.
# Linux: dist/SSE
# Windows: dist/SSE.exe (via cross-compile ou no Windows)
# ═══════════════════════════════════════════════════════════
set -euo pipefail

SSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="${SSE_DIR}/dist"
BUILD_DIR="${SSE_DIR}/build"
APP_NAME="SSE"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║         SSE — Build de Executável               ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Verificar Python ──
PYTHON="${PYTHON:-python3}"
if ! command -v $PYTHON &>/dev/null; then
    PYTHON=python
fi

PYVER=$($PYTHON --version 2>&1)
echo -e "${GREEN}✓${NC} Usando: $PYVER"

# ── Instalar PyInstaller ──
echo -e "${YELLOW}[1/3]${NC} Instalando PyInstaller..."
$PYTHON -m pip install --quiet --upgrade pip
$PYTHON -m pip install --quiet -r "${SSE_DIR}/requirements-build.txt"
echo -e "${GREEN}✓${NC} Dependências de build instaladas"

# ── Detectar SO ──
OS_TYPE="$(uname -s | tr '[:upper:]' '[:lower:]')"
SEPARATOR="/"
ICON_FILE=""
if [[ "$OS_TYPE" == "mingw"* ]] || [[ "$OS_TYPE" == "msys"* ]]; then
    OS_TYPE="windows"
    SEPARATOR="\\"
    ICON_FILE="${SSE_DIR}${SEPARATOR}assets${SEPARATOR}icons${SEPARATOR}sse-icon.ico"
    APP_NAME="SSE.exe"
elif [[ "$OS_TYPE" == "linux"* ]]; then
    OS_TYPE="linux"
    SEPARATOR="/"
    ICON_FILE="${SSE_DIR}${SEPARATOR}assets${SEPARATOR}icons${SEPARATOR}sse-icon-256.png"
fi

echo -e "${YELLOW}[2/3]${NC} Plataforma detectada: ${OS_TYPE}"

# ── Build ──
echo -e "${YELLOW}[3/3]${NC} Compilando executável..."
echo -e "  Isso pode levar alguns minutos..."

PYINST_OPTS=(
    "--onefile"
    "--name" "${APP_NAME}"
    "--distpath" "${DIST_DIR}"
    "--workpath" "${BUILD_DIR}"
    "--specpath" "${BUILD_DIR}"
    "--add-data" "${SSE_DIR}/src${SEPARATOR}src"
    "--hidden-import" "src.console.menu"
    "--hidden-import" "src.games.minecraft"
    "--hidden-import" "src.games.pokemon"
    "--hidden-import" "src.launcher.minecraft_launcher"
    "--hidden-import" "src.savers.github_saver"
    "--hidden-import" "src.savers.googledrive_saver"
    "--hidden-import" "src.savers.telegram_saver"
    "--hidden-import" "src.utils.config"
    "--hidden-import" "src.utils.file_utils"
    "--hidden-import" "src.utils.platform"
    "--collect-all" "colorama"
    "--collect-all" "telethon"
    "--collect-all" "pydrive2"
)

if [[ "$OS_TYPE" == "windows" ]] && [[ -f "$ICON_FILE" ]]; then
    PYINST_OPTS+=("--icon" "$ICON_FILE")
elif [[ -f "$ICON_FILE" ]]; then
    PYINST_OPTS+=("--icon" "$ICON_FILE")
fi

# Se for Linux, não usar --windowed para permitir terminal
if [[ "$OS_TYPE" == "linux" ]]; then
    PYINST_OPTS+=("--console")
fi

$PYTHON -m PyInstaller "${SSE_DIR}/src/main.py" "${PYINST_OPTS[@]}"

# ── Limpeza ──
rm -rf "${BUILD_DIR}"

echo ""
echo -e "${GREEN}  ✔ Build concluído!${NC}"
echo ""
echo "  Executável gerado:"
echo "    ${DIST_DIR}/${APP_NAME}"
echo ""
echo "  Tamanho: $(du -h "${DIST_DIR}/${APP_NAME}" 2>/dev/null | cut -f1)"
echo ""
echo "  O usuário final só precisa deste único arquivo!"
echo ""
