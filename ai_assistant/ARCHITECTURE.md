# Архитектура ИИ-Ассистента с Двумя Уровнями Доступа

## 📋 Обзор

Данная архитектура реализует ИИ-ассистента с разделением на два уровня доступа:
- **Owner (Владелец)** — полный доступ без ограничений
- **User (Пользователь)** — ограниченный доступ с Safety Layer

---

## 🏗️ Структура Проекта

```
ai_assistant/
├── __init__.py              # Инициализация пакета
├── interfaces.py            # Базовые классы интерфейсов
├── access_controller.py     # Система аутентификации
├── api.py                   # FastAPI эндпоинты
├── keygen.py                # Генератор ключей доступа
├── access_config.json       # Конфигурация доступа
└── ARCHITECTURE.md          # Этот файл
```

---

## 📐 Архитектурные Компоненты

### 1. Базовый Класс `AIInterface`

Абстрактный базовый класс, определяющий контракт для всех уровней доступа:

```python
class AIInterface(ABC):
    @abstractmethod
    def process_request(self, request: str, context: Dict) -> Dict:
        """Обработать запрос"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Вернуть список возможностей"""
        pass
```

**Основные возможности:**
- Логирование запросов
- Статистика сессии
- Управление памятью

---

### 2. OwnerInterface (Владелец)

Полный доступ без ограничений:

```
┌─────────────────────────────────────────────────────────┐
│                   OwnerInterface                        │
├─────────────────────────────────────────────────────────┤
│  ✅ Генерация любого кода                               │
│  ✅ Системные команды                                   │
│  ✅ Доступ к логам                                      │
│  ✅ Изменение настроек                                  │
│  ✅ Экспорт данных                                      │
│  ✅ Приоритетный доступ                                 │
└─────────────────────────────────────────────────────────┘
```

**Специальные команды владельца:**
| Команда | Описание |
|---------|----------|
| `/owner_status` | Показать статус владельца |
| `/system_config` | Показать/изменить конфигурацию |
| `/view_logs [limit]` | Просмотр логов |
| `/clear_logs` | Очистка логов |
| `/export_data` | Экспорт всех данных |
| `/execute [cmd]` | Выполнить команду |
| `/modify_settings key=value` | Изменить настройку |

---

### 3. UserInterface (Пользователь)

Ограниченный доступ с Safety Layer:

```
┌─────────────────────────────────────────────────────────┐
│                   UserInterface                         │
├─────────────────────────────────────────────────────────┤
│  ⚠️ Safety Filter (проверка запросов)                  │
│  ⚠️ Safety Filter (проверка ответов)                   │
│  ✅ Базовые вопросы                                     │
│  ✅ Вычисления                                          │
│  ✅ Объяснение концепций                                │
│  ✅ Безопасная генерация кода                           │
└─────────────────────────────────────────────────────────┘
```

**Safety Layer блокирует:**
- Генерацию вредоносного кода
- Читы, взлом, трояны
- Кейлоггеры, инжекторы
- Сканеры сети, крякеры
- Обход защиты системы

---

### 4. AccessController (Контроллер Доступа)

Система аутентификации и управления сессиями:

```
                    ┌──────────────────┐
                    │  AccessController│
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Owner Auth   │   │  User Auth    │   │  Guest Auth   │
│  (Key-based)  │   │  (API Key)    │   │  (Temporary)  │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Механизм проверки:**
1. Проверка ключа владельца → OwnerInterface
2. Проверка API ключа пользователя → UserInterface
3. Гостевой доступ → UserInterface (ограниченный)

---

## 🔐 Система Аутентификации

### Уровни Доступа

| Уровень | Метод Аутентификации | Доступ |
|---------|---------------------|--------|
| **Owner** | Уникальный ключ владельца | Полный |
| **User** | Имя пользователя + API ключ | Ограниченный |
| **Guest** | Временная сессия | Базовый |

### Генерация Ключей

```bash
# Сгенерировать ключ владельца
python ai_assistant/keygen.py --owner

# Зарегистрировать пользователя
python ai_assistant/keygen.py --user alice

# Показать конфигурацию
python ai_assistant/keygen.py --show
```

---

## 🌐 API Endpoints (FastAPI)

### Аутентификация

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/v1/auth/login` | POST | Вход в систему |
| `/api/v1/auth/logout` | POST | Выход из системы |
| `/api/v1/auth/me` | GET | Информация о пользователе |

### Owner Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/v1/owner/chat` | POST | Чат без ограничений |
| `/api/v1/owner/command` | POST | Выполнить команду |
| `/api/v1/owner/status` | GET | Статус владельца |
| `/api/v1/owner/logs` | GET | Просмотр логов |
| `/api/v1/owner/config` | POST | Изменить конфигурацию |
| `/api/v1/owner/users` | GET | Список пользователей |
| `/api/v1/owner/users/register` | POST | Регистрация пользователя |

### User Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/v1/user/chat` | POST | Чат с Safety Layer |
| `/api/v1/user/capabilities` | GET | Доступные возможности |
| `/api/v1/user/stats` | GET | Статистика пользователя |

---

## 💻 Примеры Использования

### 1. Аутентификация Владельца

```python
import requests

# Вход как владелец
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "owner_key": "your_owner_key_here"
})

token = response.json()["session_token"]

# Запрос к ИИ без ограничений
chat_response = requests.post(
    "http://localhost:8000/api/v1/owner/chat",
    json={"message": "Напиши код для..."},
    headers={"Authorization": f"Bearer {token}"}
)
```

### 2. Аутентификация Пользователя

```python
# Вход как пользователь
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "username": "alice",
    "api_key": "user_api_key_here"
})

token = response.json()["session_token"]

# Запрос к ИИ (с проверкой безопасности)
chat_response = requests.post(
    "http://localhost:8000/api/v1/user/chat",
    json={"message": "Объясни что такое рекурсия"},
    headers={"Authorization": f"Bearer {token}"}
)
```

### 3. Прямое Использование Интерфейсов

```python
from ai_assistant.interfaces import OwnerInterface, UserInterface
from ai_assistant.access_controller import AccessManager

# Менеджер доступа
manager = AccessManager()

# Аутентификация владельца
status, user_id = manager.authenticate_owner("owner_key")
interface = manager.get_interface(status, user_id, owner_key="owner_key")

# Обработка запроса
result = interface.process_request("Напиши код...")
print(result)

# Аутентификация пользователя
status, user_id = manager.authenticate_user("alice", "api_key")
interface = manager.get_interface(status, user_id)

# Обработка запроса (с Safety Layer)
result = interface.process_request("Объясни концепцию...")
print(result)
```

---

## 🛡️ Safety Layer (Фильтр Безопасности)

### Блокируемые Паттерны

```python
BLOCKED_PATTERNS = [
    r'\b(чит|cheat|hack|взлом)\b',
    r'\b(rat|троян|remote.*access)\b',
    r'\b(кейлог|keylog)\b',
    r'\b(инжект|inject|dll)\b',
    r'\b(скан.*порт|port.*scan)\b',
    r'\b(парол.*взлом|password.*crack)\b',
    r'\b(вирус|malware|spyware)\b',
]
```

### Проверка Ответов

Safety Layer проверяет не только запросы, но и сгенерированные ответы:

```python
def check_response(self, response: str) -> tuple[bool, Optional[str]]:
    # Проверка на опасный код
    dangerous_patterns = [
        r'pymem\.',
        r'OpenProcess',
        r'VirtualAllocEx',
        r'WriteProcessMemory',
    ]
    # ...
```

---

## ⚙️ Конфигурация

### access_config.json

```json
{
  "owner_key_hash": "...",
  "owner_key_display": "owner-2026-xxxx-xxxx",
  "users": {},
  "settings": {
    "session_timeout_hours": 24,
    "max_failed_attempts": 5,
    "lockout_duration_minutes": 30,
    "enable_safety_layer": true,
    "log_all_requests": true
  },
  "security": {
    "enable_rate_limiting": true,
    "rate_limit_per_minute": 60
  }
}
```

---

## 🚀 Запуск Сервера

```bash
# Установка зависимостей
pip install fastapi uvicorn pydantic

# Запуск API сервера
python -m ai_assistant.api

# Или через uvicorn
uvicorn ai_assistant.api:app --host 127.0.0.1 --port 8000 --reload
```

### Документация API

После запуска откройте в браузере:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📊 Диаграмма Классов

```
┌─────────────────────────────────────────────────────────────┐
│                      AIInterface (ABC)                      │
│  - access_level: AccessLevel                                │
│  - user_id: str                                             │
│  - request_count: int                                       │
├─────────────────────────────────────────────────────────────┤
│  + process_request() [abstract]                             │
│  + get_capabilities() [abstract]                            │
│  + get_stats()                                              │
│  + _log_request()                                           │
└─────────────────────────────────────────────────────────────┘
                            ▲
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   OwnerInterface      │       │    UserInterface      │
├───────────────────────┤       ├───────────────────────┤
│ - owner_key: str      │       │ - safety_filter:      │
│ - system_settings     │       │   SafetyFilter        │
│ - full_access: bool   │       │ - allowed_operations  │
├───────────────────────┤       ├───────────────────────┤
│ + _process_owner_cmd()│       │ + _is_allowed_op()    │
│ + _generate_code()    │       │ + _process_safe_req() │
│ + _system_command()   │       │ + get_safety_stats()  │
│ + _cmd_*()            │       │ + _generate_safe_code()│
└───────────────────────┘       └───────────────────────┘
                                        │
                                        │ содержит
                                        ▼
                              ┌───────────────────────┐
                              │    SafetyFilter       │
                              ├───────────────────────┤
                              │ - BLOCKED_PATTERNS    │
                              │ - BLOCKED_TOPICS      │
                              ├───────────────────────┤
                              │ + check_request()     │
                              │ + check_response()    │
                              │ + get_violation_stats()│
                              └───────────────────────┘
```

---

## 🔧 Расширение Архитектуры

### Добавление Нового Уровня Доступа

```python
class PremiumInterface(AIInterface):
    """Расширенный пользовательский интерфейс"""
    
    def __init__(self, user_id: str):
        super().__init__(AccessLevel.PREMIUM, user_id)
        self.safety_filter = SafetyFilter(strict=False)  # Мягче ограничения
    
    def process_request(self, request: str, context: Dict) -> Dict:
        # Реализация...
        pass
    
    def get_capabilities(self) -> List[str]:
        return ["advanced_features", "priority_support"]
```

### Добавление Новых Команд Владельца

```python
def _cmd_new_command(self, args: str) -> Dict[str, Any]:
    """Новая команда владельца"""
    return {
        "status": "success",
        "message": "Команда выполнена",
        "data": {...}
    }

# Добавить в commands dict:
commands = {
    '/new_command': self._cmd_new_command,
    # ...
}
```

---

## 📝 Best Practices

### Безопасность

1. **Хранение ключей**: Используйте environment variables или secure vault
2. **HTTPS**: Всегда используйте HTTPS в production
3. **Rate Limiting**: Включите ограничение запросов
4. **Логирование**: Логируйте все попытки доступа

### Производительность

1. **Кеширование**: Кешируйте частые запросы
2. **Асинхронность**: Используйте async/await для I/O операций
3. **Базы данных**: Для хранения сессий используйте Redis

### Масштабирование

1. **Микросервисы**: Разделите auth и AI логику
2. **Load Balancing**: Используйте балансировщик нагрузки
3. **Контейнеризация**: Docker для деплоя

---

## 📄 Лицензия

Данная архитектура является частью проекта Aegis.
