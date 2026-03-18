#!/usr/bin/env python3
"""
Генератор ключей доступа для AI Assistant

Использование:
    python keygen.py --owner          # Сгенерировать ключ владельца
    python keygen.py --user username  # Зарегистрировать пользователя
    python keygen.py --show           # Показать текущую конфигурацию
"""

import argparse
import json
import hashlib
import secrets
from pathlib import Path
from datetime import datetime


def generate_owner_key(config_path: str = "access_config.json"):
    """Сгенерировать новый ключ владельца"""
    config_file = Path(config_path)
    
    # Генерация нового ключа
    new_key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(new_key.encode()).hexdigest()
    
    # Загрузка или создание конфигурации
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {
            "owner_key_hash": "",
            "owner_key_display": "",
            "users": {},
            "settings": {
                "session_timeout_hours": 24,
                "max_failed_attempts": 5,
                "lockout_duration_minutes": 30
            }
        }
    
    # Обновление конфигурации
    config["owner_key_hash"] = key_hash
    config["owner_key_display"] = f"owner-{datetime.now().year}-" + secrets.token_hex(8)
    
    # Сохранение
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("""
╔══════════════════════════════════════════════════════════╗
║           КЛЮЧ ВЛАДЕЛЬЦА СГЕНЕРИРОВАН                    ║
╠══════════════════════════════════════════════════════════╣
║  ⚠️  ВНИМАНИЕ: Сохраните этот ключ в безопасном месте!   ║
║      Он показывается только один раз!                    ║
╚══════════════════════════════════════════════════════════╝

🔑 Ключ владельца:
   {key}

📁 Конфигурация сохранена в: {config}

💡 Использование ключа:
   - Передавайте в заголовке Authorization
   - Используйте в API: {{ "owner_key": "{key}" }}
   - Храните в секрете!

═══════════════════════════════════════════════════════════
""".format(key=key, config=config_file.absolute()))


def register_user(username: str, config_path: str = "access_config.json"):
    """Зарегистрировать нового пользователя"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"❌ Конфигурация не найдена: {config_file}")
        print("Сначала сгенерируйте ключ владельца: python keygen.py --owner")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Проверка существования пользователя
    if username in config.get("users", {}):
        print(f"❌ Пользователь '{username}' уже существует")
        return
    
    # Генерация API ключа
    api_key = secrets.token_urlsafe(24)
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    import uuid
    user_id = str(uuid.uuid4())
    
    # Добавление пользователя
    if "users" not in config:
        config["users"] = {}
    
    config["users"][username] = {
        "user_id": user_id,
        "api_key_hash": api_key_hash,
        "created_at": datetime.now().isoformat(),
        "access_level": "user",
        "metadata": {},
        "failed_attempts": 0,
        "locked_until": None
    }
    
    # Сохранение
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("""
╔══════════════════════════════════════════════════════════╗
║           ПОЛЬЗОВАТЕЛЬ ЗАРЕГИСТРИРОВАН                   ║
╠══════════════════════════════════════════════════════════╣
║  👤 Имя пользователя: {username:<30} ║
║  🔑 API Ключ (сохраните!):                               ║
╚══════════════════════════════════════════════════════════╝

🔑 API Ключ:
   {key}

📁 ID Пользователя: {user_id}

💡 Использование:
   - Логин: {{ "username": "{username}", "api_key": "{key}" }}
   - Уровень доступа: USER (с Safety Layer)

═══════════════════════════════════════════════════════════
""".format(username=username, key=api_key, user_id=user_id))


def show_config(config_path: str = "access_config.json"):
    """Показать текущую конфигурацию"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"❌ Конфигурация не найдена: {config_file}")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("""
╔══════════════════════════════════════════════════════════╗
║           ТЕКУЩАЯ КОНФИГУРАЦИЯ                           ║
╚══════════════════════════════════════════════════════════╝

📁 Файл: {config}

🔐 Владелец:
   - Настроен: {owner_set}
   - Display Key: {display_key}

👥 Пользователи: {user_count}
{users}

⚙️ Настройки:
   - Таймаут сессии: {timeout} ч.
   - Макс. попыток: {max_attempts}
   - Блокировка: {lockout} мин.

═══════════════════════════════════════════════════════════
""".format(
        config=config_file.absolute(),
        owner_set="✅ Да" if config.get("owner_key_hash") else "❌ Нет",
        display_key=config.get("owner_key_display", "N/A"),
        user_count=len(config.get("users", {})),
        users="\n".join([f"   - {u}" for u in config.get("users", {}).keys()]) or "   (нет)",
        timeout=config.get("settings", {}).get("session_timeout_hours", 24),
        max_attempts=config.get("settings", {}).get("max_failed_attempts", 5),
        lockout=config.get("settings", {}).get("lockout_duration_minutes", 30)
    ))


def main():
    parser = argparse.ArgumentParser(
        description="Генератор ключей доступа AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python keygen.py --owner          # Сгенерировать ключ владельца
  python keygen.py --user alice     # Зарегистрировать пользователя alice
  python keygen.py --show           # Показать конфигурацию
        """
    )
    
    parser.add_argument(
        '--owner',
        action='store_true',
        help='Сгенерировать новый ключ владельца'
    )
    
    parser.add_argument(
        '--user',
        type=str,
        metavar='USERNAME',
        help='Зарегистрировать нового пользователя'
    )
    
    parser.add_argument(
        '--show',
        action='store_true',
        help='Показать текущую конфигурацию'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='access_config.json',
        help='Путь к файлу конфигурации'
    )
    
    args = parser.parse_args()
    
    if args.owner:
        generate_owner_key(args.config)
    elif args.user:
        register_user(args.user, args.config)
    elif args.show:
        show_config(args.config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
