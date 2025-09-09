@echo off
REM UzIPTV - Windows Batch File
REM Bitta fayl bosish bilan ishga tushuvchi Windows skript

title UzIPTV - IPTV Playlist Search & Player

echo.
echo ========================================
echo   UzIPTV - IPTV Player dasturi
echo ========================================
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

REM Check if run.py exists
if not exist "run.py" (
    echo ❌ run.py fayli topilmadi!
    echo    Iltimos, UzIPTV papkasida ekanligingizni tekshiring
    echo.
    pause
    exit /b 1
)

echo ✅ Python topildi
echo 🚀 UzIPTV ishga tushirilmoqda...
echo.

REM Run the Python script
python run.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Xatolik yuz berdi!
    echo 📝 Yuqoridagi xabarlarni o'qib ko'ring
    echo.
    pause
)

echo.
echo 👋 UzIPTV yopildi
pause
