@echo off
chcp 65001 >nul
title DEVDOP - Iniciando n8n
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════╗
echo  ║         DEVDOP - INICIADOR DE N8N 2.2.5              ║
echo  ╚═══════════════════════════════════════════════════════╝
echo.

:: Configurar variables de entorno para esta sesion
echo [1/2] Configurando variables de entorno...
set NODES_EXCLUDE=[]
set N8N_RESTRICT_FILE_ACCESS_TO=C:/n8nvideo
echo      [OK] NODES_EXCLUDE=[]
echo      [OK] N8N_RESTRICT_FILE_ACCESS_TO=C:/n8nvideo

:: Iniciar n8n
echo.
echo [2/2] Iniciando n8n...
echo      Espera unos segundos...
echo.
echo  ══════════════════════════════════════════════════════════
echo   n8n se abrira en: http://localhost:5678
echo   Presiona Ctrl+C para detener n8n
echo  ══════════════════════════════════════════════════════════
echo.

n8n start
