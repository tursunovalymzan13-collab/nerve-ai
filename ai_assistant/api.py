"""
FastAPI приложение с разделением эндпоинтов для Owner и User

Эндпоинты:
- /api/v1/owner/* - Полный доступ для владельца
- /api/v1/user/* - Ограниченный доступ с Safety Layer
- /api/v1/auth/* - Аутентификация и управление доступом
"""

from fastapi import FastAPI, HTTPException, Header, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uvicorn

from .access_controller import AccessController, AccessManager, AuthStatus
from .interfaces import OwnerInterface, UserInterface, AccessLevel


# === Модели данных ===

class AuthRequest(BaseModel):
    """Запрос аутентификации"""
    owner_key: Optional[str] = Field(None, description="Ключ владельца")
    username: Optional[str] = Field(None, description="Имя пользователя")
    api_key: Optional[str] = Field(None, description="API ключ пользователя")
    guest: bool = Field(False, description="Гостевой доступ")


class AuthResponse(BaseModel):
    """Ответ аутентификации"""
    status: str
    access_level: str
    user_id: Optional[str] = None
    session_token: Optional[str] = None
    message: str = ""


class ChatRequest(BaseModel):
    """Запрос к ИИ"""
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Ответ ИИ"""
    status: str
    response: str
    access_level: str
    safety_checked: bool = False
    blocked: bool = False
    block_reason: Optional[str] = None


class OwnerCommandRequest(BaseModel):
    """Команда владельца"""
    command: str
    args: Optional[Dict[str, Any]] = None


class SystemConfigRequest(BaseModel):
    """Запрос изменения конфигурации"""
    settings: Dict[str, Any]


# === Приложение FastAPI ===

app = FastAPI(
    title="AI Assistant API",
    description="API с двумя уровнями доступа: Owner и User",
    version="1.0.0"
)

# Безопасность
security = HTTPBearer(auto_error=False)

# Менеджер доступа
access_manager = AccessManager()

# Активные сессии
active_sessions: Dict[str, Dict[str, Any]] = {}


# === Зависимости для аутентификации ===

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Dict[str, Any]:
    """Получить текущего пользователя из токена"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется аутентификация"
        )
    
    token = credentials.credentials
    if token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен сессии"
        )
    
    session = active_sessions[token]
    if datetime.now() > session["expires_at"]:
        del active_sessions[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия истекла"
        )
    
    return session


async def require_owner(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Требовать уровень доступа Owner"""
    if current_user["access_level"] != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется уровень доступа Owner"
        )
    return current_user


# === Эндпоинты аутентификации ===

@app.post("/api/v1/auth/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    """
    Аутентификация пользователя
    
    - **owner_key**: Ключ владельца (приоритетный доступ)
    - **username** + **api_key**: Данные пользователя
    - **guest**: Гостевой доступ
    """
    # Аутентификация владельца
    if request.owner_key:
        status_auth, user_id = access_manager.authenticate_owner(request.owner_key)
        if status_auth == AuthStatus.OWNER:
            session_token = access_manager.controller.sessions.popitem()[0]
            active_sessions[session_token] = {
                "user_id": user_id,
                "access_level": "owner",
                "expires_at": datetime.now().replace(hour=23, minute=59, second=59)
            }
            return AuthResponse(
                status="success",
                access_level="owner",
                user_id=user_id,
                session_token=session_token,
                message="Добро пожаловать, Владелец!"
            )
    
    # Аутентификация пользователя
    if request.username and request.api_key:
        status_auth, user_id = access_manager.authenticate_user(
            request.username, request.api_key
        )
        if status_auth == AuthStatus.USER:
            session_token = access_manager.controller.sessions.popitem()[0]
            active_sessions[session_token] = {
                "user_id": user_id,
                "access_level": "user",
                "expires_at": datetime.now().replace(hour=23, minute=59, second=59)
            }
            return AuthResponse(
                status="success",
                access_level="user",
                user_id=user_id,
                session_token=session_token,
                message=f"Добро пожаловать, {request.username}!"
            )
    
    # Гостевой доступ
    if request.guest:
        status_auth, user_id = access_manager.authenticate_guest()
        if status_auth == AuthStatus.GUEST:
            session_token = access_manager.controller.sessions.popitem()[0]
            active_sessions[session_token] = {
                "user_id": user_id,
                "access_level": "guest",
                "expires_at": datetime.now().replace(hour=23, minute=59, second=59)
            }
            return AuthResponse(
                status="success",
                access_level="guest",
                user_id=user_id,
                session_token=session_token,
                message="Гостевой доступ активирован"
            )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учётные данные"
    )


@app.post("/api/v1/auth/logout")
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Выйти из системы"""
    # Найти и удалить сессию
    for token, session in list(active_sessions.items()):
        if session["user_id"] == current_user["user_id"]:
            del active_sessions[token]
            return {"status": "success", "message": "Выход выполнен"}
    
    return {"status": "error", "message": "Сессия не найдена"}


@app.get("/api/v1/auth/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return {
        "user_id": current_user["user_id"],
        "access_level": current_user["access_level"],
        "expires_at": current_user["expires_at"].isoformat()
    }


# === Эндпоинты Владельца (Owner) ===

@app.post("/api/v1/owner/chat", response_model=ChatResponse)
async def owner_chat(
    request: ChatRequest,
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """
    Чат с ИИ для владельца (без ограничений)
    
    Только Owner имеет доступ к этому эндпоинту
    """
    owner_key = "owner_secret_key_2026"  # В production получать из secure storage
    interface = OwnerInterface(current_user["user_id"], owner_key)
    
    result = interface.process_request(request.message, request.context)
    
    return ChatResponse(
        status=result.get("status", "success"),
        response=result.get("message", str(result)),
        access_level="owner",
        safety_checked=False,
        blocked=False
    )


@app.post("/api/v1/owner/command")
async def owner_command(
    request: OwnerCommandRequest,
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """
    Выполнить команду владельца
    
    Доступно только Owner
    """
    owner_key = "owner_secret_key_2026"
    interface = OwnerInterface(current_user["user_id"], owner_key)
    
    command = f"/{request.command}"
    if request.args:
        import json
        command += f" {json.dumps(request.args)}"
    
    result = interface.process_request(command)
    return result


@app.get("/api/v1/owner/status")
async def owner_status(
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """Получить статус владельца"""
    owner_key = "owner_secret_key_2026"
    interface = OwnerInterface(current_user["user_id"], owner_key)
    
    return {
        "status": "success",
        "owner_verified": True,
        "capabilities": interface.get_capabilities(),
        "stats": interface.get_stats()
    }


@app.get("/api/v1/owner/logs")
async def owner_logs(
    limit: int = 10,
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """Получить логи (только Owner)"""
    owner_key = "owner_secret_key_2026"
    interface = OwnerInterface(current_user["user_id"], owner_key)
    
    result = interface._cmd_view_logs(str(limit))
    return result


@app.post("/api/v1/owner/config")
async def owner_config(
    request: SystemConfigRequest,
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """Изменить системную конфигурацию (только Owner)"""
    owner_key = "owner_secret_key_2026"
    interface = OwnerInterface(current_user["user_id"], owner_key)
    
    import json
    result = interface._cmd_system_config(json.dumps(request.settings))
    return result


@app.get("/api/v1/owner/users")
async def list_users(
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """Получить список пользователей (только Owner)"""
    return {
        "status": "success",
        "users": access_manager.controller.list_users()
    }


@app.post("/api/v1/owner/users/register")
async def register_user(
    username: str,
    current_user: Dict[str, Any] = Depends(require_owner)
):
    """Зарегистрировать нового пользователя (только Owner)"""
    try:
        api_key = access_manager.register_new_user(username)
        return {
            "status": "success",
            "username": username,
            "api_key": api_key,
            "message": "Сохраните этот ключ! Он показывается только один раз."
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# === Эндпоинты Пользователя (User) ===

@app.post("/api/v1/user/chat", response_model=ChatResponse)
async def user_chat(
    request: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Чат с ИИ для пользователя (с Safety Layer)
    
    Все запросы проходят проверку безопасности
    """
    interface = UserInterface(current_user["user_id"])
    
    result = interface.process_request(request.message, request.context)
    
    return ChatResponse(
        status=result.get("status", "success"),
        response=result.get("response", result.get("message", str(result))),
        access_level="user",
        safety_checked=result.get("safety_checked", False),
        blocked=result.get("status") == "blocked",
        block_reason=result.get("reason")
    )


@app.get("/api/v1/user/capabilities")
async def user_capabilities(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Получить доступные возможности пользователя"""
    interface = UserInterface(current_user["user_id"])
    
    return {
        "status": "success",
        "capabilities": interface.get_capabilities(),
        "safety_stats": interface.get_safety_stats()
    }


@app.get("/api/v1/user/stats")
async def user_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Получить статистику пользователя"""
    interface = UserInterface(current_user["user_id"])
    
    return {
        "status": "success",
        "stats": interface.get_stats(),
        "safety_filter": interface.get_safety_stats()
    }


# === Общие эндпоинты ===

@app.get("/")
async def root():
    """Информация о API"""
    return {
        "name": "AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/v1/auth/login",
            "owner_chat": "/api/v1/owner/chat",
            "user_chat": "/api/v1/user/chat"
        }
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# === Запуск ===

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║     AI Assistant API - FastAPI                           ║
║     Два уровня доступа: Owner / User                     ║
║                                                          ║
║     Запуск сервера:                                      ║
║     ➤ http://127.0.0.1:8000                             ║
║                                                          ║
║     Документация:                                        ║
║     ➤ http://127.0.0.1:8000/docs                        ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
