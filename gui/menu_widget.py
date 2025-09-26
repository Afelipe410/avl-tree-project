from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor, QPalette

class MenuWidget(QWidget):
    # Señales que MainWindow escuchará
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar tamaño mínimo
        self.setMinimumSize(400, 300)

        # Fondo con paleta (oscuro)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)

        # Título
        title = QLabel("Ruta Mortal")
        title.setFont(QFont("Arial", 38, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Color rojo al texto del título
        title_palette = title.palette()
        title_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 20, 60))
        title.setPalette(title_palette)

        layout.addWidget(title)

        authors = QLabel("\nAndrés Felipe Giraldo Rojas\nMiguel Angel Cruz Betancourt")
        authors.setFont(QFont("Arial", 15, QFont.Weight.Medium))
        authors.setAlignment(Qt.AlignmentFlag.AlignCenter)

        authors_palette = authors.palette()
        authors_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        authors.setPalette(authors_palette)

        layout.addWidget(authors)
        
        btn_start = QPushButton("▶ Jugar")
        btn_start.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(btn_start)
        btn_start.clicked.connect(self.start_signal.emit)

        btn_exit = QPushButton("✖ Salir")
        btn_exit.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(btn_exit)
        btn_exit.clicked.connect(self.exit_signal.emit)
