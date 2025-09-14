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
        super().__init__(menu_parent)
        from gui.game_widget import GameWidget
        from gui.tree_widget import TreeWidget

        self.avl = avl
        self.game = GameWidget({"game": {"speed": 6}})
        self.tree_w = TreeWidget(self.avl)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
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
        print(msg)
        # Mensaje visual simple
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Fin del Juego", msg)
        # Opcional: volver al menú
        self.show_menu()

    def sync_from_avl(self):
        """
        Sincroniza los obstáculos del árbol AVL con el juego.
        """
        try:
            obs_from_avl = self.avl.to_obstacles()  # lista de dicts
            
            # Debug: print the structure of the first obstacle to understand the format
            if obs_from_avl:
                print("Debug - First obstacle structure:", obs_from_avl[0])
            
            obstacles_for_game = []
            
            for o in obs_from_avl:
                # Check if the obstacle has the expected x_world position
                x_world = o.get("x_world", 0)  # Use .get() to avoid KeyError
                
                # Only include obstacles that are visible in the current game view
                if x_world >= self.game.world_offset:
                    obstacle_data = {
                        "id": o.get("id", 0),
                        "name": o.get("name", "Unknown"),
                        "color": o.get("color", "#FF0000"),
                        "text_color": o.get("text_color", "#FFFFFF"),
                        "spawn_x": x_world,
                        "x_world": x_world,
                        "lane_idx": o.get("lane_idx", 0),
                        "width": o.get("width", 50),
                        "height": o.get("height", 50),
                    }
                    obstacles_for_game.append(obstacle_data)
            
            self.game.set_obstacles(obstacles_for_game)
            
        except Exception as e:
            print(f"Error in sync_from_avl: {e}")
            print(f"obs_from_avl structure: {obs_from_avl if 'obs_from_avl' in locals() else 'Not defined'}")

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
