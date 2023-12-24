from typing import Any
from pydantic import BaseModel, Field


class ArquivoBase(BaseModel):
    nome: str = Field(max_length=32, description="Nome do arquivo")
    tamanho: float = Field(description="Tamanho do arquivo em MB")


class ArquivoCreate(ArquivoBase):
    dados: Any = Field(default=None, description="Dados do arquivo")


class ArquivoRead(ArquivoBase):
    id: int

    class Config:
        from_attributes = True
