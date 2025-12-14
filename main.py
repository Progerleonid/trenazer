import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget,
                             QScrollArea, QFrame, QGridLayout, QProgressBar,
                             QLineEdit, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("МатематикаPro")
        self.setMinimumSize(1000, 700)

        self.theme = 'light'
        self.color = 'green'
        self.language = 'ru'  # 'ru' или 'en'
        self.current_category = 'all'

        self.init_files()

        self.load_settings()
        self.load_progress()

        self.init_ui()
        self.apply_theme()
        self.update_nav_buttons()

    def tr(self, ru, en):
        """Простой переводчик"""
        return en if self.language == 'en' else ru

    def init_files(self):
        if not os.path.exists('topics.json'):
            default_topics = [
                {
                    "id": "addition",
                    "title": {"ru": "Сложение", "en": "Addition"},
                    "category": "basics",
                    "description": {"ru": "Научитесь складывать числа", "en": "Learn to add numbers"},
                    "icon": "➕",
                    "theory": {
                        "sections": [
                            {
                                "title": {"ru": "Что такое сложение?", "en": "What is addition?"},
                                "content": {"ru": "Сложение — это объединение чисел. Результат называется суммой.", "en": "Addition combines numbers. The result is called the sum."},
                                "examples": ["2 + 3 = 5", "10 + 15 = 25", "100 + 200 = 300"]
                            }
                        ]
                    },
                    "questions": [
                        {"id": 1, "question": {"ru": "Сколько будет 5 + 3?", "en": "What is 5 + 3?"}, "type": "multiple_choice", "options": ["6", "7", "8", "9"], "correct_answer": "8", "explanation": {"ru": "5 + 3 = 8", "en": "5 + 3 = 8"}},
                        {"id": 2, "question": {"ru": "Решите: 12 + 18", "en": "Solve: 12 + 18"}, "type": "input", "correct_answer": "30", "explanation": {"ru": "12 + 18 = 30", "en": "12 + 18 = 30"}}
                    ]
                },
                {
                    "id": "subtraction",
                    "title": {"ru": "Вычитание", "en": "Subtraction"},
                    "category": "basics",
                    "description": {"ru": "Научитесь вычитать числа", "en": "Learn to subtract numbers"},
                    "icon": "➖",
                    "theory": {
                        "sections": [
                            {
                                "title": {"ru": "Что такое вычитание?", "en": "What is subtraction?"},
                                "content": {"ru": "Вычитание — нахождение разности между числами.", "en": "Subtraction finds the difference between numbers."},
                                "examples": ["10 - 3 = 7", "25 - 10 = 15"]
                            }
                        ]
                    },
                    "questions": [
                        {"id": 1, "question": {"ru": "Сколько будет 10 - 4?", "en": "What is 10 - 4?"}, "type": "multiple_choice", "options": ["5", "6", "7", "8"], "correct_answer": "6", "explanation": {"ru": "10 - 4 = 6", "en": "10 - 4 = 6"}}
                    ]
                },
                {
                    "id": "multiplication",
                    "title": {"ru": "Умножение", "en": "Multiplication"},
                    "category": "basics",
                    "description": {"ru": "Таблица умножения", "en": "Multiplication table"},
                    "icon": "✖️",
                    "theory": {
                        "sections": [
                            {
                                "title": {"ru": "Основы умножения", "en": "Basics of multiplication"},
                                "content": {"ru": "Умножение — многократное сложение одного числа.", "en": "Multiplication is repeated addition."},
                                "examples": ["3 × 4 = 12", "5 × 6 = 30"]
                            }
                        ]
                    },
                    "questions": [
                        {"id": 1, "question": {"ru": "Сколько будет 6 × 7?", "en": "What is 6 × 7?"}, "type": "multiple_choice", "options": ["40", "42", "44", "46"], "correct_answer": "42", "explanation": {"ru": "6 × 7 = 42", "en": "6 × 7 = 42"}}
                    ]
                },
                {
                    "id": "division",
                    "title": {"ru": "Деление", "en": "Division"},
                    "category": "basics",
                    "description": {"ru": "Научитесь делить числа", "en": "Learn to divide numbers"},
                    "icon": "➗",
                    "theory": {
                        "sections": [
                            {
                                "title": {"ru": "Основы деления", "en": "Basics of division"},
                                "content": {"ru": "Деление — разделение на равные части.", "en": "Division splits into equal parts."},
                                "examples": ["12 ÷ 3 = 4", "20 ÷ 5 = 4"]
                            }
                        ]
                    },
                    "questions": [
                        {"id": 1, "question": {"ru": "Сколько будет 24 ÷ 6?", "en": "What is 24 ÷ 6?"}, "type": "multiple_choice", "options": ["3", "4", "5", "6"], "correct_answer": "4", "explanation": {"ru": "24 ÷ 6 = 4", "en": "24 ÷ 6 = 4"}}
                    ]
                },
                {
                    "id": "fractions",
                    "title": {"ru": "Обыкновенные дроби", "en": "Fractions"},
                    "category": "intermediate",
                    "description": {"ru": "Операции с дробями", "en": "Operations with fractions"},
                    "icon": "⅔",
                    "theory": {"sections": [{"title": {"ru": "Дроби", "en": "Fractions"}, "content": {"ru": "Часть от целого.", "en": "Part of a whole."}, "examples": ["1/2 + 1/4 = 3/4"]}]},
                    "questions": [{"id": 1, "question": {"ru": "1/3 + 1/6 = ?", "en": "1/3 + 1/6 = ?"}, "type": "input", "correct_answer": "1/2", "explanation": {"ru": "1/2", "en": "1/2"}}]
                },
                {
                    "id": "decimals",
                    "title": {"ru": "Десятичные дроби", "en": "Decimals"},
                    "category": "intermediate",
                    "description": {"ru": "Работа с десятичными числами", "en": "Working with decimals"},
                    "icon": "0.5",
                    "theory": {"sections": [{"title": {"ru": "Десятичные дроби", "en": "Decimals"}, "content": {"ru": "Числа после запятой.", "en": "Numbers after the decimal point."}, "examples": ["0.2 + 0.3 = 0.5"]}]},
                    "questions": [{"id": 1, "question": {"ru": "0.75 × 4 = ?", "en": "0.75 × 4 = ?"}, "type": "input", "correct_answer": "3", "explanation": {"ru": "3", "en": "3"}}]
                },
                {
                    "id": "percent",
                    "title": {"ru": "Проценты", "en": "Percentages"},
                    "category": "intermediate",
                    "description": {"ru": "Расчёт процентов", "en": "Calculating percentages"},
                    "icon": "%",
                    "theory": {"sections": [{"title": {"ru": "Процент", "en": "Percent"}, "content": {"ru": "Сотая часть числа.", "en": "Hundredth part of a number."}, "examples": ["10% от 200 = 20"]}]},
                    "questions": [{"id": 1, "question": {"ru": "15% от 300 = ?", "en": "15% of 300 = ?"}, "type": "input", "correct_answer": "45", "explanation": {"ru": "45", "en": "45"}}]
                },
                {
                    "id": "powers",
                    "title": {"ru": "Степени и корни", "en": "Powers and roots"},
                    "category": "intermediate",
                    "description": {"ru": "Возведение в степень", "en": "Exponentiation and roots"},
                    "icon": "²√",
                    "theory": {"sections": [{"title": {"ru": "Степени", "en": "Powers"}, "content": {"ru": "Повторное умножение.", "en": "Repeated multiplication."}, "examples": ["2^4 = 16"]}]},
                    "questions": [{"id": 1, "question": {"ru": "2^5 = ?", "en": "2^5 = ?"}, "type": "input", "correct_answer": "32", "explanation": {"ru": "32", "en": "32"}}]
                },
                {
                    "id": "equations",
                    "title": {"ru": "Линейные уравнения", "en": "Linear equations"},
                    "category": "advanced",
                    "description": {"ru": "Решение уравнений", "en": "Solving equations"},
                    "icon": "x=",
                    "theory": {"sections": [{"title": {"ru": "Уравнения", "en": "Equations"}, "content": {"ru": "Приведём подобные члены.", "en": "Combine like terms."}, "examples": ["2x + 4 = 10 → x = 3"]}]},
                    "questions": [{"id": 1, "question": {"ru": "Решите: 5x - 10 = 20", "en": "Solve: 5x - 10 = 20"}, "type": "input", "correct_answer": "6", "explanation": {"ru": "x = 6", "en": "x = 6"}}]
                },
                {
                    "id": "geometry",
                    "title": {"ru": "Геометрия", "en": "Geometry"},
                    "category": "advanced",
                    "description": {"ru": "Площади и периметры", "en": "Areas and perimeters"},
                    "icon": "△",
                    "theory": {"sections": [{"title": {"ru": "Фигуры", "en": "Shapes"}, "content": {"ru": "Треугольник, квадрат, круг.", "en": "Triangle, square, circle."}, "examples": ["S = a²"]}]},
                    "questions": [{"id": 1, "question": {"ru": "Площадь квадрата со стороной 5?", "en": "Area of a square with side 5?"}, "type": "input", "correct_answer": "25", "explanation": {"ru": "25", "en": "25"}}]
                },
                {
                    "id": "negative",
                    "title": {"ru": "Отрицательные числа", "en": "Negative numbers"},
                    "category": "advanced",
                    "description": {"ru": "Операции с отрицательными числами", "en": "Operations with negative numbers"},
                    "icon": "−",
                    "theory": {"sections": [{"title": {"ru": "Отрицательные числа", "en": "Negative numbers"}, "content": {"ru": "Числа меньше нуля.", "en": "Numbers less than zero."}, "examples": ["-2 × -3 = 6"]}]},
                    "questions": [{"id": 1, "question": {"ru": "-8 + 12 = ?", "en": "-8 + 12 = ?"}, "type": "input", "correct_answer": "4", "explanation": {"ru": "4", "en": "4"}}]
                },
                {
                    "id": "probability",
                    "title": {"ru": "Вероятность", "en": "Probability"},
                    "category": "advanced",
                    "description": {"ru": "Теория вероятностей", "en": "Probability theory"},
                    "icon": "🎲",
                    "theory": {"sections": [{"title": {"ru": "Вероятность", "en": "Probability"}, "content": {"ru": "От 0 до 1.", "en": "From 0 to 1."}, "examples": ["Вероятность орла = 0.5", "Probability of heads = 0.5"]}]},
                    "questions": [{"id": 1, "question": {"ru": "Вероятность выпадения 6 на кубике?", "en": "Probability of rolling a 6 on a die?"}, "type": "input", "correct_answer": "1/6", "explanation": {"ru": "1/6", "en": "1/6"}}]
                }
            ]

            with open('topics.json', 'w', encoding='utf-8') as f:
                json.dump(default_topics, f, ensure_ascii=False, indent=2)

        if not os.path.exists('progress.json'):
            with open('progress.json', 'w', encoding='utf-8') as f:
                json.dump({'topics': {}, 'total_score': 0, 'streak_days': 0}, f, indent=2)

        if not os.path.exists('settings.json'):
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump({'theme': 'light', 'accent_color': 'green', 'language': 'ru'}, f, indent=2)

    def load_settings(self):
        s = self.load_json('settings.json')
        if s:
            self.theme = s.get('theme', 'light')
            self.color = s.get('accent_color', 'green')
            self.language = s.get('language', 'ru')

    def save_settings(self):
        self.save_json('settings.json', {
            'theme': self.theme,
            'accent_color': self.color,
            'language': self.language
        })

    def change_language(self, text):
        new_lang = 'en' if text == "English" else 'ru'
        if new_lang != self.language:
            self.language = new_lang
            self.save_settings()
            self.retranslate_ui()

    def retranslate_ui(self):
        self.stack.clear()
        self.create_home_screen()
        self.create_settings_screen()
        self.apply_theme()
        self.update_nav_buttons()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav = QWidget()
        nav.setFixedHeight(70)
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(20, 10, 20, 10)

        title = QLabel("🧮 " + self.tr("МатематикаPro", "MathPro"))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.home_btn = QPushButton("🏠 " + self.tr("Главная", "Home"))
        self.home_btn.setObjectName("nav_btn")
        self.home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        self.settings_btn = QPushButton("⚙️ " + self.tr("Настройки", "Settings"))
        self.settings_btn.setObjectName("nav_btn")
        self.settings_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.settings_btn)

        layout.addWidget(nav)

        self.stack = QStackedWidget()
        self.stack.currentChanged.connect(self.update_nav_buttons)
        layout.addWidget(self.stack)

        self.create_home_screen()
        self.create_settings_screen()

    def update_nav_buttons(self):
        current = self.stack.currentIndex()
        self.home_btn.setStyleSheet("")
        self.settings_btn.setStyleSheet("")

        colors = {
            'green': '#58CC02', 'blue': '#1CB0F6', 'red': '#FF4B4B',
            'pink': '#FF6FD8', 'purple': '#A855F7'
        }
        c = colors[self.color]

        if current == 0:
            self.home_btn.setStyleSheet(f"background-color: {c}; color: white; border-radius: 12px; padding: 12px 24px;")
        elif current == 1:
            self.settings_btn.setStyleSheet(f"background-color: {c}; color: white; border-radius: 12px; padding: 12px 24px;")

    def create_home_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QLabel(self.tr("Добро пожаловать!", "Welcome!"))
        header.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(header)

        subtitle = QLabel(self.tr("Выберите тему для изучения", "Choose a topic to study"))
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        stats = QFrame()
        stats.setObjectName("card")
        stats.setMaximumHeight(80)
        stats_layout = QHBoxLayout(stats)

        self.score_label = QLabel(f"🏆 {self.tr('Очков', 'Points')}: {self.progress.get('total_score', 0)}")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.streak_label = QLabel(f"🔥 {self.tr('Дней', 'Days')}: {self.progress.get('streak_days', 0)}")
        self.streak_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        stats_layout.addWidget(self.score_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.streak_label)
        layout.addWidget(stats)

        filter_layout = QHBoxLayout()
        filter_label = QLabel(self.tr("Категория:", "Category:"))
        filter_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.category_combo = QComboBox()
        self.category_combo.addItems([
            self.tr("Все", "All"),
            self.tr("Основы", "Basics"),
            self.tr("Средний уровень", "Intermediate"),
            self.tr("Продвинутый", "Advanced")
        ])
        self.category_combo.currentTextChanged.connect(self.filter_topics)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.category_combo)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.topics_layout = QGridLayout(self.scroll_content)
        self.topics_layout.setSpacing(20)

        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll)

        self.load_topics()
        self.stack.addWidget(widget)

    def update_stats(self):
        self.score_label.setText(f"🏆 {self.tr('Очков', 'Points')}: {self.progress.get('total_score', 0)}")
        self.streak_label.setText(f"🔥 {self.tr('Дней', 'Days')}: {self.progress.get('streak_days', 0)}")

    def filter_topics(self, text):
        map_cat = {
            self.tr("Все", "All"): "all",
            self.tr("Основы", "Basics"): "basics",
            self.tr("Средний уровень", "Intermediate"): "intermediate",
            self.tr("Продвинутый", "Advanced"): "advanced"
        }
        self.current_category = map_cat.get(text, "all")
        self.load_topics()

    def create_settings_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QLabel("⚙️ " + self.tr("Настройки", "Settings"))
        header.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(header)

        # Тема оформления
        theme_card = QFrame()
        theme_card.setObjectName("card")
        theme_card.setMaximumWidth(700)
        theme_layout = QVBoxLayout(theme_card)
        theme_layout.setContentsMargins(30, 30, 30, 30)

        theme_title = QLabel("🌓 " + self.tr("Тема оформления", "Appearance"))
        theme_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        theme_layout.addWidget(theme_title)

        theme_select = QHBoxLayout()
        theme_label = QLabel(self.tr("Выберите тему:", "Choose theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([self.tr("Светлая", "Light"), self.tr("Тёмная", "Dark")])
        self.theme_combo.setCurrentIndex(0 if self.theme == 'light' else 1)
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        theme_select.addWidget(theme_label)
        theme_select.addWidget(self.theme_combo)
        theme_select.addStretch()
        theme_layout.addLayout(theme_select)
        layout.addWidget(theme_card, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Цветовая схема
        color_card = QFrame()
        color_card.setObjectName("card")
        color_card.setMaximumWidth(700)
        color_layout = QVBoxLayout(color_card)
        color_layout.setContentsMargins(30, 30, 30, 30)

        color_title = QLabel("🎨 " + self.tr("Цветовая схема", "Color scheme"))
        color_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        color_layout.addWidget(color_title)

        colors_grid = QGridLayout()
        colors_grid.setSpacing(15)
        color_names = {
            'green': self.tr("Зелёный", "Green"),
            'blue': self.tr("Синий", "Blue"),
            'red': self.tr("Красный", "Red"),
            'pink': self.tr("Розовый", "Pink"),
            'purple': self.tr("Фиолетовый", "Purple")
        }
        colors_list = [('green', '🟢'), ('blue', '🔵'), ('red', '🔴'), ('pink', '🩷'), ('purple', '🟣')]

        for i, (key, emoji) in enumerate(colors_list):
            btn = QPushButton(emoji + " " + color_names[key])
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda _, k=key: self.change_color(k))
            colors_grid.addWidget(btn, i // 3, i % 3)

        color_layout.addLayout(colors_grid)
        layout.addWidget(color_card, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Язык
        lang_card = QFrame()
        lang_card.setObjectName("card")
        lang_card.setMaximumWidth(700)
        lang_layout = QVBoxLayout(lang_card)
        lang_layout.setContentsMargins(30, 30, 30, 30)

        lang_title = QLabel("🌍 " + self.tr("Язык", "Language"))
        lang_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        lang_layout.addWidget(lang_title)

        lang_select = QHBoxLayout()
        lang_label = QLabel(self.tr("Выберите язык:", "Choose language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English"])
        self.lang_combo.setCurrentIndex(0 if self.language == 'ru' else 1)
        self.lang_combo.currentTextChanged.connect(self.change_language)

        lang_select.addWidget(lang_label)
        lang_select.addWidget(self.lang_combo)
        lang_select.addStretch()
        lang_layout.addLayout(lang_select)
        layout.addWidget(lang_card, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()
        self.stack.addWidget(widget)

    def change_theme(self, text):
        self.theme = 'light' if text == self.tr("Светлая", "Light") else 'dark'
        self.save_settings()
        self.apply_theme()

    def change_color(self, color):
        self.color = color
        self.save_settings()
        self.apply_theme()

    def load_topics(self):
        for i in reversed(range(self.topics_layout.count())):
            widget = self.topics_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        topics = self.load_json('topics.json') or []
        if self.current_category != 'all':
            topics = [t for t in topics if t.get('category') == self.current_category]

        for i, topic in enumerate(topics):
            card = self.create_topic_card(topic)
            self.topics_layout.addWidget(card, i // 2, i % 2)

    def create_topic_card(self, topic):
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumSize(400, 220)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)

        header = QHBoxLayout()
        icon = QLabel(topic.get('icon', '📚'))
        icon.setStyleSheet("font-size: 56px; background: transparent; padding: 0px; margin: 0px; border: none;")
        icon.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        lang = self.language
        title_text = topic['title'][lang] if isinstance(topic['title'], dict) else topic['title']
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")

        cat_map = {
            'basics': self.tr('📗 Основы', '📗 Basics'),
            'intermediate': self.tr('📘 Средний', '📘 Intermediate'),
            'advanced': self.tr('📕 Продвинутый', '📕 Advanced')
        }
        category = QLabel(cat_map.get(topic.get('category'), ''))
        category.setObjectName("subtitle")

        header.addWidget(icon)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(category)
        layout.addLayout(header)

        desc_text = topic['description'][lang] if isinstance(topic['description'], dict) else topic['description']
        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setObjectName("subtitle")
        layout.addWidget(desc)

        tp = self.progress['topics'].get(topic['id'], {})
        completed = len(tp.get('questions_completed', []))
        total = len(topic.get('questions', []))

        progress_text = QLabel(self.tr(f"Выполнено: {completed}/{total}", f"Completed: {completed}/{total}"))
        progress_text.setObjectName("subtitle")
        layout.addWidget(progress_text)

        pbar = QProgressBar()
        pbar.setMaximum(total if total else 1)
        pbar.setValue(completed)
        pbar.setTextVisible(False)
        layout.addWidget(pbar)

        buttons = QHBoxLayout()
        theory_btn = QPushButton("📖 " + self.tr("Теория", "Theory"))
        theory_btn.clicked.connect(lambda: self.show_theory(topic))
        practice_btn = QPushButton("✏️ " + self.tr("Практика", "Practice"))
        practice_btn.setEnabled(tp.get('theory_completed', False))
        practice_btn.clicked.connect(lambda: self.show_practice(topic))

        buttons.addWidget(theory_btn)
        buttons.addWidget(practice_btn)
        layout.addLayout(buttons)

        return card

    def show_theory(self, topic):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QHBoxLayout()
        back = QPushButton("← " + self.tr("Назад", "Back"))
        back.setObjectName("secondary")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        lang = self.language
        title_text = topic['title'][lang] if isinstance(topic['title'], dict) else topic['title']
        title = QLabel(f"{topic['icon']} {title_text}")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header.addWidget(back)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        for section in topic['theory']['sections']:
            sec_title_text = section['title'][lang] if isinstance(section['title'], dict) else section['title']
            sec_title = QLabel(sec_title_text)
            sec_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 20px;")
            content_layout.addWidget(sec_title)

            frame = QFrame()
            frame.setObjectName("card")
            f_layout = QVBoxLayout(frame)
            sec_content_text = section['content'][lang] if isinstance(section['content'], dict) else section['content']
            text = QLabel(sec_content_text)
            text.setWordWrap(True)
            f_layout.addWidget(text)
            content_layout.addWidget(frame)

            if 'examples' in section:
                ex_label = QLabel("📝 " + self.tr("Примеры:", "Examples:"))
                ex_label.setStyleSheet("font-size: 18px; font-weight: bold;")
                content_layout.addWidget(ex_label)
                for ex in section['examples']:
                    ex_frame = QFrame()
                    ex_frame.setObjectName("card")
                    ex_l = QVBoxLayout(ex_frame)
                    ex_t = QLabel(ex)
                    ex_t.setStyleSheet("font-family: 'Courier New'; font-size: 16px;")
                    ex_l.addWidget(ex_t)
                    content_layout.addWidget(ex_frame)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        complete_btn = QPushButton("✓ " + self.tr("Завершить теорию", "Complete theory"))
        complete_btn.clicked.connect(lambda: self.complete_theory(topic['id']))
        layout.addWidget(complete_btn)

        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def show_practice(self, topic):
        self.current_topic = topic
        self.current_question = 0
        self.practice_score = 0
        self.show_question()

    def show_question(self):
        questions = self.current_topic['questions']
        if self.current_question >= len(questions):
            self.show_results()
            return

        question = questions[self.current_question]
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QHBoxLayout()
        back = QPushButton("← " + self.tr("Назад", "Back"))
        back.setObjectName("secondary")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        lang = self.language
        title_text = self.current_topic['title'][lang] if isinstance(self.current_topic['title'], dict) else self.current_topic['title']
        title = QLabel(f"{self.current_topic['icon']} {title_text} - " + self.tr("Практика", "Practice"))
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header.addWidget(back)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        prog_label = QLabel(self.tr(f"Вопрос {self.current_question + 1} из {len(questions)}", f"Question {self.current_question + 1} of {len(questions)}"))
        prog_label.setObjectName("subtitle")
        layout.addWidget(prog_label)

        pbar = QProgressBar()
        pbar.setMaximum(len(questions))
        pbar.setValue(self.current_question + 1)
        layout.addWidget(pbar)

        score_label = QLabel(f"🏆 " + self.tr("Очков в этой сессии:", "Points in this session:") + f" {self.practice_score}")
        score_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(score_label)

        q_frame = QFrame()
        q_frame.setObjectName("card")
        q_layout = QVBoxLayout(q_frame)
        q_layout.setContentsMargins(40, 40, 40, 40)

        q_text_str = question['question'][self.language] if isinstance(question['question'], dict) else question['question']
        q_text = QLabel(q_text_str)
        q_text.setStyleSheet("font-size: 22px; font-weight: bold;")
        q_text.setWordWrap(True)
        q_layout.addWidget(q_text)

        if question['type'] == 'multiple_choice':
            for opt in question['options']:
                btn = QPushButton(opt)
                btn.setMinimumHeight(60)
                btn.clicked.connect(lambda _, a=opt: self.check_answer(a, question))
                q_layout.addWidget(btn)
        else:
            lbl = QLabel(self.tr("Введите ваш ответ:", "Enter your answer:"))
            q_layout.addWidget(lbl)
            input_field = QLineEdit()
            input_field.setPlaceholderText(self.tr("Ваш ответ...", "Your answer..."))
            input_field.setMinimumHeight(50)
            q_layout.addWidget(input_field)
            check_btn = QPushButton(self.tr("Проверить ответ", "Check answer"))
            check_btn.setMinimumHeight(50)
            check_btn.clicked.connect(lambda: self.check_answer(input_field.text(), question))
            q_layout.addWidget(check_btn)

        layout.addWidget(q_frame)
        layout.addStretch()

        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def check_answer(self, user_answer, question):
        topic_id = self.current_topic['id']
        tp = self.progress['topics'].setdefault(topic_id, {})
        q_id = question['id']
        completed = tp.get('questions_completed', [])

        correct = str(user_answer).strip() == str(question['correct_answer']).strip()

        if correct and q_id not in completed:
            self.practice_score += 10
            completed.append(q_id)
            tp['questions_completed'] = completed
            tp['score'] = tp.get('score', 0) + 10
            self.progress['total_score'] = self.progress.get('total_score', 0) + 10
            self.save_progress()

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        frame = QFrame()
        frame.setObjectName("card")
        f_layout = QVBoxLayout(frame)
        f_layout.setContentsMargins(40, 40, 40, 40)

        if correct:
            label = QLabel("✅ " + self.tr("Правильно!", "Correct!"))
            label.setStyleSheet("font-size: 28px; font-weight: bold; color: #58CC02;")
        else:
            label = QLabel("❌ " + self.tr("Неправильно", "Incorrect") + f"\n\n" + self.tr("Правильный ответ:", "Correct answer:") + f" {question['correct_answer']}")
            label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF4B4B;")

        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(label)

        if 'explanation' in question:
            exp_text = question['explanation'][self.language] if isinstance(question['explanation'], dict) else question['explanation']
            exp = QLabel(f"💡 {exp_text}")
            exp.setWordWrap(True)
            exp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            exp.setStyleSheet("font-size: 16px; margin-top: 20px;")
            f_layout.addWidget(exp)

        layout.addWidget(frame)

        next_btn = QPushButton(self.tr("Следующий вопрос →", "Next question →"))
        next_btn.setMinimumHeight(60)
        next_btn.clicked.connect(self.next_question)
        layout.addWidget(next_btn)

        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def next_question(self):
        self.current_question += 1
        self.show_question()

    def show_results(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)

        frame = QFrame()
        frame.setObjectName("card")
        f_layout = QVBoxLayout(frame)
        f_layout.setContentsMargins(60, 60, 60, 60)

        title = QLabel("🎉 " + self.tr("Практика завершена!", "Practice completed!"))
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(title)

        earned = QLabel(self.tr("Заработано: +{0} очков", "Earned: +{0} points").format(self.practice_score))
        earned.setStyleSheet("font-size: 24px; margin-top: 20px;")
        earned.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(earned)

        total = QLabel(self.tr("Общий счёт: {0} очков", "Total score: {0} points").format(self.progress.get('total_score', 0)))
        total.setStyleSheet("font-size: 20px;")
        total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(total)

        layout.addWidget(frame)

        home_btn = QPushButton(self.tr("Вернуться на главную", "Back to home"))
        home_btn.setMinimumHeight(60)
        home_btn.clicked.connect(self.go_home_after_practice)
        layout.addWidget(home_btn)

        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def go_home_after_practice(self):
        self.stack.setCurrentIndex(0)
        self.load_topics()
        self.update_stats()

    def complete_theory(self, topic_id):
        tp = self.progress['topics'].setdefault(topic_id, {})
        tp['theory_completed'] = True
        self.save_progress()
        self.stack.setCurrentIndex(0)
        self.load_topics()

    def apply_theme(self):
        colors = {
            'green': {'p': '#58CC02', 'd': '#46A302'},
            'blue': {'p': '#1CB0F6', 'd': '#1899D6'},
            'red': {'p': '#FF4B4B', 'd': '#E63939'},
            'pink': {'p': '#FF6FD8', 'd': '#E654C1'},
            'purple': {'p': '#A855F7', 'd': '#9333EA'}
        }
        c = colors[self.color]

        if self.theme == 'light':
            bg = '#FFFFFF'
            bg2 = '#F7F7F7'
            txt = '#2B2B2B'
            txt2 = '#777777'
            brd = '#E5E5E5'
        else:
            bg = '#1F1F1F'
            bg2 = '#2B2B2B'
            txt = '#FFFFFF'
            txt2 = '#AAAAAA'
            brd = '#404040'

        self.setStyleSheet(f"""
            QMainWindow {{background-color: {bg};}}
            QWidget {{background-color: {bg}; color: {txt};}}
            QPushButton {{background-color: {c['p']}; color: white; border: none; border-radius: 12px; padding: 12px 24px; font-weight: bold;}}
            QPushButton:hover {{background-color: {c['d']};}}
            QPushButton#secondary {{background-color: {bg2}; color: {txt}; border: 2px solid {brd}; border-radius: 12px; padding: 12px;}}
            QPushButton#secondary:hover {{background-color: {brd};}}
            QPushButton#nav_btn {{background-color: {bg2}; color: {txt}; border: 2px solid {brd}; border-radius: 12px; padding: 12px 24px; font-weight: bold;}}
            QPushButton#nav_btn:hover {{border-color: {c['p']};}}
            QLabel {{color: {txt}; background: transparent;}}
            QLabel#subtitle {{color: {txt2}; font-size: 13px;}}
            QFrame#card {{background-color: {bg2}; border-radius: 16px; border: 1px solid {brd};}}
            QProgressBar {{border-radius: 8px; background: {brd}; height: 12px;}}
            QProgressBar::chunk {{background: {c['p']}; border-radius: 8px;}}
            QScrollArea {{background-color: {bg}; border: none;}}
            QScrollBar:vertical {{width: 0px;}}
            QScrollBar:horizontal {{height: 0px;}}
            QLineEdit {{background: {bg2}; border: 2px solid {brd}; border-radius: 8px; padding: 10px; color: {txt};}}
            QLineEdit:focus {{border-color: {c['p']};}}
            QComboBox {{background: {bg2}; border: 2px solid {brd}; border-radius: 8px; padding: 8px; color: {txt};}}
            QComboBox:hover {{border-color: {c['p']};}}
            QComboBox QAbstractItemView {{background: {bg2}; selection-background-color: {c['p']};}}
        """)

        self.setWindowTitle("🧮 " + self.tr("МатематикаPro", "MathPro"))
        self.update_nav_buttons()
        if self.stack.currentIndex() == 0:
            self.update_stats()

    def load_json(self, filename):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения {filename}: {e}")
        return None

    def save_json(self, filename, data):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка записи {filename}: {e}")

    def load_progress(self):
        self.progress = self.load_json('progress.json') or {'topics': {}, 'total_score': 0, 'streak_days': 0}

    def save_progress(self):
        self.save_json('progress.json', self.progress)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MathApp()
    window.show()
    sys.exit(app.exec())