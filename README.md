# 🚀 NERVE AI - Полная инструкция

## ✅ Всё готово!

Ваш проект полностью подготовлен для публикации в интернете.

---

## 📁 Файлы в папке:

| Файл | Назначение |
|------|------------|
| **public_server.py** | Сервер с вашим ИИ |
| **requirements.txt** | Зависимости |
| **Procfile** | Для хостинга |
| **.gitignore** | Игнор файлов |
| **АВТО_НАСТРОЙКА.bat** | Автоматическая настройка |
| **ОПУБЛИКОВАТЬ.bat** | Быстрая публикация |
| **1_НАЧНИ_ЗДЕСЬ.txt** | Начните отсюда |

---

## 🎯 БЫСТРЫЙ СТАРТ

### Вариант 1: Автоматически (рекомендуется)

1. **Дважды кликните** на `АВТО_НАСТРОЙКА.bat`
2. Введите Email и Имя
3. Следуйте инструкциям

### Вариант 2: Вручную

```bash
# 1. Настройте Git
git config --global user.email "ваш@email.com"
git config --global user.name "Ваше Имя"

# 2. Инициализируйте
git init
git add public_server.py requirements.txt Procfile
git commit -m "NERVE AI"
git branch -M main

# 3. Создайте репозиторий на GitHub
# https://github.com/new → nerve-ai

# 4. Отправьте код
git remote add origin https://github.com/ВАШ_USERNAME/nerve-ai.git
git push -u origin main

# 5. Разместите на Render
# https://render.com → New + → Web Service → Connect nerve-ai
```

---

## 🌐 Публикация на Render

### 1. Создайте репозиторий на GitHub
```
https://github.com/new
Name: nerve-ai
Public: ✅
Create repository
```

### 2. Отправьте код
```bash
git remote add origin https://github.com/ВАШ_USERNAME/nerve-ai.git
git push -u origin main
```

### 3. Разместите на Render
```
1. https://render.com
2. Sign Up (через GitHub)
3. Dashboard → New + → Web Service
4. Connect: nerve-ai
5. Build: pip install -r requirements.txt
6. Start: gunicorn public_server:app --bind 0.0.0.0:$PORT --workers 4
7. Create Web Service
```

### 4. Готово!
Через 3-5 минут: `https://nerve-ai-xxxx.onrender.com`

---

## 🔑 Ключ владельца

```
NERVE_MASTER_KEY_2026
```

Используйте на сайте для входа в режим владельца (без ограничений).

---

## 🤖 Ваш ИИ

Сервер использует `ai_assistant` (ваш собственный ИИ):

- **User режим**: с Safety Filter
- **Owner режим**: БЕЗ ограничений

---

## ✅ Проверка локально

```bash
python public_server.py
# http://localhost:5000
```

---

**Ваш ИИ будет работать 24/7 в облаке! 🎉**
