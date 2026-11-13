@echo off
title InnoSphere - Database Setup & Reset
cls

echo ============================================================================
echo   InnoSphere - Database Setup & Seed Tool
echo ============================================================================
echo.
echo Initializing 16 tables, 4 views, 4 stored procedures, 3 functions, 
echo 4 triggers, indexes, and full sample seed data...
echo.

python database/setup_db.py

echo.
echo ============================================================================
echo   Database Setup Completed!
echo   Run 'run.bat' to start the application.
echo ============================================================================
echo.
pause
