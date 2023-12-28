from cryptography.fernet import Fernet


def decryptData(data, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(data)
