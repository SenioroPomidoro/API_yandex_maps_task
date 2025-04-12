import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QLineEdit, QVBoxLayout, \
    QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPalette
from PyQt6.QtCore import Qt

from app import const
from app.api.geocoder_api import get_coords
from app.api.static_api import get_map_image


class MapsApp(QMainWindow):
    def __init__(self) -> None:
        """Функция инициализации приложения"""
        super().__init__()
        self.setWindowTitle("MapsApp")
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(600, 600)

        self.scale = 1  # Масштаб (В диапазоне 0-21)
        self.long_lat = [39.0, 58.0]
        self.theme_id = 0  # 0 - светлая, 1 - темная
        self.marker_coords = None

        self.key_binds = {
            Qt.Key.Key_PageUp: lambda: self.change_scale(1),
            Qt.Key.Key_PageDown: lambda: self.change_scale(-1),
            Qt.Key.Key_Up: lambda: self.shift_coordinates(shift_y=const.MAP_SHIFT_Y),
            Qt.Key.Key_Down: lambda: self.shift_coordinates(shift_y=-const.MAP_SHIFT_Y),
            Qt.Key.Key_Right: lambda: self.shift_coordinates(shift_x=const.MAP_SHIFT_X),
            Qt.Key.Key_Left: lambda: self.shift_coordinates(shift_x=-const.MAP_SHIFT_X)
        }

        self.initUi()
        self.update_app_theme()  # Применяем начальную тему
        self.next_frame()

    def initUi(self):
        """Инициализация интерфейса"""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.theme_button = QPushButton("Темная тема", self)
        self.theme_button.setGeometry(450, 50, 140, 30)
        self.theme_button.clicked.connect(self.toggle_theme)

        # Панель поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите адрес для поиска...")
        self.search_button = QPushButton("Искать")
        self.search_button.clicked.connect(self.search_location)
        self.search_input.returnPressed.connect(self.search_location)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        self.town_label = QLabel()
        self.town_label.resize(720, 540)
        self.town_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.town_label)

    def toggle_theme(self):
        """Переключение между темами"""
        self.theme_id = 1 - self.theme_id
        self.update_app_theme()
        self.next_frame()

    def update_app_theme(self):
        """Обновление стилей приложения в зависимости от темы"""
        palette = QApplication.palette()
        if self.theme_id == 1:
            # Темная тема
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.darkGray)
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, Qt.GlobalColor.darkGray)
            self.theme_button.setText("Светлая тема")
        else:
            # Светлая тема
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Button, Qt.GlobalColor.lightGray)
            self.theme_button.setText("Темная тема")

        QApplication.instance().setPalette(palette)

    def next_frame(self):
        """Загрузка изображения"""
        try:
            image_bytes = get_map_image(
                scale=self.scale,
                long_lat=self.long_lat,
                theme=const.MAP_COLOR_THEMES[self.theme_id],
                marker_coords=self.marker_coords
            )
            with open(const.MAP_IMAGE_FILE, "wb") as file:
                file.write(image_bytes)
            self.town_label.setPixmap(QPixmap(const.MAP_IMAGE_FILE))
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка получения изображения карты: : {str(err)}")

    def search_location(self):
        address = self.search_input.text().strip()
        if not address:
            return

        try:
            coords = get_coords(address)
            if coords:
                self.long_lat = coords
                self.marker_coords = coords
                self.next_frame()
            else:
                self.marker_coords = None
                QMessageBox.warning(self, "Ошибка", "Объект по такому адресу не найден!")
                self.next_frame()
        except Exception as e:
            self.marker_coords = None
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")
            self.next_frame()

    def change_scale(self, amount):
        self.scale += amount
        self.scale = max(const.SCALE_LIMITS[0], min(self.scale, const.SCALE_LIMITS[1]))

    def shift_coordinates(self, shift_x: float = 0, shift_y: float = 0):
        self.long_lat[0] += shift_x / (2 ** self.scale)
        self.long_lat[1] += shift_y / (2 ** self.scale)

        self.long_lat[0] = min(const.LONGITUDE_LIMITS[1], max(self.long_lat[0], const.LONGITUDE_LIMITS[0]))
        self.long_lat[1] = min(const.LATITUDE_LIMITS[1], max(self.long_lat[1], const.LATITUDE_LIMITS[0]))

    def keyPressEvent(self, event):
        """Обработка нажатий на клавиши"""
        key_id = event.key()

        if key_id in self.key_binds:
            self.key_binds[key_id]()
            self.next_frame()

    def closeEvent(self, a0):
        """Обработчик выхода из приложения"""
        os.remove(const.MAP_IMAGE_FILE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MapsApp()
    ex.show()
    sys.exit(app.exec())
