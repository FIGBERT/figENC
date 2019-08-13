import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
from prompts import success


def rsa_key(pub, priv, passkey):
    """Generate a private and public key to the provided filepaths.
    
    Keyword arguments:
    pub -- path to save the public key
    priv -- path to save the private key
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_key_text = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=(
            serialization.BestAvailableEncryption(
                bytes(passkey, "utf-8")
            ) if passkey != "" else serialization.NoEncryption()
        )
    )
    public_key_text = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(priv, "wb") as private_file, \
        open(pub, "wb") as public_file:
            private_file.write(private_key_text)
            public_file.write(public_key_text)


def mixed_key(pub, priv, sym, passkey):
    """Generate a private, public, and symmetric key to the 
    provided filepaths.
    
    Keyword arguments:
    pub -- path to save the public key
    priv -- path to save the private key
    sym -- path to save the symmetric key
    """
    rsa_key(pub, priv, passkey)
    symmetric_key = Fernet.generate_key()
    with open(sym, "wb") as sym_file:
        sym_file.write(symmetric_key)


def key_manager(target_files, save_folder, passkey):
    """Call either the `rsa_key` function or the `mixed_key`
    function, according to the needs of the target files.
    
    Keyword arguments:
    target_files -- a list of the files to be encrypted
    save_folder -- the directory to save the keys
    passkey -- the password to enhance the RSA encryption (OPTIONAL)
    """
    priv_src = save_folder + "/private_key.pem"
    pub_src = save_folder + "/public_key.pem"
    sym_src = save_folder + "/symmetric_key.key"
    rsa = True
    for fl in target_files:
        if os.path.getsize(fl) > 446:
            rsa = False
    if rsa:
        rsa_key(pub_src, priv_src, passkey)
    else:
        mixed_key(
            pub_src,
            priv_src,
            sym_src,
            passkey
        )

def just_key_manager(mode, save_folder, passkey):
    """Call either the `rsa_key` function or the `mixed_key`
    function, according to passed mode.
    
    Keyword arguments:
    mode -- either 0 (RSA) or 1 (Mixed)
    save_folder -- the directory to save the keys
    passkey -- the password to enhance the RSA encryption (OPTIONAL)
    """
    rsa = True if mode == 0 else False
    pub_src = save_folder + "/public_key.pem"
    priv_src = save_folder + "/private_key.pem"
    sym_src = save_folder + "/symmetric_key.key"
    if rsa:
        rsa_key(pub_src, priv_src, passkey)
    else:
        mixed_key(pub_src, priv_src, sym_src, passkey)
    success("key")