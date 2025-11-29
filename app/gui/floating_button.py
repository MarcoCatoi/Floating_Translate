from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QCursor


class FloatingButton(QWidget):
    """
    Botão flutuante sempre visível e arrastável.
    Emite clicked_for_selection quando o usuário clica no botão azul.
    """

    clicked_for_selection = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Fundo totalmente transparente
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
        
        # Janela pequena, sem borda, sempre no topo
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )

        self.setWindowTitle("Floating Translate")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Botão principal
        self.button = QPushButton("Traduzir área")
        self.button.setFixedSize(120, 32)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #2d89ef;
                color: white;
                border-radius: 6px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1b5fbd;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.clicked_for_selection.emit)

        # posição inicial (canto inferior direito)
        self.adjustSize()
        self.move_to_bottom_right()

        # suporte a arrastar
        self._drag_pos = None
        # redireciona os eventos do widget para o botão
        self.button.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        # Se o evento é no botão principal, tratamos como se fosse no widget
        if obj is self.button:
            if event.type() == event.Type.MouseButtonPress:
                self.mousePressEvent(event)
                return True
            elif event.type() == event.Type.MouseMove:
                self.mouseMoveEvent(event)
                return True
            elif event.type() == event.Type.MouseButtonRelease:
                self.mouseReleaseEvent(event)
                return True
        return super().eventFilter(obj, event)

    def move_to_bottom_right(self) -> None:
        screen = self.screen().geometry()
        margin = 20
        x = screen.right() - self.width() - margin
        y = screen.bottom() - self.height() - margin
        self.move(x, y)

    # --- arrastar janela com o mouse ---
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self._drag_pos is not None and event.button() == Qt.LeftButton:
            self._drag_pos = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
