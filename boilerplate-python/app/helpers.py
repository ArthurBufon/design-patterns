"""Funções utilitárias equivalentes a `app/helpers.php` no Laravel."""

from __future__ import annotations

import os
import re
import traceback
from typing import Any


def formatar_mensagem_erro(th: BaseException) -> str:
    """Mensagem padronizada: texto | arquivo | linha (como no PHP)."""
    tb = th.__traceback__
    if tb is not None:
        frames = traceback.extract_tb(tb)
        if frames:
            last = frames[-1]
            return f"{th} | {last.filename} | {last.lineno}"
    return str(th)


def somente_numeros(string: str) -> str:
    """Remove tudo que não for dígito."""
    return re.sub(r"[^0-9]", "", string)


def ambiente_dev() -> bool:
    """
    Retorna True se `APP_ENV` contiver a substring 'desenvolvimento'.

    No PHP original a assinatura de retorno estava como string, mas o valor
    era booleano; aqui o tipo reflete o uso real.
    """
    ambiente = os.environ.get("APP_ENV", "producao")
    return "desenvolvimento" in ambiente
