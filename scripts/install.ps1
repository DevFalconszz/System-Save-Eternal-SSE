<#
.SYNOPSIS
    SSE — Instalador Automático para Windows 🪟
.DESCRIPTION
    Instala Python (se necessário), dependências e cria atalho para o SSE
#>

$ErrorActionPreference = "Stop"
$SSE_DIR = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$CONFIG_DIR = "$env:APPDATA\sse"

Write-Host "  ╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║       SSE — Instalador Automático (Windows)     ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Verificar Python ──
Write-Host "[1/4] Verificando Python..." -ForegroundColor Yellow
$PYTHON = $null

try {
    $PYTHON = (Get-Command python -ErrorAction Stop).Source
} catch {
    try {
        $PYTHON = (Get-Command python3 -ErrorAction Stop).Source
    } catch {
        Write-Host "  Python não encontrado! Deseja baixar e instalar?" -ForegroundColor Yellow
        $choice = Read-Host "  >>> Instalar Python 3? (s/N)"
        if ($choice -eq "s") {
            $url = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
            $installer = "$env:TEMP\python-installer.exe"
            Write-Host "  Baixando Python 3.12..." -ForegroundColor Cyan
            Invoke-WebRequest -Uri $url -OutFile $installer
            Write-Host "  Instalando Python..." -ForegroundColor Cyan
            Start-Process -Wait -FilePath $installer -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1"
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")
            $PYTHON = (Get-Command python -ErrorAction Stop).Source
        } else {
            Write-Host "  Instalação cancelada." -ForegroundColor Red
            exit 1
        }
    }
}

$pyVer = & $PYTHON --version
Write-Host "  OK $pyVer" -ForegroundColor Green

# ── Verificar Tkinter ──
Write-Host "[2/4] Verificando Tkinter..." -ForegroundColor Yellow
try {
    & $PYTHON -c "import tkinter; print('  OK Tkinter disponível')" 2>&1
} catch {
    Write-Host "  Tkinter não encontrado. Normalmente já vem com Python no Windows." -ForegroundColor Yellow
}

# ── Instalar dependências ──
Write-Host "[3/4] Instalando dependências..." -ForegroundColor Yellow
$pip = Split-Path -Parent $PYTHON
$pip = Join-Path $pip "pip"  # Windows usa pip.exe
if (-not (Test-Path "$pip.exe")) {
    $pip = "pip"
}
& $python -m pip install --quiet --upgrade pip
& $python -m pip install --quiet -r "$SSE_DIR\requirements.txt"
Write-Host "  OK Dependências instaladas" -ForegroundColor Green

# ── Criar atalho ──
Write-Host "[4/4] Criando atalho no Menu Iniciar..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\SSE.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "$SSE_DIR\sse.bat"
$Shortcut.WorkingDirectory = $SSE_DIR
$Shortcut.Description = "System Save Eternal — Backup de Saves"
$Shortcut.Save()
Write-Host "  OK Atalho criado: $ShortcutPath" -ForegroundColor Green

Write-Host ""
Write-Host "  ✔ Instalação concluída!" -ForegroundColor Green
Write-Host ""
Write-Host "  Para executar o SSE:" -ForegroundColor Yellow
Write-Host "    python $SSE_DIR\src\main.py"
Write-Host "    ou dê duplo clique em sse.bat"
Write-Host "    ou pelo Menu Iniciar > SSE"
Write-Host ""
