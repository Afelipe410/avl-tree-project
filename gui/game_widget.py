from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient, QFont
import math
import random

class GameWidget(QWidget):
    hit_signal = pyqtSignal()
    game_over_signal = pyqtSignal(str)

    def __init__(self, avl_tree, config: dict, parent=None):
        super().__init__(parent)
        self.avl_tree = avl_tree          
        self.config = config or {}
        self.speed = self.config.get("game", {}).get("speed", 6)
        self.world_offset = 0
        self.car_x = 0
        # Control de ejecucion: hasta que no se "start()" el juego no avanza
        self.running = False
        # Cola de spawns. Se genera a partir del árbol y cada obstáculo tendrá x_world > world_offset
        self._spawn_queue = []
        self._prepared_spawns = False
        # Timer de juego (no arrancar hasta que se pulse "Jugar")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

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
        self.goal_x = 10000 

        # AVL
        self.avl = None

        # Timer de juego (no arrancar hasta que se pulse "Jugar")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

    def sync_obstacles_from_avl(self, avl):
        """
        Sincroniza obstáculos visibles con el árbol AVL.
        Solo se muestran los que estén adelante del carro.
        """
        # Mantener referencia al árbol; forzar regeneración de spawns cuando el árbol cambie
        self.avl_tree = avl
        self._prepared_spawns = False
        # NO sobrescribimos self.obstacles aquí; las plantillas del árbol serán convertidas por _prepare_spawns
        # cuando corresponda (y GameWidget decidirá la posición x_world)

    def set_obstacles(self, obs: list):
        """Establece la lista de obstáculos visibles en el juego"""
        self.obstacles = [
            {**o, "spawn_x": o.get("spawn_x", o.get("x_world", 0))}
            for o in obs
        ]

    def update_game(self):
        # Avanzar sólo si el juego está en ejecución (presionaron "Jugar")
        if self.running:
            self.world_offset += self.speed
        self.road_line_offset = self.world_offset % 40

        # Preparar spawns desde el AVL si no se hizo todavía
        if not self._prepared_spawns and self.avl_tree and self.avl_tree.root:
            self._prepare_spawns_from_avl()
            self._prepared_spawns = True

        # Asegurar que los spawns (aunque estén fuera de pantalla) estén en self.obstacles
        if self._spawn_queue:
            existing_ids = {o.get("id") for o in self.obstacles}
            for ob in list(self._spawn_queue):
                if ob.get("id") not in existing_ids:
                    self.obstacles.append(ob)
                    existing_ids.add(ob.get("id"))

        # Eliminar obstáculos que ya pasaron
        car_world_x = self.world_offset + self.car_x
        if self.avl_tree:
            self.avl_tree.remove_passed_obstacles(car_world_x)

        # Sólo tomar obstáculos directamente desde el AVL si NO estamos usando la cola de spawns.
        if not self._spawn_queue and self.avl_tree:
            # to_obstacles() debe devolver plantillas sin x_world (el juego las posicionará)
            self.obstacles = self.avl_tree.to_obstacles()

        
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
                
                # calcular rect para obstáculo en pantalla (con x_world moviéndose por world_offset)
                ob_screen_x = ob["x_world"] - self.world_offset
                ob_rect = (
                    ob_screen_x,
                    self.lane_y[ob.get("lane_idx", 1)] - ob.get("height", 32),
                    ob.get("width", 32),
                    ob.get("height", 32),
                )
                if self.check_collision(car_rect, ob_rect):
                    self.hit_signal.emit()
                    self.lives -= 1
                    try:
                        # eliminar obstáculo golpeado
                        self.obstacles.remove(ob)
                    except ValueError:
                        pass
 
        # Eliminar obstáculos ya pasados
        self.obstacles = [
            ob for ob in self.obstacles
            if ob["x_world"] - self.world_offset + ob["width"] > self.car_x
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
            ob_screen_x = ob["x_world"] - self.world_offset
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
            p.drawRect(goal_screen_x, 80, 20, 320)
            p.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            p.setPen(QColor("#FFD700"))
            p.drawText(goal_screen_x - 20, 55, 60, 20, Qt.AlignmentFlag.AlignCenter, "META")

    def _draw_life_bar(self, p: QPainter):
        max_lives = 10
        bar_width = 500
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

    def _prepare_spawns_from_avl(self):
        """Genera una cola de obstáculos que aparecerán desde el borde derecho en orden aleatorio.
        Usa las plantillas (dicts) del árbol y les asigna x_world > world_offset para que entren desde la derecha."""
        if not self.avl_tree:
            return
        templates = self.avl_tree.to_obstacles()
        if not templates:
            return
        templates_copy = [t.copy() for t in templates]
        random.shuffle(templates_copy)
        base_x = self.world_offset + max(self.width(), 800) + 100
        spacing_min, spacing_extra = 160, 120
        x = base_x
        for t in templates_copy:
            ob = t.copy()
            ob["x_world"] = x + random.randint(0, spacing_extra)
            if "lane_idx" not in ob:
                ob["lane_idx"] = random.randint(0, len(self.lane_y)-1)
            if "id" not in ob:
                ob["id"] = random.randint(100000, 999999)
            ob.setdefault("width", 32)
            ob.setdefault("height", 32)
            self._spawn_queue.append(ob)
            x += spacing_min + random.randint(0, spacing_extra)
        for ob in self._spawn_queue:
            ob["x_world"] += random.randint(0, 60)
 
    def register_new_obstacle(self, template: dict):
        """Registrar un nuevo obstáculo: lo agrega como spawn a la derecha (no se moverá si !running)."""
        ob = template.copy()
        ob.setdefault("width", 32)
        ob.setdefault("height", 32)
        if "id" not in ob:
            ob["id"] = random.randint(100000, 999999)
        # Ubicar a la derecha del viewport actual para que 'entre' desde la derecha
        ob["x_world"] = self.world_offset + max(self.width(), 800) + 150 + random.randint(0, 300)
        if "lane_idx" not in ob:
            ob["lane_idx"] = random.randint(0, len(self.lane_y)-1)
        self._spawn_queue.append(ob)
        # Añadir también a self.obstacles para feedback visual inmediato (no se moverá hasta start)
        self.obstacles.append(ob)
 
    def start(self):
        """Iniciar la simulación: world_offset empezará a avanzar."""
        # preparar spawns si aún no se hizo y empezar timer
        if not self._prepared_spawns and self.avl_tree and self.avl_tree.root:
            self._prepare_spawns_from_avl()
            self._prepared_spawns = True
        self.running = True
        if not self.timer.isActive():
            self.timer.start(30)