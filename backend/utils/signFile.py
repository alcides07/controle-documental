import os
from PDFNetPython3.PDFNetPython import *
from typing import Tuple
from cryptography.fernet import Fernet

from consts import KEYS_DIR

key = Fernet.generate_key()
cipher_suite = Fernet(key)


def signFile(input_file: str, signatureID: str, signature: str, x_coordinate: int,
             y_coordinate: int, id_data: str, pages: Tuple = None, output_file: str = None):
    """Sign a PDF file"""

    # An output file is automatically generated with the word signed added at its end
    if not output_file:
        output_file = (os.path.splitext(input_file)[0]) + ".pdf"
    # Initialize the library
    PDFNet.Initialize(
        "demo:1703715356380:7c83f1a103000000004d11877bc04ef34f67f2634a52321d32ced42fe7")
    doc = PDFDoc(input_file)
    # Create a signature field
    sigField = SignatureWidget.Create(doc, Rect(
        x_coordinate, y_coordinate, x_coordinate+100, y_coordinate+50), signatureID)
    # Iterate throughout document pages
    for page in range(1, (doc.GetPageCount() + 1)):
        # If required for specific pages
        if pages:
            if str(page) not in pages:
                continue
        pg = doc.GetPage(page)
        # Create a signature text field and push it on the page
        pg.AnnotPushBack(sigField)
    # Signature image
    sign_filename = os.path.join(
        os.path.dirname("static/signatures/"), signature)
    # Self signed certificate

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    pk_filename = os.path.join(parent_dir, "static", "container.pfx")

    # Retrieve the signature field.
    approval_field = doc.GetField(signatureID)
    approval_signature_digsig_field = DigitalSignatureField(approval_field)
    # Add appearance to the signature field.
    img = Image.Create(doc.GetSDFDoc(), sign_filename)
    found_approval_signature_widget = SignatureWidget(
        approval_field.GetSDFObj())
    found_approval_signature_widget.CreateSignatureAppearance(img)
    # Prepare the signature and signature handler for signing.
    approval_signature_digsig_field.SignOnNextSave(pk_filename, '')
    # The signing will be done during the following incremental save operation.

    temp_output_file = os.path.join(os.path.dirname(
        output_file), 'temp_' + os.path.basename(output_file))
    doc.Save(temp_output_file, SDFDoc.e_incremental)

    with open(temp_output_file, 'rb') as file:
        data = file.read()
    encrypted_data = cipher_suite.encrypt(data)

    with open(output_file, 'wb') as file:
        file.write(encrypted_data)
    os.remove(temp_output_file)

    saveKey(id_data)

    return encrypted_data


def saveKey(id_data: str):
    os.makedirs(KEYS_DIR, exist_ok=True)
    with open(os.path.join(KEYS_DIR, id_data + ".key"), "wb") as key_file:
        key_file.write(key)
