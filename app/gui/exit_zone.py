from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont


class ExitZone(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self._radius = 50  # raio do círculo
        size = self._radius * 2
        self.resize(size, size)
        self.move_to_bottom_center()
        self.hide()

    def move_to_bottom_center(self) -> None:
        screen = self.screen().geometry()
        x = screen.center().x() - self.width() // 2
        y = screen.bottom() - self.height() - 40  # sobe um pouco
        self.move(x, y)

    def center_point(self):
        g = self.geometry()
        return g.center()

    def radius(self) -> int:
        return self._radius

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # círculo preenchido, sem borda
        fill_color = QColor(255, 0, 0, 90)  # vermelho translúcido
        painter.setPen(Qt.NoPen)            # sem borda
        painter.setBrush(fill_color)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # desenhar o "X" no centro
        painter.setPen(QColor(255, 255, 255, 220))  # X branco
        font = QFont()
        font.setBold(True)
        font.setPointSize(22)  # ajusta se o círculo for maior/menor
        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            "X"
        )

