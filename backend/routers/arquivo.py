from typing import Annotated, Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.responses import FileResponse
from utils.removeSignature import removeSignature
from utils.saveSignature import saveSignature
from consts import KEYS_DIR, FILES_DIR
from utils.saveFile import saveFile
from utils.signFile import signFile
from utils.configCerticate import configCerticate
from utils.decryptData import decryptData
from utils.encryptData import encryptData
from schemas.arquivo import ArquivoCreate, ArquivoRead
from models.arquivo import Arquivo
from orm.arquivo import create_arquivo, update_total_arquivo
from utils.bytesToMegabytes import bytesToMegabytes
from orm.common.index import delete_object, get_by_id, get_all, update_total
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile, BackgroundTasks
import os
import tempfile


TEMP_DIR = "./temp/"

router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
)


def remove_temp(fd: int, temp_file_path: str):
    os.close(fd)
    os.remove(temp_file_path)


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
async def create(
    arquivo: Annotated[UploadFile, File(description="Arquivo .pdf para upload")],
    assinatura: Annotated[UploadFile, File(description="Arquivo .png .jpg ou .jpeg contendo a assinatura")],
    author: str = Body(description="Nome do autor"),
    db: Session = Depends(get_db),
):
    if arquivo.content_type not in ["application/pdf"]:
        raise HTTPException(
            status_code=400, detail="Erro. Formato de arquivo inválido!")

    if bytesToMegabytes(arquivo.size) > 10:
        raise HTTPException(
            status_code=400, detail="Erro. Tamanho de arquivo excedido!")

    if (assinatura.content_type not in ["image/jpeg", "image/png", "image/jpg"]):
        raise HTTPException(
            status_code=400, detail="Erro. Formato de assinatura inválido!")

    configCerticate(author=author)
    # dados_arquivo = arquivo.file.read()
    # dados_criptografados, key = encryptData()

    arquivo_schema = ArquivoCreate(nome=arquivo.filename, tamanho=bytesToMegabytes(
        arquivo.size), local="")
    data = await create_arquivo(db=db, arquivo=arquivo_schema)

    dirFile = await saveFile(arquivo, str(data.id))
    dirSignature = await saveSignature(assinatura, str(data.id))
    signFile(
        FILES_DIR + str(data.id) + "-" + arquivo.filename,
        author,
        str(data.id) + "-" + assinatura.filename,
        330,
        280)

    data = jsonable_encoder(data)
    data_dict = dict(data)
    data_dict["local"] = dirFile

    update_total_arquivo(db=db, model=Arquivo, id=data["id"], data=data_dict)
    await removeSignature(dirSignature)

    # os.makedirs(KEYS_DIR, exist_ok=True)

    # with open(os.path.join(KEYS_DIR, str(data.id)+".key"), "wb") as key_file:
    #     key_file.write(key)

    return jsonable_encoder(data)


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

    # with open(os.path.join(KEYS_DIR, str(id)+".key"), "rb") as key_file:
    #     key = key_file.read()

    # dados_descriptografados = decryptData(arquivo.dados, key)

    # fd, temp_file_path = tempfile.mkstemp()
    # with open(temp_file_path, "wb") as temp_file:
    #     temp_file.write(dados_descriptografados)

    # background_tasks.add_task(remove_temp, fd, temp_file_path)

    return FileResponse(
        arquivo.local, media_type="application/pdf", filename=arquivo.nome)


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
