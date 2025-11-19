"""
Responsável por capturar uma região da tela usando Pillow (ImageGrab).
O bbox deve ser uma tupla (x1, y1, x2, y2) em coordenadas de tela.
"""
# Após o término do programa, testar o metodo MSS, pois tem maior compátibilidade de sistemas

from typing import Tuple, Optional

from PIL import Image, ImageGrab


def grab_region(bbox: Tuple[int, int, int, int]) -> Image.Image:           # Captura uma região da tela e retorna um objeto PIL.Image.

    if len(bbox) != 4:
        raise ValueError("bbox deve ser uma tupla (x1, y1, x2, y2)")

    x1, y1, x2, y2 = bbox

    if x2 <= x1 or y2 <= y1:
        raise ValueError("bbox inválido: (x2, y2) deve ser maior que (x1, y1)")

    img = ImageGrab.grab(bbox=bbox)
    return img


def grab_fullscreen() -> Image.Image:           # Captura a tela inteira e retorna um objeto PIL.Image.
    
    img = ImageGrab.grab()
    return img


def save_capture(bbox: Tuple[int, int, int, int],           # Captura uma região da tela e salva em disco.
                 path: str,
                 format: Optional[str] = None) -> None:

    img = grab_region(bbox)
    img.save(path, format=format)