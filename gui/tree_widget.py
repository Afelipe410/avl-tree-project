from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient
from PyQt6.QtCore import Qt
from gui.avl_tree import AVLTree

class TreeWidget(QWidget):
    def __init__(self, avl: AVLTree, parent=None):
        super().__init__(parent)
        self.avl = avl
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

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
        
        # Agregar un espaciador para empujar el botón hacia abajo
        layout.addStretch()
        
        # Botón con mejor estilo en la parte inferior
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
        x_world = self.parent().game.world_offset + 300 + random.randint(0, 500)
        lane = random.randint(0, 3)  # asegúrate de 4 carriles

        obstacle_type = random.choice(self.obstacle_types)
        ob = {
        "id": random.randint(1000, 9999),
        "name": obstacle_type["name"],
        "color": obstacle_type["color"],
        "text_color": obstacle_type["text_color"],
        "x_world": x_world,
        "lane_idx": lane,
        "width": 32,
        "height": 32,
    }
        self.avl.insert(x_world, ob)
        self.update()


    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo con gradiente
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#F8F9FA"))
        gradient.setColorAt(1, QColor("#E9ECEF"))
        p.fillRect(self.rect(), QBrush(gradient))

        if not self.avl.root:
            # Mensaje cuando no hay obstáculos
            p.setPen(QPen(QColor("#7F8C8D"), 2))
            p.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 
                      "🚫 No hay obstáculos en el árbol\n\nHaz clic en 'Agregar Obstáculo' para comenzar")
            return

        # Dibujar árbol recursivo - ajustamos la altura inicial para dejar espacio al botón
        tree_area_height = self.height() - 80  # Reservar espacio para el botón
        self._draw_node(p, self.avl.root, self.width() // 2, 60, self.width() // 4)

    def _draw_node(self, p, node, x, y, dx):
        if not node:
            return

        # Dibujar líneas a los hijos primero (para que queden detrás)
        line_pen = QPen(QColor("#34495E"), 3, Qt.PenStyle.SolidLine)
        line_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(line_pen)
        
        if node.left:
            # Línea curva hacia la izquierda
            p.drawLine(x - 5, y + 15, x - dx + 5, y + 45)
            self._draw_node(p, node.left, x - dx, y + 60, dx // 2)
            
        if node.right:
            # Línea curva hacia la derecha
            p.drawLine(x + 5, y + 15, x + dx - 5, y + 45)
            self._draw_node(p, node.right, x + dx, y + 60, dx // 2)

        # Dibujar el nodo solo si tiene datos válidos
        node_size = 50
        obstacle = node.obstacle
        
        # Validación adicional del obstáculo
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

        # Nodo principal con gradiente
        gradient = QLinearGradient(x - node_size//2, y - node_size//2, 
                                 x + node_size//2, y + node_size//2)
        gradient.setColorAt(0, node_color.lighter(120))
        gradient.setColorAt(1, node_color.darker(110))
        
        node_brush = QBrush(gradient)
        p.setBrush(node_brush)
        
        # Borde del nodo
        border_pen = QPen(QColor("#2C3E50"), 2)
        p.setPen(border_pen)
        p.drawEllipse(x - node_size//2, y - node_size//2, node_size, node_size)

        # Texto del nodo - SOLUCIONADO: solo una vez, sin duplicados
        p.setPen(QPen(text_color, 1))
        
        # ID en la parte superior
        id_text = f"#{node.obstacle['id']}" if node.obstacle else f"#{node.key}"
        p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        p.drawText(x - 25, y - 15, 50, 12, Qt.AlignmentFlag.AlignCenter, id_text)
        
        # Nombre del obstáculo en el centro
        if obstacle and "name" in obstacle:
            name_text = obstacle["name"]
            p.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            p.drawText(x - 25, y - 5, 50, 12, Qt.AlignmentFlag.AlignCenter, name_text)
        
        # Posición X en la parte inferior
        pos_text = f"X:{node.key}"
        p.setFont(QFont("Segoe UI", 7, QFont.Weight.Normal))
        p.drawText(x - 25, y + 8, 50, 12, Qt.AlignmentFlag.AlignCenter, pos_text)