"""
Funções de pré-processamento de imagem para melhorar o OCR:
- conversão para escala de cinza
- aumento de tamanho (upscale)
- binarização (threshold)
- remoção simples de ruído
"""

from typing import Union

import numpy as np
from PIL import Image
import cv2

ArrayLikeImage = Union[Image.Image, np.ndarray]

def _to_ndarray(image: ArrayLikeImage) -> np.ndarray:
    
    if isinstance(image, np.ndarray):
        return image

    # Converte PIL.Image -> np.ndarray (RGB) -> BGR para OpenCV
    arr = np.array(image)
    if len(arr.shape) == 2:
        # já está em escala de cinza
        return arr
    # RGB -> BGR
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def basic_enhance(image: ArrayLikeImage, scale: float = 1.8) -> np.ndarray:
    img = _to_ndarray(image)

    # Converte para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # Aumenta a imagem (interpolação cúbica para texto ficar mais nítido)
    up = cv2.resize(#
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC,
    )

    # Binarização com OTSU (separa texto/fundo)
    _, thr = cv2.threshold(
        up, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thr


def denoise(image: ArrayLikeImage, ksize: int = 3) -> np.ndarray:
    """
    Aplica um filtro de mediana simples para reduzir ruído,
    útil se a imagem estiver muito granulada.
    """
    img = _to_ndarray(image)

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    den = cv2.medianBlur(gray, ksize)
    return den


def enhance_for_ocr(image: ArrayLikeImage, scale: float = 1.8) -> np.ndarray:
    """
    Pipeline padrão de pré-processamento para usar antes do OCR.

    Equivalente a:
      1) basic_enhance (grayscale + upscale + threshold)
      2) denoise leve (opcional, mas aqui aplicado por padrão)
    """
    basic = basic_enhance(image, scale=scale)
    final = denoise(basic, ksize=3)
    return final
