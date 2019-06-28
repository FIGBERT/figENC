from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

def symmetric_enc():
    symmetric_key = Fernet.generate_key()
    with open('symmetric_key.key', 'wb') as symmetric_file:
        symmetric_file.write(symmetric_key)

def rsa_enc():
    symmetric_key = Fernet.generate_key()
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_key_passcode = input("Private Key Password: ")
    private_key_text = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(private_key_passcode, 'utf-8'))
    )
    public_key_text = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('private_key.pem', 'wb') as private_file:
        private_file.write(private_key_text)
    with open('public_key.pem', 'wb') as public_file:
        public_file.write(public_key_text)
    with open('symmetric_key.key', 'wb') as symmetric_file:
        symmetric_file.write(symmetric_key)