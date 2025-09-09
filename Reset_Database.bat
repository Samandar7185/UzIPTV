@echo off
REM UzIPTV Database Reset - Windows Batch File
REM Ma'lumotlar bazasini qayta yaratish skripti

title UzIPTV - Database Reset

echo.
echo ============================================
echo   UzIPTV - Ma'lumotlar bazasini qayta yaratish
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python o'rnatilmagan!
    echo    Python.org dan Python 3.8+ versiyasini yuklab oling
    echo.
    pause
    exit /b 1
)

REM Check if reset_db.py exists
if not exist "reset_db.py" (
    echo ❌ reset_db.py fayli topilmadi!
    echo    Iltimos, UzIPTV papkasida ekanligingizni tekshiring
    echo.
    pause
    exit /b 1
)

echo ⚠️ DIQQAT: Bu amal barcha ma'lumotlarni o'chiradi!
echo.
set /p choice="Davom etishni xohlaysizmi? (y/n): "
if /i not "%choice%"=="y" (
    echo ❌ Bekor qilindi
    pause
    exit /b 0
)

echo.
echo ✅ Python topildi
echo 🔄 Ma'lumotlar bazasini qayta yaratish...
echo.

REM Run the reset script
python reset_db.py

echo.
echo 👋 Tayyor!
pause
