import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import QTimer
from gui.json_loader import load_game_from_json
from gui.gameplay_widget import GameplayWidget
from gui.menu_widget import MenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proyecto AVL - Estructuras de Datos 2025 - II")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu = MenuWidget()

        self.gameplay = None 
        self.load_level("level1.json")

        self.stack.addWidget(self.menu)
        self.menu.start_signal.connect(self.start_game)
        self.menu.load_level_signal.connect(self.on_load_level_request)
        self.menu.exit_signal.connect(self.exit_game)

        self.stack.setCurrentWidget(self.menu)
        QTimer.singleShot(0, self.showMaximized)

    def start_game(self):
        self.stack.setCurrentWidget(self.gameplay)
        self.gameplay.game.setFocus()
        # Iniciar simulacion del juego
        try: 
            self.gameplay.game.start()
        except Exception:
            pass
        self.gameplay.game.setFocus()

    def exit_game(self):
        QApplication.quit()

    def on_load_level_request(self, file_path):
        try:
            self.load_level(file_path)
            QMessageBox.information(self, "Nivel Cargado", f"Se ha cargado el nivel desde:\n{file_path}")
            self.stack.setCurrentWidget(self.menu)
        except Exception as e:
            QMessageBox.critical(self, "Error de Carga", f"No se pudo cargar el archivo de nivel.\nError: {e}")

    def load_level(self, file_path):
        if self.gameplay:
            self.stack.removeWidget(self.gameplay)
            self.gameplay.deleteLater()

        config, avl = load_game_from_json(file_path)
        self.gameplay = GameplayWidget(avl, parent=self.stack)

        self.gameplay.game.config = config
        self.gameplay.game.speed = config.get("game", {}).get("speed", self.gameplay.game.speed)
        self.gameplay.game.goal_x = config.get("game", {}).get("distance_total", self.gameplay.game.goal_x)
        self.stack.addWidget(self.gameplay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
