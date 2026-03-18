"""
ИИ-Помощник v2.0
Персональный ИИ для кодинга, игр и поддержки
С архитектурой Dual Access (Owner/User)
"""

from .memory import Memory
from .learner import Learner
from .emotions import EmotionAnalyzer, EmpathicResponder
from .coder import CodeAssistant
from .game_dev import GameDevAssistant
from .ai_core import AIAssistant
from .chat_ui import ChatUI, run_chat

# Dual Access Architecture
from .interfaces import (
    AIInterface,
    OwnerInterface,
    UserInterface,
    AccessLevel,
    SafetyFilter
)
from .access_controller import (
    AccessController,
    AccessManager,
    AuthStatus
)

__version__ = '2.0.0'
__author__ = 'Personal AI Assistant'

__all__ = [
    # Original modules
    'Memory',
    'Learner',
    'EmotionAnalyzer',
    'EmpathicResponder',
    'CodeAssistant',
    'GameDevAssistant',
    'AIAssistant',
    'ChatUI',
    'run_chat',
    # Dual Access Architecture
    'AIInterface',
    'OwnerInterface',
    'UserInterface',
    'AccessLevel',
    'SafetyFilter',
    'AccessController',
    'AccessManager',
    'AuthStatus'
]
