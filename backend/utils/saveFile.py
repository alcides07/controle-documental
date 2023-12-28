import os
from fastapi import UploadFile
from consts import FILES_DIR


async def saveFile(arquivo: UploadFile, id: str):
    os.makedirs(FILES_DIR, exist_ok=True)
    dir = os.path.join(FILES_DIR + id + "-" + arquivo.filename)

    with open(dir, "wb") as file:
        data = await arquivo.read()
        file.write(data)
    return dir
