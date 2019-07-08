from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

#rsa_key() generates a symmetric key as well as a public and private key
def rsa_key(passkey, savefolder):
    # Generating the symmetric key for use encrypting the file
    symmetric_key = Fernet.generate_key()
    # Generating the private key object for use encrypting the symmetric key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    # Generating the public key object for use decrypting the symmetric key
    public_key = private_key.public_key()
    private_key_passcode = passkey
    # Turning the private key object to readable text for export
    private_key_text = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(private_key_passcode, 'utf-8'))
    )
    # Turning the public key object to readable text for export
    public_key_text = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Checking the validity of the filepath provided
    if savefolder[-1] != '/':
        savefolder += '/'
    # Writing the keys to their respective files
    private_key_file = savefolder + 'private_key.pem'
    public_key_file = savefolder + 'public_key.pem'
    symmetric_key_file = savefolder + 'symmetric_key.key'
    with open(private_key_file, 'wb') as private_file:
        private_file.write(private_key_text)
    with open(public_key_file, 'wb') as public_file:
        public_file.write(public_key_text)
    with open(symmetric_key_file, 'wb') as symmetric_file:
        symmetric_file.write(symmetric_key)

#weak_key() generates a symmetric key as well as a public and private key
def weak_key(savefolder):
    # Generating the symmetric key for use encrypting the file
    symmetric_key = Fernet.generate_key()
    # Generating the private key object for use encrypting the symmetric key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    # Generating the public key object for use decrypting the symmetric key
    public_key = private_key.public_key()
    # Turning the private key object to readable text for export
    private_key_text = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    # Turning the public key object to readable text for export
    public_key_text = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Checking the validity of the filepath provided
    if savefolder[-1] != '/':
        savefolder += '/'
    # Writing the keys to their respective files
    private_key_file = savefolder + 'private_key.pem'
    public_key_file = savefolder + 'public_key.pem'
    symmetric_key_file = savefolder + 'symmetric_key.key'
    with open(private_key_file, 'wb') as private_file:
        private_file.write(private_key_text)
    with open(public_key_file, 'wb') as public_file:
        public_file.write(public_key_text)
    with open(symmetric_key_file, 'wb') as symmetric_file:
        symmetric_file.write(symmetric_key)