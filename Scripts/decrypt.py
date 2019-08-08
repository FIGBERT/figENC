from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def rsa_dec(file, priv, passkey):
    with open(priv, "rb") as priv_src, \
            open(file, "rb") as read_file:
        private_key = serialization.load_pem_private_key(
            priv_src.read(),
            password=bytes(passkey, "utf-8") if passkey != "" else None,
            backend=default_backend()
        )
        content = read_file.read()[:-1]
    original_message = private_key.decrypt(
        content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(file, "wb") as write_file:
        write_file.write(original_message)

def mixed_dec(file, priv, sym, passkey):
    with open(priv, "rb") as priv_src, \
            open(sym, "rb") as sym_src, \
            open(file, "rb") as read_file:
        private_key = serialization.load_pem_private_key(
            priv_src.read(),
            password=bytes(passkey, "utf-8") if passkey != "" else None,
            backend=default_backend()
        )
        sym_data = sym_src.read()
        try:
            sym_dec = private_key.decrypt(
                sym_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            symmetric_key = Fernet(sym_dec)
        except:
            symmetric_key = Fernet(sym_data)
        content = read_file.read()[:-1]
    original_message = symmetric_key.decrypt(content)
    with open(file, "wb") as write_file:
        write_file.write(original_message)


def dec_manager(files, key_dir, passkey):
    priv = key_dir + "/private_key.pem"
    sym = key_dir + "/symmetric_key.key"
    rsa = True
    for fl in files:
        with open(fl, "rb") as read_file:
            tag = read_file.read()[-1]
        if tag == 48:
            rsa_dec(fl, priv, passkey)
        else:
            mixed_dec(fl, priv, sym, passkey)
            rsa = False
    if not rsa:
        with open(priv, "rb") as priv_src, \
                open(sym, "rb") as sym_src:
            private_key = serialization.load_pem_private_key(
                priv_src.read(),
                password=bytes(passkey, "utf-8") if passkey != "" else None,
                backend=default_backend()
            )
            sym_data = sym_src.read()
            try:
                sym_dec = private_key.decrypt(
                    sym_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            except:
                return None
        with open(sym, "wb") as sym_src:
            sym_src.write(sym_dec)