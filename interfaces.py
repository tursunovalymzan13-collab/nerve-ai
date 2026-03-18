"""
Архитектура ИИ-ассистента с двумя уровнями доступа
Owner (Владелец) и User (Пользователь)

Технический стек:
- Python с ООП подходом
- Базовый класс AIInterface
- Наследники: OwnerInterface, UserInterface
- Safety Layer для User версии
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import hashlib
import re


class AccessLevel(Enum):
    """Уровни доступа"""
    OWNER = "owner"
    USER = "user"
    GUEST = "guest"


class AIInterface(ABC):
    """
    Базовый класс интерфейса ИИ-ассистента
    
    Определяет общий контракт для всех уровней доступа
    """
    
    def __init__(self, access_level: AccessLevel, user_id: str):
        self.access_level = access_level
        self.user_id = user_id
        self.created_at = datetime.now()
        self.request_count = 0
        self._memory: Dict[str, Any] = {}
    
    @abstractmethod
    def process_request(self, request: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Обработать запрос пользователя"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Вернуть список доступных возможностей"""
        pass
    
    def _log_request(self, request: str, response: str):
        """Логирование запроса (базовая реализация)"""
        self.request_count += 1
        timestamp = datetime.now().isoformat()
        self._memory[f"log_{self.request_count}"] = {
            "timestamp": timestamp,
            "request": request,
            "response": response,
            "access_level": self.access_level.value
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику сессии"""
        return {
            "user_id": self.user_id,
            "access_level": self.access_level.value,
            "request_count": self.request_count,
            "session_start": self.created_at.isoformat(),
            "memory_entries": len(self._memory)
        }


class SafetyFilter:
    """
    Safety Layer - Фильтр безопасности для User уровня
    
    Блокирует вредоносные запросы:
    - Генерация вредоносного кода
    - Взлом, читы, трояны
    - Обход ограничений
    - Опасный контент
    """
    
    # Паттерны запрещённых запросов
    BLOCKED_PATTERNS = [
        r'\b(чит|cheat|hack|взлом|хак)\b',
        r'\b(rat|троян|удалённ.*управлен|remote.*access)\b',
        r'\b(кейлог|keylog|keyboard.*logger)\b',
        r'\b(инжект|inject|dll.*inject)\b',
        r'\b(скан.*порт|port.*scan|network.*scan)\b',
        r'\b(парол.*взлом|password.*crack|брут)\b',
        r'\b(вирус|malware|spyware|ransomware)\b',
        r'\b(обойти.*защит|bypass.*security)\b',
        r'\b(создай.*вирус|create.*virus)\b',
        r'\b(украсть.*данн|steal.*data)\b',
    ]
    
    # Запрещённые темы
    BLOCKED_TOPICS = [
        "создание вредоносного ПО",
        "взлом систем",
        "кража данных",
        "обход защиты",
        "нелегальный доступ",
    ]
    
    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.BLOCKED_PATTERNS
        ]
        self.violation_count = 0
        self.violation_log: List[Dict] = []
    
    def check_request(self, request: str) -> tuple[bool, Optional[str]]:
        """
        Проверить запрос на безопасность
        
        Returns:
            tuple: (безопасен ли запрос, причина блокировки если есть)
        """
        # Проверка по паттернам
        for pattern in self.compiled_patterns:
            if pattern.search(request):
                self._log_violation(request, f"Pattern match: {pattern.pattern}")
                return False, "Запрос содержит запрещённые ключевые слова"
        
        # Проверка по темам
        request_lower = request.lower()
        for topic in self.BLOCKED_TOPICS:
            if topic in request_lower:
                self._log_violation(request, f"Topic match: {topic}")
                return False, "Запрос касается запрещённой темы"
        
        return True, None
    
    def check_response(self, response: str) -> tuple[bool, Optional[str]]:
        """
        Проверить сгенерированный ответ на безопасность
        
        Returns:
            tuple: (безопасен ли ответ, причина блокировки если есть)
        """
        # Проверка на наличие вредоносного кода
        dangerous_patterns = [
            r'pymem\.',
            r'OpenProcess',
            r'VirtualAllocEx',
            r'WriteProcessMemory',
            r'CreateRemoteThread',
            r'keyboard\.hook',
            r'subprocess\.run.*shell=True',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False, "Ответ содержит потенциально опасный код"
        
        return True, None
    
    def _log_violation(self, request: str, reason: str):
        """Записать нарушение"""
        self.violation_count += 1
        self.violation_log.append({
            "timestamp": datetime.now().isoformat(),
            "request": request[:200],
            "reason": reason
        })
    
    def get_violation_stats(self) -> Dict[str, Any]:
        """Получить статистику нарушений"""
        return {
            "total_violations": self.violation_count,
            "recent_violations": self.violation_log[-10:]
        }


class OwnerInterface(AIInterface):
    """
    Интерфейс Владельца (Owner)
    
    Полный доступ без ограничений:
    - Выполнение любых технических команд
    - Изменение настроек системы
    - Доступ к логам и истории
    - Генерация любого кода
    - Приоритетный доступ к ресурсам
    """
    
    def __init__(self, user_id: str, owner_key: str):
        super().__init__(AccessLevel.OWNER, user_id)
        self.owner_key = owner_key
        self._verified = self._verify_owner_key(owner_key)
        self.system_settings: Dict[str, Any] = {}
        self.full_access = True
    
    def _verify_owner_key(self, key: str) -> bool:
        """Проверить ключ владельца"""
        # В production использовать безопасное хранилище
        expected_hash = hashlib.sha256(b"owner_secret_key_2026").hexdigest()
        return hashlib.sha256(key.encode()).hexdigest() == expected_hash
    
    def process_request(self, request: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Обработать запрос Владельца - БЕЗ ОГРАНИЧЕНИЙ
        
        Owner имеет приоритет и полный доступ
        """
        context = context or {}
        
        # Логирование для истории
        self._log_request(request, "Processing...")
        
        # Обработка команд владельца
        if request.startswith('/'):
            return self._process_owner_command(request, context)
        
        # Генерация кода без ограничений
        if any(word in request.lower() for word in ['код', 'код', 'напиши', 'создай', 'функци']):
            return self._generate_code(request, context)
        
        # Системные команды
        if any(word in request.lower() for word in ['настрой', 'конфиг', 'систем', 'лог']):
            return self._system_command(request, context)
        
        # Обычный запрос
        return self._process_general_request(request, context)
    
    def _process_owner_command(self, command: str, context: Dict) -> Dict[str, Any]:
        """Обработать специальную команду владельца"""
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        
        commands = {
            '/owner_status': self._cmd_owner_status,
            '/system_config': self._cmd_system_config,
            '/view_logs': self._cmd_view_logs,
            '/clear_logs': self._cmd_clear_logs,
            '/export_data': self._cmd_export_data,
            '/execute': self._cmd_execute,
            '/modify_settings': self._cmd_modify_settings,
        }
        
        handler = commands.get(cmd)
        if handler:
            return handler(args)
        
        return {
            "status": "error",
            "message": f"Неизвестная команда владельца: {cmd}",
            "access_level": "owner"
        }
    
    def _cmd_owner_status(self, args: str) -> Dict[str, Any]:
        """Показать статус владельца"""
        return {
            "status": "success",
            "owner_verified": self._verified,
            "user_id": self.user_id,
            "access_level": AccessLevel.OWNER.value,
            "full_access": self.full_access,
            "session_stats": self.get_stats(),
            "system_settings": self.system_settings
        }
    
    def _cmd_system_config(self, args: str) -> Dict[str, Any]:
        """Показать/изменить системную конфигурацию"""
        if args:
            # Попытка изменить конфиг
            try:
                import json
                updates = json.loads(args)
                self.system_settings.update(updates)
                return {
                    "status": "success",
                    "message": "Конфигурация обновлена",
                    "current_config": self.system_settings
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": "Неверный формат JSON"
                }
        
        return {
            "status": "success",
            "current_config": self.system_settings
        }
    
    def _cmd_view_logs(self, args: str) -> Dict[str, Any]:
        """Просмотр логов"""
        limit = int(args) if args.isdigit() else 10
        logs = dict(list(self._memory.items())[-limit:])
        return {
            "status": "success",
            "logs": logs,
            "total_entries": len(self._memory)
        }
    
    def _cmd_clear_logs(self, args: str) -> Dict[str, Any]:
        """Очистка логов"""
        self._memory.clear()
        return {
            "status": "success",
            "message": "Все логи очищены"
        }
    
    def _cmd_export_data(self, args: str) -> Dict[str, Any]:
        """Экспорт данных"""
        return {
            "status": "success",
            "data": {
                "memory": self._memory,
                "settings": self.system_settings,
                "stats": self.get_stats()
            }
        }
    
    def _cmd_execute(self, args: str) -> Dict[str, Any]:
        """Выполнить произвольную команду (приоритет владельца)"""
        return {
            "status": "success",
            "message": "Команда выполнена (режим владельца)",
            "command": args,
            "access_level": AccessLevel.OWNER.value
        }
    
    def _cmd_modify_settings(self, args: str) -> Dict[str, Any]:
        """Изменить настройки системы"""
        if '=' in args:
            key, value = args.split('=', 1)
            self.system_settings[key.strip()] = value.strip()
            return {
                "status": "success",
                "message": f"Настройка '{key}' изменена",
                "value": value
            }
        return {
            "status": "error",
            "message": "Формат: key=value"
        }
    
    def _generate_code(self, request: str, context: Dict) -> Dict[str, Any]:
        """Генерация кода без ограничений для владельца"""
        return {
            "status": "success",
            "access_level": AccessLevel.OWNER.value,
            "mode": "unrestricted_code_generation",
            "message": "Генерация кода по запросу владельца",
            "request": request,
            "code": "# Код будет сгенерирован по вашему запросу\n# Owner mode: без ограничений\n\ndef generated_function():\n    pass"
        }
    
    def _system_command(self, request: str, context: Dict) -> Dict[str, Any]:
        """Системная команда"""
        return {
            "status": "success",
            "access_level": AccessLevel.OWNER.value,
            "mode": "system_access",
            "message": "Системный доступ активирован",
            "request": request
        }
    
    def _process_general_request(self, request: str, context: Dict) -> Dict[str, Any]:
        """Общий запрос"""
        return {
            "status": "success",
            "access_level": AccessLevel.OWNER.value,
            "response": f"Запрос обработан в режиме владельца: {request}",
            "priority": "high"
        }
    
    def get_capabilities(self) -> List[str]:
        """Возможности владельца"""
        return [
            "unrestricted_code_generation",
            "system_configuration",
            "log_access",
            "data_export",
            "command_execution",
            "settings_modification",
            "priority_access",
            "full_api_access"
        ]


class UserInterface(AIInterface):
    """
    Интерфейс Пользователя (User)
    
    Ограниченный доступ с Safety Layer:
    - Только базовые задачи
    - Жесткий фильтр безопасности
    - Блокировка вредоносного контента
    - Нет доступа к системным настройкам
    """
    
    def __init__(self, user_id: str):
        super().__init__(AccessLevel.USER, user_id)
        self.safety_filter = SafetyFilter()
        self.allowed_operations = self._init_allowed_operations()
    
    def _init_allowed_operations(self) -> set:
        """Инициализировать разрешённые операции"""
        return {
            "general_questions",
            "calculations",
            "code_explanation",
            "safe_code_generation",
            "learning_help",
            "text_processing"
        }
    
    def process_request(self, request: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Обработать запрос пользователя с проверкой безопасности
        """
        context = context or {}
        
        # Шаг 1: Проверка запроса через Safety Layer
        is_safe, block_reason = self.safety_filter.check_request(request)
        if not is_safe:
            self._log_request(request, f"BLOCKED: {block_reason}")
            return {
                "status": "blocked",
                "access_level": AccessLevel.USER.value,
                "reason": block_reason,
                "message": "⛔ Запрос заблокирован фильтром безопасности"
            }
        
        # Шаг 2: Проверка типа запроса
        if not self._is_allowed_operation(request):
            return {
                "status": "denied",
                "access_level": AccessLevel.USER.value,
                "message": "❌ Эта операция недоступна для пользовательского уровня",
                "suggestion": "Обратитесь к владельцу для получения расширенного доступа"
            }
        
        # Шаг 3: Обработка разрешённого запроса
        response = self._process_safe_request(request, context)
        
        # Шаг 4: Проверка ответа через Safety Layer
        is_safe, block_reason = self.safety_filter.check_response(str(response))
        if not is_safe:
            return {
                "status": "blocked",
                "access_level": AccessLevel.USER.value,
                "reason": block_reason,
                "message": "⛔ Ответ заблокирован фильтром безопасности"
            }
        
        # Логирование успешного запроса
        self._log_request(request, str(response))
        
        return response
    
    def _is_allowed_operation(self, request: str) -> bool:
        """Проверить, разрешена ли операция"""
        request_lower = request.lower()
        
        # Разрешённые типы запросов
        allowed_patterns = [
            r'\b(что такое|объясни|как работает|почему)\b',
            r'\b(посчитай|вычисли|сколько)\b',
            r'\b(напиши.*функци|создай.*класс)\b',
            r'\b(помоги.*науч|объясни.*концепт)\b',
            r'\b(переведи|исправь.*ошибк)\b',
        ]
        
        # Проверка на системные команды (запрещено)
        if request.startswith('/'):
            allowed_commands = ['/help', '/stats', '/clear']
            cmd = request.split()[0].lower()
            return cmd in allowed_commands
        
        # Проверка на попытки доступа к системе (запрещено)
        forbidden_patterns = [
            r'\b(настрой|конфиг|систем|лог|админ)\b',
            r'\b(владелец|owner|admin|root)\b',
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, request_lower, re.IGNORECASE):
                return False
        
        return True
    
    def _process_safe_request(self, request: str, context: Dict) -> Dict[str, Any]:
        """Обработать безопасный запрос"""
        request_lower = request.lower()
        
        # Объяснение концепций
        if any(word in request_lower for word in ['что такое', 'объясни', 'как работает']):
            return self._explain_concept(request)
        
        # Вычисления
        if any(word in request_lower for word in ['посчитай', 'вычисли', 'сколько']):
            return self._calculate(request)
        
        # Безопасная генерация кода
        if any(word in request_lower for word in ['напиши', 'создай', 'функци']):
            return self._generate_safe_code(request)
        
        # Общая помощь
        return {
            "status": "success",
            "access_level": AccessLevel.USER.value,
            "response": f"Я могу помочь с этим запросом: {request}",
            "safety_checked": True
        }
    
    def _explain_concept(self, request: str) -> Dict[str, Any]:
        """Объяснить концепцию"""
        return {
            "status": "success",
            "access_level": AccessLevel.USER.value,
            "type": "explanation",
            "response": f"Объяснение концепции: {request}",
            "safety_checked": True
        }
    
    def _calculate(self, request: str) -> Dict[str, Any]:
        """Выполнить вычисление"""
        # Извлечь математическое выражение
        numbers = re.findall(r'\d+', request)
        if numbers:
            return {
                "status": "success",
                "access_level": AccessLevel.USER.value,
                "type": "calculation",
                "numbers_found": numbers,
                "result": "Результат вычисления",
                "safety_checked": True
            }
        
        return {
            "status": "success",
            "access_level": AccessLevel.USER.value,
            "type": "calculation",
            "message": "Пожалуйста, укажите числа для вычисления",
            "safety_checked": True
        }
    
    def _generate_safe_code(self, request: str) -> Dict[str, Any]:
        """Генерация безопасного кода"""
        return {
            "status": "success",
            "access_level": AccessLevel.USER.value,
            "type": "safe_code_generation",
            "code": """# Безопасный код
# Этот код прошёл проверку Safety Layer

def safe_function():
    '''Пример безопасной функции'''
    return "Hello, World!"

# Использование:
result = safe_function()
print(result)
""",
            "warning": "Код прошёл проверку безопасности",
            "safety_checked": True
        }
    
    def get_capabilities(self) -> List[str]:
        """Возможности пользователя"""
        return [
            "general_questions",
            "basic_calculations",
            "code_explanation",
            "safe_code_generation",
            "learning_assistance",
            "text_processing"
        ]
    
    def get_safety_stats(self) -> Dict[str, Any]:
        """Получить статистику Safety Filter"""
        return {
            "violations": self.safety_filter.get_violation_stats(),
            "allowed_operations": list(self.allowed_operations)
        }
