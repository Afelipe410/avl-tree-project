from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer
from gui.avl_tree import AVLTree

class GameplayWidget(QWidget):
    """
    Widget principal que integra la jugabilidad y la visualización del árbol AVL.

    - Muestra el juego y el árbol AVL en una sola interfaz.
    - Sincroniza los obstáculos del árbol AVL con el juego periódicamente.
    - Escucha eventos de golpe para mostrar las vidas restantes.
    - Permite volver al menú principal si el padre lo soporta.
    """
    def __init__(self, avl: AVLTree, menu_parent=None):
        """
        Inicializa el widget de jugabilidad.

        Args:
            avl (AVLTree): Instancia del árbol AVL con los obstáculos.
            menu_parent: Widget padre para navegación de menú (opcional).
        """
        super().__init__(menu_parent)
        from gui.game_widget import GameWidget
        from gui.tree_widget import TreeWidget

        self.avl = avl
        self.game = GameWidget({"game": {"speed": 6}})
        self.tree_w = TreeWidget(self.avl)

        # Layout horizontal: juego a la izquierda, árbol a la derecha
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.game, 3)
        layout.addWidget(self.tree_w, 2)

        # Conecta la señal de golpe del juego
        self.game.hit_signal.connect(self.on_hit)

        # Sincroniza los obstáculos del árbol AVL con el juego cada 250 ms
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_from_avl)
        self.sync_timer.start(250)

    def sync_from_avl(self):
        obs_from_avl = self.avl.to_obstacles()
        # Convierte todos los obstáculos del AVL al formato del juego
        obstacles_for_game = [
            {
                "id": o.get("id"),
                "name": o.get("name"),
                "color": o.get("color"),
                "text_color": o.get("text_color"),
                "spawn_x": o.get("x_world", 0),
                "lane_idx": o.get("lane_idx", 0),
                "width": o.get("width", 32),
                "height": o.get("height", 32),
            }
            for o in obs_from_avl
        ]
        self.game.set_obstacles(obstacles_for_game)

    def on_hit(self):
        """
        Maneja el evento de golpe, mostrando las vidas restantes en consola.
        """
        print("Jugador golpeado! Vidas:", self.game.lives)

    def show_menu(self):
        """
        Permite volver al menú principal si el widget padre lo soporta.
        """
        if self.parent() and hasattr(self.parent(), "setCurrentIndex"):
            self.parent().setCurrentIndex(0)
