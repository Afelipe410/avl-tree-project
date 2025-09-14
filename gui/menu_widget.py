from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPalette

class MenuWidget(QWidget):
    # Señales que MainWindow escucha
    start_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar el widget principal
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #2c3e50, stop: 1 #34495e);
            }
        """)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        # Spacer superior para centrar mejor el contenido
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Título del juego
        title_label = QLabel("🎮 JUEGO 🎮")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                background: transparent;
                padding: 10px;
                border-radius: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        layout.addWidget(title_label)

        # Nombres de los autores
        lbl = QLabel("Andrés Felipe Giraldo Rojas - Miguel Angel Cruz Betancourt")
        lbl.setFont(QFont("Arial", 12, QFont.Weight.Normal))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("""
            QLabel {
                color: #bdc3c7;
                background: transparent;
                padding: 15px;
                margin: 10px;
            }
        """)
        layout.addWidget(lbl)

        # Espaciador entre título y botones
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Botón iniciar
        btn_start = QPushButton("🚀 Jugar")
        btn_start.setMinimumHeight(50)
        btn_start.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_start.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #27ae60, stop: 1 #2ecc71);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #2ecc71, stop: 1 #27ae60);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #229954, stop: 1 #27ae60);
                transform: translateY(1px);
            }
        """)
        btn_start.clicked.connect(self.start_signal.emit)
        layout.addWidget(btn_start)

        # Espaciador entre botones
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Botón salir
        btn_exit = QPushButton("❌ Salir")
        btn_exit.setMinimumHeight(50)
        btn_exit.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_exit.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #e74c3c, stop: 1 #c0392b);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #c0392b, stop: 1 #e74c3c);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #a93226, stop: 1 #c0392b);
                transform: translateY(1px);
            }
        """)
        btn_exit.clicked.connect(self.exit_signal.emit)
        layout.addWidget(btn_exit)

        # Spacer inferior para centrar mejor el contenido
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))