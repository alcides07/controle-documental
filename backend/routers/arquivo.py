from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse
from schemas.arquivo import ArquivoCreate, ArquivoRead
from models.arquivo import Arquivo
from orm.arquivo import create_arquivo
from utils.bytesToMegabytes import bytesToMegabytes
from orm.common.index import delete_object, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile, BackgroundTasks
from cryptography.fernet import Fernet
import os
import tempfile


KEY_DIR = "./keys/"
TEMP_DIR = "./temp/"

router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
)


def remove_temp(fd: int, temp_file_path: str):
    os.close(fd)
    os.remove(temp_file_path)


def generate_key():
    return Fernet.generate_key()


@router.get("/",
            response_model=List[ArquivoRead],
            summary="Lista arquivos",
            dependencies=[Depends(get_authenticated_user)],
            )
def read(
        db: Session = Depends(get_db),
):
    arquivos = get_all(db, Arquivo)

    return arquivos


@router.post("/",
             response_model=ArquivoRead,
             status_code=201,
             summary="Cadastra um arquivo",
             dependencies=[Depends(get_authenticated_user)],
             )
def create(
    arquivo: Annotated[UploadFile, File(description="Arquivo .pdf para upload")],
    db: Session = Depends(get_db),
):
    if arquivo.content_type not in ["application/pdf"]:
        raise HTTPException(
            status_code=400, detail="Erro. Formato de arquivo inválido!")

    if bytesToMegabytes(arquivo.size) > 10:
        raise HTTPException(
            status_code=400, detail="Erro. Tamanho de arquivo excedido!")

    key = generate_key()
    cipher_suite = Fernet(key)

    dados_arquivo = arquivo.file.read()
    dados_criptografados = cipher_suite.encrypt(dados_arquivo)

    arquivo_schema = ArquivoCreate(nome=arquivo.filename, tamanho=bytesToMegabytes(
        arquivo.size), dados=dados_criptografados)
    data = create_arquivo(db=db, arquivo=arquivo_schema)

    os.makedirs(KEY_DIR, exist_ok=True)

    open(os.path.join(KEY_DIR, '__init__.py'), 'w')

    with open(os.path.join(KEY_DIR, str(data.id)+".key"), "wb") as key_file:
        key_file.write(key)

    return jsonable_encoder(data, exclude=set(["dados"]))


@router.get("/{id}/",
            response_model=ArquivoRead,
            summary="Lista um arquivo",
            dependencies=[Depends(get_authenticated_user)],
            )
def read_id(
        id: int = Path(description="identificador do arquivo"),
        db: Session = Depends(get_db)
):
    data = jsonable_encoder(get_by_id(db, Arquivo, id))

    return data


@router.get("/{id}/download/",
            response_model=Any,
            status_code=201,
            summary="Baixa um arquivo",
            dependencies=[Depends(get_authenticated_user)],
            )
def download(
    background_tasks: BackgroundTasks,
    id: int = Path(description="identificador do arquivo"),
    db: Session = Depends(get_db),
):

    arquivo = get_by_id(db=db, id=id, model=Arquivo)

    with open(os.path.join(KEY_DIR, str(id)+".key"), "rb") as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)
    dados_descriptografados = cipher_suite.decrypt(arquivo.dados)

    fd, temp_file_path = tempfile.mkstemp()
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(dados_descriptografados)

    background_tasks.add_task(remove_temp, fd, temp_file_path)

    return FileResponse(
        temp_file_path, media_type="application/pdf", filename=arquivo.nome)


@router.delete("/{id}/",
               response_model=ArquivoRead,
               summary="Deleta um arquivo",
               dependencies=[Depends(get_authenticated_user)],
               )
def delete(
        id: int = Path(description="identificador do arquivo"),
        db: Session = Depends(get_db)
):

    arquivo = jsonable_encoder(delete_object(db, Arquivo, id))
    return arquivo
