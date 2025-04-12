from app.main import QApplication, MapsApp, sys

app = QApplication(sys.argv)
window = MapsApp()
window.show()
sys.exit(app.exec())
