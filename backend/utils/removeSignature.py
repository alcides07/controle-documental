import os


async def removeSignature(file_path: str):
    os.remove(file_path)
