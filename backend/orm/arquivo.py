from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.arquivo import Arquivo
from schemas.arquivo import ArquivoCreate


async def create_arquivo(db: Session, arquivo: ArquivoCreate):
    db_arquivo = Arquivo(
        **arquivo.model_dump())
    db.add(db_arquivo)
    db.commit()
    db.refresh(db_arquivo)
    return db_arquivo


def update_total_arquivo(db: Session, model: Any, id: int, data: Any):
    db_object = db.query(model).filter(model.id == id).first()

    if (db_object):
        for key, value in data.items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
        return db_object

    raise HTTPException(status.HTTP_404_NOT_FOUND)
