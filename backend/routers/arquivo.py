from typing import Annotated, Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.responses import FileResponse
from utils.removeSignature import removeSignature
from utils.saveSignature import saveSignature
from consts import KEYS_DIR, FILES_DIR
from utils.saveFile import saveFile
from utils.signFile import signFile
from utils.configCerticate import configCerticate
from schemas.arquivo import ArquivoCreate, ArquivoRead
from models.arquivo import Arquivo
from orm.arquivo import create_arquivo, update_total_arquivo
from utils.bytesToMegabytes import bytesToMegabytes
from orm.common.index import delete_object, get_by_id, get_all, get_by_key_value
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import File, UploadFile
import os
from cryptography.fernet import Fernet
import tempfile
import hashlib

router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
)


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

    arquivo_schema = ArquivoCreate(nome=arquivo.filename, tamanho=bytesToMegabytes(
        arquivo.size), local="", codigo="")
    data = await create_arquivo(db=db, arquivo=arquivo_schema)

    dirFile = await saveFile(arquivo, str(data.id))
    dirSignature = await saveSignature(assinatura, str(data.id))
    data_criptograf = signFile(
        FILES_DIR + str(data.id) + "-" + arquivo.filename,
        author,
        str(data.id) + "-" + assinatura.filename,
        330,
        280,
        str(data.id)
    )

    data = jsonable_encoder(data)
    data_dict = dict(data)
    data_dict["local"] = dirFile

    hash_object = hashlib.sha256(data_criptograf)
    hex_dig = hash_object.hexdigest()

    data_dict["codigo"] = hex_dig

    update_total_arquivo(db=db, model=Arquivo, id=data["id"], data=data_dict)
    await removeSignature(dirSignature)

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
    id: int = Path(description="identificador do arquivo"),
    db: Session = Depends(get_db),
):

    arquivo = get_by_id(db=db, id=id, model=Arquivo)

    with open(os.path.join(KEYS_DIR, str(id)+".key"), "rb") as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    with open(os.path.join(FILES_DIR, str(id) + "-" + arquivo.nome), "rb") as data_file:
        file = data_file.read()

    dados_descriptografados = cipher_suite.decrypt(file)

    temp_file = tempfile.NamedTemporaryFile(delete=False)

    with open(temp_file.name, 'wb') as file:
        file.write(dados_descriptografados)

    return FileResponse(
        temp_file.name, media_type="application/pdf", filename=arquivo.nome)


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


@router.post("/autenticacao/",
             response_model=Any,
             summary="Verifica a integridade um arquivo",
             dependencies=[Depends(get_authenticated_user)],
             )
def autenticar(
        codigo: str = Query(description="Código de autenticação"),
        db: Session = Depends(get_db)
):

    arquivo = jsonable_encoder(get_by_key_value(db, Arquivo, "codigo", codigo))

    with open(os.path.join(FILES_DIR, str(arquivo["id"]) + "-" + arquivo["nome"]), "rb") as data_file:
        file = data_file.read()

    if (Arquivo):
        with open(os.path.join(KEYS_DIR, str(arquivo["id"])+".key"), "rb") as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        dados_descriptografados = cipher_suite.decrypt(file)

        temp_file = tempfile.NamedTemporaryFile(delete=False)

        with open(temp_file.name, 'wb') as file:
            file.write(dados_descriptografados)

        return FileResponse(
            temp_file.name, media_type="application/pdf", filename=arquivo["nome"])
