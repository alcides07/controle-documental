from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encryptData(dados_arquivo):
    key = generate_key()
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(dados_arquivo), key
