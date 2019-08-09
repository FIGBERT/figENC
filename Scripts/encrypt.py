import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from prompts import success


def RSA(target_file, public_key_source):
    """Encrypts the passed file with the passed RSA public key
    
    Keyword arguments:
    target_file -- the filepath to the file to be encrypted
    public_key_source -- the filepath to the public key
    """
    with open(public_key_source, "rb") as public_key_file, \
        open(target_file) as read_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )
            file_data = read_file.read()
    if not isinstance(file_data, bytes):
        file_data = bytes(file_data, "utf-8")
    data = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    data += b"0"
    with open(target_file, "wb") as write_file:
        write_file.write(data)


def Symmetric(target_file, symmetric_key_source):
    """Encrypts the passed file with the passed symmetric key
    
    Keyword arguments:
    target_file -- the filepath to the file to be encrypted
    symmetric_key_source -- the filepath to the symmetric key
    """
    with open(symmetric_key_source, "rb") as symmetric_key_file:
        symmetric_key_data = symmetric_key_file.read()
    symmetric_key = Fernet(symmetric_key_data)
    try:
        with open(target_file) as read_file:
            file_data = read_file.read()
        file_data = bytes(file_data, "utf-8")
    except UnicodeDecodeError:
        with open(target_file, "rb") as read_file:
            file_data = read_file.read()
    data = symmetric_key.encrypt(file_data)
    data += b"1"
    with open(target_file, "wb") as write_file:
        write_file.write(data)

def enc_manager(target_files, save_folder):
    """Encrypt all files passed to the function with the symmetric key,
    and then replace the symmetric key file's contents with an encrypted
    version, encrypted with the public key.

    Keyword arguments:
    target_file_raw -- a string composed of file locations seperated by colons
    save_folder -- the location of the saved key trio
    """
    pub_src = save_folder + "/public_key.pem"
    sym_src = save_folder + "/symmetric_key.key"
    if not os.path.exists(sym_src):
        for fl in target_files:
            RSA(fl, pub_src)
    else:
        for fl in target_files:
            if os.path.getsize(fl) > 446:
                Symmetric(fl, sym_src)
            else:
                RSA(fl, pub_src)
        with open(pub_src, "rb") as pub_file, \
            open(sym_src, "rb") as sym_file:
                public_key = serialization.load_pem_public_key(
                    pub_file.read(),
                    backend=default_backend()
                )
                symmetric_key_data = sym_file.read()
        encrypted_key = public_key.encrypt(
            symmetric_key_data,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
                )
            )
        with open(sym_src, "wb") as crypto_key_file:
            crypto_key_file.write(encrypted_key)
    success()