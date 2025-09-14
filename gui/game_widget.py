from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient, QFont
import math

class GameWidget(QWidget):
    hit_signal = pyqtSignal()
    game_over_signal = pyqtSignal(str)

    def __init__(self, config: dict):
        super().__init__()
        self.config = config or {}
        self.speed = self.config.get("game", {}).get("speed", 6)
        self.world_offset = 0

        # Carro
        self.car_x = 80
        self.car_lane = 1
        self.lane_y = [120, 200, 280, 360]
        self.car_w, self.car_h = 100, 40
        self.car_color = QColor("#AAA0A0")
        self.car_color_jump = QColor("#107EB9")

        # Ruedas
        self.wheel_r = 13
        self.wheel_angle = 0.0

        # Salto
        self.jumping = False
        self.jump_height = 70
        self.jump_progress = 0
        self.jump_max = 35

        # Obstáculos
        self.obstacles = []
        self.lives = 10

        # Animación de líneas de carretera
        self.road_line_offset = 0

        # Meta
        self.goal_x = 10000  # distancia hasta la meta

        # AVL
        self.avl = None

        # Timer de juego
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

    def sync_obstacles_from_avl(self, avl):
        """
        Sincroniza obstáculos visibles con el árbol AVL.
        Solo se muestran los que estén adelante del carro.
        """
        self.avl = avl
        if not avl or not avl.root:
            return

        obstacles_for_game = []
        nodes = avl.inorder()  # recorrido en orden ascendente por X
        for node in nodes:
            x_world = node.key
            if x_world >= self.world_offset:
                ob = node.obstacle.copy()
                ob["spawn_x"] = x_world
                obstacles_for_game.append(ob)

        self.set_obstacles(obstacles_for_game)

    def set_obstacles(self, obs: list):
        """Establece la lista de obstáculos visibles en el juego"""
        self.obstacles = [
            {**o, "spawn_x": o.get("spawn_x", o.get("x_world", 0))}
            for o in obs
        ]

    def update_game(self):
        # Animación carretera
        self.world_offset += self.speed
        self.road_line_offset = self.world_offset % 40

        # Salto
        if self.jumping:
            self.jump_progress += 1
            if self.jump_progress >= self.jump_max:
                self.jumping = False
                self.jump_progress = 0

        # Rotación ruedas
        circ = 2 * math.pi * self.wheel_r
        if circ > 0:
            self.wheel_angle = (self.wheel_angle + (self.speed / circ) * 360) % 360

        # Colisiones
        if not self.jumping:
            car_rect = (self.car_x, self.car_y() - self.car_h,
                        self.car_w, self.car_h)
            for ob in list(self.obstacles):
                ob_screen_x = ob["spawn_x"] - self.world_offset
                ob_rect = (ob_screen_x, self.lane_y[ob["lane_idx"]] - ob["height"],
                           ob["width"], ob["height"])
                if self.check_collision(car_rect, ob_rect):
                    self.lives -= 1
                    self.hit_signal.emit()
                    self.obstacles.remove(ob)
                    if self.avl:
                        self.avl.delete(ob["x_world"])
                    break

        # Eliminar obstáculos ya pasados
        self.obstacles = [
            ob for ob in self.obstacles
            if ob["spawn_x"] - self.world_offset + ob["width"] > self.car_x
        ]

        # Revisar fin de juego
        if self.lives <= 0:
            self.timer.stop()
            self.game_over_signal.emit("Que mal, perdiste! No te quedan vidas.")
        elif self.world_offset >= self.goal_x:
            self.timer.stop()
            self.game_over_signal.emit("Felicidades, ganaste! Llegaste a la meta.")

        self.update()

    def car_y(self):
        """Posición Y del carro con offset de salto"""
        base = self.lane_y[self.car_lane]
        if not self.jumping:
            return base
        # parabólica simple
        peak = self.jump_max // 2
        d = self.jump_progress - peak
        return base - int(self.jump_height - (d * d * self.jump_height) / (peak * peak))

    def check_collision(self, r1, r2):
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return not (x1+w1 < x2 or x1 > x2+w2 or y1+h1 < y2 or y1 > y2+h2)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Up and self.car_lane > 0:
            self.car_lane -= 1
        elif e.key() == Qt.Key.Key_Down and self.car_lane < len(self.lane_y)-1:
            self.car_lane += 1
        elif e.key() == Qt.Key.Key_Space and not self.jumping:
            self.jumping = True
            self.jump_progress = 0
        elif e.key() == Qt.Key.Key_Escape:
            if self.parent() and hasattr(self.parent(), "show_menu"):
                self.parent().show_menu()

    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo césped
        p.fillRect(self.rect(), QColor("#2D5016"))
        # Carretera
        road_gradient = QLinearGradient(0, 0, 0, self.height())
        road_gradient.setColorAt(0, QColor("#404040"))
        road_gradient.setColorAt(1, QColor("#2A2A2A"))
        p.fillRect(0, 80, self.width(), 320, QBrush(road_gradient))

        self._draw_road_lines(p)
        self._draw_car(p)
        self._draw_obstacles(p)
        self._draw_goal(p)
        self._draw_life_bar(p)

    def _draw_road_lines(self, p: QPainter):
        p.setPen(QPen(QColor("white"), 4))
        p.drawLine(0, 80, self.width(), 80)
        p.drawLine(0, 400, self.width(), 400)

        p.setPen(QPen(QColor("white"), 3))
        for i in range(len(self.lane_y)-1):
            y = (self.lane_y[i] + self.lane_y[i+1]) // 2
            self._draw_dashed_line(p, y)
        
        center_y = (self.lane_y[1] + self.lane_y[2]) // 2
        p.setPen(QPen(QColor("#FFD700"), 4))
        self._draw_dashed_line(p, center_y, is_center=True)

    def _draw_dashed_line(self, p: QPainter, y: int, is_center=False):
        dash_length = 30 if is_center else 25
        gap_length = 15 if is_center else 12
        x = -self.road_line_offset
        while x < self.width():
            if x + dash_length > 0:
                p.drawLine(max(0, x), y, min(self.width(), x + dash_length), y)
            x += dash_length + gap_length

    def _draw_car(self, p: QPainter):
        y = self.car_y()
        color = self.car_color_jump if self.jumping else self.car_color
        # Sombra
        if not self.jumping or self.jump_progress < 8:
            shadow_y = self.lane_y[self.car_lane] + 3
            p.setBrush(QBrush(QColor(0, 0, 0, 80)))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(self.car_x + 5, shadow_y - 15, self.car_w - 10, 20)
        # Chasis
        gradient = QLinearGradient(0, y - self.car_h, 0, y)
        gradient.setColorAt(0, color.lighter(140))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1, color.darker(120))
        p.setBrush(QBrush(gradient))
        p.setPen(QPen(color.darker(150), 2))
        p.drawRoundedRect(self.car_x, y - self.car_h, self.car_w, self.car_h, 6, 6)
        # Cabina y parabrisas
        cabin_w, cabin_h = 50, 25
        cabin_x = self.car_x + 20
        cabin_y = y - self.car_h - cabin_h + 5
        p.setBrush(QBrush(color.darker(130)))
        p.setPen(QPen(color.darker(160), 1))
        p.drawRoundedRect(cabin_x, cabin_y, cabin_w, cabin_h, 4, 4)
        p.setBrush(QBrush(QColor("#87CEEB")))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(cabin_x + 5, cabin_y + 3, cabin_w - 10, cabin_h - 6, 3, 3)
        # Ventanas laterales
        p.setBrush(QBrush(QColor("#87CEEB").darker(110)))
        p.drawRect(cabin_x - 6, cabin_y + 8, 10, 15)
        p.drawRect(cabin_x + cabin_w - 4, cabin_y + 8, 10, 15)
        # Luces y ruedas
        p.setBrush(QBrush(QColor("#606060")))
        p.drawRect(self.car_x + self.car_w, y - self.car_h + 8, 6, 24)
        p.setBrush(QBrush(QColor("#FFFACD")))
        p.setPen(QPen(QColor("#DAA520"), 1))
        p.drawEllipse(self.car_x + self.car_w + 2, y - self.car_h + 10, 8, 8)
        p.drawEllipse(self.car_x + self.car_w + 2, y - self.car_h + 22, 8, 8)
        p.setBrush(QBrush(QColor("#DC143C")))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(self.car_x - 3, y - self.car_h + 12, 6, 6)
        p.drawEllipse(self.car_x - 3, y - self.car_h + 22, 6, 6)
        # Ruedas
        self._draw_wheel(p, self.car_x + 20, y - 6)
        self._draw_wheel(p, self.car_x + self.car_w - 20, y - 6)

    def _draw_wheel(self, p: QPainter, cx: int, cy: int):
        r = self.wheel_r
        p.setBrush(QBrush(QColor(0, 0, 0, 100)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - r + 2, cy - r + 2, 2*r, 2*r)
        p.setBrush(QBrush(QColor("#1C1C1C")))
        p.setPen(QPen(QColor("black"), 2))
        p.drawEllipse(cx - r, cy - r, 2*r, 2*r)
        rim_r = int(r * 0.7)
        rim_gradient = QLinearGradient(cx - rim_r, cy - rim_r, cx + rim_r, cy + rim_r)
        rim_gradient.setColorAt(0, QColor("#C0C0C0"))
        rim_gradient.setColorAt(0.5, QColor("#A0A0A0"))
        rim_gradient.setColorAt(1, QColor("#808080"))
        p.setBrush(QBrush(rim_gradient))
        p.setPen(QPen(QColor("#606060"), 1))
        p.drawEllipse(cx - rim_r, cy - rim_r, 2*rim_r, 2*rim_r)
        center_r = int(r * 0.3)
        p.setBrush(QBrush(QColor("#404040")))
        p.drawEllipse(cx - center_r, cy - center_r, 2*center_r, 2*center_r)
        p.save()
        p.translate(cx, cy)
        p.rotate(self.wheel_angle)
        p.setPen(QPen(QColor("#707070"), 2))
        for _ in range(4):
            p.drawLine(0, 0, rim_r - 3, 0)
            p.rotate(90)
        p.restore()

    def _draw_obstacles(self, p: QPainter):
        for ob in self.obstacles:
            ob_screen_x = ob["spawn_x"] - self.world_offset
            y = self.lane_y[ob["lane_idx"]] - ob["height"]
            w = ob["width"]
            h = ob["height"]
            p.setBrush(QColor("#B91C1C"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRect(ob_screen_x, y, w, h)
            # Sombra
            p.setBrush(QBrush(QColor(0, 0, 0, 120)))
            p.drawEllipse(ob_screen_x + 2, self.lane_y[ob["lane_idx"]] + 2, w, h//2)
            # Gradiente
            grad = QLinearGradient(0, y, 0, self.lane_y[ob["lane_idx"]])
            grad.setColorAt(0, QColor("#FF4444"))
            grad.setColorAt(1, QColor("#CC0000"))
            p.setBrush(QBrush(grad))
            p.setPen(QPen(QColor("#AA0000"), 2))
            p.drawRoundedRect(ob_screen_x, y, w, h, 4, 4)
            # Línea decorativa
            p.setPen(QPen(QColor("#FFFF00"), 2))
            p.drawLine(ob_screen_x + 3, y + h//2, ob_screen_x + w - 3, y + h//2)

    def _draw_goal(self, p: QPainter):
        goal_screen_x = self.goal_x - self.world_offset
        if -50 < goal_screen_x < self.width():
            p.setBrush(QBrush(QColor("#FFD700")))
            p.setPen(QPen(QColor("#DAA520"), 2))
            p.drawRect(goal_screen_x, 80, 10, 320)
            p.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            p.setPen(QColor("#FFD700"))
            p.drawText(goal_screen_x - 20, 70, 50, 20, Qt.AlignmentFlag.AlignCenter, "META")

    def _draw_life_bar(self, p: QPainter):
        max_lives = 10
        bar_width = 200
        bar_height = 18
        bar_x = (self.width() - bar_width) // 2
        bar_y = 12
        p.setBrush(QBrush(QColor("#444")))
        p.setPen(QPen(QColor("#222"), 2))
        p.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 8, 8)
        lives_ratio = max(0, min(self.lives / max_lives, 1))
        life_color = QColor.fromRgbF(1 - lives_ratio, lives_ratio, 0)
        p.setBrush(QBrush(life_color))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(bar_x + 2, bar_y + 2, int((bar_width - 4) * lives_ratio), bar_height - 4, 6, 6)