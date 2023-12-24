from sqlalchemy import Column, Integer, String, LargeBinary, Float
from database import Base


class Arquivo(Base):
    __tablename__ = "arquivos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, index=True)

    tamanho = Column(Float)

    dados = Column(LargeBinary)
