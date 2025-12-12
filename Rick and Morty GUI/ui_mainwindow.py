# ui_mainwindow.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTabWidget, QTextEdit, QListWidget,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox,
    QSpinBox, QHeaderView
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from api import *
from storage import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rick & Morty Explorer")
        self.resize(1000, 700)
        self.encyclopedia = load_encyclopedia()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.setup_main_tab()
        self.setup_character_tab()
        self.setup_episode_tab()
        self.setup_location_tab()
        self.setup_random_tab()
        self.setup_episodes_tab()
        self.setup_encyclopedia_tab()
        self.setup_history_tab()

        self.setStyleSheet("""
            QMainWindow { background-color: #121212; color: #00ff41; }
            QPushButton { background-color: #00ff41; color: black; font-weight: bold; padding: 10px; border-radius: 8px; }
            QPushButton:hover { background-color: #00cc33; }
            QLineEdit, QComboBox, QSpinBox { padding: 8px; background: #1e1e1e; border: 1px solid #00ff41; color: white; }
            QLabel { color: #00ff41; font-size: 14px; }
            QTabWidget::pane { border: 1px solid #00ff41; }
            QTabBar::tab { background: #1e1e1e; color: white; padding: 10px; }
            QTabBar::tab:selected { background: #00ff41; color: black; }
        """)

    def add_history(self, text):
        add_to_history(text)
        # Обновляем вкладку истории, если она существует
        if hasattr(self, 'history_list'):
            self.history_list.addItem(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def setup_main_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Rick & Morty Explorer")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        try:
            pixmap = QPixmap("resources/rick_morty_logo.png").scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo)
        except:
            pass

        buttons = [
            ("Найти персонажа", self.tabs.setCurrentIndex, 1),
            ("Найти эпизод", self.tabs.setCurrentIndex, 2),
            ("Найти локацию", self.tabs.setCurrentIndex, 3),
            ("Случайный персонаж", self.tabs.setCurrentIndex, 4),
            ("Список всех эпизодов", self.tabs.setCurrentIndex, 5),
            ("Энциклопедия", self.tabs.setCurrentIndex, 6),
            ("История действий", self.tabs.setCurrentIndex, 7),
            ("Выход", self.close),
        ]

        for text, cmd, *args in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda _, c=cmd, a=args: c(*a) if a else c())
            layout.addWidget(btn)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Главная")

    def show_character_info(self, char):
        info = f"""
        <h2>{char['name']}</h2>
        <b>Статус:</b> {char['status']}<br>
        <b>Вид:</b> {char['species']}<br>
        <b>Пол:</b> {char.get('gender', 'Неизвестно')}<br>
        <b>Локация:</b> {char['location']['name']}<br>
        <b>Происхождение:</b> {char['origin']['name']}<br>
        <b>Эпизодов:</b> {len(char['episode'])}
        """
        return info

    def setup_character_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.char_input = QLineEdit()
        self.char_input.setPlaceholderText("Введите имя персонажа...")
        search_btn = QPushButton("Найти")
        search_layout.addWidget(self.char_input)
        search_layout.addWidget(search_btn)

        self.char_result = QTextEdit()
        self.char_result.setReadOnly(True)

        add_btn = QPushButton("Добавить в энциклопедию")
        add_btn.clicked.connect(self.add_to_encyclopedia_from_result)

        layout.addLayout(search_layout)
        layout.addWidget(self.char_result)
        layout.addWidget(add_btn)

        search_btn.clicked.connect(self.search_character)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Персонаж")

        self.current_character = None

    def search_character(self):
        name = self.char_input.text().strip()
        if not name:
            return
        char = search_character(name)
        if char:
            self.current_character = char
            self.char_result.setHtml(self.show_character_info(char))
            self.add_history(f"Поиск персонажа: {char['name']}")
        else:
            self.char_result.setText("Персонаж не найден!")
            QMessageBox.warning(self, "Ошибка", "Персонаж не найден")

    def add_to_encyclopedia_from_result(self):
        if not self.current_character:
            return
        char = self.current_character
        name = char['name']
        self.encyclopedia[name] = {
            "id": char['id'],
            "image": char['image'],
            "status": char['status'],
            "species": char['species'],
            "location": char['location']['name'],
            "episodes": len(char['episode']),
            "rating": 5  # по умолчанию
        }
        save_encyclopedia(self.encyclopedia)
        self.add_history(f"Добавлен в энциклопедию: {name}")
        QMessageBox.information(self, "Успех", f"{name} добавлен в энциклопедию!")

    # ... (остальные вкладки аналогично — ниже сокращённый код для экономии места)

    def setup_episode_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        h = QHBoxLayout()
        self.ep_input = QLineEdit()
        self.ep_input.setPlaceholderText("Например: S01E05")
        btn = QPushButton("Найти эпизод")
        h.addWidget(self.ep_input)
        h.addWidget(btn)
        self.ep_result = QTextEdit()
        self.ep_result.setReadOnly(True)
        layout.addLayout(h)
        layout.addWidget(self.ep_result)
        btn.clicked.connect(self.search_episode)
        widget.setLayout(layout)
        self.tabs.addTab(widget, "Эпизод")

    def search_episode(self):
        code = self.ep_input.text().strip().upper()
        if not code:
            return
        ep = search_episode(code)
        if ep:
            chars = ", ".join([c.split("/")[-1] for c in ep['characters'][:5]])
            text = f"<h2>{ep['name']} ({ep['episode']})</h2>" \
                   f"<b>Дата выхода:</b> {ep['air_date']}<br>" \
                   f"<b>Персонажи (первые 5):</b> {chars}"
            self.ep_result.setHtml(text)
            self.add_history(f"Поиск эпизода: {ep['episode']}")
        else:
            self.ep_result.setText("Эпизод не найден")

    def setup_location_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        h = QHBoxLayout()
        self.loc_input = QLineEdit()
        self.loc_input.setPlaceholderText("Введите название локации...")
        btn = QPushButton("Найти")
        h.addWidget(self.loc_input)
        h.addWidget(btn)
        self.loc_result = QTextEdit()
        self.loc_result.setReadOnly(True)
        layout.addLayout(h)
        layout.addWidget(self.loc_result)
        btn.clicked.connect(self.search_location)
        widget.setLayout(layout)
        self.tabs.addTab(widget, "Локация")

    def search_location(self):
        name = self.loc_input.text().strip()
        if not name:
            return
        loc = search_location(name)
        if loc:
            text = f"<h2>{loc['name']}</h2>" \
                   f"<b>Тип:</b> {loc['type']}<br>" \
                   f"<b>Измерение:</b> {loc['dimension']}<br>" \
                   f"<b>Жителей:</b> {len(loc['residents'])}"
            self.loc_result.setHtml(text)
            self.add_history(f"Поиск локации: {loc['name']}")
        else:
            self.loc_result.setText("Локация не найдена")

    def setup_random_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        btn = QPushButton("Получить случайного персонажа")
        btn.clicked.connect(self.show_random_character)
        self.random_result = QTextEdit()
        self.random_result.setReadOnly(True)
        add_btn = QPushButton("Добавить в энциклопедию")
        add_btn.clicked.connect(self.add_to_encyclopedia_from_result)
        layout.addWidget(btn)
        layout.addWidget(self.random_result)
        layout.addWidget(add_btn)
        widget.setLayout(layout)
        self.tabs.addTab(widget, "Случайный")

    def show_random_character(self):
        char = get_random_character()
        if char:
            self.current_character = char
            self.random_result.setHtml(self.show_character_info(char))
            self.add_history(f"Случайный персонаж: {char['name']}")

    def setup_episodes_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        top = QHBoxLayout()
        self.season_combo = QComboBox()
        self.season_combo.addItems(["Все"] + [f"Сезон {i}" for i in range(1, 8)])
        load_btn = QPushButton("Загрузить все эпизоды")
        top.addWidget(QLabel("Фильтр по сезону:"))
        top.addWidget(self.season_combo)
        top.addWidget(load_btn)

        self.episodes_table = QTableWidget()
        self.episodes_table.setColumnCount(4)
        self.episodes_table.setHorizontalHeaderLabels(["№", "Название", "Код", "Дата выхода"])
        self.episodes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addLayout(top)
        layout.addWidget(self.episodes_table)

        load_btn.clicked.connect(self.load_all_episodes)
        self.season_combo.currentTextChanged.connect(self.filter_episodes)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Эпизоды")

        self.all_episodes = []

    def load_all_episodes(self):
        self.all_episodes = get_all_episodes()
        self.filter_episodes()

    def filter_episodes(self):
        season = self.season_combo.currentText()
        self.episodes_table.setRowCount(0)
        for ep in self.all_episodes:
            if season == "Все" or ep['episode'].startswith(season.replace("Сезон ", "S")):
                row = self.episodes_table.rowCount()
                self.episodes_table.insertRow(row)
                self.episodes_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.episodes_table.setItem(row, 1, QTableWidgetItem(ep['name']))
                self.episodes_table.setItem(row, 2, QTableWidgetItem(ep['episode']))
                self.episodes_table.setItem(row, 3, QTableWidgetItem(ep['air_date']))

    def setup_encyclopedia_tab(self):
        widget = QWidget()
        layout = QHBoxLayout()

        self.encyclopedia_list = QListWidget()
        self.encyclopedia_list.itemClicked.connect(self.show_encyclopedia_character)

        right = QVBoxLayout()
        self.enc_char_info = QTextEdit()
        self.enc_char_info.setReadOnly(True)
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 5)
        self.rating_spin.setPrefix("Рейтинг: ")
        self.rating_spin.valueChanged.connect(self.update_rating)

        del_btn = QPushButton("Удалить из энциклопедии")
        del_btn.clicked.connect(self.delete_from_encyclopedia)

        right.addWidget(self.enc_char_info)
        right.addWidget(self.rating_spin)
        right.addWidget(del_btn)

        layout.addWidget(self.encyclopedia_list, 2)
        layout.addLayout(right, 3)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Энциклопедия")
        self.refresh_encyclopedia_list()

    def refresh_encyclopedia_list(self):
        self.encyclopedia_list.clear()
        for name in self.encyclopedia:
            self.encyclopedia_list.addItem(name)

    def show_encyclopedia_character(self, item):
        name = item.text()
        data = self.encyclopedia[name]
        char = get_character_by_id(data['id'])
        if char:
            self.enc_char_info.setHtml(self.show_character_info(char))
            self.rating_spin.setValue(data.get('rating', 5))
            self.current_enc_name = name

    def update_rating(self, value):
        if hasattr(self, 'current_enc_name'):
            self.encyclopedia[self.current_enc_name]['rating'] = value
            save_encyclopedia(self.encyclopedia)

    def delete_from_encyclopedia(self):
        if hasattr(self, 'current_enc_name'):
            name = self.current_enc_name
            del self.encyclopedia[name]
            save_encyclopedia(self.encyclopedia)
            self.refresh_encyclopedia_list()
            self.enc_char_info.clear()
            self.add_history(f"Удалён из энциклопедии: {name}")

    def setup_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        export_btn = QPushButton("Экспорт истории в JSON")
        export_btn.clicked.connect(lambda: QMessageBox.information(self, "OK", "История сохранена в history.json"))
        layout.addWidget(self.history_list)
        layout.addWidget(export_btn)
        for entry in load_history():
            self.history_list.addItem(f"[{entry['time']}] {entry['action']}")
        widget.setLayout(layout)
        self.tabs.addTab(widget, "История")