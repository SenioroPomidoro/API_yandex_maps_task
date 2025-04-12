import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from app.api.static_api import create_new_map_image


class MapsApp(QMainWindow):
    def __init__(self) -> None:
        """Функция инициализации приложения"""
        super().__init__()
        self.setWindowTitle("MapsApp")
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(600, 600)

        self.scale = 1  # Масштаб (В диапазоне 0-21)
        self.ll = "39,58"

        self.keys_in_use = [
            Qt.Key.Key_PageUp,
            Qt.Key.Key_PageDown,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Right,
            Qt.Key.Key_Left
        ]

        self.initUi()
        self.next_frame()

    def initUi(self):
        """Инициализация интерфейса"""
        self.town_label = QLabel(self)
        self.town_label.resize(720, 540)

    def next_frame(self):
        """Загрузка изображения"""
        self.update_params()
        create_new_map_image(self.params)
        self.town_label.setPixmap(QPixmap("app/map/map_image.png"))

    def update_params(self):
        """Обновление параметров запроса"""
        if self.scale > 21:
            self.scale = 21
        if self.scale < 0:
            self.scale = 0

        ll = self.ll.split(",")
        if float(ll[1]) <= -85:
            ll[1] = "-85"
        elif float(ll[1]) >= 85:
            ll[1] = "85"
        if float(ll[0]) >= 180:
            ll[0] = "-180"
        elif float(ll[0]) <= -180:
            ll[0] = "180"
        self.ll = ",".join(ll)

        self.params = {
            "ll": self.ll,
            "z": str(self.scale)
        }

    def keyPressEvent(self, event):
        """Обработка нажатий на клавиши"""
        key_id = event.key()

        if key_id in self.keys_in_use:
            if key_id == Qt.Key.Key_PageUp:
                self.scale += 1
            elif key_id == Qt.Key.Key_PageDown:
                self.scale -= 1
            elif key_id == Qt.Key.Key_Up:
                shift = 100 / (2 ** self.scale)
                ll = self.ll.split(",")
                ll[1] = str(float(ll[1]) + shift)
                self.ll = ",".join(ll)
            elif key_id == Qt.Key.Key_Down:
                shift = 100 / (2 ** self.scale)
                ll = self.ll.split(",")
                ll[1] = str(float(ll[1]) - shift)
                self.ll = ",".join(ll)
            elif key_id == Qt.Key.Key_Right:
                shift = 150 / (2 ** self.scale)
                ll = self.ll.split(",")
                ll[0] = str(float(ll[0]) + shift)
                self.ll = ",".join(ll)
            elif key_id == Qt.Key.Key_Left:
                shift = 150 / (2 ** self.scale)
                ll = self.ll.split(",")
                ll[0] = str(float(ll[0]) - shift)
                self.ll = ",".join(ll)

            self.next_frame()

    def closeEvent(self, a0):
        """Обработчик выхода из приложения"""
        os.remove("app/map/map_image.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MapsApp()
    ex.show()
    sys.exit(app.exec())
