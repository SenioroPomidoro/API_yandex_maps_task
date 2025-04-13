import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QVBoxLayout, \
    QWidget, QHBoxLayout, QCheckBox

from app import const
from app.api.geocoder_api import get_coords, get_address, get_postal_code, get_toponym
from app.api.static_api import get_map_image
from app.classes.LineEdit import SuperMegaQLineEdit


class MapsApp(QMainWindow):
    def __init__(self) -> None:
        """Функция инициализации приложения"""
        super().__init__()
        self.setWindowTitle("MapsApp")
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(600, 650)

        self.scale = 1  # Масштаб (В диапазоне 0-21)
        self.long_lat = [39.0, 58.0]
        self.theme_id = 0  # 0 - светлая, 1 - темная
        self.marker_coords = None
        self.address_filed_text = ""
        self.postal_code = ""

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
        self.update_map_image()

    def initUi(self):
        """Инициализация интерфейса"""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.theme_button = QPushButton("Темная тема", self)
        self.theme_button.setGeometry(450, 50, 140, 30)
        self.theme_button.clicked.connect(self.toggle_theme)

        # Панель поиска
        self.search_input = SuperMegaQLineEdit()
        self.search_input.setPlaceholderText("Введите адрес для поиска...")
        self.search_button = QPushButton("Искать")
        self.reset_button = QPushButton("Сбросить")
        self.search_button.clicked.connect(self.search_location_with_input)
        self.reset_button.clicked.connect(self.reset_search_result)
        self.reset_button.clicked.connect(self.reset_search_result)
        self.search_input.returnPressed.connect(self.search_location_with_input)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_button)
        layout.addLayout(search_layout)

        self.town_label = QLabel(self)
        self.town_label.resize(720, 540)
        self.town_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.town_label)

        self.address_label = QLabel(self)
        self.address_label.resize(600, 50)
        self.address_label.move(10, 570)

        self.show_postal_code_checkbox = QCheckBox(self)
        self.show_postal_code_checkbox.setText("Показать почтовый индекс")
        self.show_postal_code_checkbox.resize(self.show_postal_code_checkbox.sizeHint())
        self.show_postal_code_checkbox.move(250, 50)
        self.show_postal_code_checkbox.toggled.connect(self.radio_reaction)

    def radio_reaction(self):
        """Функция, обрабатывающая смену показа почтового индекса"""
        self.update_widgets()

    def set_address_text(self, address):
        self.address_label.setText(address)
        self.address_label.resize(self.address_label.sizeHint())
        self.address_label.setWordWrap(True)  # Автоматический перенос строк
        self.address_label.setFixedWidth(580)

    def reset_search_result(self):
        self.search_input.setText("")
        self.address_filed_text = ""
        self.postal_code = None
        self.marker_coords = None
        self.update_map_image()
        self.update_widgets()

    def toggle_theme(self):
        """Переключение между темами"""
        self.theme_id = 1 - self.theme_id
        self.update_app_theme()
        self.update_map_image()

    def update_app_theme(self):
        """Обновление стилей приложения в зависимости от темы"""
        palette = QApplication.palette()
        if self.theme_id == 1:
            # Темная тема
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.darkGray)
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            self.theme_button.setText("Светлая тема")
        else:
            # Светлая тема
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            self.theme_button.setText("Темная тема")

        QApplication.instance().setPalette(palette)

    def update_widgets(self):
        address_text = self.address_filed_text
        if self.show_postal_code_checkbox.isChecked():
            address_text = self.postal_code + ", " + address_text
        self.set_address_text("Адрес: " + address_text)

    def update_map_image(self):
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
            QMessageBox.critical(
                self, "Ошибка",
                f"Ошибка получения изображения карты: : {str(err)}"
            )

    def set_search_result(self, toponym):
        coords = get_coords(toponym)
        if coords:
            self.long_lat = coords
            self.marker_coords = coords.copy()
            self.address_filed_text = get_address(toponym)
            self.postal_code = get_postal_code(toponym)
        else:
            self.marker_coords = None
            self.address_filed_text = ""
            self.postal_code = ""
            QMessageBox.warning(
                self, "Ошибка",
                "Объект по такому адресу не найден!"
            )

        self.update_map_image()
        self.update_widgets()

    def search_location_with_input(self):
        address = self.search_input.text().strip()
        if not address:
            return
        try:
            toponym = get_toponym(address)
            self.set_search_result(toponym)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")

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
            self.update_map_image()

    def closeEvent(self, a0):
        """Обработчик выхода из приложения"""
        os.remove(const.MAP_IMAGE_FILE)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MapsApp()
    ex.show()
    sys.exit(app.exec())
