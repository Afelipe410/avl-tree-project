from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient
from PyQt6.QtCore import Qt, QTimer
from gui.avl_tree import AVLTree

class TreeWidget(QWidget):
    def __init__(self, avl: AVLTree, parent=None):
        super().__init__(parent)
        self.avl = avl
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.highlighted_nodes = []
        self.highlight_timer = QTimer(self)
        self.highlight_timer.timeout.connect(self._update_highlight)

        # Lista de tipos de obstáculos con sus colores
        self.obstacle_types = [
            {"name": "Aceite", "color": "#2C3E50", "text_color": "#ECF0F1"},
            {"name": "Hueco", "color": "#8B4513", "text_color": "#FFFFFF"},
            {"name": "Cono", "color": "#E67E22", "text_color": "#FFFFFF"},
            {"name": "Piedra", "color": "#95A5A6", "text_color": "#2C3E50"},
            {"name": "Charco", "color": "#3498DB", "text_color": "#FFFFFF"},
            {"name": "Rama", "color": "#27AE60", "text_color": "#FFFFFF"},
            {"name": "Vidrio", "color": "#E8F8F5", "text_color": "#2C3E50"},
            {"name": "Metal", "color": "#566573", "text_color": "#FFFFFF"}
        ]

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Etiqueta para mostrar recorridos
        self.traversal_label = QLabel("Recorrido: ")
        self.traversal_label.setFont(QFont("Segoe UI", 10))
        self.traversal_label.setWordWrap(True)
        layout.addWidget(self.traversal_label)

        # Espaciador
        layout.addStretch()
        
        # Botones de recorridos
        traversal_layout = QGridLayout()
        self.bfs_btn = QPushButton("BFS")
        self.preorder_btn = QPushButton("Pre-orden")
        self.inorder_btn = QPushButton("En-orden")
        self.postorder_btn = QPushButton("Post-orden")
        
        traversal_layout.addWidget(self.bfs_btn, 0, 0)
        traversal_layout.addWidget(self.preorder_btn, 0, 1)
        traversal_layout.addWidget(self.inorder_btn, 1, 0)
        traversal_layout.addWidget(self.postorder_btn, 1, 1)
        layout.addLayout(traversal_layout)

        self.bfs_btn.clicked.connect(lambda: self.show_traversal('bfs'))
        self.preorder_btn.clicked.connect(lambda: self.show_traversal('preorder'))
        self.inorder_btn.clicked.connect(lambda: self.show_traversal('inorder'))
        self.postorder_btn.clicked.connect(lambda: self.show_traversal('postorder'))

        # Botón de agregar
        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Agregar Obstáculo")
        self.add_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498DB, stop:1 #2980B9);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5DADE2, stop:1 #3498DB);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980B9, stop:1 #1B4F72);
            }
        """)
        btns.addWidget(self.add_btn)
        layout.addLayout(btns)
        self.add_btn.clicked.connect(self._add_random_obstacle)

        # Establecer fondo del widget
        self.setStyleSheet("""
            TreeWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
                border-radius: 10px;
            }
        """)

    def _add_random_obstacle(self):
        import random
        lane = random.randint(0, len(self.parent().game.lane_y)-1)
        obstacle_type = random.choice(self.obstacle_types)
        # Crear plantilla SIN x_world: GameWidget asignará la x_world para que aparezca desde la derecha
        ob = {
            "id": random.randint(1000, 9999),
            "name": obstacle_type["name"],
            "color": obstacle_type["color"],
            "text_color": obstacle_type["text_color"],
            "lane_idx": lane,
            "width": 32,
            "height": 32,
        }
        # La clave en el árbol usa una X temporal (no se usa para dibujo directo)
        key = (self.parent().game.world_offset + 1000 + random.randint(0, 1000), ob["lane_idx"])
        self.avl.insert(key, ob)
        # Notificar al GameWidget para que se cree el spawn desde la derecha
        try: 
            self.parent().game.register_new_obstacle(ob)
        except Exception:
            pass
        self.update()
    
    def show_traversal(self, traversal_type):
        traversal_map = {
            'bfs': self.avl.bfs,
            'preorder': self.avl.preorder,
            'inorder': self.avl.inorder,
            'postorder': self.avl.postorder,
        }
        nodes = traversal_map.get(traversal_type, self.avl.inorder)()
        self.highlighted_nodes = list(nodes) 
        
        path_text = " -> ".join([f"#{node.obstacle['id']}" for node in nodes])
        self.traversal_label.setText(f"Recorrido {traversal_type.upper()}: {path_text}")
        
        if self.highlighted_nodes:
            self.highlight_timer.start(300)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo con gradiente
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#F8F9FA"))
        gradient.setColorAt(1, QColor("#E9ECEF"))
        p.fillRect(self.rect(), QBrush(gradient))

        if not self.avl.root:
            p.setPen(QPen(QColor("#7F8C8D"), 2))
            p.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 
                      "🚫 No hay obstáculos en el árbol\n\nHaz clic en 'Agregar Obstáculo' para comenzar")
            return
        
        self._draw_node(p, self.avl.root, self.width() // 2, 120, self.width() // 4)

    def _update_highlight(self):
        if not self.highlighted_nodes:
            self.highlight_timer.stop()
            self.update() 
            return
        self.highlighted_nodes.pop(0)
        self.update()

    def _draw_node(self, p, node, x, y, dx):
        if not node:
            return

        line_pen = QPen(QColor("#34495E"), 3, Qt.PenStyle.SolidLine)
        line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(line_pen)
        
        if node.left:
            p.drawLine(x - 5, y + 25, x - dx + 5, y + 75)
            self._draw_node(p, node.left, x - dx, y + 80, dx // 2)
            
        if node.right:
            p.drawLine(x + 5, y + 25, x + dx - 5, y + 75)
            self._draw_node(p, node.right, x + dx, y + 80, dx // 2)

        # Dibujar el nodo solo si tiene datos válidos
        node_size = 50
        obstacle = node.obstacle
        
        # Validación del obstáculo
        if not obstacle or not isinstance(obstacle, dict):
            return
            
        if obstacle and "color" in obstacle:
            # Color del obstáculo
            node_color = QColor(obstacle["color"])
            text_color = QColor(obstacle["text_color"])
        else:
            # Color por defecto
            node_color = QColor("#3498DB")
            text_color = QColor("#FFFFFF")

        # Sombra del nodo
        shadow_brush = QBrush(QColor(0, 0, 0, 50))
        p.setBrush(shadow_brush)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(x - node_size//2 + 3, y - node_size//2 + 3, node_size, node_size)

        gradient = QLinearGradient(x - node_size//2, y - node_size//2, 
                                 x + node_size//2, y + node_size//2)
        gradient.setColorAt(0, node_color.lighter(120))
        gradient.setColorAt(1, node_color.darker(110))
        
        node_brush = QBrush(gradient)
        p.setBrush(node_brush)
        
        # Borde del nodo (resaltado si está en la animación)
        is_highlighted = self.highlighted_nodes and self.highlighted_nodes[0] == node
        border_color = QColor("#FFD700") if is_highlighted else QColor("#2C3E50")
        border_width = 4 if is_highlighted else 2
        border_pen = QPen(border_color, border_width)
        p.setPen(border_pen)
        p.drawEllipse(x - node_size//2, y - node_size//2, node_size, node_size)

        p.setPen(QPen(text_color, 1))
        
        key_x, key_y = node.key

        # ID en la parte superior
        id_text = f"#{node.obstacle['id']}" if node.obstacle else f"#{key_x}"
        p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        p.drawText(x - 25, y - 15, 50, 12, Qt.AlignmentFlag.AlignCenter, id_text)
        
        # Nombre del obstáculo en el centro
        if obstacle and "name" in obstacle:
            name_text = obstacle["name"]
            p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            p.drawText(x - 25, y - 5, 50, 12, Qt.AlignmentFlag.AlignCenter, name_text)
        
        # Posición X en la parte inferior
        pos_text = f"({key_x}, {key_y})"
        p.setFont(QFont("Segoe UI", 7, QFont.Weight.Normal))
        p.drawText(x - 25, y + 8, 50, 12, Qt.AlignmentFlag.AlignCenter, pos_text)