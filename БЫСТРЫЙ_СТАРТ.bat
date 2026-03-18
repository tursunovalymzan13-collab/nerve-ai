@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              NERVE AI - Настройка за 1 минуту                    ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Автоматическая настройка Git с тестовыми данными
echo ⚙️  Настройка Git...
echo.

git config --global user.email "nerve.ai.user@example.com"
git config --global user.name "NERVE AI User"

echo ✅ Git настроен!
echo.

REM Инициализация репозитория
echo ⚙️  Инициализация репозитория...
echo.

git init
git add public_server.py requirements.txt Procfile README.md .gitignore
git commit -m "NERVE AI - готово к публикации"
git branch -M main

echo.
echo ✅ Репозиторий готов!
echo.
echo ═══════════════════════════════════════════════════════════════════
echo СЛЕДУЮЩИЙ ШАГ: Создание репозитория на GitHub
echo ═══════════════════════════════════════════════════════════════════
echo.
echo 1. Откройте: https://github.com/new
echo.
echo 2. Введите имя репозитория: nerve-ai
echo.
echo 3. Выберите: Public ✅
echo.
echo 4. Нажмите: Create repository
echo.
echo 5. После создания выполните:
echo.
echo    git remote add origin https://github.com/ВАШ_USERNAME/nerve-ai.git
echo    git push -u origin main
echo.
echo    (замените ВАШ_USERNAME на ваш логин GitHub)
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Автоматически открываем GitHub
start https://github.com/new

echo 🌐 GitHub открыт в браузере!
echo.
pause
