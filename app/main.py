import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from app import const
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

        self.key_binds = {
            Qt.Key.Key_PageUp: lambda: self.change_scale(1),
            Qt.Key.Key_PageDown: lambda: self.change_scale(-1),
            Qt.Key.Key_Up: lambda: self.shift_coordinates(shift_y=const.MAP_SHIFT_Y),
            Qt.Key.Key_Down: lambda: self.shift_coordinates(shift_y=-const.MAP_SHIFT_Y),
            Qt.Key.Key_Right: lambda: self.shift_coordinates(shift_x=const.MAP_SHIFT_X),
            Qt.Key.Key_Left: lambda: self.shift_coordinates(shift_x=-const.MAP_SHIFT_X)
        }

        self.initUi()
        self.next_frame()

    def initUi(self):
        """Инициализация интерфейса"""
        self.town_label = QLabel(self)
        self.town_label.resize(720, 540)

    def next_frame(self):
        """Загрузка изображения"""

        try:
            image_bytes = get_map_image(self.scale, self.long_lat)
            with open(const.MAP_IMAGE_FILE, "wb") as file:
                file.write(image_bytes)
            self.town_label.setPixmap(QPixmap(const.MAP_IMAGE_FILE))
        except Exception as err:
            print("Ошибка получения изображения карты: ", err)

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
