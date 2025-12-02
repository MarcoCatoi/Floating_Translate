# app/app.py
from __future__ import annotations

import sys
from typing import Tuple

from PySide6.QtWidgets import QApplication

from app.gui.overlay import Overlay
from app.gui.bubble import TranslationBubble
from app.gui.floating_button import FloatingButton
from app.core.capture import grab_region
from app.core.preprocess import enhance_for_ocr
from app.core.ocr import image_to_text
from app.core.translate import translate_en_to_pt


class FloatingTranslateApp:
    def __init__(self) -> None:
        self.panel = TranslationBubble()
        
        self.overlay = Overlay()
        self.overlay.selection_made.connect(self.on_selection_made)

        self.floating_button = FloatingButton()
        self.floating_button.clicked_for_selection.connect(self.show_overlay)
        self.floating_button.quit_requested.connect(self.quit)
        self.floating_button.show()

    def quit(self) -> None:
        self.overlay.close()
        self.panel.close()
        self.floating_button.close()
        QApplication.instance().quit()
        
    def show_overlay(self) -> None:
        self.overlay.show_overlay()

    def on_selection_made(self, bbox: Tuple[int, int, int, int]) -> None:
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
    app = QApplication(sys.argv)
    ft_app = FloatingTranslateApp()
    rc = app.exec()
    sys.exit(rc)


if __name__ == "__main__":
    main()
