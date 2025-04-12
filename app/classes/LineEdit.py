from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal


class SuperMegaQLineEdit(QLineEdit):
    textSubmitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.key() in [
            Qt.Key.Key_PageUp,
            Qt.Key.Key_PageDown,
            Qt.Key.Key_Left,
            Qt.Key.Key_Right,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down
        ]:
            event.ignore()
        else:
            super().keyPressEvent(event)
