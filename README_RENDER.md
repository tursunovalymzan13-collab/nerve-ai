# 🚀 NERVE AI - Публикация на Render

## ✅ ФАЙЛЫ ГОТОВЫ

- **main.py** - Сервер FastAPI + OpenAI
- **index.html** - Фронтенд
- **requirements.txt** - Зависимости
- **Procfile** - Команда запуска

---

## 📝 ИНСТРУКЦИЯ

### 1. Отправьте на GitHub

```bash
cd D:\Aegis
git add main.py index.html requirements.txt Procfile
git commit -m "NERVE AI - Ready for Render"
git push origin main
```

### 2. На Render.com

1. **Dashboard** → **New +** → **Web Service**
2. **Connect** ваш репозиторий `nerve-ai`
3. **Настройки:**

| Поле | Значение |
|------|----------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free |

4. **Create Web Service**

### 3. Добавьте OPENAI_API_KEY

1. В панели Render → **Environment**
2. **Add Variable:**

```
Key: OPENAI_API_KEY
Value: sk-proj-ваш-ключ-от-openai
```

3. **Save Changes**

### 4. Готово!

Через 3-5 минут: `https://nerve-ai-xxxx.onrender.com`

---

## 🔑 Ключ владельца

```
NERVE_MASTER_KEY_2026
```

---

## ✅ ПРОВЕРКА

1. Откройте сайт
2. Напишите: "Привет! Как дела?"
3. Получите реальный ответ от GPT-4

---

**Ваш ИИ работает 24/7! 🎉**
