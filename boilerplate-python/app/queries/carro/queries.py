"""Consultas reutilizáveis para `Carro` — espelho de `App\\Queries\\Carro\\Queries`."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.helpers import formatar_mensagem_erro
from app.models.carro import Carro

_ORDER_COLS = frozenset(
    {"id", "marca", "modelo", "ano", "cor", "placa", "km", "created_at", "updated_at"},
)


class CarroQueries:
    """Monta consultas, aplica filtros/ordenação e executa CRUD."""

    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    def session(self) -> Session:
        """Expõe a sessão para transações coordenadas pelos services."""
        return self._session

    def index(self, filtros: dict[str, Any]) -> dict[str, Any]:
        try:
            stmt = select(Carro)
            stmt = self._aplicar_filtros(stmt, filtros)
            stmt = self._aplicar_ordenacao(stmt, filtros)
            lista = list(self._session.scalars(stmt).all())
            return {"sucesso": True, "dados": {"lista": lista}, "erros": []}
        except Exception as th:
            return {
                "sucesso": False,
                "dados": {"lista": []},
                "erros": [formatar_mensagem_erro(th)],
            }

    def show(self, filtros: dict[str, Any]) -> dict[str, Any]:
        try:
            stmt = select(Carro)
            stmt = self._aplicar_filtros(stmt, filtros)
            model = self._session.scalars(stmt).first()
            return {"sucesso": True, "dados": {"model": model}, "erros": []}
        except Exception as th:
            return {
                "sucesso": False,
                "dados": {"model": None},
                "erros": [formatar_mensagem_erro(th)],
            }

    def _aplicar_filtros(
        self,
        stmt: Select[tuple[Carro]],
        filtros: dict[str, Any],
    ) -> Select[tuple[Carro]]:
        for chave, valor in filtros.items():
            if valor is None or valor == "":
                continue

            if chave == "id":
                stmt = stmt.where(Carro.id == valor)
            elif chave == "marca":
                stmt = stmt.where(Carro.marca.like(f"%{valor}%"))
            elif chave == "modelo":
                stmt = stmt.where(Carro.modelo.like(f"%{valor}%"))
            elif chave == "ano":
                stmt = stmt.where(Carro.ano == valor)
            elif chave == "placa":
                stmt = stmt.where(Carro.placa == valor)

        return stmt

    def _aplicar_ordenacao(
        self,
        stmt: Select[tuple[Carro]],
        filtros: dict[str, Any],
    ) -> Select[tuple[Carro]]:
        ordenacao = filtros.get("ordenacao")
        if not ordenacao:
            return stmt
        coluna = ordenacao.get("coluna")
        ordem = ordenacao.get("ordem")
        if not coluna or not ordem:
            return stmt
        if coluna not in _ORDER_COLS:
            return stmt
        ordem_l = str(ordem).lower()
        if ordem_l not in ("asc", "desc"):
            return stmt
        col = getattr(Carro, coluna)
        if ordem_l == "asc":
            return stmt.order_by(col.asc())
        return stmt.order_by(col.desc())

    def store(self, dados: dict[str, Any]) -> dict[str, Any]:
        try:
            retorno = Carro(**dados)
            self._session.add(retorno)
            self._session.flush()
            sucesso = retorno.id is not None
            if not sucesso:
                raise RuntimeError("Erro ao salvar carro!")
            return {
                "sucesso": sucesso,
                "dados": {"model": retorno, "id": retorno.id},
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
            model = self._session.get(Carro, id_)
            if model is None:
                raise NoResultFound()

            for key, value in dados.items():
                setattr(model, key, value)

            self._session.flush()
            return {"sucesso": True, "dados": {"model": model}, "erros": []}
        except Exception as th:
            return {
                "sucesso": False,
                "dados": [],
                "erros": [formatar_mensagem_erro(th)],
            }

    def destroy(self, id_: str | int) -> dict[str, Any]:
        try:
            pk = int(id_) if not isinstance(id_, int) else id_
            model = self._session.get(Carro, pk)
            if model is None:
                raise NoResultFound()

            self._session.delete(model)
            self._session.flush()
            linhas_afetadas = 1
            sucesso = linhas_afetadas > 0
            return {"sucesso": sucesso, "dados": [], "erros": []}
        except Exception as th:
            return {
                "sucesso": False,
                "dados": [],
                "erros": [formatar_mensagem_erro(th)],
            }
