import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
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

        # cargar nivel desde JSON
        config, avl = load_game_from_json("level1.json")

        self.gameplay = GameplayWidget(avl)

        # pasar configuración al GameWidget
        if self.gameplay.game:
            self.gameplay.game.config = config
            self.gameplay.game.speed = config.get("game", {}).get("speed", self.gameplay.game.speed)
            self.gameplay.game.goal_x = config.get("game", {}).get("distance_total", self.gameplay.game.goal_x)

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.gameplay)

        self.menu.start_signal.connect(self.start_game)
        self.menu.exit_signal.connect(self.exit_game)

        self.stack.setCurrentWidget(self.menu)
        QTimer.singleShot(0, self.showMaximized)

    def start_game(self):
        self.stack.setCurrentWidget(self.gameplay)
        self.gameplay.game.setFocus()

    def exit_game(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
