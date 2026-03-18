"""
AccessController - Система управления доступом

Определяет уровень доступа пользователя на основе:
- Уникального ID
- Ключа доступа (API Key)
- Токена аутентификации

Механизм проверки:
1. Проверка наличия ключа владельца
2. Проверка токена пользователя
3. Выдача соответствующего интерфейса
"""

import hashlib
import secrets
import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import uuid


class AuthStatus(Enum):
    """Статус аутентификации"""
    OWNER = "owner"
    USER = "user"
    GUEST = "guest"
    INVALID = "invalid"


class AccessController:
    """
    Контроллер доступа
    
    Управляет аутентификацией и выдаёт соответствующий интерфейс
    """
    
    def __init__(self, config_path: str = "access_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._init_default_owner()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Конфигурация по умолчанию
        return {
            "owner_key_hash": "",
            "users": {},
            "settings": {
                "session_timeout_hours": 24,
                "max_failed_attempts": 5,
                "lockout_duration_minutes": 30
            }
        }
    
    def _save_config(self):
        """Сохранить конфигурацию"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _init_default_owner(self):
        """Инициализировать ключ владельца по умолчанию"""
        if not self.config.get("owner_key_hash"):
            # Генерация ключа владельца
            default_key = "owner_secret_key_2026"
            self.config["owner_key_hash"] = hashlib.sha256(default_key.encode()).hexdigest()
            self.config["owner_key_display"] = self._generate_display_key()
            self._save_config()
    
    def _generate_display_key(self) -> str:
        """Сгенерировать отображаемый ключ"""
        return secrets.token_hex(16)
    
    def generate_owner_key(self) -> str:
        """
        Сгенерировать новый ключ владельца
        
        Returns:
            str: Ключ владельца (показать только один раз!)
        """
        new_key = secrets.token_urlsafe(32)
        self.config["owner_key_hash"] = hashlib.sha256(new_key.encode()).hexdigest()
        self._save_config()
        return new_key
    
    def register_user(self, username: str, metadata: Optional[Dict] = None) -> str:
        """
        Зарегистрировать нового пользователя
        
        Args:
            username: Имя пользователя
            metadata: Дополнительные данные
        
        Returns:
            str: API ключ пользователя
        """
        if username in self.config.get("users", {}):
            raise ValueError(f"Пользователь '{username}' уже существует")
        
        api_key = secrets.token_urlsafe(24)
        user_id = str(uuid.uuid4())
        
        if "users" not in self.config:
            self.config["users"] = {}
        
        self.config["users"][username] = {
            "user_id": user_id,
            "api_key_hash": hashlib.sha256(api_key.encode()).hexdigest(),
            "created_at": datetime.now().isoformat(),
            "access_level": "user",
            "metadata": metadata or {},
            "failed_attempts": 0,
            "locked_until": None
        }
        
        self._save_config()
        
        # Вернуть ключ только один раз
        return api_key
    
    def authenticate(self, credentials: Dict[str, str]) -> Tuple[AuthStatus, Optional[str]]:
        """
        Аутентифицировать пользователя
        
        Args:
            credentials: Данные для аутентификации
                - owner_key: Ключ владельца
                - api_key: API ключ пользователя
                - username: Имя пользователя
        
        Returns:
            Tuple[AuthStatus, Optional[str]]: Статус и user_id
        """
        # Проверка владельца
        if "owner_key" in credentials:
            owner_key = credentials["owner_key"]
            expected_hash = self.config.get("owner_key_hash", "")
            
            if hashlib.sha256(owner_key.encode()).hexdigest() == expected_hash:
                user_id = "owner_" + str(uuid.uuid4())
                self._create_session(user_id, AuthStatus.OWNER)
                return AuthStatus.OWNER, user_id
        
        # Проверка пользователя
        if "api_key" in credentials and "username" in credentials:
            username = credentials["username"]
            api_key = credentials["api_key"]
            
            users = self.config.get("users", {})
            if username in users:
                user_data = users[username]
                
                # Проверка блокировки
                if user_data.get("locked_until"):
                    lock_time = datetime.fromisoformat(user_data["locked_until"])
                    if datetime.now() < lock_time:
                        return AuthStatus.INVALID, None
                    else:
                        # Сброс блокировки
                        user_data["locked_until"] = None
                        user_data["failed_attempts"] = 0
                
                # Проверка ключа
                expected_hash = user_data.get("api_key_hash", "")
                if hashlib.sha256(api_key.encode()).hexdigest() == expected_hash:
                    user_id = user_data.get("user_id")
                    self._create_session(user_id, AuthStatus.USER)
                    return AuthStatus.USER, user_id
                else:
                    # Увеличение счётчика неудачных попыток
                    user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1
                    
                    # Блокировка после превышения лимита
                    if user_data["failed_attempts"] >= self.config["settings"]["max_failed_attempts"]:
                        lockout_minutes = self.config["settings"]["lockout_duration_minutes"]
                        user_data["locked_until"] = (
                            datetime.now() + timedelta(minutes=lockout_minutes)
                        ).isoformat()
                    
                    self._save_config()
                    return AuthStatus.INVALID, None
        
        # Гостевой доступ
        if "guest" in credentials and credentials["guest"]:
            user_id = "guest_" + str(uuid.uuid4())
            self._create_session(user_id, AuthStatus.GUEST)
            return AuthStatus.GUEST, user_id
        
        return AuthStatus.INVALID, None
    
    def _create_session(self, user_id: str, status: AuthStatus):
        """Создать сессию"""
        session_id = secrets.token_urlsafe(32)
        timeout = self.config["settings"]["session_timeout_hours"]
        
        self.sessions[session_id] = {
            "user_id": user_id,
            "status": status.value,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=timeout)
        }
    
    def validate_session(self, session_id: str) -> Optional[AuthStatus]:
        """Проверить валидность сессии"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        if datetime.now() > session["expires_at"]:
            del self.sessions[session_id]
            return None
        
        return AuthStatus(session["status"])
    
    def get_interface_for_user(self, auth_status: AuthStatus, user_id: str, 
                                owner_key: Optional[str] = None):
        """
        Получить соответствующий интерфейс для пользователя
        
        Args:
            auth_status: Статус аутентификации
            user_id: ID пользователя
            owner_key: Ключ владельца (если есть)
        
        Returns:
            AIInterface: Соответствующий интерфейс
        """
        from .interfaces import OwnerInterface, UserInterface, AccessLevel
        
        if auth_status == AuthStatus.OWNER and owner_key:
            return OwnerInterface(user_id, owner_key)
        
        elif auth_status == AuthStatus.USER:
            return UserInterface(user_id)
        
        elif auth_status == AuthStatus.GUEST:
            return UserInterface(user_id)
        
        else:
            # По умолчанию - пользователь с ограничениями
            return UserInterface("anonymous_" + str(uuid.uuid4()))
    
    def revoke_session(self, session_id: str) -> bool:
        """Отозвать сессию"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def list_users(self) -> list:
        """Получить список пользователей (без хешей ключей)"""
        users = self.config.get("users", {})
        return [
            {
                "username": username,
                "user_id": data.get("user_id"),
                "created_at": data.get("created_at"),
                "access_level": data.get("access_level")
            }
            for username, data in users.items()
        ]
    
    def delete_user(self, username: str, requester_status: AuthStatus) -> bool:
        """
        Удалить пользователя
        
        Только владелец может удалять пользователей
        """
        if requester_status != AuthStatus.OWNER:
            return False
        
        if username in self.config.get("users", {}):
            del self.config["users"][username]
            self._save_config()
            return True
        return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """Получить информацию о конфигурации (без чувствительных данных)"""
        return {
            "owner_configured": bool(self.config.get("owner_key_hash")),
            "total_users": len(self.config.get("users", {})),
            "settings": self.config.get("settings", {}),
            "active_sessions": len(self.sessions)
        }


class AccessManager:
    """
    Менеджер доступа - Facade для упрощённой работы
    
    Пример использования:
        manager = AccessManager()
        
        # Аутентификация владельца
        status, user_id = manager.authenticate_owner("your_owner_key")
        interface = manager.get_interface(status, user_id, owner_key="your_owner_key")
        
        # Аутентификация пользователя
        status, user_id = manager.authenticate_user("username", "api_key")
        interface = manager.get_interface(status, user_id)
    """
    
    def __init__(self, config_path: str = "access_config.json"):
        self.controller = AccessController(config_path)
        self.current_session: Optional[str] = None
    
    def authenticate_owner(self, owner_key: str) -> Tuple[AuthStatus, Optional[str]]:
        """Аутентификация владельца"""
        status, user_id = self.controller.authenticate({"owner_key": owner_key})
        return status, user_id
    
    def authenticate_user(self, username: str, api_key: str) -> Tuple[AuthStatus, Optional[str]]:
        """Аутентификация пользователя"""
        status, user_id = self.controller.authenticate({
            "username": username,
            "api_key": api_key
        })
        return status, user_id
    
    def authenticate_guest(self) -> Tuple[AuthStatus, Optional[str]]:
        """Гостевая аутентификация"""
        status, user_id = self.controller.authenticate({"guest": True})
        return status, user_id
    
    def get_interface(self, auth_status: AuthStatus, user_id: str,
                      owner_key: Optional[str] = None):
        """Получить интерфейс для пользователя"""
        return self.controller.get_interface_for_user(
            auth_status, user_id, owner_key
        )
    
    def register_new_user(self, username: str, metadata: Optional[Dict] = None) -> str:
        """Зарегистрировать нового пользователя"""
        return self.controller.register_user(username, metadata)
    
    def get_owner_key_info(self) -> str:
        """Получить информацию о ключе владельца"""
        config = self.controller.config
        return config.get("owner_key_display", "Ключ не настроен")
