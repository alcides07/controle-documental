import os
from fastapi import UploadFile


async def saveSignature(signature: UploadFile, id: str):
    os.makedirs("./static/signatures/", exist_ok=True)

    dir = os.path.join("./static/signatures/", id + "-" + signature.filename)

    with open(dir, "wb") as file:
        data = await signature.read()
        file.write(data)

    return dir
