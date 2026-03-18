"""
Модуль эмоций ИИ-помощника
Анализ настроения, эмпатичные ответы, поддержка
"""

import re
from typing import Dict, List, Optional, Tuple
from random import choice


class EmotionAnalyzer:
    """Анализ эмоционального состояния пользователя"""
    
    # Словари эмоций (русский язык)
    EMOTION_WORDS = {
        'sad': [
            'груст', 'печаль', 'тоск', 'уны', 'депресс', 'апати', 'скучн',
            'больн', 'страд', 'слез', 'рыд', 'ны', 'мрач', 'тяжёл', 'гнет'
        ],
        'happy': [
            'рад', 'счастлив', 'весел', 'лик', 'восторг', 'класс', 'отличн',
            'прекрасн', 'замечательн', 'чудесн', 'удач', 'поздрав', 'победа'
        ],
        'angry': [
            'зл', 'гнев', 'ярост', 'бес', 'раздраж', 'сердит', 'агресс',
            'ненавист', 'фу', 'отврат', 'ужас', 'кошмар', 'достал', 'задолбал'
        ],
        'anxious': [
            'тревог', 'нерв', 'волн', 'страх', 'паник', 'беспоко', 'напряж',
            'стресс', 'давлен', 'боюсь', 'опас', 'рис', 'сомнен', 'пережив'
        ],
        'tired': [
            'устал', 'выгор', 'измуч', 'сон', 'вял', 'слаб', 'истощ',
            'переутом', 'валюсь', 'нет сил', 'тяжело', 'трудно'
        ],
        'motivated': [
            'хочу', 'готов', 'могу', 'сделаю', 'начну', 'продолжу', 'вперёд',
            'достиг', 'цель', 'план', 'успе', 'прогресс', 'расту', 'развива'
        ]
    }
    
    # Интенсификаторы (усиливают эмоцию)
    INTENSIFIERS = [
        'очень', 'крайне', 'ужасно', 'невероятно', 'сильно', 'прямо',
        'действительно', 'реально', 'просто', 'так', 'слишком'
    ]
    
    # Негации (меняют эмоцию на противоположную)
    NEGATIONS = ['не', 'ни', 'без', 'никак', 'нисколько']
    
    # Эмодзи для эмоций
    EMOTION_EMOJIS = {
        'sad': '😔',
        'happy': '😊',
        'angry': '😠',
        'anxious': '😰',
        'tired': '😴',
        'motivated': '💪',
        'neutral': '🙂'
    }
    
    def __init__(self):
        self.current_mood = 'neutral'
        self.mood_history = []
        self.user_mood_patterns = {}
    
    def analyze(self, text: str) -> Dict[str, any]:
        """Анализ текста на эмоции"""
        text_lower = text.lower()
        
        emotions = {}
        
        for emotion, words in self.EMOTION_WORDS.items():
            score = 0
            matched_words = []
            
            for word in words:
                if word in text_lower:
                    score += 1
                    matched_words.append(word)
            
            # Проверка интенсификаторов
            for intensifier in self.INTENSIFIERS:
                if intensifier in text_lower:
                    score *= 1.5
            
            # Проверка негаций
            for negation in self.NEGATIONS:
                if negation in text_lower:
                    score *= -0.5
            
            if score > 0:
                emotions[emotion] = {
                    'score': score,
                    'words': matched_words
                }
        
        # Определить доминирующую эмоцию
        if emotions:
            dominant = max(emotions.items(), key=lambda x: x[1]['score'])
            self.current_mood = dominant[0]
        else:
            self.current_mood = 'neutral'
        
        # Сохранить в историю
        self.mood_history.append({
            'text': text[:100],
            'mood': self.current_mood,
            'emotions': emotions
        })
        
        # Ограничить историю
        if len(self.mood_history) > 100:
            self.mood_history = self.mood_history[-100:]
        
        return {
            'mood': self.current_mood,
            'emotions': emotions,
            'emoji': self.EMOTION_EMOJIS.get(self.current_mood, '🙂')
        }
    
    def get_supportive_response(self, mood: str) -> str:
        """Получить поддерживающий ответ в зависимости от настроения"""
        
        responses = {
            'sad': [
                "Мне жаль, что тебе сейчас тяжело. Я с тобой, и мы справимся вместе. 💙",
                "Грустить — это нормально. Дай себе время, я рядом, если нужно поговорить.",
                "Ты не один. Иногда нужно просто выдохнуть. Я верю в тебя.",
                "Помни: даже самые тёмные ночи заканчиваются рассветом. 🌅"
            ],
            'happy': [
                "Это здорово! Рад за тебя! 🎉",
                "Отличные новости! Твоя радость заразна! 😊",
                "Так держать! Ты молодец!",
                "Люблю твой позитив! Продолжай в том же духе! ✨"
            ],
            'angry': [
                "Понимаю твою злость. Иногда это нормальная реакция. Давай выдохнем вместе.",
                "Злиться — нормально. Главное — не держать это в себе. Я выслушаю.",
                "Давай сделаем паузу. Твои чувства важны, но не стоит их держать внутри.",
                "Я на твоей стороне. Расскажи, что случилось? 🤝"
            ],
            'anxious': [
                "Тревога может быть тяжёлой, но ты справишься. Я с тобой. 💙",
                "Давай сделаем глубокий вдох вместе. Всё будет хорошо.",
                "Ты сильнее, чем думаешь. Один шаг за раз.",
                "Беспокоиться — нормально. Но помни: ты уже справлялся с трудностями раньше."
            ],
            'tired': [
                "Отдых — это важно. Не забывай заботиться о себе. ☕",
                "Ты много работаешь, это достойно уважения. Но отдых тоже нужен.",
                "Может, стоит сделать перерыв? Мир не рухнет, если ты отдохнёшь.",
                "Горжусь твоим упорством, но помни о балансе. 💆"
            ],
            'motivated': [
                "Вот это настрой! 🔥 Вперёд к целям!",
                "Твоя энергия вдохновляет! Давай сделаем это!",
                "С таким настроем ты горы свернёшь! 💪",
                "Поддерживаю на 100%! Ты сможешь!"
            ],
            'neutral': [
                "Я рядом, если нужно что-то обсудить. 🙂",
                "Как твои дела? Я всегда готов выслушать.",
                "На связи! Чем могу помочь?",
                "Просто знай: я всегда здесь для тебя. 💙"
            ]
        }
        
        return choice(responses.get(mood, responses['neutral']))
    
    def get_encouragement(self, context: str = '') -> str:
        """Получить ободряющую фразу"""
        encouragements = [
            "Ты справишься! Я верю в тебя! 💪",
            "Каждый шаг вперёд — это победа.",
            "Ты сильнее, чем думаешь.",
            "Ошибки — это часть пути. Всё получится!",
            "Ты уже прошёл долгий путь. Горжусь тобой!",
            "Дыши глубже. Всё будет хорошо. 🌟",
            "Ты не один. Я с тобой!",
            "Продолжай идти вперёд, даже маленькими шагами."
        ]
        
        return choice(encouragements)
    
    def track_mood_change(self, new_mood: str):
        """Отследить изменение настроения"""
        if self.mood_history:
            prev_mood = self.mood_history[-1]['mood']
            if prev_mood != new_mood:
                self.user_mood_patterns[f'{prev_mood}_to_{new_mood}'] = \
                    self.user_mood_patterns.get(f'{prev_mood}_to_{new_mood}', 0) + 1
    
    def get_mood_summary(self) -> str:
        """Получить сводку о настроении за последнее время"""
        if not self.mood_history:
            return "Пока нет данных о настроении."
        
        mood_counts = {}
        for record in self.mood_history[-50:]:
            mood = record['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        if not mood_counts:
            return "Настроение стабильное."
        
        dominant = max(mood_counts.items(), key=lambda x: x[1])
        
        mood_names_ru = {
            'sad': 'грусть',
            'happy': 'радость',
            'angry': 'злость',
            'anxious': 'тревога',
            'tired': 'усталость',
            'motivated': 'мотивация',
            'neutral': 'нейтральное'
        }
        
        return f"Преобладает {mood_names_ru.get(dominant[0], dominant[0])} ({dominant[1]} раз)"
    
    def is_user_distressed(self) -> bool:
        """Проверить, нуждается ли пользователь в поддержке"""
        return self.current_mood in ['sad', 'anxious', 'tired', 'angry']
    
    def get_emoji(self) -> str:
        """Получить эмодзи текущего настроения"""
        return self.EMOTION_EMOJIS.get(self.current_mood, '🙂')


class EmpathicResponder:
    """Генератор эмпатичных ответов"""
    
    def __init__(self, analyzer: EmotionAnalyzer):
        self.analyzer = analyzer
    
    def respond(self, user_message: str, ai_response: str) -> str:
        """Добавить эмпатию к ответу ИИ"""
        emotion_result = self.analyzer.analyze(user_message)
        mood = emotion_result['mood']
        
        # Если пользователь расстроен, добавить поддержку перед основным ответом
        if self.analyzer.is_user_distressed():
            support = self.analyzer.get_supportive_response(mood)
            return f"{support}\n\n{ai_response}"
        
        # Если пользователь счастлив, разделить радость
        if mood == 'happy':
            celebration = self.analyzer.get_supportive_response('happy')
            return f"{celebration}\n\n{ai_response}"
        
        return ai_response
    
    def add_encouragement(self, text: str) -> str:
        """Добавить ободрение к тексту"""
        return f"{text}\n\n💙 {self.analyzer.get_encouragement()}"
