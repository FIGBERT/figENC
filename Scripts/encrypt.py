from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def rsa_enc(target_file_raw, save_folder):
    """Encrypt all files passed to the function with the symmetric key,
    and then replace the symmetric key file's contents with an encrypted
    version, encrypted with the public key.

    Keyword arguments:
    target_file_raw -- a string composed of file locations seperated by colons
    save_folder -- the location of the saved key trio
    """
    #Turning target_file_raw from a list in string form to a list
    target_file_list = target_file_raw.split(":")
    if save_folder[-1] != '/':
            save_folder += '/'
    #Determining the key source
    public_key_source = save_folder + 'public_key.pem'
    symmetric_key_source = save_folder + 'symmetric_key.key'
    for target_file in target_file_list:
        #Creating the keys from the source files
        with open(public_key_source, 'rb') as public_key_file, \
            open(symmetric_key_source, 'rb') as symmetric_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend = default_backend()
            )
            symmetric_key_data = symmetric_key_file.read()
            symmetric_key = Fernet(symmetric_key_data)
        #Encrypting and outputting the data
        with open(target_file) as read_file:
            file_data = read_file.read()
        data = symmetric_key.encrypt(bytes(file_data, 'utf-8'))
        with open(target_file, 'wb') as write_file:
            write_file.write(data)
    #Encrypting and outputting the symmetric key
    encrypted_key = public_key.encrypt(
        symmetric_key_data,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
            )
        )
    with open(symmetric_key_source, 'wb') as crypto_key_file:
        crypto_key_file.write(encrypted_key)