from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from gui.avl_tree import AVLTree

class TreeWidget(QWidget):
    def __init__(self, avl: AVLTree, parent=None):
        super().__init__(parent)
        self.avl = avl
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        lbl = QLabel("Árbol AVL de obstáculos")
        lbl.setFont(QFont("Arial", 12))
        layout.addWidget(lbl)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("Agregar obstáculo")
        btns.addWidget(self.add_btn)
        layout.addLayout(btns)
        self.add_btn.clicked.connect(self._add_random_obstacle)

    def _add_random_obstacle(self):
        import random
        x_world = 800 + random.randint(0, 800)
        lane = random.randint(0, 2)
        ob = {
            "id": random.randint(1000, 9999),
            "x_world": x_world,
            "lane_idx": lane,
            "width": 32,
            "height": 32,
        }
        self.avl.insert(x_world, ob)
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#9D3633"))

        if not self.avl.root:
            p.setPen(QColor("#888"))
            p.drawText(20, 60, "(sin obstáculos)")
            return

        # Dibujar árbol recursivo
        self._draw_node(p, self.avl.root, self.width() // 2, 40, self.width() // 4)

    def _draw_node(self, p, node, x, y, dx):
        if not node:
            return

        # Línea a hijos
        if node.left:
            p.setPen(QPen(QColor("#aaa"), 2))
            p.drawLine(x, y, x - dx, y + 60)
            self._draw_node(p, node.left, x - dx, y + 60, dx // 2)
        if node.right:
            p.setPen(QPen(QColor("#aaa"), 2))
            p.drawLine(x, y, x + dx, y + 60)
            self._draw_node(p, node.right, x + dx, y + 60, dx // 2)

        # Nodo
        p.setBrush(QColor("#87cefa"))
        p.setPen(QColor("#000"))
        p.drawEllipse(x - 20, y - 20, 40, 40)

        txt = f"{node.key}"
        if node.obstacle:
            txt = f"{node.obstacle['id']}"
        p.drawText(x - 15, y + 5, txt)
