#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# SSE — Instalador Automático para Linux 🐧
# ═══════════════════════════════════════════════════════════
set -euo pipefail

SSE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${HOME}/.local/bin"
CONFIG_DIR="${HOME}/.config/sse"
VENV_DIR="${SSE_DIR}/venv"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║       SSE — Instalador Automático (Linux)       ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── Verificar Python ──
echo -e "${YELLOW}[1/4]${NC} Verificando Python..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo -e "${RED}Python 3 não encontrado!${NC}"
    echo "  Instale com seu gerenciador de pacotes:"
    echo "    • Debian/Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo "    • Fedora:        sudo dnf install python3 python3-pip"
    echo "    • Arch:          sudo pacman -S python python-pip"
    exit 1
fi

PYVER=$($PYTHON --version 2>&1 | grep -oP '\d+\.\d+')
echo -e "  ${GREEN}✓${NC} Python ${PYVER} encontrado: $($PYTHON -c "import sys; print(sys.executable)")"

# ── Verificar Tkinter ──
echo -e "${YELLOW}[2/4]${NC} Verificando Tkinter..."
if ! $PYTHON -c "import tkinter" 2>/dev/null; then
    echo -e "${YELLOW}  Tkinter não encontrado. Instalando...${NC}"
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y python3-tk 2>/dev/null || true
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3-tkinter 2>/dev/null || true
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm tk 2>/dev/null || true
    fi
fi
echo -e "  ${GREEN}✓${NC} Tkinter disponível"

# ── Criar virtualenv ──
echo -e "${YELLOW}[3/4]${NC} Configurando ambiente virtual..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "${SSE_DIR}/requirements.txt"
echo -e "  ${GREEN}✓${NC} Dependências instaladas (venv)"

# ── Criar atalho ──
echo -e "${YELLOW}[4/4]${NC} Criando atalho..."
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/sse" << 'SCRIPT'
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
# Se estiver dentro do diretório do projeto, usa venv; senão tenta executável global
if [ -f "${SCRIPT_DIR}/venv/bin/activate" ]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
    python "${SCRIPT_DIR}/src/main.py" "$@"
elif command -v sse &>/dev/null; then
    sse "$@"
else
    python3 -m sse "$@"
fi
SCRIPT
chmod +x "$BIN_DIR/sse"

echo -e "  ${GREEN}✓${NC} Atalho criado: ${BIN_DIR}/sse"

# ── Finalizar ──
echo ""
echo -e "${GREEN}  ✔ Instalação concluída!${NC}"
echo ""
echo "  Para executar o SSE:"
echo "    sse"
echo ""
echo "  Ou diretamente:"
echo "    cd ${SSE_DIR} && source venv/bin/activate && python src/main.py"
echo ""
echo "  Se ${BIN_DIR} não estiver no PATH, adicione ao ~/.bashrc:"
echo "    export PATH=\"\${HOME}/.local/bin:\${PATH}\""
echo ""
