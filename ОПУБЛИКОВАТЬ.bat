@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         NERVE AI - Автоматическая публикация                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Проверка Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не найден! Установите Git: https://git-scm.com
    pause
    exit /b 1
)

echo ✅ Git найден
echo.

REM Инициализация
git init
git add public_server.py requirements.txt Procfile README.md .gitignore ЗАПУСК.txt
git commit -m "NERVE AI - Initial commit"
git branch -M main

echo.
echo ✅ Репозиторий готов
echo.
echo ═══════════════════════════════════════════════════════════════════
echo СЛЕДУЮЩИЕ ШАГИ:
echo.
echo 1. Создайте репозиторий на GitHub:
echo    https://github.com/new
echo    Name: nerve-ai
echo    Public: ✅
echo.
echo 2. Выполните команды (замените USERNAME на ваш):
echo    git remote add origin https://github.com/USERNAME/nerve-ai.git
echo    git push -u origin main
echo.
echo 3. Разместите на Render:
echo    https://render.com
echo    New + ^→ Web Service ^→ Connect nerve-ai
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Предложение открыть GitHub
set /p open="Открыть GitHub для создания репозитория? (Y/N): "
if /i "%open%"=="Y" (
    start https://github.com/new
)

pause


pause
