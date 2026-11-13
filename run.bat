@echo off
title InnoSphere - Unified Innovation Portal
cls

echo ============================================================================
echo   InnoSphere - One-Click Launcher
echo ============================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please ensure Python 3.10+ is installed and added to PATH.
    echo.
    pause
    exit /b 1
)

python run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Application stopped with error code %ERRORLEVEL%.
    pause
)
