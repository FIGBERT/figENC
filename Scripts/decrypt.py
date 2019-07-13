from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet


def rsa_dec(target_file_raw, save_folder, passkey):
    """Decrypt all files passed to the function with the symmetric key,
    and then replace the symmetric key file's contents with the decrypted
    version, decrypted with the private key.

    Keyword arguements:
    target_file_raw -- a string composed of file locations seperated by colons
    save_folder -- the location of the saved key trio
    passkey -- the passkey used to enhance the encryption algorithm (OPTIONAL)
    """
    #Turning target_file_raw from a list in string form to a list
    target_file_list = target_file_raw.split(":")
    if save_folder[-1] != "/":
        save_folder += "/"
    #Determining the key source
    private_key_source = save_folder + "private_key.pem"
    symmetric_key_source = save_folder + "symmetric_key.key"
    #Creating the keys from the source files
    with open(private_key_source, "rb") as private_key_file, \
        open(symmetric_key_source, "rb") as symmetric_key_file:
        if passkey != "":
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password = bytes(passkey, "utf-8"),
                backend = default_backend()
                )
        else:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password = None,
                backend = default_backend()
            )
        encoded_key_data = symmetric_key_file.read()
        symmetric_key_data = private_key.decrypt(
            encoded_key_data,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
                )
            )
        symmetric_key = Fernet(symmetric_key_data)
    #Decrypting and outputting the data
    for target_file in target_file_list:
        with open(target_file, "rb") as open_file:
            encrypted_data = open_file.read()
            original_message = symmetric_key.decrypt(encrypted_data)
            open_file.write(original_message)
    #Outputting the decrypted symmetric key
    with open(symmetric_key_source, "wb") as symmetric_file:
        symmetric_file.write(symmetric_key_data)