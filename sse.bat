@echo off
title System Save Eternal — SSE
color 0A
echo.
echo   ╔══════════════════════════════════════════════════╗
echo   ║          SYSTEM SAVE ETERNAL - SSE              ║
echo   ╚══════════════════════════════════════════════════╝
echo.
python "%~dp0src\main.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo   Pressione qualquer tecla para sair...
    pause >nul
)
