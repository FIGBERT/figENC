from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

def rsa_enc():
    with open('public_key.pem', 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )
    with open('symmetric_key.key', 'rb') as symmetric_key_file:
        symmetric_key_data = symmetric_key_file.read()
        symmetric_key = Fernet(symmetric_key_data)
    file_to_encrypt = input("File to encrypt: ")
    with open(file_to_encrypt) as read_file:
        file_data = read_file.read()
    data = symmetric_key.encrypt(bytes(file_data, 'utf-8'))
    encrypted_key = public_key.encrypt(
        symmetric_key_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(file_to_encrypt, 'wb') as write_file:
        write_file.write(data)
    encrypt_symmetry = input("Are you encrypting more files this session? (y/n): ")
    if encrypt_symmetry == "n":
        with open('symmetric_key.key', 'wb') as crypto_key_file:
            crypto_key_file.write(encrypted_key)
        print("Encryption successful. Proceed into cyberspace with confidence.\n")
    else:
        print("Encryption successful. Proceed into cyberspace with confidence.\n")