"""
Модуль обучения ИИ-помощника
Система оценки ответов, адаптация на основе фидбека
"""

import json
from typing import Dict, List, Optional, Any
from collections import defaultdict
from datetime import datetime

try:
    from .memory import Memory
except ImportError:
    from memory import Memory


class Learner:
    """Система обучения на основе обратной связи"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.response_patterns = defaultdict(list)
        self.user_style = {}
        self._load_learned_data()
    
    def _load_learned_data(self):
        """Загрузить изученные паттерны"""
        prefs = self.memory.get_all_preferences()
        self.user_style = prefs.get('user_style', {})
    
    def mark_good(self, conversation_id: int, comment: Optional[str] = None):
        """Отметить ответ как хороший"""
        self.memory.add_feedback(conversation_id, 'good', comment)
        
        # Усилить паттерны этого ответа
        conv = self.memory.get_recent_conversations(1)
        if conv:
            last_conv = conv[0]
            self._analyze_successful_response(last_conv)
    
    def mark_bad(self, conversation_id: int, comment: Optional[str] = None):
        """Отметить ответ как плохой"""
        self.memory.add_feedback(conversation_id, 'bad', comment)
        
        # Ослабить паттерны этого ответа
        conv = self.memory.get_recent_conversations(1)
        if conv:
            last_conv = conv[0]
            self._analyze_failed_response(last_conv)
    
    def _analyze_successful_response(self, conversation: Dict):
        """Анализ успешного ответа для обучения"""
        user_msg = conversation.get('user_message', '')
        ai_response = conversation.get('ai_response', '')
        
        # Определить тип запроса
        msg_type = self._classify_message(user_msg)
        
        # Сохранить успешный паттерн
        self.response_patterns[msg_type].append({
            'user_msg': user_msg,
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Ограничить количество паттернов
        if len(self.response_patterns[msg_type]) > 50:
            self.response_patterns[msg_type] = self.response_patterns[msg_type][-50:]
    
    def _analyze_failed_response(self, conversation: Dict):
        """Анализ неудачного ответа"""
        # Можно добавить логику избегания подобных ответов
        pass
    
    def _classify_message(self, message: str) -> str:
        """Классификация типа сообщения"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['код', 'функци', 'класс', 'def ', 'import ', 'перемен']):
            return 'coding'
        elif any(word in message_lower for word in ['игр', 'механик', 'спрайт', 'уровен', 'npc']):
            return 'game_dev'
        elif any(word in message_lower for word in ['плох', 'устал', 'рад', 'груст', 'тревог', 'счастлив']):
            return 'emotional'
        elif any(word in message_lower for word in ['почему', 'как', 'что', 'объясни']):
            return 'question'
        elif any(word in message_lower for word in ['привет', 'здравствуй', 'добрый']):
            return 'greeting'
        else:
            return 'general'
    
    def get_similar_successful_response(self, message: str) -> Optional[str]:
        """Найти похожий успешный ответ из прошлого"""
        msg_type = self._classify_message(message)
        
        patterns = self.response_patterns.get(msg_type, [])
        if not patterns:
            return None
        
        # Простой поиск по ключевым словам
        message_words = set(message.lower().split())
        
        best_match = None
        best_score = 0
        
        for pattern in patterns:
            pattern_words = set(pattern['user_msg'].lower().split())
            overlap = len(message_words & pattern_words)
            
            if overlap > best_score:
                best_score = overlap
                best_match = pattern['response']
        
        return best_match if best_score >= 2 else None
    
    def learn_preference(self, key: str, value: Any, category: Optional[str] = None):
        """Запомнить предпочтение пользователя"""
        self.memory.set_preference(key, value, category)
        if key == 'user_style':
            self.user_style = value
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Получить все предпочтения"""
        return self.memory.get_all_preferences()
    
    def extract_knowledge(self, statement: str, category: Optional[str] = None):
        """Извлечь знание из утверждения пользователя"""
        # Простая эвристика: если есть "я люблю", "я предпочитаю", и т.д.
        statement_lower = statement.lower()
        
        knowledge_fragments = []
        
        if 'я люблю' in statement_lower:
            knowledge_fragments.append(statement)
        elif 'я предпочитаю' in statement_lower:
            knowledge_fragments.append(statement)
        elif 'мне нравится' in statement_lower:
            knowledge_fragments.append(statement)
        elif 'запомни что' in statement_lower:
            knowledge_fragments.append(statement)
        
        for fragment in knowledge_fragments:
            self.memory.add_knowledge(fragment, category or 'user_preference')
        
        return len(knowledge_fragments) > 0
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Получить статистику обучения"""
        feedback_stats = self.memory.get_feedback_stats()
        
        return {
            'good_responses': feedback_stats.get('good', 0),
            'bad_responses': feedback_stats.get('bad', 0),
            'learned_patterns': sum(len(p) for p in self.response_patterns.values()),
            'pattern_types': list(self.response_patterns.keys()),
            'user_preferences': len(self.memory.get_all_preferences())
        }
    
    def generate_adaptive_response(self, message: str, base_response: str) -> str:
        """Адаптировать ответ на основе изученных предпочтений"""
        # Если пользователь предпочитает краткие ответы
        if self.user_style.get('response_length') == 'short':
            base_response = base_response[:200] + "..." if len(base_response) > 200 else base_response
        
        # Если пользователь предпочитает формальный стиль
        if self.user_style.get('tone') == 'formal':
            base_response = base_response.replace('привет', 'здравствуйте')
        
        return base_response
    
    def reset_learning(self):
        """Сбросить все обученные данные"""
        self.response_patterns.clear()
        self.user_style = {}
        # Не удаляем базу данных, только кэш


class ResponseGenerator:
    """Генератор ответов на основе обученных паттернов"""
    
    def __init__(self, learner: Learner):
        self.learner = learner
    
    def generate(self, message: str, context: Dict = None) -> str:
        """Сгенерировать ответ"""
        # Сначала попробовать найти похожий успешный ответ
        similar = self.learner.get_similar_successful_response(message)
        if similar:
            return similar
        
        # Иначе вернуть базовый ответ (будет переопределено в ai_core)
        return ""
