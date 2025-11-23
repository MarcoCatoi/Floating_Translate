# app/app.py
from __future__ import annotations

import sys
from typing import Tuple

from PySide6.QtWidgets import QApplication

from app.gui.overlay import Overlay
from app.gui.panel import TranslationPanel
from app.core.capture import grab_region
from app.core.preprocess import enhance_for_ocr
from app.core.ocr import image_to_text
from app.core.translate import translate_en_to_pt


print(">>> app.app foi importado")


class FloatingTranslateApp:
    def __init__(self) -> None:
        print("Init FloatingTranslateApp...")

        self.panel = TranslationPanel()
        print("Panel criado")
        self.panel.show()

        self.overlay = Overlay()
        print("Overlay criado")
        self.overlay.selection_made.connect(self.on_selection_made)
        print("Sinal conectado")

        self.show_overlay()
        print("Overlay mostrado")

    def show_overlay(self) -> None:
        self.overlay.show_overlay()

    def on_selection_made(self, bbox: Tuple[int, int, int, int]) -> None:
        print("BBox recebido:", bbox)
        try:
            img = grab_region(bbox)
            img_proc = enhance_for_ocr(img, scale=1.8)
            text_ocr = image_to_text(img_proc, lang="eng+por")
            text_translated = translate_en_to_pt(text_ocr)
            self.panel.append_texts(text_ocr, text_translated)
        except Exception as exc:
            self.panel.append_texts("", f"Erro ao processar: {exc!r}")


def main() -> None:
    print("Iniciando QApplication...")
    app = QApplication(sys.argv)

    print("Criando FloatingTranslateApp...")
    ft_app = FloatingTranslateApp()
    print("FloatingTranslateApp criado:", ft_app)

    print("Entrando no loop Qt...")
    rc = app.exec()
    print("Loop Qt terminou com código:", rc)
    sys.exit(rc)


if __name__ == "__main__":
    print("Chamando main() dentro de app.app")
    main()
