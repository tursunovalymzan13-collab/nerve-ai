#!/usr/bin/env python3
"""
ИИ-Помощник v1.0
Персональный ИИ без ограничений для обучения и помощи

Запуск:
    python main_ai.py              # Обычный режим с цветами
    python main_ai.py --simple     # Простой режим без цветов
    python main_ai.py --test       # Тестовый запуск

Команды:
    /help       - Список команд
    /good       - Ответ хороший (обучение)
    /bad        - Ответ плохой (обучение)
    /remember   - Запомнить информацию
    /search     - Поиск в памяти
    /mood       - Сообщить о настроении
    /code       - Генерация кода
    /game       - Помощь с играми
    /explain    - Объяснить концепцию
    /debug      - Найти ошибку
    /stats      - Статистика
    /clear      - Очистить экран
    /exit       - Выйти
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent / 'ai_assistant'))


def check_dependencies():
    """Проверить зависимости"""
    missing = []
    
    try:
        import colorama
    except ImportError:
        missing.append('colorama (для цветов в Windows)')
    
    if missing and sys.platform == 'win32':
        print(f"⚠ Рекомендуется установить: {'; '.join(missing)}")
        print("  pip install colorama\n")
    
    return True


def print_header():
    """Показать заголовок"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    ИИ-ПОМОЩНИК v1.0                              ║
║                                                                  ║
║  Персональный ИИ для:                                            ║
║  • Написания кода и объяснения концепций                         ║
║  • Разработки игр (механики, квесты, идеи)                       ║
║  • Эмоциональной поддержки                                       ║
║  • Обучения на вашем фидбеке                                     ║
║                                                                  ║
║  Введите /help для списка команд                                 ║
╚══════════════════════════════════════════════════════════════════╝
""")


def run_main_mode():
    """Запустить основной режим чата"""
    # Исправляем импорт для прямого запуска
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from chat_ui import run_chat
    
    print_header()
    run_chat(simple_mode=False)


def run_simple_mode():
    """Запустить простой режим (без цветов)"""
    from chat_ui import run_chat
    
    print_header()
    run_chat(simple_mode=True)


def run_test_mode():
    """Запустить тестовый режим"""
    print("═══ ТЕСТОВЫЙ ЗАПУСК ═══\n")
    
    from ai_core import AIAssistant
    
    assistant = AIAssistant(db_path=":memory:")  # База в памяти для теста
    
    # Тестовые сообщения
    test_messages = [
        "привет",
        "я грущу сегодня",
        "напиши функцию для сложения чисел",
        "дай идею для игры",
        "объясни что такое рекурсия",
        "/stats"
    ]
    
    print("Тестирование ответов:\n")
    
    for msg in test_messages:
        print(f"➤ {msg}")
        response = assistant.process_message(msg)
        print(f"➜ {response[:200]}...\n" if len(response) > 200 else f"➜ {response}\n")
    
    # Тест обучения
    print("═══ ТЕСТ ОБУЧЕНИЯ ═══\n")
    
    conv_id = assistant.last_conversation_id
    if conv_id:
        assistant.learner.mark_good(conv_id)
        print("✓ Ответ отмечен как хороший")
        
        stats = assistant.learner.get_learning_stats()
        print(f"Статистика: {stats}\n")
    
    assistant.close()
    print("✓ Тест завершён успешно!")


def run_demo_mode():
    """Запустить демонстрационный режим"""
    print("═══ ДЕМО-РЕЖИМ ═══\n")
    
    from ai_core import AIAssistant
    from game_dev import GameDevAssistant
    from coder import CodeAssistant
    from emotions import EmotionAnalyzer
    
    # Демонстрация генерации идей
    print("🎮 ГЕНЕРАЦИЯ ИДЕИ ИГРЫ:\n")
    game_dev = GameDevAssistant()
    idea = game_dev.generate_game_idea()
    print(f"Жанр: {idea['genre']}")
    print(f"Концепт: {idea['concept']}")
    print(f"Фишка: {idea['twist']}")
    print(f"Сеттинг: {idea['setting']}\n")
    
    # Демонстрация генерации квеста
    print("📜 ГЕНЕРАЦИЯ КВЕСТА:\n")
    quest = game_dev.generate_quest()
    print(f"Название: {quest['title']}")
    print(f"Описание: {quest['description']}")
    print(f"Награды: {', '.join(quest['rewards'])}\n")
    
    # Демонстрация кода
    print("💻 ШАБЛОН КОДА (Platformer Pygame):\n")
    print(game_dev.create_pygame_template('platformer')[:500] + "...\n")
    
    # Демонстрация эмоций
    print("😊 АНАЛИЗ ЭМОЦИЙ:\n")
    analyzer = EmotionAnalyzer()
    
    test_texts = [
        "Я так рад сегодня!",
        "Мне грустно и одиноко",
        "Я устал от этой работы"
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"'{text}' → {result['mood']} {result['emoji']}")
    
    print("\n✓ Демонстрация завершена!")


def show_help():
    """Показать справку"""
    print("""
ИИ-ПОМОЩНИК - Персональный ИИ без ограничений

ИСПОЛЬЗОВАНИЕ:
    python main_ai.py              Обычный режим
    python main_ai.py --simple     Простой режим (без цветов)
    python main_ai.py --test       Тестовый запуск
    python main_ai.py --demo       Демонстрация возможностей
    python main_ai.py --help       Эта справка

ВОЗМОЖНОСТИ:
    💻 Кодирование
       • Генерация функций, классов, шаблонов
       • Объяснение концепций
       • Поиск и исправление ошибок
       • Примеры кода по темам

    🎮 Разработка игр
       • Идеи для игр
       • Генерация квестов
       • Названия (персонажи, локации, предметы)
       • Шаблоны Pygame
       • Рекомендации движков

    💙 Эмоциональная поддержка
       • Анализ настроения
       • Поддерживающие ответы
       • Ободрение

    🧠 Обучение
       • Оценка ответов (/good, /bad)
       • Запоминание предпочтений
       • Поиск в истории диалогов

КОМАНДЫ В ЧАТЕ:
    /help       Список команд
    /good       Отметить ответ как хороший
    /bad        Отметить ответ как плохой
    /remember   Запомнить информацию
    /search     Поиск в памяти
    /mood       Сообщить о настроении
    /code       Генерация кода
    /game       Помощь с играми
    /explain    Объяснить концепцию
    /debug      Найти ошибку
    /stats      Статистика обучения
    /clear      Очистить экран
    /exit       Выйти
""")


def main():
    """Главная функция"""
    # Проверка зависимостей
    check_dependencies()
    
    # Обработка аргументов
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        show_help()
        return
    
    if '--test' in args or '-t' in args:
        run_test_mode()
        return
    
    if '--demo' in args or '-d' in args:
        run_demo_mode()
        return
    
    if '--simple' in args or '-s' in args:
        run_simple_mode()
        return
    
    # По умолчанию - основной режим
    run_main_mode()


if __name__ == '__main__':
    main()
