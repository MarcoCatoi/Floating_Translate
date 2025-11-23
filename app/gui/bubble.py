from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PySide6.QtGui import QPalette, QColor


class TranslationBubble(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Janela pequena, sem borda, sempre no topo
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )

        # Fundo preto semitransparente
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setWindowOpacity(0.35)

        # --- barra superior com "Tradução" + X ---
        title = QLabel("Tradução")
        title.setStyleSheet("color: white; font-weight: bold;")

        btn_close = QPushButton("×")
        btn_close.setFixedSize(18, 18)
        btn_close.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 50);
                border-radius: 9px;
            }
        """)
        btn_close.clicked.connect(self.close)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(title)
        top_layout.addStretch(1)
        top_layout.addWidget(btn_close)

        # --- área de texto apenas de tradução ---
        self.text_translated = QTextEdit()
        self.text_translated.setReadOnly(True)
        self.text_translated.setStyleSheet("""
            QTextEdit {
                background: transparent;
                color: white;
                border: none;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.text_translated)
        self.setLayout(main_layout)

        self.resize(420, 160)
        self.move_to_bottom_right()
        self._drag_pos = None

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

    def move_to_bottom_right(self) -> None:
        screen = self.screen().geometry()
        margin = 40
        x = screen.right() - self.width() - margin
        y = screen.bottom() - self.height() - margin
        self.move(x, y)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)
            
    # API pública usada pelo app
    def set_translation(self, translated: str) -> None:
        self.text_translated.setPlainText(translated or "")

    def append_translation(self, translated: str) -> None:
        if translated:
            self.text_translated.append(translated)
            self.text_translated.append("-" * 30)

    # Atalho: ESC fecha a bubble
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
