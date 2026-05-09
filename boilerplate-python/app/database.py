"""Fábrica de sessão SQLAlchemy (equivalente conceitual ao bootstrap de DB do Laravel)."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_DATABASE_URL = "sqlite:///./carros.db"


def get_engine(url: str | None = None):
    """Cria engine a partir de `DATABASE_URL` ou SQLite local."""
    return create_engine(url or os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL))


def get_session_factory(url: str | None = None):
    """Retorna `sessionmaker` configurado (expire_on_commit=False, como uso típico em services)."""
    engine = get_engine(url)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


def create_tables(url: str | None = None) -> None:
    """Cria tabelas a partir dos modelos (útil em dev; em produção prefira migrations/SQL)."""
    import app.models.carro  # noqa: F401 — registra `Carro` no metadata
    from app.models.base import Base

    engine = get_engine(url)
    Base.metadata.create_all(engine)
