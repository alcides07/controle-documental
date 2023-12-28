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
