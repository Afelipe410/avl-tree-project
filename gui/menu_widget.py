from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

class MenuWidget(QWidget):
    # Señales que MainWindow escuchará
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar tamaño mínimo
        self.setMinimumSize(300, 200)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Título
        title = QLabel("🎮 JUEGO 🎮")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Nombres de los autores
        authors = QLabel("Presentado por:\nAndrés Felipe Giraldo Rojas \nMiguel Angel Cruz Betancourt")
        authors.setFont(QFont("Arial", 11))
        authors.setAlignment(Qt.AlignmentFlag.AlignCenter)
        authors.setWordWrap(True)
        layout.addWidget(authors)

        # Profesor
        teacher = QLabel("Presentado a:\nJeferson Arango Lopez")
        teacher.setFont(QFont("Arial", 11))
        teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        teacher.setWordWrap(True)
        layout.addWidget(teacher)

        # Botón Jugar
        btn_start = QPushButton("Jugar")
        btn_start.setFont(QFont("Arial", 14))
        btn_start.clicked.connect(self.start_signal.emit)
        layout.addWidget(btn_start)

        # Botón Salir
        btn_exit = QPushButton("Salir")
        btn_exit.setFont(QFont("Arial", 14))
        btn_exit.clicked.connect(self.exit_signal.emit)
        layout.addWidget(btn_exit)
