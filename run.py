import os

from app import const
from app.main import QApplication, MapsApp, sys

os.makedirs(const.MAP_IMAGE_PATH, exist_ok=True)

app = QApplication(sys.argv)
window = MapsApp()
window.show()
sys.exit(app.exec())
