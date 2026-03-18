@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              NERVE AI - Полная автоматическая настройка          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Проверка Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не найден!
    echo    Установите: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git найден
echo.

REM Настройка Git (спросим пользователя)
echo ───────────────────────────────────────────────────────────────────
echo Настройка Git (нужно сделать один раз)
echo ───────────────────────────────────────────────────────────────────
echo.

set /p email="Введите ваш Email: "
set /p username="Введите ваше имя: "

if "%email%"=="" (
    echo ❌ Email обязателен!
    pause
    exit /b 1
)

git config --global user.email "%email%"
git config --global user.name "%username%"

echo.
echo ✅ Git настроен
echo.

REM Инициализация репозитория
echo ───────────────────────────────────────────────────────────────────
echo Инициализация репозитория
echo ───────────────────────────────────────────────────────────────────

git init
git add public_server.py requirements.txt Procfile README.md .gitignore
git commit -m "NERVE AI - готово к публикации"
git branch -M main

echo.
echo ✅ Репозиторий готов
echo.

REM Предложение открыть GitHub
echo ───────────────────────────────────────────────────────────────────
echo Создание репозитория на GitHub
echo ───────────────────────────────────────────────────────────────────
echo.
echo Сейчас откроется GitHub для создания репозитория.
echo.
echo 1. Введите имя: nerve-ai
echo 2. Выберите: Public
echo 3. Нажмите: Create repository
echo.

set /p confirm="Открыть GitHub? (Y/N): "
if /i "%confirm%"=="Y" (
    start https://github.com/new
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo СЛЕДУЮЩИЙ ШАГ:
echo ═══════════════════════════════════════════════════════════════════
echo.
echo После создания репозитория выполните:
echo.
echo    git remote add origin https://github.com/ВАШ_USERNAME/nerve-ai.git
echo    git push -u origin main
echo.
echo (замените ВАШ_USERNAME на ваш логин GitHub)
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

pause


pause
