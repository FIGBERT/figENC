from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

def rsa_dec():
    passcode = input("Private Key passcode: ")
    with open('private_key.pem', 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=bytes(passcode, 'utf-8'),
            backend=default_backend()
        )
    with open('symmetric_key.key', 'rb') as symmetric_key_file:
        encoded_key_data = symmetric_key_file.read()
        symmetric_key_data = private_key.decrypt(
            encoded_key_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        symmetric_key = Fernet(symmetric_key_data)
    file_to_decrypt = input("File to decrypt: ")
    with open(file_to_decrypt, 'rb') as read_file:
        encrypted_data = read_file.read()
    original_message = symmetric_key.decrypt(encrypted_data)
    with open(file_to_decrypt, 'wb') as write_file:
        write_file.write(original_message)
    decrypt_symmetry = input("Are you decrypting more files this session? (y/n): ")
    if decrypt_symmetry == "n":
        with open('symmetric_key.key', 'wb') as symmetric_file:
            symmetric_file.write(symmetric_key_data)
        print("Decryption completed.\n")
    else:
        print("Decryption completed.\n")