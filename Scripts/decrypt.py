import os
from check import find_path
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
    print("3. Reached the decryption for loop")
    for target_file in target_file_list:
        with open(target_file, "rb") as read_file:
            content = read_file.read()
        print("4. Opened the target file")
        if content[-1] == 48:
            print("5. Dectected encryption type as RSA")
            with open(private_key_source, "rb") as private_key_file:
                if passkey != "":
                    print("6. Passcode")
                    private_key = serialization.load_pem_private_key(
                        private_key_file.read(),
                        password = bytes(passkey, "utf-8"),
                        backend = default_backend()
                    )
                else:
                    print("6. No passcode")
                    private_key = serialization.load_pem_private_key(
                        private_key_file.read(),
                        password = None,
                        backend = default_backend()
                    )
            print("7. Private key loaded")
            encrypted_data = content[:-1]
            print("8. Removed final character from encrypted data")
            original_message = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("9. Decrypted data")
            with open(target_file, "wb") as write_file:
                write_file.write(original_message)
            print("10. Wrote decrypted data to file")
        elif content[-1] == 49:
            print("5. Detected the encryption type as symmetric")
            with open(private_key_source, "rb") as private_key_file, \
                open(symmetric_key_source, "rb") as symmetric_key_file:
                if passkey != "":
                    print("6. Passcode")
                    private_key = serialization.load_pem_private_key(
                        private_key_file.read(),
                        password = bytes(passkey, "utf-8"),
                        backend = default_backend()
                    )
                else:
                    print("6. Passcode")
                    private_key = serialization.load_pem_private_key(
                        private_key_file.read(),
                        password = None,
                        backend = default_backend()
                    )
                print("7. Private key loaded")
                encoded_key_data = symmetric_key_file.read()
                print("8. Symmetric key loaded")
            symmetric_key_data = private_key.decrypt(
                encoded_key_data,
                padding.OAEP(
                    mgf = padding.MGF1(algorithm = hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )
            print("9. Symmetric key data activated")
            symmetric_key = Fernet(symmetric_key_data)
            print("10. Symmetric key activated")
            #Decrypting and outputting the data
            encrypted_data = content[:-1]
            print("11. Removed final characted from encrypted data")
            original_message = symmetric_key.decrypt(encrypted_data)
            print("12. Decrypted data")
            with open(target_file, "wb") as write_file:
                write_file.write(original_message)
            print("13. Wrote decrypted data to file")
    if os.path.exists(symmetric_key_source):
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
        with open(symmetric_key_source, "wb") as symmetric_out:
            symmetric_out.write(symmetric_key_data)