#!/usr/bin/env python3
"""
NERVE AI - Публичный сервер для хостинга
Использует ВАШ собственный ИИ (ai_core.AIAssistant)
"""

import os
import sys
import json
import hashlib
import secrets
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

# Импорт ВАШЕГО ИИ
try:
    from ai_assistant.ai_core import AIAssistant
    AI_AVAILABLE = True
    print("✅ ai_assistant загружен")
except ImportError as e:
    AI_AVAILABLE = False
    print(f"⚠️  ai_assistant не найден: {e}")

# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

OWNER_KEY = os.getenv("OWNER_KEY", "NERVE_MASTER_KEY_2026")

BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ============================================================================
# СОСТОЯНИЕ
# ============================================================================

class State:
    def __init__(self):
        self.site_enabled = True
        self.logs: List[Dict] = []
        self.users: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        self.ai = AIAssistant() if AI_AVAILABLE else None
    
    def add_log(self, user_id: str, req: str, resp: str, level: str):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "request": req[:500],
            "response": resp[:1000],
            "access_level": level
        })
        if len(self.logs) > 500:
            self.logs = self.logs[-500:]

state = State()

# ============================================================================
# ПРИЛОЖЕНИЕ
# ============================================================================

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
CORS(app)

# ============================================================================
# HTML ШАБЛОН
# ============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NERVE AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #6366f1;
            --bg: #0f172a;
            --bg-card: #1e293b;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
        }
        body {
            font-family: system-ui, sans-serif;
            background: linear-gradient(135deg, var(--bg) 0%, #1e1b4b 100%);
            color: var(--text);
            min-height: 100vh;
        }
        .nav {
            background: rgba(15,23,42,0.95);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(99,102,241,0.2);
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
        }
        .nav-logo {
            font-size: 1.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 100px 20px 40px;
        }
        .chat-container {
            background: var(--bg-card);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(99,102,241,0.2);
        }
        .chat-header {
            padding: 1.5rem;
            background: rgba(99,102,241,0.1);
            border-bottom: 1px solid rgba(99,102,241,0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-messages {
            height: 500px;
            overflow-y: auto;
            padding: 1.5rem;
        }
        .message {
            margin-bottom: 1rem;
            display: flex;
            gap: 1rem;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { flex-direction: row-reverse; }
        .message-avatar {
            width: 40px; height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        .message.user .message-avatar {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
        }
        .message.ai .message-avatar {
            background: linear-gradient(135deg, #ec4899, #db2777);
        }
        .message-content {
            max-width: 75%;
            padding: 1rem 1.5rem;
            border-radius: 16px;
            line-height: 1.6;
        }
        .message.user .message-content {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            border-bottom-right-radius: 4px;
        }
        .message.ai .message-content {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-bottom-left-radius: 4px;
        }
        .chat-input {
            padding: 1.5rem;
            border-top: 1px solid rgba(99,102,241,0.2);
        }
        .input-wrapper {
            display: flex;
            gap: 1rem;
        }
        .input-wrapper input {
            flex: 1;
            padding: 1rem 1.5rem;
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            background: var(--bg);
            color: var(--text);
            font-size: 1rem;
        }
        .input-wrapper input:focus {
            outline: none;
            border-color: #6366f1;
        }
        .send-btn {
            width: 50px; height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            border: none;
            color: white;
            font-size: 1.25rem;
            cursor: pointer;
        }
        .send-btn:hover { transform: scale(1.05); }
        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }
        .modal.active { display: flex; }
        .modal-content {
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 16px;
            max-width: 400px;
            width: 90%;
        }
        .form-group { margin-bottom: 1rem; }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
        }
        .form-group input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: var(--bg);
            color: var(--text);
        }
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white;
        }
        .notification {
            position: fixed;
            top: 100px; right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            color: white;
            z-index: 3000;
        }
        .notification.success { background: #22c55e; }
        .notification.error { background: #ef4444; }
        pre {
            background: #0a0a0f;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }
        code { color: #22c55e; font-family: monospace; }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-logo">🧠 NERVE AI</div>
        <button id="loginBtn" onclick="showLogin()" class="btn btn-primary">🔐 Вход</button>
    </nav>
    
    <div class="container">
        <div class="chat-container">
            <div class="chat-header">
                <span id="chatTitle">Чат с NERVE AI</span>
                <span id="accessIndicator" style="color: #22c55e;">● User</span>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message ai">
                    <div class="message-avatar">🧠</div>
                    <div class="message-content">Готов к работе. Введите запрос.</div>
                </div>
            </div>
            
            <div class="chat-input">
                <div class="input-wrapper">
                    <input type="text" id="messageInput" placeholder="Введите запрос..." onkeypress="if(event.key==='Enter')sendMessage()">
                    <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
                </div>
            </div>
        </div>
    </div>
    
    <div id="loginModal" class="modal">
        <div class="modal-content">
            <h2 style="margin-bottom: 1.5rem; color: #6366f1;">🔐 Вход</h2>
            <div class="form-group">
                <label>Имя пользователя</label>
                <input type="text" id="loginUsername" placeholder="username">
            </div>
            <div class="form-group">
                <label>Пароль</label>
                <input type="password" id="loginPassword" placeholder="password">
            </div>
            <div class="form-group">
                <label>Ключ владельца</label>
                <input type="text" id="ownerKey" placeholder="NERVE_MASTER_KEY_2026">
            </div>
            <button onclick="login()" class="btn btn-primary" style="width: 100%;">Войти</button>
        </div>
    </div>
    
    <div id="notifications"></div>
    
    <script>
        let sessionToken = localStorage.getItem('nerve_session');
        let isOwner = false;
        
        if (sessionToken) {
            const savedOwner = localStorage.getItem('nerve_is_owner');
            if (savedOwner === 'true') {
                isOwner = true;
                updateUI();
            }
        }
        
        function showLogin() {
            document.getElementById('loginModal').classList.add('active');
        }
        
        function hideLogin() {
            document.getElementById('loginModal').classList.remove('active');
        }
        
        function updateUI() {
            if (isOwner) {
                document.getElementById('loginBtn').style.display = 'none';
                document.getElementById('accessIndicator').textContent = '● OWNER';
                document.getElementById('accessIndicator').style.color = '#f59e0b';
                document.getElementById('chatTitle').textContent = 'NERVE AI • OWNER';
            }
        }
        
        function showNotification(msg, type = 'info') {
            const div = document.createElement('div');
            div.className = 'notification ' + type;
            div.textContent = msg;
            document.getElementById('notifications').appendChild(div);
            setTimeout(() => div.remove(), 3000);
        }
        
        async function login() {
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            const ownerKey = document.getElementById('ownerKey').value;
            
            if (!ownerKey) {
                showNotification('Введите ключ владельца', 'error');
                return;
            }
            
            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        username: username || 'user',
                        password: password || 'pass',
                        owner_key: ownerKey 
                    })
                });
                
                const data = await res.json();
                
                if (res.ok && data.success) {
                    sessionToken = data.session_token;
                    isOwner = data.access_level === 'owner';
                    
                    localStorage.setItem('nerve_session', sessionToken);
                    localStorage.setItem('nerve_is_owner', isOwner ? 'true' : 'false');
                    
                    updateUI();
                    hideLogin();
                    showNotification('Добро пожаловать, Owner!', 'success');
                } else {
                    showNotification(data.error || 'Ошибка входа', 'error');
                }
            } catch (e) {
                showNotification('Ошибка подключения', 'error');
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');
            const user_input = input.value.trim();
            
            if (!user_input) return;
            
            addMessage(user_input, 'user');
            input.value = '';
            
            sendBtn.disabled = true;
            input.disabled = true;
            
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + (sessionToken || '')
                    },
                    body: JSON.stringify({ 
                        message: user_input,
                        is_owner: isOwner 
                    })
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    let response = data.response;
                    if (response.includes('```')) {
                        response = response.replace(/```(\\w*)\\n?([\\s\\S]*?)```/g, '<pre><code>$2</code></pre>');
                    }
                    response = response.replace(/\\n/g, '<br>');
                    addMessage(response, 'ai');
                } else {
                    addMessage('⚠️ Ошибка: ' + (data.error || 'Unknown'), 'ai');
                }
            } catch (e) {
                addMessage('⚠️ Ошибка подключения', 'ai');
            }
            
            sendBtn.disabled = false;
            input.disabled = false;
            input.focus();
        }
        
        function addMessage(html, type) {
            const container = document.getElementById('chatMessages');
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            const avatar = type === 'user' ? '👤' : '🧠';
            
            div.innerHTML = '<div class="message-avatar">' + avatar + '</div><div class="message-content">' + html + '</div>';
            
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""

# ============================================================================
# API ЭНДПОИНТЫ
# ============================================================================

@app.route('/')
def index():
    if not state.site_enabled:
        return '<h1 style="color:#ef4444;text-align:center;margin-top:20%;">⚠️ САЙТ ОТКЛЮЧЁН</h1>', 503
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/login', methods=['POST'])
def api_login():
    """Вход в систему"""
    data = request.json
    owner_key = data.get('owner_key', '')
    
    if owner_key == OWNER_KEY:
        session_token = secrets.token_urlsafe(32)
        state.sessions[session_token] = {
            'user_id': 'owner',
            'access_level': 'owner'
        }
        logger.info("✅ Владелец вошёл")
        return jsonify({
            'success': True,
            'session_token': session_token,
            'access_level': 'owner'
        })
    
    return jsonify({'error': 'Неверный ключ владельца'}), 401


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """ЧАТ С ИИ - ИСПОЛЬЗУЕТ ВАШ ai_core.AIAssistant"""
    data = request.json
    user_input = data.get('message', '')
    is_owner = data.get('is_owner', False)
    
    if not user_input:
        return jsonify({'error': 'Пустой запрос'}), 400
    
    # Проверка токена
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    access_level = 'user'
    
    if token and token in state.sessions:
        access_level = state.sessions[token].get('access_level', 'user')
    
    # ГЕНЕРАЦИЯ ОТВЕТА ВАШИМ ИИ
    if state.ai and AI_AVAILABLE:
        response = state.ai.process_message(user_input)
    else:
        response = f"⚠️ ИИ не загружен. Ваш запрос: {user_input}"
    
    # Логирование
    state.add_log(
        user_id=token or 'anonymous',
        req=user_input,
        resp=response,
        level='owner' if is_owner else 'user'
    )
    
    return jsonify({
        'response': response,
        'access_level': 'owner' if is_owner else 'user'
    })


@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'ai_assistant_loaded': AI_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    NERVE AI Server                               ║
║              Ваш собственный ИИ (ai_core)                        ║
╠══════════════════════════════════════════════════════════════════╣
║  🌐 Порт: {port}                                                   ║
║  🤖 ИИ: ai_core.AIAssistant                                      ║
║  🔑 Owner Key: {OWNER_KEY} ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False)


# Для Gunicorn
def create_app():
    return app

def create_app():
    return app
