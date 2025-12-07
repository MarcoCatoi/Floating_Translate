from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QCursor, QIcon

from app.gui.exit_zone import ExitZone


class FloatingButton(QWidget):
    clicked_for_selection = Signal()
    quit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.button = QPushButton()
        self.button.setFixedSize(48, 48)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.button.setIcon(QIcon("app/resources/translate_icon.png"))
        self.button.setIconSize(self.button.size())
        self.button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 24px;
                border: 2px solid white;
            }
            QPushButton:hover {
                background-color: #1b5fbd;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)

        # estado para diferenciar clique x arraste
        self._press_pos: QPoint | None = None
        self._dragging = False
        self.exit_zone = ExitZone()
        self.exit_zone.hide()
        # não conecta clicked direto; vai ser emitido manualmente
        self.button.installEventFilter(self)

        self.adjustSize()
        self.move_to_top_right()

    def move_to_top_right(self) -> None:
        screen = self.screen().geometry()
        margin = 20
        x = screen.right() - self.width() - margin
        y = screen.top() + margin
        self.move(x, y)
 
    def _init_hotspot(self) -> None:
        """
        Define a posição do hotspot. Aqui: centro inferior da tela.
        """
        screen = self.screen().geometry()
        cx = screen.center().x()
        cy = screen.bottom() - 80  # sobe um pouco do fundo
        self._hotspot_center = QPoint(cx, cy)

    def _is_over_hotspot(self) -> bool:
        """
        Verifica se o centro do botão está dentro do círculo do hotspot.
        """
        # centro do botão em coordenadas de tela
        btn_geom = self.geometry()          # posição global do widget
        cx_btn = btn_geom.center().x()
        cy_btn = btn_geom.center().y()

        dx = cx_btn - self._hotspot_center.x()
        dy = cy_btn - self._hotspot_center.y()
        dist2 = dx * dx + dy * dy
        return dist2 <= self._hotspot_radius * self._hotspot_radius

    def eventFilter(self, obj, event):
        if obj is self.button:
            t = event.type()

            if t == event.Type.MouseButtonPress and event.button() == Qt.LeftButton:
                self._press_pos = event.globalPosition().toPoint()
                self._dragging = False
                # só posiciona, mas não mostra ainda
                self.exit_zone.move_to_bottom_center()
                return False

            elif t == event.Type.MouseMove and event.buttons() & Qt.LeftButton and self._press_pos is not None:
                current = event.globalPosition().toPoint()
                if not self._dragging:
                    if (current - self._press_pos).manhattanLength() > 5:
                        self._dragging = True

                if self._dragging:
                    # move o botão
                    offset = current - self._press_pos
                    self.move(self.pos() + offset)
                    self._press_pos = current

                    # calcula colisão com o centro da exit_zone
                    btn_geom = self.geometry()          # global
                    cx_btn = btn_geom.center().x()
                    cy_btn = btn_geom.center().y()

                    center = self.exit_zone.center_point()
                    r = self.exit_zone.radius()

                    dx = cx_btn - center.x()
                    dy = cy_btn - center.y()
                    dist2 = dx * dx + dy * dy

                    if dist2 <= r * r:
                        # entrou no raio: mostra a zona
                        if not self.exit_zone.isVisible():
                            self.exit_zone.show()
                    else:
                        # saiu do raio: esconde
                        if self.exit_zone.isVisible():
                            self.exit_zone.hide()

                    return True  # consumimos o move

                return False

            elif t == event.Type.MouseButtonRelease and event.button() == Qt.LeftButton:
                if self._dragging:
                    # ao soltar, se ainda estiver dentro da zona -> sair
                    btn_geom = self.geometry()
                    cx_btn = btn_geom.center().x()
                    cy_btn = btn_geom.center().y()

                    center = self.exit_zone.center_point()
                    r = self.exit_zone.radius()

                    dx = cx_btn - center.x()
                    dy = cy_btn - center.y()
                    dist2 = dx * dx + dy * dy

                    if dist2 <= r * r:
                        self.quit_requested.emit()
                else:
                    # clique normal, sem arraste
                    self.clicked_for_selection.emit()

                self._press_pos = None
                self._dragging = False
                self.exit_zone.hide()   # sempre some ao soltar
                return True

        return super().eventFilter(obj, event)

