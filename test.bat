@echo off
title InnoSphere - Automated Test Suite
cls

echo ============================================================================
echo   InnoSphere - Automated Test Suite
echo ============================================================================
echo.
echo [1/3] Running Database Constraints, Procedures & Trigger Tests...
python tests/test_db.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Database tests failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Running REST API & Business Logic Tests...
python tests/test_api.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] API tests failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Running Frontend Page & Route Tests...
python tests/test_routes.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Route tests failed.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo   ALL TESTS PASSED SUCCESSFULLY (100%% Operational Integrity)!
echo ============================================================================
echo.
pause
