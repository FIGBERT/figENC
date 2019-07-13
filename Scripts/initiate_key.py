from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def rsa_key(passkey, save_folder):
    """Generate and save a private, public and symmetric key.
    
    Keyword arguments:
    save_folder -- the folder to save the keys to (i.e. C://Desktop)
    passkey -- the passkey used to enhance the encryption algorithm (OPTIONAL)
    """
    #Generating three key objects (symmetric, private, public)
    symmetric_key = Fernet.generate_key()
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 4096,
        backend = default_backend()
    )
    public_key = private_key.public_key()
    #Converting the public and private key objects to a saveable format
    if passkey != "": #
        private_key_passcode = passkey
        private_key_text = private_key.private_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PrivateFormat.PKCS8,
            encryption_algorithm = serialization.BestAvailableEncryption(
                bytes(private_key_passcode, 'utf-8')
                )
        )
    else:
        private_key_text = private_key.private_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PrivateFormat.PKCS8,
            encryption_algorithm = serialization.NoEncryption()
        )
    public_key_text = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )
    #Saving the keys to the provided directory.
    if save_folder[-1] != '/':
        save_folder += '/'
    private_key_file = save_folder + 'private_key.pem'
    public_key_file = save_folder + 'public_key.pem'
    symmetric_key_file = save_folder + 'symmetric_key.key'
    with open(private_key_file, 'wb') as private_file, \
        open(public_key_file, 'wb') as public_file, \
        open(symmetric_key_file, 'wb') as symmetric_file:
        private_file.write(private_key_text)
        public_file.write(public_key_text)
        symmetric_file.write(symmetric_key)