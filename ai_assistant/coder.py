"""
Модуль кодинга ИИ-помощника
Генерация кода, шаблоны, паттерны, объяснения
"""

from typing import Dict, List, Optional, Any

try:
    from .memory import Memory
except ImportError:
    from memory import Memory


class CodeAssistant:
    """Помощник по программированию"""
    
    # Шаблоны кода для различных задач
    CODE_TEMPLATES = {
        'python_function': '''
def {name}({params}):
    """{docstring}"""
    {body}
    return {return_value}
''',
        'python_class': '''
class {name}:
    """{docstring}"""
    
    def __init__(self, {init_params}):
        {init_body}
    
    def {method_name}(self, {method_params}):
        {method_body}
''',
        'python_decorator': '''
def {name}(func):
    def wrapper(*args, **kwargs):
        # До вызова функции
        result = func(*args, **kwargs)
        # После вызова функции
        return result
    return wrapper
''',
        'python_context_manager': '''
class {name}:
    def __enter__(self):
        # Инициализация
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Очистка
        pass
''',
        'javascript_function': '''
function {name}({params}) {{
    {body}
    return {return_value};
}}
''',
        'javascript_arrow': '''
const {name} = ({params}) => {{
    {body}
}};
''',
        'javascript_class': '''
class {name} {{
    constructor({params}) {{
        {body}
    }}
    
    {method}() {{
        {methodBody}
    }}
}}
''',
        'sql_select': '''
SELECT {columns}
FROM {table}
WHERE {condition}
ORDER BY {order}
LIMIT {limit};
''',
        'sql_insert': '''
INSERT INTO {table} ({columns})
VALUES ({values});
''',
        'html_template': '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{css}">
</head>
<body>
    {body}
    <script src="{js}"></script>
</body>
</html>
''',
        'css_basic': '''
{selector} {{
    display: {display};
    margin: {margin};
    padding: {padding};
    background-color: {bg-color};
    color: {color};
}}
''',
        'try_except': '''
try:
    {try_body}
except {exception} as e:
    {except_body}
finally:
    {finally_body}
''',
        'file_read': '''
with open('{filename}', 'r', encoding='utf-8') as f:
    content = f.read()
''',
        'file_write': '''
with open('{filename}', 'w', encoding='utf-8') as f:
    f.write({content})
''',
        'database_connection': '''
import sqlite3

conn = sqlite3.connect('{database}')
cursor = conn.cursor()

cursor.execute({query})

conn.commit()
conn.close()
''',
        'api_request': '''
import requests

response = requests.get('{url}', params={params})
data = response.json()
''',
        'async_function': '''
async def {name}({params}):
    {body}
    return {return_value}
''',
        'dataclass': '''
from dataclasses import dataclass, field
from typing import {types}

@dataclass
class {name}:
    {fields}
'''
    }
    
    # Паттерны для типичных задач
    CODING_PATTERNS = {
        'singleton': '''
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
''',
        'observer': '''
class Observer:
    def update(self, data):
        pass

class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)
''',
        'factory': '''
class Factory:
    @staticmethod
    def create(obj_type, *args, **kwargs):
        return obj_type(*args, **kwargs)
''',
        'decorator_pattern': '''
class Component:
    def operation(self):
        pass

class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()
''',
        'builder': '''
class Builder:
    def __init__(self):
        self.result = None
    
    def reset(self):
        self.result = []
    
    def build(self):
        return self.result
'''
    }
    
    # Объяснения концепций
    CONCEPT_EXPLANATIONS = {
        'переменная': 'Переменная — это именованное место в памяти, где хранится значение. В Python тип определяется автоматически.',
        'функция': 'Функция — это блок кода, который выполняет определённую задачу и может возвращать результат.',
        'класс': 'Класс — это шаблон для создания объектов. Определяет атрибуты (данные) и методы (функции).',
        'наследование': 'Наследование позволяет классу получать атрибуты и методы от другого класса.',
        'полиморфизм': 'Полиморфизм позволяет объектам разных классов иметь методы с одинаковым именем.',
        'инкапсуляция': 'Инкапсуляция скрывает внутреннее состояние объекта и требует взаимодействия через методы.',
        'декоратор': 'Декоратор — это функция, которая модифицирует поведение другой функции.',
        'генератор': 'Генератор — это функция, которая возвращает итератор и использует ключевое слово yield.',
        'асинхронность': 'Асинхронный код позволяет выполнять задачи без блокировки основного потока.',
        'рекурсия': 'Рекурсия — это когда функция вызывает саму себя для решения подзадач.'
    }
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self._load_custom_patterns()
    
    def _load_custom_patterns(self):
        """Загрузить пользовательские паттерны из памяти"""
        patterns = self.memory.get_code_patterns_by_language('python')
        for pattern in patterns:
            name = f"custom_{pattern['name']}"
            if name not in self.CODE_TEMPLATES:
                self.CODE_TEMPLATES[name] = pattern['pattern']
    
    def generate_function(self, name: str, params: List[str], 
                          docstring: str = '', return_type: str = 'None',
                          body_lines: List[str] = None) -> str:
        """Сгенерировать функцию Python"""
        template = self.CODE_TEMPLATES['python_function']
        
        return template.format(
            name=name,
            params=', '.join(params),
            docstring=docstring,
            body='\n    '.join(body_lines) if body_lines else 'pass',
            return_value='None' if return_type == 'None' else 'result'
        )
    
    def generate_class(self, name: str, init_params: List[str],
                       methods: List[Dict] = None, docstring: str = '') -> str:
        """Сгенерировать класс Python"""
        template = self.CODE_TEMPLATES['python_class']
        
        init_body = '\n        '.join([f'self.{p} = {p}' for p in init_params]) or 'pass'
        
        methods_code = ''
        if methods:
            for method in methods:
                methods_code += f'''
    def {method.get('name', 'method')}({', '.join(method.get('params', ['self']))}):
        {method.get('body', 'pass')}
'''
        
        return template.format(
            name=name,
            docstring=docstring,
            init_params=', '.join(init_params),
            init_body=init_body,
            method_name=methods[0].get('name', 'method') if methods else 'method',
            method_params=', '.join(methods[0].get('params', ['self'])) if methods else '',
            method_body=methods[0].get('body', 'pass') if methods else 'pass'
        )
    
    def get_pattern(self, pattern_name: str) -> Optional[str]:
        """Получить шаблон по имени"""
        return self.CODE_TEMPLATES.get(pattern_name) or \
               self.CODING_PATTERNS.get(pattern_name)
    
    def explain_concept(self, concept: str) -> str:
        """Объяснить концепцию программирования"""
        concept_lower = concept.lower()
        
        for key, explanation in self.CONCEPT_EXPLANATIONS.items():
            if key in concept_lower:
                return explanation
        
        return f"Концепция '{concept}' требует дополнительного контекста. Уточните, что именно вас интересует."
    
    def debug_code(self, code: str, error_message: str = '') -> str:
        """Анализ кода и поиск ошибок"""
        suggestions = []
        
        # Проверка распространённых ошибок
        if 'IndentationError' in error_message:
            suggestions.append("❗ Проверьте отступы — в Python они должны быть одинаковыми (обычно 4 пробела)")
        
        if 'NameError' in error_message:
            suggestions.append("❗ Переменная или функция не определена. Проверьте имя и область видимости")
        
        if 'TypeError' in error_message:
            suggestions.append("❗ Несоответствие типов. Проверьте, какие типы данных вы используете")
        
        if 'KeyError' in error_message:
            suggestions.append("❗ Ключ не найден в словаре. Проверьте наличие ключа перед доступом")
        
        if 'IndexError' in error_message:
            suggestions.append("❗ Индекс вне диапазона. Проверьте длину списка/строки")
        
        if 'AttributeError' in error_message:
            suggestions.append("❗ Атрибут или метод не существует. Проверьте имя и тип объекта")
        
        if 'ImportError' in error_message or 'ModuleNotFoundError' in error_message:
            suggestions.append("❗ Модуль не найден. Установите его через pip или проверьте имя")
        
        if 'SyntaxError' in error_message:
            suggestions.append("❗ Синтаксическая ошибка. Проверьте скобки, кавычки, двоеточия")
        
        if 'FileNotFoundError' in error_message:
            suggestions.append("❗ Файл не найден. Проверьте путь и существование файла")
        
        if 'ZeroDivisionError' in error_message:
            suggestions.append("❗ Деление на ноль. Добавьте проверку перед делением")
        
        if 'ValueError' in error_message:
            suggestions.append("❗ Неправильное значение. Проверьте формат данных")
        
        # Проверка кода на типичные проблемы
        if 'def ' in code and ': ' not in code and ':\n' not in code:
            suggestions.append("⚠ После объявления функции нужно двоеточие")
        
        if 'if ' in code and ': ' not in code and ':\n' not in code:
            suggestions.append("⚠ После условия if нужно двоеточие")
        
        if code.count('(') != code.count(')'):
            suggestions.append("⚠ Несбалансированные скобки ()")
        
        if code.count('[') != code.count(']'):
            suggestions.append("⚠ Несбалансированные квадратные скобки []")
        
        if not suggestions:
            suggestions.append("Код выглядит корректно. Если есть ошибка, пришлите текст ошибки для анализа.")
        
        return "\n".join(suggestions)
    
    def optimize_code(self, code: str) -> Dict[str, Any]:
        """Предложить оптимизации кода"""
        suggestions = []
        
        # Проверка на возможность использования list comprehension
        if 'for ' in code and 'append' in code:
            suggestions.append("💡 Рассмотрите использование list comprehension для компактности")
        
        # Проверка на повторяющиеся вычисления
        if code.count('len(') > 2:
            suggestions.append("💡 Сохраните результат len() в переменную, если вызываете много раз")
        
        # Проверка на возможность использования get() для словарей
        if 'if ' in code and 'in ' in code and '[' in code:
            suggestions.append("💡 Используйте dict.get(key) вместо проверки ключа через if")
        
        # Проверка на строковые конкатенации в цикле
        if 'for ' in code and '+=' in code and 'str' in code:
            suggestions.append("💡 Используйте ''.join(list) вместо конкатенации в цикле")
        
        # Проверка на возможность использования enumerate
        if 'range(len(' in code:
            suggestions.append("💡 Используйте enumerate() вместо range(len())")
        
        if not suggestions:
            suggestions.append("Код выглядит оптимально!")
        
        return {
            'suggestions': suggestions,
            'original_lines': len(code.split('\n'))
        }
    
    def save_custom_pattern(self, name: str, code: str, language: str = 'python',
                            description: str = ''):
        """Сохранить пользовательский паттерн"""
        self.memory.add_code_pattern(name, code, language, description)
    
    def get_code_examples(self, topic: str) -> List[str]:
        """Получить примеры кода по теме"""
        examples = {
            'цикл': [
                "for i in range(10):\n    print(i)",
                "while condition:\n    do_something()",
                "for key, value in dictionary.items():\n    print(key, value)"
            ],
            'список': [
                "my_list = [1, 2, 3, 4, 5]",
                "squares = [x**2 for x in range(10)]",
                "filtered = [x for x in numbers if x > 0]"
            ],
            'словарь': [
                "my_dict = {'key': 'value', 'name': 'Alice'}",
                "my_dict.get('key', 'default')",
                "{k: v*2 for k, v in data.items()}"
            ],
            'функция': [
                "def greet(name):\n    return f'Hello, {name}!'",
                "add = lambda x, y: x + y",
                "def process(data, callback):\n    return callback(data)"
            ],
            'класс': [
                "class Person:\n    def __init__(self, name):\n        self.name = name",
                "@dataclass\nclass Point:\n    x: int\n    y: int",
                "class Child(Parent):\n    pass"
            ],
            'файл': [
                "with open('file.txt', 'r') as f:\n    content = f.read()",
                "with open('output.txt', 'w') as f:\n    f.write('text')",
                "lines = open('file.txt').readlines()"
            ],
            'исключение': [
                "try:\n    risky_operation()\nexcept Exception as e:\n    print(f'Error: {e}')",
                "try:\n    do_something()\nexcept ValueError:\n    handle_value_error()\nfinally:\n    cleanup()",
                "raise ValueError('Неправильное значение')"
            ]
        }
        
        topic_lower = topic.lower()
        for key, exs in examples.items():
            if key in topic_lower:
                return exs
        
        return ["Примеры не найдены. Уточните тему (цикл, список, функция, класс, файл, исключение)."]
    
    def create_boilerplate(self, project_type: str) -> str:
        """Создать шаблон проекта"""
        boilerplates = {
            'telegram_bot': '''
import telebot
from telebot import types

API_TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
''',
            'flask_app': '''
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
''',
            'django_model': '''
from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
''',
            'pygame_basic': '''
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    # Рисование здесь
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
''',
            'sqlite_db': '''
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_connection(db_name='database.db'):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

if __name__ == '__main__':
    init_db()
'''
        }
        
        return boilerplates.get(project_type, "Шаблон не найден. Доступные: telegram_bot, flask_app, django_model, pygame_basic, sqlite_db")
