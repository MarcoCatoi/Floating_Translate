from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtGui import QCursor


class FloatingButton(QWidget):
    """
    Botão flutuante sempre visível.
    Emite:
      - clicked_for_selection: clique normal no botão azul
      - quit_requested: quando o usuário solta o mouse sobre a área vermelha "Sair"
    """

    clicked_for_selection = Signal()
    quit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Janela pequena, sem borda, sempre no topo
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )

        self.setWindowTitle("Floating Translate")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # --- área de encerramento (quadrado vermelho à esquerda) ---
        self.exit_label = QLabel("X")
        self.exit_label.setFixedSize(22, 22)
        self.exit_label.setAlignment(Qt.AlignCenter)
        self.exit_label.setStyleSheet("""
            QLabel {
                background-color: rgba(220, 50, 47, 200);
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
        """)

        # --- botão principal ---
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
        layout.setSpacing(6)
        layout.addWidget(self.exit_label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.clicked_for_selection.emit)

        # tamanho + posição inicial (canto inferior direito)
        self.adjustSize()
        self.move_to_bottom_right()

        # suporte a arrastar a janela
        self._drag_pos = None

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
            # posição do mouse relativa ao widget
            local_pos = event.position().toPoint()

            # se soltar em cima da label vermelha -> pedir encerramento
            if self.exit_label.geometry().contains(local_pos):
                self.quit_requested.emit()

            self._drag_pos = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
