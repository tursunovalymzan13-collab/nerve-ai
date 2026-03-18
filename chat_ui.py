"""
Интерфейс чата ИИ-помощника
Консольный UI с поддержкой команд, истории, подсветки
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from typing import Optional
from datetime import datetime

try:
    from .ai_core import AIAssistant
except ImportError:
    from ai_core import AIAssistant


# ANSI цвета для терминала
class Colors:
    """Цвета для консольного вывода"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Цвета текста
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Цвета фона
    BG_BLACK = '\033[40m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    
    @classmethod
    def disable(cls):
        """Отключить цвета (для Windows без ANSI)"""
        cls.RESET = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.BLACK = ''
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.MAGENTA = ''
        cls.CYAN = ''
        cls.WHITE = ''
        cls.BG_BLACK = ''
        cls.BG_BLUE = ''
        cls.BG_GREEN = ''


# Проверка поддержки ANSI в Windows
if sys.platform == 'win32':
    try:
        from colorama import init
        init()
    except ImportError:
        # Если colorama нет, пробуем включить ANSI
        os.system('')


class ChatUI:
    """Консольный интерфейс чата"""
    
    def __init__(self, assistant: AIAssistant):
        self.assistant = assistant
        self.history = []
        self.max_history = 100
        self.running = True
    
    def print_banner(self):
        """Показать приветственный баннер"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║          ИИ-ПОМОЩНИК v1.0                    ║
║          Твой персональный помощник          ║
╠══════════════════════════════════════════════════════════╣
║  💻 Код  │  🎮 Игры  │  💙 Поддержка  │  🧠 Обучение    ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}Введите /help для списка команд{Colors.RESET}
{Colors.DIM}─────────────────────────────────────────────────────────{Colors.RESET}
"""
        print(banner)
        
        # Приветствие от ассистента
        greeting = self.assistant.process_message("привет")
        self._print_ai_message(greeting)
    
    def print_welcome(self):
        """Показать простое приветствие"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══ ИИ-ПОМОЩНИК ═══{Colors.RESET}\n")
        greeting = self.assistant.process_message("привет")
        self._print_ai_message(greeting)
        print(f"\n{Colors.DIM}Введите /help для команд{Colors.RESET}\n")
    
    def _print_user_message(self, message: str):
        """Вывести сообщение пользователя"""
        timestamp = datetime.now().strftime("%H:%M")
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.YELLOW}Вы:{Colors.RESET} {message}")
    
    def _print_ai_message(self, message: str):
        """Вывести ответ ИИ"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Разделить сообщение на строки
        lines = message.split('\n')
        
        # Первая строка с индикатором
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.BLUE}ИИ:{Colors.RESET} {lines[0]}")
        
        # Остальные строки с отступом
        for line in lines[1:]:
            if line.strip():
                print(f"  {Colors.DIM}│{Colors.RESET} {line}")
    
    def _print_error(self, message: str):
        """Вывести ошибку"""
        print(f"{Colors.RED}❌ {message}{Colors.RESET}")
    
    def _print_system(self, message: str):
        """Вывести системное сообщение"""
        print(f"{Colors.DIM}⚙ {message}{Colors.RESET}")
    
    def _add_to_history(self, user_msg: str, ai_msg: str):
        """Добавить в историю"""
        self.history.append({
            'user': user_msg,
            'ai': ai_msg,
            'timestamp': datetime.now()
        })
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def _process_input(self, user_input: str) -> bool:
        """
        Обработать ввод пользователя
        Возвращает False если нужно выйти
        """
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Проверка на выход
        if user_input.lower() in ['/exit', '/quit', 'выход', 'пока']:
            return False
        
        # Вывод сообщения пользователя
        self._print_user_message(user_input)
        
        # Обработка
        response = self.assistant.process_message(user_input)
        
        # Проверка на выход
        if response == 'goodbye':
            self._print_ai_message("До свидания! Возвращайся скорее! 💙")
            return False
        
        # Проверка на очистку
        if response == '\x08':
            os.system('cls' if sys.platform == 'win32' else 'clear')
            self.print_welcome()
            return True
        
        # Вывод ответа
        self._print_ai_message(response)
        
        # Добавление в историю
        self._add_to_history(user_input, response)
        
        return True
    
    def run(self, simple_mode: bool = False):
        """Запустить чат"""
        try:
            if simple_mode:
                self.print_welcome()
            else:
                self.print_banner()
            
            while self.running:
                try:
                    # Приглашение к вводу
                    user_input = input(f"\n{Colors.GREEN}➤{Colors.RESET} ")
                    
                    # Обработка
                    self.running = self._process_input(user_input)
                    
                except KeyboardInterrupt:
                    print(f"\n{Colors.DIM}Нажмите /exit для выхода{Colors.RESET}")
                except EOFError:
                    break
            
            # Завершение
            self._cleanup()
            
        except Exception as e:
            self._print_error(f"Ошибка: {e}")
            self._cleanup()
    
    def _cleanup(self):
        """Очистка при завершении"""
        print(f"\n{Colors.DIM}Сохранение и закрытие...{Colors.RESET}")
        self.assistant.close()
        print(f"{Colors.GREEN}✓ До встречи!{Colors.RESET}\n")
    
    def show_history(self, limit: int = 10):
        """Показать историю"""
        print(f"\n{Colors.BOLD}═══ ИСТОРИЯ ({min(limit, len(self.history))} последних) ═══{Colors.RESET}\n")
        
        for i, record in enumerate(self.history[-limit:], 1):
            print(f"{Colors.DIM}{i}. [{record['timestamp'].strftime('%H:%M')}]{Colors.RESET}")
            print(f"   {Colors.YELLOW}Вы:{Colors.RESET} {record['user'][:60]}...")
            print(f"   {Colors.BLUE}ИИ:{Colors.RESET} {record['ai'][:60]}...\n")


class SimpleChatUI(ChatUI):
    """Упрощённая версия без цветов"""
    
    def __init__(self, assistant: AIAssistant):
        super().__init__(assistant)
        Colors.disable()
    
    def print_banner(self):
        """Показать простой баннер"""
        print("""
╔══════════════════════════════════════════════════════════╗
║          ИИ-ПОМОЩНИК v1.0                                ║
║          Твой персональный помощник                      ║
╠══════════════════════════════════════════════════════════╣
║  Код  |  Игры  |  Поддержка  |  Обучение                ║
╚══════════════════════════════════════════════════════════╝

Введите /help для списка команд
""")
        greeting = self.assistant.process_message("привет")
        self._print_ai_message(greeting)


def create_chat(simple_mode: bool = False) -> ChatUI:
    """Создать интерфейс чата"""
    assistant = AIAssistant()
    
    if simple_mode:
        return SimpleChatUI(assistant)
    else:
        return ChatUI(assistant)


def run_chat(simple_mode: bool = False):
    """Быстрый запуск чата"""
    ui = create_chat(simple_mode)
    ui.run()


if __name__ == '__main__':
    # Проверка аргументов командной строки
    simple = '--simple' in sys.argv or '-s' in sys.argv
    run_chat(simple_mode=simple)
