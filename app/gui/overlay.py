"""
overlay.py

Janela fullscreen transparente que permite selecionar uma área
retangular na tela com o mouse. Ao soltar o botão, emite um
sinal com o bbox (x1, y1, x2, y2) em coordenadas de tela.

Uso típico:
    overlay = Overlay()
    overlay.selection_made.connect(callback_que_recebe_bbox)
    overlay.show_overlay()

Depois, no callback, você chama:
    img = grab_region(bbox)
    img_proc = enhance_for_ocr(img)
    text = image_to_text(img_proc, lang="eng+por")
"""

from __future__ import annotations

from typing import Tuple

from PySide6.QtGui import QPalette, QColor, QCursor
from PySide6.QtCore import Qt, QRect, QPoint, Signal
from PySide6.QtWidgets import QWidget, QRubberBand


class Overlay(QWidget):
    """
    Janela transparente em tela cheia para seleção de área.

    - Clique e arraste com o botão esquerdo para desenhar a seleção.
    - Ao soltar o botão, emite selection_made(bbox) e se esconde.
    """

    selection_made = Signal(tuple)  # (x1, y1, x2, y2)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._origin = None
        self._rubber_band = None

        # Janela sem borda, fullscreen e sempre no topo
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool  # evita aparecer na barra de tarefas em alguns casos
        )
        
        # FUNDO VISÍVEL (teste)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Aplicando opacidade
        self.setWindowOpacity(0.35)
              
        # Cursor em cruz para indicar seleção
        self.setCursor(QCursor(Qt.CrossCursor))
        # Captura o mouse em toda a tela
        self.setMouseTracking(True)

        # Vai cobrir a tela inteira quando show_overlay() for chamado
        self.hide()

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------
    def show_overlay(self) -> None:
        self._origin = None
        if self._rubber_band is not None:
            self._rubber_band.hide()

        self.showFullScreen()
        self.activateWindow()
        self.raise_()
    # ------------------------------------------------------------------
    # Eventos de mouse
    # ------------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.LeftButton:
            return

        self._origin = event.globalPosition().toPoint()

        if self._rubber_band is None:
            self._rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        local_origin = self.mapFromGlobal(self._origin)
        self._rubber_band.setGeometry(QRect(local_origin, local_origin))
        self._rubber_band.show()

    def mouseMoveEvent(self, event) -> None:
        if self._origin is None or self._rubber_band is None:
            return

        current_pos = event.globalPosition().toPoint()
        rect = QRect(self._origin, current_pos).normalized()
        # Converter para coordenadas relativas ao widget
        top_left = self.mapFromGlobal(rect.topLeft())
        bottom_right = self.mapFromGlobal(rect.bottomRight())
        self._rubber_band.setGeometry(QRect(top_left, bottom_right))

    def mouseReleaseEvent(self, event) -> None:
        if event.button() != Qt.LeftButton:
            return

        if self._origin is None or self._rubber_band is None:
            self.hide()
            return
        dpi_scale = 1.25
        end_pos = event.globalPosition().toPoint()
        rect = QRect(self._origin, end_pos).normalized()

        x1 = rect.left() * dpi_scale
        y1 = rect.top() * dpi_scale
        x2 = rect.right() * dpi_scale
        y2 = rect.bottom() * dpi_scale

        self._rubber_band.hide()
        self.hide()

        # Emite o bbox em coordenadas de tela
        self.selection_made.emit((x1, y1, x2, y2))


# Pequeno teste manual
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from app.core.capture import grab_region

    def on_selection(bbox: Tuple[int, int, int, int]) -> None:
        print("Seleção:", bbox)
        img = grab_region(bbox)
        img.show()
        QApplication.instance().quit()

    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.selection_made.connect(on_selection)
    overlay.show_overlay()
    sys.exit(app.exec())
