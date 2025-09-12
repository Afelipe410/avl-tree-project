import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QTimer
from gui.avl_tree import AVLTree
from gui.gameplay_widget import GameplayWidget
from gui.menu_widget import MenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proyecto AVL - Estructuras de Datos")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu = MenuWidget()

        self.avl = AVLTree()
        self.avl.insert(1200, {'id': 1, 'x_world': 1200, 'lane_idx': 1, 'width': 32, 'height': 32})
        self.avl.insert(1600, {'id': 2, 'x_world': 1600, 'lane_idx': 0, 'width': 32, 'height': 32})
        self.avl.insert(2000, {'id': 3, 'x_world': 2000, 'lane_idx': 2, 'width': 32, 'height': 32})

        self.gameplay = GameplayWidget(self.avl)

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