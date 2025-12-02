# app/app.py
from __future__ import annotations

import sys
from typing import Tuple

from PySide6.QtWidgets import QApplication

from app.gui.overlay import Overlay
from app.gui.bubble import TranslationBubble
from app.gui.floating_button import FloatingButton
#from app.gui.exit_button import ExitButton
from app.core.capture import grab_region
from app.core.preprocess import enhance_for_ocr
from app.core.ocr import image_to_text
from app.core.translate import translate_en_to_pt


print(">>> app.app foi importado")


class FloatingTranslateApp:
    def __init__(self) -> None:
        print("Init FloatingTranslateApp...")

        self.panel = TranslationBubble()
        print("Panel criado")
        self.panel.show()

        self.overlay = Overlay()
        print("Overlay criado")
        self.overlay.selection_made.connect(self.on_selection_made)
        print("Sinal conectado")

        self.floating_button = FloatingButton()
        self.floating_button.clicked_for_selection.connect(self.show_overlay)
        self.floating_button.quit_requested.connect(self.quit)
        self.floating_button.show()

        #self.exit_button = ExitButton()
        #self.exit_button.quit_requested.connect(self.quit)
        #self.exit_button.show()

    def quit(self) -> None:
        self.overlay.close()
        self.panel.close()
        self.floating_button.close()
        QApplication.instance().quit()
        
    def show_overlay(self) -> None:
        self.overlay.show_overlay()

    def on_selection_made(self, bbox: Tuple[int, int, int, int]) -> None:
        print("BBox recebido:", bbox)
        try:
            img = grab_region(bbox)
            img_proc = enhance_for_ocr(img, scale=1.8)
            text_ocr = image_to_text(img_proc, lang="eng+por")
            text_translated = translate_en_to_pt(text_ocr)
            self.panel.append_translation(text_translated)
            self.panel.show()
            self.panel.raise_()
            self.panel.activateWindow()
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
