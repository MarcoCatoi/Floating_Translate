"""
Responsável por fazer OCR (reconhecimento de texto) usando Tesseract
via biblioteca pytesseract.

Este módulo assume que o Tesseract está instalado no sistema e,
se necessário, que o caminho do executável foi configurado.
"""

from typing import Optional, Union

from PIL import Image
import pytesseract

import numpy

'''
Se o Tesseract não estiver no PATH do Windows, descomente e ajuste a linha abaixo:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
'''

def image_to_text(
    image: Union[Image.Image, "numpy.ndarray"],
    lang: str = "eng+por",
    psm: Optional[int] = None,
    oem: Optional[int] = None,
) -> str:
    
    config_parts = []           # Executa OCR em uma imagem e retorna o texto reconhecido.

    if psm is not None:
        config_parts.append(f"--psm {psm}")

    if oem is not None:
        config_parts.append(f"--oem {oem}")

    config = " ".join(config_parts).strip()

    text = pytesseract.image_to_string(
        image,
        lang=lang,
        config=config if config else None,
    )

    return text.strip()


def detect_data(
    image: Union[Image.Image, "numpy.ndarray"],
    lang: str = "eng+por",
    psm: Optional[int] = None,
    oem: Optional[int] = None,
) -> dict:          # Retorna dados estruturados do Tesseract
    
    config_parts = []

    if psm is not None:
        config_parts.append(f"--psm {psm}")

    if oem is not None:
        config_parts.append(f"--oem {oem}")

    config = " ".join(config_parts).strip()

    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config=config if config else None,
        output_type=pytesseract.Output.DICT,
    )
    return data