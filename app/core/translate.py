"""
Camada de tradução offline usando Argos Translate.

Principais funções:
- ensure_models_installed: opcional, para baixar/instalar modelos en↔pt
- init_translator: carrega idiomas instalados e guarda objetos de tradução
- translate_en_to_pt / translate_pt_to_en: funções simples de uso
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import argostranslate.package as argos_package
import argostranslate.translate as argos_translate


# Pares de idiomas que você quer suportar
LANGUAGE_PAIRS = [
    ("en", "pt"),
    ("pt", "en"),
]


@dataclass
class TranslatorPair:
    """Guarda objetos de tradução de um idioma para outro."""
    from_code: str
    to_code: str
    translator: object  # objeto de tradução do Argos


class TranslationManager:
    """
    Gerencia tradutores Argos já carregados na memória.
    """

    def __init__(self) -> None:
        self._pairs: Dict[tuple[str, str], TranslatorPair] = {}

    def init_from_installed(self) -> None:
        """
        Carrega idiomas e tradutores a partir dos modelos
        Já instalados no Argos.
        Não baixa nada, só usa o que já existe.
        """
        installed_langs = argos_translate.get_installed_languages()

        # Mapeia code -> objeto de idioma
        by_code = {lang.code: lang for lang in installed_langs}

        for from_code, to_code in LANGUAGE_PAIRS:
            if from_code not in by_code or to_code not in by_code:
                # modelo ainda não instalado para esse par
                continue

            src = by_code[from_code]
            dst = by_code[to_code]

            translator = src.get_translation(dst)
            self._pairs[(from_code, to_code)] = TranslatorPair(
                from_code=from_code,
                to_code=to_code,
                translator=translator,
            )

    def has_pair(self, from_code: str, to_code: str) -> bool:
        return (from_code, to_code) in self._pairs

    def translate(self, text: str, from_code: str, to_code: str) -> str:
        """
        Traduz texto de from_code -> to_code usando um tradutor carregado.
        """
        key = (from_code, to_code)
        if key not in self._pairs:
            raise RuntimeError(
                f"Par de idiomas não inicializado: {from_code}->{to_code}. "
                f"Chame init_from_installed() ou instale os modelos."
            )

        pair = self._pairs[key]
        return pair.translator.translate(text or "")


# Instância global simples para o app todo usar
_manager: Optional[TranslationManager] = None


def get_manager() -> TranslationManager:
    """
    Retorna (e cria se necessário) um TranslationManager global.
    """
    global _manager
    if _manager is None:
        _manager = TranslationManager()
        _manager.init_from_installed()
    return _manager


def ensure_models_installed() -> None:
    """
    Opcional: baixa e instala automaticamente os modelos en↔pt
    usando o índice oficial do Argos.

    Use este método uma vez (ou num comando separado) para
    preparar o ambiente de tradução.
    """
    # Atualiza índice de pacotes
    argos_package.update_package_index()
    available = argos_package.get_available_packages()

    for from_code, to_code in LANGUAGE_PAIRS:
        # Verifica se já existe modelo instalado; se sim, pula
        already = _is_model_installed(from_code, to_code)
        if already:
            continue

        # Procura o pacote correspondente no índice
        pkg = next(
            p for p in available
            if p.from_code == from_code and p.to_code == to_code
        )
        download_path = pkg.download()
        argos_package.install_from_path(download_path)




def _is_model_installed(from_code: str, to_code: str) -> bool:      
    
    installed = argos_translate.get_installed_languages()
    by_code = {lang.code: lang for lang in installed}
    if from_code not in by_code or to_code not in by_code:
        return False
    src = by_code[from_code]
    dst = by_code[to_code]
    try:
        _ = src.get_translation(dst)
        return True
    except Exception:
        return False


# Funções de conveniência para o resto do app

def translate_en_to_pt(text: str) -> str:
    mgr = get_manager()
    return mgr.translate(text, from_code="en", to_code="pt")


def translate_pt_to_en(text: str) -> str:
    mgr = get_manager()
    return mgr.translate(text, from_code="pt", to_code="en")