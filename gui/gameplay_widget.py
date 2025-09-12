from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer
from gui.avl_tree import AVLTree

class GameplayWidget(QWidget):
    def __init__(self, avl: AVLTree, menu_parent=None):
        super().__init__(menu_parent)
        from gui.game_widget import GameWidget
        from gui.tree_widget import TreeWidget

        self.avl = avl
        self.game = GameWidget({"game": {"speed": 6}})
        self.tree_w = TreeWidget(self.avl)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.game, 3)
        layout.addWidget(self.tree_w, 2)

        self.game.hit_signal.connect(self.on_hit)

        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_from_avl)
        self.sync_timer.start(250)

    def sync_from_avl(self):
        obs = self.avl.to_obstacles()
        self.game.set_obstacles([dict(o) for o in obs])

    def on_hit(self):
        print("Jugador golpeado! Vidas:", self.game.lives)

    def show_menu(self):
        if self.parent() and hasattr(self.parent(), "setCurrentIndex"):
            self.parent().setCurrentIndex(0)
