from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer
from gui.avl_tree import AVLTree
from gui.game_widget import GameWidget
from gui.tree_widget import TreeWidget

class GameplayWidget(QWidget):
    def __init__(self, avl: AVLTree, parent=None):
        super().__init__(parent)
        self.avl = avl
        self.game = GameWidget(self.avl, {"game": {"speed": 6}})
        self.tree_w = TreeWidget(self.avl)
        self.game = GameWidget(self.avl, {"game": {"speed": 6}}, parent=self)
        self.tree_w = TreeWidget(self.avl, parent=self)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.game, 3)
        layout.addWidget(self.tree_w, 2)

        self.game.hit_signal.connect(self.on_hit)
        self.game.game_over_signal.connect(self.on_game_over)

        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_from_avl)
        self.sync_timer.start(250)

    def on_hit(self):
        print("Jugador golpeado! Vidas:", self.game.lives)

    def on_game_over(self, msg):
        QMessageBox.information(self, "Fin del Juego", msg)
        self.show_menu()

    def sync_from_avl(self):
        try:
            self.tree_w.update()
        except Exception:
            pass

    def show_menu(self):
        if self.parent() and hasattr(self.parent(), "setCurrentIndex"):
            self.parent().setCurrentIndex(0)
