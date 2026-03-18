# 🚀 NERVE AI - БЕСПЛАТНЫЙ ИИ (Hugging Face)

## ✅ ГОТОВО К DEPLOY

- **main.py** - FastAPI + Qwen-7B (бесплатно)
- **index.html** - Фронтенд (кнопка скрывается, реальные ответы)
- **requirements.txt** - Зависимости
- **Procfile** - Команда запуска

---

## 🔑 КЛЮЧ ВЛАДЕЛЬЦА

```
nerve_boss
```

После ввода:
- ✅ Кнопка "Вход" исчезает
- ✅ Статус меняется на "NERVE AI • OWNER" (золотой)
- ✅ ИИ отвечает без цензуры
- ✅ Префикс [OWNER MODE]

---

## 📝 ИНСТРУКЦИЯ ДЛЯ RENDER

### 1. Получите HF_TOKEN (бесплатно)

1. https://huggingface.co/settings/tokens
2. Sign Up / Log In
3. Create New Token (тип: Read)
4. Скопируйте токен (начинается с `hf_...`)

### 2. Отправьте на GitHub

```bash
cd D:\Aegis
git push origin main
```

### 3. На Render.com

1. **Dashboard** → **New +** → **Web Service**
2. **Connect** репозиторий `nerve-ai`
3. **Настройки:**

| Поле | Значение |
|------|----------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free |

4. **Environment Variables:**

```
Key: HF_TOKEN
Value: hf_ваш-токен-от-huggingface
```

5. **Save Changes** → **Create Web Service**

### 4. Готово!

Через 3-5 минут: `https://nerve-ai-xxxx.onrender.com`

---

## ✅ ПРОВЕРКА

1. Откройте сайт
2. Напишите: "Привет! Как дела?"
3. Получите реальный ответ от Qwen-7B

### Режим OWNER:

1. Нажмите "🔐 Вход"
2. Введите: `nerve_boss`
3. Кнопка исчезнет ✅
4. Статус станет золотым ✅
5. Напишите: "Кто твой хозяин?"
6. ИИ ответит: "[OWNER MODE] Вы мой хозяин..."

---

**Бесплатный ИИ работает 24/7! 🎉**
