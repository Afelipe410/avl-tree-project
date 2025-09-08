# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QTimer
from gui.game_widget import GameWidget
from gui.menu_widget import MenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proyecto AVL - Estructuras de Datos")
        self.setWindowFlags(self.windowFlags())

        # Widget central: stack para menú y juego
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Widgets
        self.menu = MenuWidget()
        self.game = GameWidget({})

        # Agregar al stack
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.game)

        # Conexiones
        self.menu.start_signal.connect(self.start_game)
        self.menu.exit_signal.connect(self.exit_game)

        # Mostrar menú primero
        self.stack.setCurrentWidget(self.menu)

        # Maximizar después de mostrar
        QTimer.singleShot(0, self.showMaximized)

    def start_game(self):
        self.stack.setCurrentWidget(self.game)
        self.game.setFocus()

    def exit_game(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # primero mostrar
    sys.exit(app.exec())
