from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QCursor


class ExitButton(QWidget):
    """
    Botão fixo de sair, centralizado na parte de baixo da tela.
    Emite quit_requested quando clicado.
    """

    quit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Fundo totalmente transparente
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
        
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )

        self.setWindowTitle("Sair Floating Translate")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.button = QPushButton("Sair")
        self.button.setFixedSize(80, 28)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #dc3247;
                color: white;
                border-radius: 6px;
                padding: 2px 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71f34;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.quit_requested.emit)

        self.adjustSize()
        self.move_to_bottom_center()

    def move_to_bottom_center(self) -> None:
        screen = self.screen().geometry()
        margin_bottom = 20
        x = screen.center().x() - self.width() // 2
        y = screen.bottom() - self.height() - margin_bottom
        self.move(x, y)
