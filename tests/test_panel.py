import sys
from PySide6.QtWidgets import QApplication
from app.gui.panel import TranslationPanel

app = QApplication(sys.argv)
panel = TranslationPanel()
panel.set_texts("Exemplo de texto original", "Exemplo de tradução")
panel.show()
app.exec()