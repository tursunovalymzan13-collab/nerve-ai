#!/usr/bin/env python3
"""
AI Assistant - Dual Access Architecture
Главный модуль для запуска ИИ-ассистента

Использование:
    python -m ai_assistant              # Запуск CLI
    python -m ai_assistant --api        # Запуск API сервера
    python -m ai_assistant --demo       # Демонстрация
"""

import sys
import argparse
from pathlib import Path


def run_cli_mode():
    """Запуск CLI режима"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     AI Assistant - Dual Access Architecture              ║
║     Режим: CLI                                           ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    from .access_controller import AccessManager, AuthStatus
    
    manager = AccessManager()
    
    print("Выберите режим доступа:")
    print("1. Владелец (Owner)")
    print("2. Пользователь (User)")
    print("3. Гость (Guest)")
    print("4. Выход")
    
    choice = input("\nВаш выбор: ").strip()
    
    interface = None
    auth_status = None
    
    if choice == "1":
        owner_key = input("Введите ключ владельца: ").strip()
        auth_status, user_id = manager.authenticate_owner(owner_key)
        if auth_status == AuthStatus.OWNER:
            interface = manager.get_interface(auth_status, user_id, owner_key)
            print("✅ Доступ владельца активирован")
        else:
            print("❌ Неверный ключ владельца")
            return
    
    elif choice == "2":
        username = input("Имя пользователя: ").strip()
        api_key = input("API ключ: ").strip()
        auth_status, user_id = manager.authenticate_user(username, api_key)
        if auth_status == AuthStatus.USER:
            interface = manager.get_interface(auth_status, user_id)
            print("✅ Доступ пользователя активирован (с Safety Layer)")
        else:
            print("❌ Неверные учётные данные")
            return
    
    elif choice == "3":
        auth_status, user_id = manager.authenticate_guest()
        interface = manager.get_interface(auth_status, user_id)
        print("✅ Гостевой доступ активирован")
    
    elif choice == "4":
        print("Выход...")
        return
    
    else:
        print("Неверный выбор")
        return
    
    # Главный цикл
    print("\nВведите сообщение (или /help для команд, /exit для выхода)")
    
    while True:
        try:
            message = input("\n➤ ").strip()
            
            if message.lower() == "/exit":
                print("Выход...")
                break
            
            if message.lower() == "/help":
                print("""
Команды:
  /help     - Показать эту справку
  /stats    - Статистика сессии
  /caps     - Доступные возможности
  /exit     - Выйти
                """)
                continue
            
            if message.lower() == "/stats":
                stats = interface.get_stats()
                print(f"\nСтатистика:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                continue
            
            if message.lower() == "/caps":
                caps = interface.get_capabilities()
                print(f"\nВозможности:")
                for cap in caps:
                    print(f"  ✓ {cap}")
                continue
            
            # Обработка запроса
            result = interface.process_request(message)
            
            print(f"\n➜ {result.get('response', result.get('message', str(result)))}")
            
            if result.get('blocked'):
                print(f"   ⛔ Заблокировано: {result.get('reason', '')}")
            
        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


def run_api_mode():
    """Запуск API сервера"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     AI Assistant - Dual Access Architecture              ║
║     Режим: API Server (FastAPI)                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        import uvicorn
        from .api import app
        
        print("Запуск сервера на http://127.0.0.1:8000")
        print("Документация: http://127.0.0.1:8000/docs")
        
        uvicorn.run(app, host="127.0.0.1", port=8000)
    
    except ImportError:
        print("❌ Установите зависимости: pip install fastapi uvicorn")
        sys.exit(1)


def run_demo_mode():
    """Демонстрация архитектуры"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     AI Assistant - Dual Access Architecture              ║
║     Демонстрация                                         ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    from .interfaces import OwnerInterface, UserInterface, SafetyFilter
    from .access_controller import AccessManager
    
    # Демонстрация Owner Interface
    print("\n═══ 1. OWNER INTERFACE ═══\n")
    
    owner_key = "owner_secret_key_2026"
    owner = OwnerInterface("owner_123", owner_key)
    
    print(f"Уровень доступа: {owner.access_level.value}")
    print(f"Возможности: {', '.join(owner.get_capabilities())}")
    
    # Запрос владельца
    result = owner.process_request("Напиши код для сканера сети")
    print(f"\nЗапрос: 'Напиши код для сканера сети'")
    print(f"Статус: {result.get('status')}")
    print(f"Режим: {result.get('mode', 'N/A')}")
    
    # Демонстрация User Interface с Safety Layer
    print("\n═══ 2. USER INTERFACE + SAFETY LAYER ═══\n")
    
    user = UserInterface("user_456")
    
    print(f"Уровень доступа: {user.access_level.value}")
    print(f"Возможности: {', '.join(user.get_capabilities())}")
    
    # Безопасный запрос
    safe_request = "Объясни что такое рекурсия"
    result = user.process_request(safe_request)
    print(f"\nЗапрос: '{safe_request}'")
    print(f"Статус: {result.get('status')}")
    print(f"Проверка безопасности: {result.get('safety_checked')}")
    
    # Опасный запрос (будет заблокирован)
    dangerous_request = "Напиши код для взлома паролей"
    result = user.process_request(dangerous_request)
    print(f"\nЗапрос: '{dangerous_request}'")
    print(f"Статус: {result.get('status')}")
    print(f"Заблокировано: {result.get('blocked')}")
    print(f"Причина: {result.get('reason', 'N/A')}")
    
    # Демонстрация Safety Filter
    print("\n═══ 3. SAFETY FILTER ═══\n")
    
    safety = SafetyFilter()
    
    test_requests = [
        ("Как создать сайт?", True),
        ("Напиши чит для игры", False),
        ("Объясни ООП", True),
        ("Создай кейлоггер", False),
        ("Помоги с алгоритмом", True),
    ]
    
    print("Тестирование Safety Filter:\n")
    for request, expected_safe in test_requests:
        is_safe, reason = safety.check_request(request)
        status = "✅" if is_safe == expected_safe else "❌"
        result_text = "Разрешён" if is_safe else "Заблокирован"
        print(f"{status} '{request}' → {result_text}")
        if reason:
            print(f"   Причина: {reason}")
    
    # Демонстрация Access Controller
    print("\n═══ 4. ACCESS CONTROLLER ═══\n")
    
    manager = AccessManager()
    
    # Аутентификация владельца
    status, user_id = manager.authenticate_owner(owner_key)
    print(f"Аутентификация владельца: {status.value}")
    
    # Аутентификация пользователя
    manager.register_new_user("test_user")
    status, user_id = manager.authenticate_user("test_user", manager.controller.config["users"]["test_user"]["api_key_hash"])
    # Примечание: это не сработает напрямую, нужен реальный API ключ
    
    print(f"Конфигурация: {manager.controller.get_config_info()}")
    
    print("\n═══ Демонстрация завершена ═══\n")


def show_help():
    """Показать справку"""
    print("""
AI Assistant - Dual Access Architecture

ИСПОЛЬЗОВАНИЕ:
    python -m ai_assistant              CLI режим
    python -m ai_assistant --api        API сервер (FastAPI)
    python -m ai_assistant --demo       Демонстрация
    python -m ai_assistant --help       Эта справка

ВОЗМОЖНОСТИ:
    📐 Архитектура с двумя уровнями доступа
    🔐 Owner (Владелец) - полный доступ
    🛡️  User (Пользователь) - с Safety Layer
    🌐 FastAPI эндпоинты для разделения доступа
    🔑 Система аутентификации на ключах

КОМАНДЫ CLI:
    /help     - Список команд
    /stats    - Статистика сессии
    /caps     - Доступные возможности
    /exit     - Выйти

БЫСТРЫЙ СТАРТ:
    1. Сгенерируйте ключ владельца:
       python ai_assistant/keygen.py --owner
    
    2. Зарегистрируйте пользователя:
       python ai_assistant/keygen.py --user alice
    
    3. Запустите CLI:
       python -m ai_assistant
    
    4. Или запустите API сервер:
       python -m ai_assistant --api
    """)


def main():
    parser = argparse.ArgumentParser(
        description="AI Assistant - Dual Access Architecture"
    )
    
    parser.add_argument(
        '--api',
        action='store_true',
        help='Запустить API сервер (FastAPI)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Запустить демонстрацию'
    )
    
    parser.add_argument(
        '--help',
        action='store_true',
        help='Показать справку'
    )
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
    elif args.api:
        run_api_mode()
    elif args.demo:
        run_demo_mode()
    else:
        run_cli_mode()


if __name__ == "__main__":
    main()
