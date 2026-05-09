from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Carro(Base):
    """Modelo `carros` — espelho de `App\Models\Carro`."""

    __tablename__ = "carros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    marca: Mapped[str] = mapped_column(String(80))
    modelo: Mapped[str] = mapped_column(String(120))
    ano: Mapped[int] = mapped_column(Integer)
    cor: Mapped[str | None] = mapped_column(String(40), nullable=True)
    placa: Mapped[str] = mapped_column(String(10), unique=True)
    km: Mapped[int] = mapped_column(Integer, server_default="0")
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
