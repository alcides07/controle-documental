import OpenSSL
from utils.createKeyPair import createKeyPair
from utils.createCertificate import createCertificate
import os


def configCerticate(author: str):
    """Generate the certificate"""
    os.makedirs("./static", exist_ok=True)
    summary = {}
    summary['OpenSSL Version'] = OpenSSL.__version__
    # Generating a Private Key...
    key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)
    # PEM encoded
    with open('./static/private_key.pem', 'wb') as pk:
        pk_str = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, key)
        pk.write(pk_str)
        summary['Private Key'] = pk_str
    # Done - Generating a private key...
    # Generating a self-signed client certification...
    cert = createCertificate(pKey=key, author=author)
    with open('./static/certificate.cer', 'wb') as cer:
        cer_str = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        cer.write(cer_str)
        summary['Self Signed Certificate'] = cer_str
    # Done - Generating a self-signed client certification...
    # Generating the public key...
    with open('./static/public_key.pem', 'wb') as pub_key:
        pub_key_str = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())
        pub_key.write(pub_key_str)
        summary['Public Key'] = pub_key_str
    # Done - Generating the public key...
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    open('./static/container.pfx', 'wb').write(p12.export())
    # You may convert a PKSC12 file (.pfx) to a PEM format
    # Done - Generating a container file of the private key and the certificate...
    # To Display A Summary

    return True
