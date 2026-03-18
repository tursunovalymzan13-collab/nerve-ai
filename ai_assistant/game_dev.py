"""
Модуль разработки игр ИИ-помощника
Механики, дизайн, скрипты, генерация контента
"""

from typing import Dict, List, Optional, Any
from random import choice, randint


class GameDevAssistant:
    """Помощник по разработке игр"""
    
    # Игровые механики
    GAME_MECHANICS = {
        'platformer': {
            'description': 'Платформер — игра, где персонаж прыгает по платформам',
            'core_elements': ['гравитация', 'прыжки', 'коллизии', 'враги', 'бонусы'],
            'engines': ['Unity', 'Godot', 'Pygame', 'GameMaker']
        },
        'rpg': {
            'description': 'RPG — ролевая игра с прокачкой персонажа',
            'core_elements': ['статы', 'инвентарь', 'квесты', 'диалоги', 'бой'],
            'engines': ['RPG Maker', 'Unity', 'Unreal', 'Godot']
        },
        'shooter': {
            'description': 'Шутер — игра со стрельбой',
            'core_elements': ['оружие', 'враги', 'патроны', 'здоровье', 'прицел'],
            'engines': ['Unreal', 'Unity', 'Godot']
        },
        'puzzle': {
            'description': 'Головоломка — игра на логику',
            'core_elements': ['сетка', 'элементы', 'правила', 'цель', 'ходы'],
            'engines': ['Unity', 'Godot', 'Construct']
        },
        'racing': {
            'description': 'Гонки — соревнование на скорость',
            'core_elements': ['трасса', 'машины', 'физика', 'ИИ соперников', 'круги'],
            'engines': ['Unity', 'Unreal', 'Godot']
        },
        'strategy': {
            'description': 'Стратегия — управление ресурсами и войсками',
            'core_elements': ['база', 'ресурсы', 'юниты', 'технологии', 'карта'],
            'engines': ['Unity', 'Unreal', '0 A.D.']
        },
        'horror': {
            'description': 'Хоррор — игра на выживание с элементами страха',
            'core_elements': ['атмосфера', 'монстры', 'ресурсы', 'укрытия', 'скримеры'],
            'engines': ['Unreal', 'Unity', 'RenPy']
        },
        'visual_novel': {
            'description': 'Визуальная новелла — интерактивная история',
            'core_elements': ['сюжет', 'персонажи', 'выборы', 'концовки', 'фон'],
            'engines': ['RenPy', 'TyranoBuilder', 'Unity']
        }
    }
    
    # Генераторы контента
    NAME_GENERATORS = {
        'character': {
            'prefixes': ['Арг', 'Бор', 'Вал', 'Гар', 'Дар', 'Зор', 'Ир', 'Кар', 'Лор', 'Мор', 
                        'Нор', 'Ор', 'Ран', 'Сар', 'Тор', 'Уль', 'Фар', 'Хар', 'Зар', 'Яр'],
            'suffixes': ['иус', 'акус', 'еус', 'ион', 'ор', 'ус', 'ис', 'ас', 'ос', 'ус',
                        'мир', 'слав', 'бор', 'вол', 'гор', 'дар', 'жар', 'зор', 'лав', 'мир']
        },
        'location': {
            'prefixes': ['Древ', 'Тём', 'Свет', 'Крас', 'Син', 'Зел', 'Чёр', 'Бел', 'Глуб', 'Выс',
                        'Под', 'Над', 'Меж', 'Около', 'Внутри', 'Снару', 'После', 'До'],
            'suffixes': ['град', 'гор', 'лес', 'мор', 'пуст', 'дол', 'холм', 'ост', 'пик', 'край',
                        'земл', 'мир', 'край', 'угол', 'мест', 'прост', 'терр', 'зон', 'реги']
        },
        'item': {
            'adjectives': ['Древний', 'Забытый', 'Проклятый', 'Благословенный', 'Тёмный', 
                          'Светлый', 'Кровавый', 'Ледяной', 'Огненный', 'Грозовой'],
            'nouns': ['Меч', 'Щит', 'Кольцо', 'Амулет', 'Кинжал', 'Посох', 'Лук', 'Топор',
                     'Копьё', 'Булава', 'Перчатки', 'Ботинки', 'Шлем', 'Доспех', 'Плащ']
        }
    }
    
    # Шаблоны квестов
    QUEST_TEMPLATES = [
        {
            'type': 'fetch',
            'structure': 'Найти {item} в {location} и принести {npc}',
            'rewards': ['опыт', 'золото', 'предмет', 'репутация']
        },
        {
            'type': 'kill',
            'structure': 'Убить {enemy} ({count} шт.) в {location}',
            'rewards': ['опыт', 'золото', 'трофей', 'репутация']
        },
        {
            'type': 'escort',
            'structure': 'Сопроводить {npc} от {start} до {end}',
            'rewards': ['опыт', 'золото', 'открытие локации']
        },
        {
            'type': 'explore',
            'structure': 'Исследовать {location} и найти {objective}',
            'rewards': ['опыт', 'открытие карты', 'секрет']
        },
        {
            'type': 'craft',
            'structure': 'Создать {item} используя {materials}',
            'rewards': ['опыт', 'предмет', 'рецепт']
        }
    ]
    
    # Баланс игры
    BALANCE_FORMULAS = {
        'xp_to_level': 'base_xp * (multiplier ** (level - 1))',
        'damage': '(attack * skill_multiplier) - (enemy_defense * armor_penetration)',
        'health': 'base_health + (health_per_level * level)',
        'gold_reward': 'base_gold * (1 + difficulty_modifier) * level',
        'drop_chance': 'base_chance * (1 + luck_bonus)'
    }
    
    def __init__(self):
        self.generated_content = []
    
    def get_mechanic_info(self, genre: str) -> Dict[str, Any]:
        """Получить информацию о механике жанра"""
        genre_lower = genre.lower()
        
        for key, info in self.GAME_MECHANICS.items():
            if key in genre_lower:
                return info
        
        return {
            'description': 'Жанр не найден. Доступные: platformer, rpg, shooter, puzzle, racing, strategy, horror, visual_novel',
            'core_elements': [],
            'engines': []
        }
    
    def generate_character_name(self, style: str = 'fantasy') -> str:
        """Сгенерировать имя персонажа"""
        gen = self.NAME_GENERATORS['character']
        prefix = choice(gen['prefixes'])
        suffix = choice(gen['suffixes'])
        return prefix + suffix
    
    def generate_location_name(self, style: str = 'fantasy') -> str:
        """Сгенерировать название локации"""
        gen = self.NAME_GENERATORS['location']
        prefix = choice(gen['prefixes'])
        suffix = choice(gen['suffixes'])
        return prefix + suffix
    
    def generate_item_name(self, rarity: str = 'common') -> str:
        """Сгенерировать название предмета"""
        gen = self.NAME_GENERATORS['item']
        adj = choice(gen['adjectives'])
        noun = choice(gen['nouns'])
        
        rarity_modifiers = {
            'common': '',
            'rare': 'Редкий ',
            'epic': 'Легендарный ',
            'legendary': 'Мифический '
        }
        
        return rarity_modifiers.get(rarity, '') + adj + ' ' + noun
    
    def generate_quest(self, quest_type: str = None) -> Dict[str, Any]:
        """Сгенерировать квест"""
        if quest_type:
            templates = [t for t in self.QUEST_TEMPLATES if t['type'] == quest_type]
            if not templates:
                templates = self.QUEST_TEMPLATES
        else:
            templates = self.QUEST_TEMPLATES
        
        template = choice(templates)
        
        # Заполнение шаблона
        quest = {
            'type': template['type'],
            'title': self._generate_quest_title(template['type']),
            'description': template['structure'].format(
                item=self.generate_item_name(),
                location=self.generate_location_name(),
                npc=self.generate_character_name(),
                enemy=self.generate_character_name(),
                count=randint(3, 10),
                start=self.generate_location_name(),
                end=self.generate_location_name(),
                objective=choice(['сокровище', 'артефакт', 'секрет', 'выход']),
                materials=', '.join([self.generate_item_name() for _ in range(3)])
            ),
            'rewards': template['rewards']
        }
        
        return quest
    
    def _generate_quest_title(self, quest_type: str) -> str:
        """Сгенерировать название квеста"""
        titles = {
            'fetch': [
                'Поиски пропавшего',
                'Древняя реликвия',
                'Потерянное сокровище'
            ],
            'kill': [
                'Охота на монстра',
                'Очищение земель',
                'Враг у ворот'
            ],
            'escort': [
                'Опасный путь',
                'Верная охрана',
                'Через тернии'
            ],
            'explore': [
                'Тайны старого места',
                'Неизведанные земли',
                'Секреты прошлого'
            ],
            'craft': [
                'Мастер на все руки',
                'Легендарный предмет',
                'Искусство создания'
            ]
        }
        
        return choice(titles.get(quest_type, ['Новое приключение']))
    
    def calculate_game_balance(self, formula: str, **kwargs) -> float:
        """Рассчитать баланс игры"""
        if formula == 'xp_to_level':
            base_xp = kwargs.get('base_xp', 100)
            multiplier = kwargs.get('multiplier', 1.5)
            level = kwargs.get('level', 1)
            return base_xp * (multiplier ** (level - 1))
        
        elif formula == 'damage':
            attack = kwargs.get('attack', 10)
            skill_multiplier = kwargs.get('skill_multiplier', 1)
            enemy_defense = kwargs.get('enemy_defense', 5)
            armor_penetration = kwargs.get('armor_penetration', 1)
            return (attack * skill_multiplier) - (enemy_defense * armor_penetration)
        
        elif formula == 'health':
            base_health = kwargs.get('base_health', 100)
            health_per_level = kwargs.get('health_per_level', 10)
            level = kwargs.get('level', 1)
            return base_health + (health_per_level * level)
        
        elif formula == 'gold_reward':
            base_gold = kwargs.get('base_gold', 50)
            difficulty_modifier = kwargs.get('difficulty_modifier', 0)
            level = kwargs.get('level', 1)
            return base_gold * (1 + difficulty_modifier) * level
        
        elif formula == 'drop_chance':
            base_chance = kwargs.get('base_chance', 0.1)
            luck_bonus = kwargs.get('luck_bonus', 0)
            return base_chance * (1 + luck_bonus)
        
        return 0
    
    def get_engine_recommendation(self, game_type: str, experience: str = 'beginner') -> str:
        """Рекомендовать движок для игры"""
        recommendations = {
            'platformer': {
                'beginner': 'GameMaker или Pygame — простые в освоении',
                'intermediate': 'Godot — бесплатный и мощный',
                'advanced': 'Unity — индустриальный стандарт'
            },
            'rpg': {
                'beginner': 'RPG Maker — создан специально для RPG',
                'intermediate': 'Godot с плагинами для RPG',
                'advanced': 'Unreal Engine с Blueprint'
            },
            'shooter': {
                'beginner': 'Unity с FPS шаблоном',
                'intermediate': 'Unreal Engine — лучшая графика',
                'advanced': 'Unreal Engine 5 с Nanite'
            },
            'puzzle': {
                'beginner': 'Construct 3 — визуальное программирование',
                'intermediate': 'Godot — лёгкий и быстрый',
                'advanced': 'Unity — много ассетов'
            },
            'visual_novel': {
                'beginner': 'RenPy — создан для новелл',
                'intermediate': 'RenPy с кастомизацией',
                'advanced': 'Unity с Fungus'
            }
        }
        
        game_info = self.get_mechanic_info(game_type)
        if not game_info['core_elements']:
            return "Неизвестный жанр. Попробуйте: platformer, rpg, shooter, puzzle, visual_novel"
        
        return recommendations.get(game_type, {}).get(experience, 'Unity — универсальный выбор')
    
    def generate_game_idea(self, constraints: Dict = None) -> Dict[str, Any]:
        """Сгенерировать идею для игры"""
        genres = list(self.GAME_MECHANICS.keys())
        genre = choice(genres)
        
        ideas = {
            'platformer': {
                'concept': 'Платформер о {protagonist}, который должен {goal}',
                'twist': ['гравитация меняется', 'время замедляется', 'мир перевёрнут'],
                'setting': ['постапокалипсис', 'космос', 'подземелье', 'облака']
            },
            'rpg': {
                'concept': 'RPG где вы {protagonist} в мире {setting}',
                'twist': ['статы меняются от решений', 'смерть окончательна', 'враги растут с вами'],
                'setting': ['где магия исчезает', 'после катастрофы', 'в параллельной реальности']
            },
            'shooter': {
                'concept': 'Шутер от {perspective} с {weapon_type}',
                'twist': ['пули искривляются', 'оружие живое', 'время останавливается'],
                'setting': ['киберпанк', 'средневековье', 'под водой', 'в снах']
            },
            'puzzle': {
                'concept': 'Головоломка где нужно {action} для достижения {target}',
                'twist': ['элементы двигаются сами', 'есть гравитация', 'можно менять правила'],
                'setting': ['лаборатория', 'древний храм', 'космическая станция']
            }
        }

        idea = ideas.get(genre, ideas['platformer'])

        return {
            'genre': genre,
            'concept': idea['concept'].format(
                protagonist=choice(['робот', 'маг', 'учёный', 'вор', 'герой']),
                goal=choice(['спасти мир', 'найти артефакт', 'выжить', 'победить босса']),
                perspective=choice(['первого', 'третьего', 'сверху']),
                weapon_type=choice(['разным оружием', 'одним уникальным оружием', 'магией']),
                action=choice(['перемещать блоки', 'менять цвет', 'создавать объекты']),
                target=choice(['цели', 'рекорда', 'выхода'])
            ),
            'twist': choice(idea['twist']),
            'setting': choice(idea['setting']),
            'target_audience': choice(['казуалы', 'хардкорщики', 'дети', 'взрослые'])
        }
    
    def create_pygame_template(self, game_type: str) -> str:
        """Создать шаблон кода для Pygame"""
        templates = {
            'basic': '''
import pygame
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Моя игра")
clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Игрок
player = pygame.Rect(WIDTH//2, HEIGHT//2, 50, 50)
speed = 5

# Главный цикл
running = True
while running:
    clock.tick(FPS)
    
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed
    
    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.display.flip()

pygame.quit()
sys.exit()
''',
            'platformer': '''
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Физика
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Игрок
player = pygame.Rect(100, HEIGHT - 150, 40, 60)
velocity_y = 0
on_ground = False
speed = 5

# Платформы
platforms = [
    pygame.Rect(0, HEIGHT - 50, WIDTH, 50),  # Земля
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20),
    pygame.Rect(100, 250, 200, 20)
]

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = JUMP_STRENGTH
                on_ground = False
    
    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    
    # Гравитация
    velocity_y += GRAVITY
    player.y += velocity_y
    
    # Коллизии
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            if velocity_y > 0:  # Падение вниз
                player.bottom = platform.top
                velocity_y = 0
                on_ground = True
    
    # Границы
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        velocity_y = 0
        on_ground = True
    
    # Отрисовка
    screen.fill((135, 206, 235))  # Небо
    for platform in platforms:
        pygame.draw.rect(screen, (139, 69, 19), platform)  # Коричневый
    pygame.draw.rect(screen, (255, 0, 0), player)  # Красный игрок
    pygame.display.flip()

pygame.quit()
sys.exit()
''',
            'shooter': '''
import pygame
import sys
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Игрок
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 70, 50, 50)
speed = 5

# Пули
bullets = []
bullet_speed = 10

# Враги
enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 60  # кадры

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.centerx - 5, player.top, 10, 20))
    
    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    
    # Пули
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
    
    # Враги
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_interval:
        enemy_spawn_timer = 0
        enemy = pygame.Rect(
            pygame.random.randint(0, WIDTH - 50),
            0, 50, 50
        )
        enemies.append(enemy)
    
    for enemy in enemies[:]:
        enemy.y += 3
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
        
        # Коллизия с пулями
        for bullet in bullets[:]:
            if bullet.colliderect(enemy):
                if bullet in bullets:
                    bullets.remove(bullet)
                enemies.remove(enemy)
                break
    
    # Отрисовка
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.display.flip()

pygame.quit()
sys.exit()
'''
        }
        
        return templates.get(game_type, templates['basic'])
    
    def get_game_design_tips(self, topic: str) -> List[str]:
        """Получить советы по дизайну игр"""
        tips = {
            'геймплей': [
                'Игрок должен чувствовать прогресс — добавляйте награды',
                'Сложность должна расти постепенно',
                'Давайте игроку выбор и последствия',
                'Тестируйте на реальных игроках'
            ],
            'графика': [
                'Единый стиль важнее детализации',
                'Используйте контраст для важных объектов',
                'Анимации делают мир живым',
                'UI должен быть читаемым'
            ],
            'звук': [
                'Музыка задаёт настроение',
                'Звуковые эффекты дают обратную связь',
                'Голосовая актёрская игра улучшает погружение',
                'Не перегружайте аудио'
            ],
            'сюжет': [
                'Показывайте, а не рассказывайте',
                'Давайте игроку влиять на историю',
                'Создавайте запоминающихся персонажей',
                'Темп повествования должен варьироваться'
            ],
            'уровни': [
                'Начинайте с обучения',
                'Чередуйте интенсивность',
                'Давайте игроку передышки',
                'Секреты поощряют исследование'
            ],
            'баланс': [
                'Слишком легко = скучно',
                'Слишком сложно = фрустрация',
                'Давайте разные стратегии победы',
                'Балансируйте через тестирование'
            ]
        }
        
        topic_lower = topic.lower()
        for key, tip_list in tips.items():
            if key in topic_lower:
                return tip_list
        
        return [
            'Сфокусируйтесь на одном ключевом механике',
            'Прототипируйте быстро, тестируйте часто',
            'Игра должна быть весёлой в основе',
            'Завершите проект, даже если он маленький'
        ]
