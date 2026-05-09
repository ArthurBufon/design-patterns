from __future__ import annotations

import logging
import re
from typing import Any, Protocol

from app.helpers import formatar_mensagem_erro
from app.models.carro import Carro
from app.queries.carro.queries import CarroQueries

logger = logging.getLogger(__name__)


class MensagensFlash(Protocol):
    """Substituto injetável de `session()->flash` do Laravel (somente web)."""

    def mensagem_sucesso(self, message: str) -> None: ...

    def mensagem_erro(self, message: str) -> None: ...


class Service:
    """Service web — espelho de `App\\Services\\Carro\\Service`."""

    def __init__(
        self,
        queries: CarroQueries,
        flash: MensagensFlash | None = None,
    ) -> None:
        self._queries = queries
        self._flash = flash

    def index(self, filtros: dict[str, Any]) -> dict[str, Any]:
        return self._queries.index(filtros)

    def show(self, filtros: dict[str, Any]) -> dict[str, Any]:
        return self._queries.show(filtros)

    def store(self, dados: dict[str, Any]) -> dict[str, Any]:
        try:
            with self._queries.session.begin():
                dados_database = self._formatar_database(dados)
                retorno_database = self._queries.store(dados_database)
                if not retorno_database["sucesso"]:
                    raise RuntimeError(
                        retorno_database["erros"][0]
                        if retorno_database["erros"]
                        else "Erro ao salvar carro."
                    )
            return {
                "sucesso": True,
                "dados": retorno_database["dados"],
                "erros": [],
            }
        except Exception as th:
            return {
                "sucesso": False,
                "dados": [],
                "erros": [formatar_mensagem_erro(th)],
            }

    def update(self, id_: int, dados: dict[str, Any]) -> dict[str, Any]:
        try:
            with self._queries.session.begin():
                dados_database = self._formatar_database(dados)
                retorno_database = self._queries.update(id_, dados_database)
                if not retorno_database["sucesso"]:
                    raise RuntimeError(
                        retorno_database["erros"][0]
                        if retorno_database["erros"]
                        else "Erro ao atualizar carro."
                    )
            return {
                "sucesso": True,
                "dados": retorno_database["dados"],
                "erros": [],
            }
        except Exception as th:
            return {
                "sucesso": False,
                "dados": [],
                "erros": [formatar_mensagem_erro(th)],
            }

    def destroy(self, carro: Carro) -> dict[str, Any]:
        try:
            with self._queries.session.begin():
                retorno_database = self._queries.destroy(carro.id)
                if not retorno_database["sucesso"]:
                    raise RuntimeError(
                        retorno_database["erros"][0]
                        if retorno_database["erros"]
                        else "Erro não identificado!"
                    )
            if self._flash is not None:
                self._flash.mensagem_sucesso("Carro excluído com sucesso!")
            return {"sucesso": True, "dados": [], "erros": []}
        except Exception as th:
            if self._flash is not None:
                self._flash.mensagem_erro("Erro ao excluir carro!")
            self.logar_erro({"id": carro.id}, formatar_mensagem_erro(th))
            return {
                "sucesso": False,
                "dados": [],
                "erros": [formatar_mensagem_erro(th)],
            }

    def _formatar_database(self, dados: dict[str, Any]) -> dict[str, Any]:
        mapa: dict[str, Any] = {}

        if "marca" in dados:
            mapa["marca"] = dados["marca"]
        if "modelo" in dados:
            mapa["modelo"] = dados["modelo"]
        if "ano" in dados:
            mapa["ano"] = int(dados["ano"])
        if "cor" in dados:
            mapa["cor"] = dados["cor"]
        if "placa" in dados:
            mapa["placa"] = self._normalizar_placa(str(dados["placa"]))
        if "km" in dados:
            mapa["km"] = int(dados["km"])

        return mapa

    @staticmethod
    def _normalizar_placa(placa: str) -> str:
        sem_espacos = re.sub(r"\s+", "", placa.strip())
        return sem_espacos.upper()

    def logar_erro(self, dados: dict[str, Any], mensagem_erro: str) -> None:
        id_ = dados.get("id", "?")
        mensagem_formatada = f"Erro ao processar carro (id {id_}): {mensagem_erro}"
        logger.error(
            mensagem_formatada,
            extra={
                "sucesso": "false",
                "dados": dados,
                "erros": [mensagem_formatada],
            },
        )
