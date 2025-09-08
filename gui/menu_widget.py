# gui/menu_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class MenuWidget(QWidget):
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Títulos
        title = QLabel(" Proyecto AVL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 50px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(" Andrés Felipe Giraldo - Miguel Angel Cruz")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 25px;")
        layout.addWidget(subtitle)

        # Botones
        start_btn = QPushButton("Iniciar Juego")
        start_btn.setFixedSize(500, 50)
        start_btn.clicked.connect(self.start_signal)
        layout.addWidget(start_btn)

        exit_btn = QPushButton("Salir")
        exit_btn.setFixedSize(500, 50)
        exit_btn.clicked.connect(self.exit_signal)
        layout.addWidget(exit_btn)

        self.setLayout(layout)
