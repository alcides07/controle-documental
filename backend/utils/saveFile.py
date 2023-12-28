import os
from fastapi import UploadFile
from consts import FILES_DIR


async def saveFile(arquivo: UploadFile, id: str):
    os.makedirs(FILES_DIR, exist_ok=True)

    with open(os.path.join(FILES_DIR + id + "-" + arquivo.filename), "wb") as file:
        data = await arquivo.read()
        file.write(data)
