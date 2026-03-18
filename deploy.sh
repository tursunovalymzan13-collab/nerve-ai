#!/bin/bash
# Скрипт автоматической публикации NERVE AI на Render

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         NERVE AI - Автоматическая публикация                     ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не найден! Установите Git."
    exit 1
fi

echo "✅ Git найден"

# Инициализация
git init
git add public_server.py requirements.txt Procfile README.md .gitignore
git commit -m "NERVE AI - Initial commit"
git branch -M main

echo ""
echo "✅ Репозиторий готов"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "СЛЕДУЮЩИЕ ШАГИ:"
echo ""
echo "1. Создайте репозиторий на GitHub:"
echo "   https://github.com/new"
echo "   Name: nerve-ai"
echo "   Public: ✅"
echo ""
echo "2. Выполните команды:"
echo "   git remote add origin https://github.com/ВАШ_USERNAME/nerve-ai.git"
echo "   git push -u origin main"
echo ""
echo "3. Разместите на Render:"
echo "   https://render.com"
echo "   New + → Web Service → Connect nerve-ai"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
