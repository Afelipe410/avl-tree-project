from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

class MenuWidget(QWidget):
    # Señales que MainWindow escucha
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        lbl = QLabel("Proyecto AVL - Estructuras de Datos")
        lbl.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        # Botón iniciar
        btn_start = QPushButton("Jugar")
        btn_start.setMinimumHeight(40)
        btn_start.clicked.connect(self.start_signal.emit)
        layout.addWidget(btn_start)

        # Botón salir
        btn_exit = QPushButton("Salir")
        btn_exit.setMinimumHeight(40)
        btn_exit.clicked.connect(self.exit_signal.emit)
        layout.addWidget(btn_exit)
