from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QCursor, QIcon


class FloatingButton(QWidget):
    clicked_for_selection = Signal()

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
        # opcional: ícone
        # self.button.setIcon(QIcon("app/resources/translate_icon.png"))
        # self.button.setIconSize(self.button.size() * 0.6)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #2d89ef;
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

        # não conecta clicked direto; vai ser emitido manualmente
        self.button.installEventFilter(self)

        self.adjustSize()
        self.move_to_bottom_right()

    def move_to_bottom_right(self) -> None:
        screen = self.screen().geometry()
        margin = 20
        x = screen.right() - self.width() - margin
        y = screen.bottom() - self.height() - margin
        self.move(x, y)

    def eventFilter(self, obj, event):
        if obj is self.button:
            t = event.type()
            if t == event.Type.MouseButtonPress and event.button() == Qt.LeftButton:
                self._press_pos = event.globalPosition().toPoint()
                self._dragging = False
                return False  # deixa o botão ver o press (para visual)

            elif t == event.Type.MouseMove and event.buttons() & Qt.LeftButton and self._press_pos is not None:
                current = event.globalPosition().toPoint()
                if not self._dragging:
                    # começa a arrastar só depois de mover um pouco
                    if (current - self._press_pos).manhattanLength() > 5:
                        self._dragging = True
                if self._dragging:
                    offset = current - self._press_pos
                    self.move(self.pos() + offset)
                    self._press_pos = current
                    return True  # consumimos o move
                return False

            elif t == event.Type.MouseButtonRelease and event.button() == Qt.LeftButton:
                # se NÃO estava arrastando, tratamos como clique "real"
                if not self._dragging:
                    self.clicked_for_selection.emit()
                self._press_pos = None
                self._dragging = False
                return True  # já tratamos release; evita clicked interno

        return super().eventFilter(obj, event)
