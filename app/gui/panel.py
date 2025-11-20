"""
panel.py

Janela/painel para exibir:
- texto original (OCR)
- texto traduzido (Argos)

Pode ser usada sozinha (teste) ou integrada ao app principal.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)


class TranslationPanel(QWidget):
    """
    Painel simples com:
      - campo de texto original (somente leitura)
      - campo de texto traduzido (somente leitura)
      - botões de copiar/limpar
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Floating Translate - Painel")
        self.resize(500, 400)

        # Widgets
        self.label_original = QLabel("Texto original (OCR):")
        self.text_original = QTextEdit()
        self.text_original.setReadOnly(True)

        self.label_translated = QLabel("Texto traduzido:")
        self.text_translated = QTextEdit()
        self.text_translated.setReadOnly(True)

        self.btn_copy = QPushButton("Copiar tradução")
        self.btn_clear = QPushButton("Limpar")

        # Layout de botões
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_clear)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label_original)
        main_layout.addWidget(self.text_original, 1)
        main_layout.addWidget(self.label_translated)
        main_layout.addWidget(self.text_translated, 1)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Conexões
        self.btn_copy.clicked.connect(self.copy_translation_to_clipboard)
        self.btn_clear.clicked.connect(self.clear_texts)

    # ------------------------------------------------------------------
    # Métodos públicos para o app usar
    # ------------------------------------------------------------------
    def set_texts(self, original: str, translated: str) -> None:
        """
        Atualiza os campos com novo texto.
        """
        self.text_original.setPlainText(original or "")
        self.text_translated.setPlainText(translated or "")

    def append_texts(self, original: str, translated: str) -> None:
        """
        Acrescenta nova captura ao final (com separador).
        """
        if original:
            self.text_original.append(original)
            self.text_original.append("-" * 40)
        if translated:
            self.text_translated.append(translated)
            self.text_translated.append("-" * 40)

    # ------------------------------------------------------------------
    # Slots internos
    # ------------------------------------------------------------------
    def copy_translation_to_clipboard(self) -> None:
        """
        Copia o texto traduzido para a área de transferência.
        """
        text = self.text_translated.toPlainText()
        if not text:
            return
        clipboard = self.window().windowHandle().screen().context().clipboard() \
            if hasattr(self.window(), "windowHandle") else None

        # Maneira mais simples (funciona na maioria dos casos):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(text)

    def clear_texts(self) -> None:
        """
        Limpa os dois campos de texto.
        """
        self.text_original.clear()
        self.text_translated.clear()