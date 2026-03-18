"""
Модуль памяти ИИ-помощника
Хранит диалоги, предпочтения пользователя, обучающие метки
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


class Memory:
    """База знаний ИИ-помощника на SQLite"""
    
    def __init__(self, db_path: str = "ai_memory.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()
    
    def _init_tables(self):
        """Создание таблиц базы данных"""
        cursor = self.conn.cursor()
        
        # Таблица диалогов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                mood TEXT,
                context TEXT
            )
        """)
        
        # Таблица обучающих меток (правильно/неправильно)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                feedback_type TEXT NOT NULL,
                comment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        # Таблица предпочтений пользователя
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                category TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица знаний (факты, которые запомнил ИИ)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                category TEXT,
                confidence INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица шаблонов кода
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                language TEXT,
                pattern TEXT NOT NULL,
                description TEXT,
                usage_count INTEGER DEFAULT 0,
                rating INTEGER DEFAULT 0
            )
        """)
        
        # Индексы для ускорения поиска
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_conv ON feedback(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge(category)")
        
        self.conn.commit()
    
    # === Диалоги ===
    
    def add_conversation(self, user_message: str, ai_response: str, 
                         mood: Optional[str] = None, context: Optional[Dict] = None):
        """Добавить запись диалога"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (user_message, ai_response, mood, context)
            VALUES (?, ?, ?, ?)
        """, (user_message, ai_response, mood, json.dumps(context) if context else None))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Получить последние диалоги"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def search_conversations(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Поиск по диалогам"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE user_message LIKE ? OR ai_response LIKE ?
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", limit))
        return [dict(row) for row in cursor.fetchall()]
    
    # === Обратная связь (обучение) ===
    
    def add_feedback(self, conversation_id: int, feedback_type: str, 
                     comment: Optional[str] = None):
        """Добавить оценку ответа (good/bad)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (conversation_id, feedback_type, comment)
            VALUES (?, ?, ?)
        """, (conversation_id, feedback_type, comment))
        self.conn.commit()
    
    def get_feedback_stats(self) -> Dict[str, int]:
        """Получить статистику оценок"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT feedback_type, COUNT(*) as count 
            FROM feedback 
            GROUP BY feedback_type
        """)
        return {row['feedback_type']: row['count'] for row in cursor.fetchall()}
    
    def get_good_examples(self, limit: int = 10) -> List[Dict]:
        """Получить примеры хороших ответов"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.* FROM conversations c
            INNER JOIN feedback f ON c.id = f.conversation_id
            WHERE f.feedback_type = 'good'
            ORDER BY f.timestamp DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    # === Предпочтения ===
    
    def set_preference(self, key: str, value: Any, category: Optional[str] = None):
        """Сохранить предпочтение"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO preferences (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, json.dumps(value) if isinstance(value, (dict, list)) else str(value), category))
        self.conn.commit()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Получить предпочтение"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            try:
                return json.loads(row['value'])
            except (json.JSONDecodeError, TypeError):
                return row['value']
        return default
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Получить все предпочтения"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value, category FROM preferences")
        result = {}
        for row in cursor.fetchall():
            try:
                result[row['key']] = json.loads(row['value'])
            except (json.JSONDecodeError, TypeError):
                result[row['key']] = row['value']
        return result
    
    # === Знания ===
    
    def add_knowledge(self, fact: str, category: Optional[str] = None):
        """Добавить факт в базу знаний"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO knowledge (fact, category)
            VALUES (?, ?)
        """, (fact, category))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_knowledge(self, category: Optional[str] = None) -> List[Dict]:
        """Получить знания, опционально по категории"""
        cursor = self.conn.cursor()
        if category:
            cursor.execute("SELECT * FROM knowledge WHERE category = ? ORDER BY created_at DESC", 
                          (category,))
        else:
            cursor.execute("SELECT * FROM knowledge ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def search_knowledge(self, keyword: str) -> List[Dict]:
        """Поиск по знаниям"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM knowledge 
            WHERE fact LIKE ?
            ORDER BY created_at DESC
        """, (f"%{keyword}%",))
        return [dict(row) for row in cursor.fetchall()]
    
    # === Шаблоны кода ===
    
    def add_code_pattern(self, name: str, pattern: str, language: str, 
                         description: Optional[str] = None):
        """Сохранить шаблон кода"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO code_patterns (name, language, pattern, description)
            VALUES (?, ?, ?, ?)
        """, (name, language, pattern, description))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_code_pattern(self, name: str) -> Optional[Dict]:
        """Получить шаблон по имени"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM code_patterns WHERE name = ?", (name,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_code_patterns_by_language(self, language: str) -> List[Dict]:
        """Получить шаблоны по языку"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM code_patterns 
            WHERE language = ? 
            ORDER BY usage_count DESC
        """, (language,))
        return [dict(row) for row in cursor.fetchall()]
    
    def rate_code_pattern(self, pattern_id: int, rating: int):
        """Оценить шаблон кода"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE code_patterns 
            SET rating = rating + ?, usage_count = usage_count + 1
            WHERE id = ?
        """, (rating, pattern_id))
        self.conn.commit()
    
    # === Статистика ===
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить общую статистику"""
        cursor = self.conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM conversations")
        stats['total_conversations'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM knowledge")
        stats['total_knowledge'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM code_patterns")
        stats['total_patterns'] = cursor.fetchone()['count']
        
        stats['feedback'] = self.get_feedback_stats()
        
        return stats
    
    def close(self):
        """Закрыть соединение"""
        self.conn.close()
    
    def __del__(self):
        self.close()
