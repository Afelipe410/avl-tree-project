# gui/game_widget.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
import math

class GameWidget(QWidget):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config or {}

        # Configuración del juego
        self.refresh_ms   = self.config.get("game", {}).get("refresh_time", 50)
        self.speed_px     = self.config.get("game", {}).get("speed", 5)
        self.jump_power   = self.config.get("game", {}).get("jump_height", 80)
        self.car_color_on = QColor(self.config.get("game", {}).get("car_color", "red"))
        self.car_color_jump = QColor("#00C853")  

        self.setMinimumSize(800, 420)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Estado del carro
        self.car_x = 80
        self.car_width  = 120
        self.car_height = 40
        self.cabin_height = 22
        self.wheel_r = 14
        self.wheel_angle_deg = 0.0

        # Carriles
        self.road_h = 120
        self._recompute_geometry()
        self.lane_idx = 1
        self._set_car_ground_y_by_lane()

        # Salto
        self.is_jumping = False
        self.vy = 0.0
        self.gravity = 1.9

        # Scroll de carretera
        self.road_scroll = 0.0
        self.stripe_w = 40
        self.stripe_gap = 30
        self.stripe_h = 6

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(self.refresh_ms)

    def _recompute_geometry(self):
        self.road_y = self.height() - self.road_h
        top = self.road_y - 140
        mid = self.road_y - 100
        bot = self.road_y - 60
        self.lanes = [top, mid, bot]

    def _set_car_ground_y_by_lane(self):
        self.car_ground_y = self.lanes[self.lane_idx]
        self.car_y = self.car_ground_y

    def _tick(self):
        self.road_scroll = (self.road_scroll + self.speed_px) % (self.stripe_w + self.stripe_gap)
        circ = 2 * math.pi * self.wheel_r
        if circ > 0:
            self.wheel_angle_deg = (self.wheel_angle_deg + (self.speed_px / circ) * 360.0) % 360.0

        if self.is_jumping:
            self.vy += self.gravity
            self.car_y += self.vy
            if self.car_y >= self.car_ground_y:
                self.car_y = self.car_ground_y
                self.is_jumping = False
                self.vy = 0.0

        self.update()

    def resizeEvent(self, _event):
        self._recompute_geometry()
        self._set_car_ground_y_by_lane()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            self.lane_idx = max(0, self.lane_idx - 1)
            self._set_car_ground_y_by_lane()
            if not self.is_jumping:
                self.car_y = self.car_ground_y
        elif key == Qt.Key.Key_Down:
            self.lane_idx = min(2, self.lane_idx + 1)
            self._set_car_ground_y_by_lane()
            if not self.is_jumping:
                self.car_y = self.car_ground_y
        elif key == Qt.Key.Key_Space:
            if not self.is_jumping:
                self.is_jumping = True
                self.vy = -math.sqrt(2 * self.gravity * max(40, self.jump_power))
        elif key == Qt.Key.Key_Escape:
            # Regresar al menú si presiona ESC
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(0)

        self.setFocus()

    def paintEvent(self, _event):
        p = QPainter(self)
        # Cielo
        p.fillRect(self.rect(), QColor("#87CEEB"))
        # Carretera
        p.fillRect(0, self.road_y, self.width(), self.road_h, QColor("#3C3C3C"))
        # Rayas
        p.setBrush(QBrush(QColor("#EAEAEA")))
        p.setPen(Qt.PenStyle.NoPen)
        stripe_y = self.road_y + self.road_h // 2 - self.stripe_h // 2
        x = -self.road_scroll
        while x < self.width():
            p.fillRect(int(x), stripe_y, self.stripe_w, self.stripe_h, QColor("#EAEAEA"))
            x += self.stripe_w + self.stripe_gap
        # Carro
        self._draw_car(p)

    def _draw_car(self, p: QPainter):
        body_color = self.car_color_jump if self.is_jumping else self.car_color_on
        chasis_y = int(self.car_y)
        chasis_h = self.car_height
        chasis_rect = (self.car_x, chasis_y - chasis_h, self.car_width, chasis_h)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(body_color))
        p.fillRect(*chasis_rect, body_color)
        # Cabina
        cabin_w = int(self.car_width * 0.5)
        cabin_h = self.cabin_height
        cabin_x = self.car_x + int(self.car_width * 0.22)
        cabin_y = chasis_y - chasis_h - cabin_h + 4
        p.fillRect(cabin_x, cabin_y, cabin_w, cabin_h, body_color)
        # Ventana
        win_margin = 4
        p.fillRect(cabin_x + win_margin, cabin_y + win_margin,
                   cabin_w - 2 * win_margin, cabin_h - 2 * win_margin,
                   QColor("#B3E5FC"))
        # Parachoques y luces
        bumper_h = 6
        p.fillRect(self.car_x - 6, chasis_y - chasis_h + 10, 6, chasis_h - 20, QColor("#222"))
        p.fillRect(self.car_x + self.car_width, chasis_y - chasis_h + 12, 6, chasis_h - 24, QColor("#222"))
        p.fillRect(self.car_x + self.car_width + 6, chasis_y - chasis_h + 18, 6, 12, QColor("#FFD54F"))
        # Ruedas
        wheel_y = chasis_y - 6
        front_cx = self.car_x + int(self.car_width * 0.78)
        back_cx  = self.car_x + int(self.car_width * 0.22)
        self._draw_wheel(p, back_cx, wheel_y, self.wheel_r, self.wheel_angle_deg)
        self._draw_wheel(p, front_cx, wheel_y, self.wheel_r, self.wheel_angle_deg)
        # Sombra
        p.setBrush(QBrush(QColor(0, 0, 0, 40)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPoint(self.car_x + self.car_width // 2, wheel_y + 6),
                      self.car_width // 2 - 10, 8)

    def _draw_wheel(self, p: QPainter, cx: int, cy: int, r: int, angle_deg: float):
        p.setBrush(QBrush(QColor("#111111")))
        p.setPen(QPen(QColor("#000000")))
        p.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)
        rim_r = int(r * 0.65)
        p.setBrush(QBrush(QColor("#BDBDBD")))
        p.setPen(QPen(QColor("#555555")))
        p.drawEllipse(cx - rim_r, cy - rim_r, 2 * rim_r, 2 * rim_r)
        p.save()
        p.translate(cx, cy)
        p.rotate(angle_deg)
        p.setPen(QPen(QColor("#424242"), 2))
        for _ in range(4):
            p.drawLine(0, 0, rim_r, 0)
            p.rotate(90)
        p.restore()
