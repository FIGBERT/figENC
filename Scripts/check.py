from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os, inspect, sys
import prompts

def password_check(first_pass, second_pass):
    """Returns `True` is the two passed strings match,
    `False` otherwise.
    
    Keyword arguments:
    first_pass -- the first password/string
    second_pass -- the second password/string
    """
    if first_pass == second_pass:
        return True
    else:
        return False


# def find_path(filename):
#     """Return the correct filepath if you are running
#     figENC as a bundled application
    
#     Keyword arguments:
#     filename -- the filename to convert to a filepath
#     """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, filename)


def find_path(file):
        """Return the correct filepath if you are running
        figENC as a script

        Keyword arguments:
        file -- the filename to convert to a filepath
        """
        return os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        ) + "/{}".format(file)


def key_enc(files, pass1, pass2, key_dir):
    """Return `True` if all of the conditions are valid
    for fresh-key passworded encryption. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    files -- a tuple of filepaths
    pass1 -- the first password
    pass2 -- the second password confirmation
    key_dir -- the directory where the keys are to be saved
    """
    broken_paths = ""
    for fl in files:
        if not os.access(fl, os.W_OK):
            broken_paths += (fl + "\n")
        else:
            continue
    password_match = password_check(pass1, pass2)
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    priv = key_dir + "/private_key.pem"
    pub = key_dir + "/public_key.pem"
    sym = key_dir + "/symmetric_key.key"
    write_key = prompts.overwrite_prompt() if os.path.exists(priv) or os.path.exists(pub) or os.path.exists(sym) else True
    if broken_paths == "" and password_match and key_dir_access and write_key:
        return True
    elif not write_key:
        return False
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not password_match:
            prompts.password_error()
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        return False


def weak_key_enc(files, key_dir):
    """Return `True` if all of the conditions are valid
    for fresh-key passwordless encryption. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    files -- a tuple of filepaths
    key_dir -- the directory where the keys are to be saved
    """
    broken_paths = ""
    for fl in files:
        if not os.access(fl, os.W_OK):
            broken_paths += (fl + "\n")
        else:
            continue
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    priv = key_dir + "/private_key.pem"
    pub = key_dir + "/public_key.pem"
    sym = key_dir + "/symmetric_key.key"
    write_key = prompts.overwrite_prompt() if os.path.exists(priv) or os.path.exists(pub) or os.path.exists(sym) else True
    if broken_paths == "" and key_dir_access and write_key:
        return True
    elif not write_key:
        return False
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        return False


def enc(files, key_dir):
    """Return `True` if all of the conditions are valid
    for generated key encryption. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    files -- a tuple of filepaths
    key_dir -- the directory where the keys are located
    """
    broken_paths = ""
    rsa = True
    for fl in files:
        if not os.access(fl, os.W_OK):
            broken_paths += (fl + "\n")
        if os.path.getsize(fl) > 446:
            rsa = False
    pub = key_dir + "/public_key.pem"
    sym = key_dir + "/symmetric_key.key"
    proper_keys = True if (os.path.exists(pub) and rsa) or (not rsa and os.path.exists(pub) and os.path.exists(sym)) else False
    if broken_paths == "" and proper_keys:
        return True
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not proper_keys:
            prompts.missing_keys(key_dir)


def key(key_dir, pass1, pass2):
    """Return `True` if all of the conditions are valid
    for generating passworded keys. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    key_dir -- the directory where are to be saved
    pass1 -- the first password
    pass2 -- the second confirmation password
    """
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    password_match = password_check(pass1, pass2)
    priv = key_dir + "/private_key.pem"
    pub = key_dir + "/public_key.pem"
    sym = key_dir + "/symmetric_key.key"
    write_key = prompts.overwrite_prompt() if os.path.exists(priv) or os.path.exists(pub) or os.path.exists(sym) else True
    if key_dir_access and write_key and password_match:
        return True
    else:
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        if not password_match:
            prompts.password_error()
        return False


def weak_key(key_dir):
    """Return `True` if all of the conditions are valid
    for generating passwordless keys. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    key_dir -- the directory where are to be saved
    """
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    priv = key_dir + "/private_key.pem"
    pub = key_dir + "/public_key.pem"
    sym = key_dir + "/symmetric_key.key"
    write_key = prompts.overwrite_prompt() if os.path.exists(priv) or os.path.exists(pub) or os.path.exists(sym) else True
    if key_dir_access and write_key:
        return True
    else:
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        return False


def dec(files, pass1, pass2, key_dir):
    """Return `True` if all of the conditions are valid
    for passworded decryption. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    files -- a tuple of filepaths
    pass1 -- the first password
    pass2 -- the second confirmation password
    key_dir -- the directory where the keys are located
    """
    broken_paths = ""
    rsa = True
    for fl in files:
        if not os.access(fl, os.W_OK):
            broken_paths += fl + "\n"
        with open(fl, "rb") as read_file:
            tag = read_file.read()[-1]
        if tag == 49:
            rsa = False
    password_match = password_check(pass1, pass2)
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    priv = key_dir + "/private_key.pem"
    sym = key_dir + "/symmetric_key.key"
    proper_keys = True if (rsa and os.path.exists(priv)) or (not rsa and os.path.exists(priv) and os.path.exists(sym)) else False
    correct_pass = True
    with open(priv, "rb") as priv_src:
        try:
            serialization.load_pem_private_key(
                priv_src.read(),
                password=bytes(pass1, "utf-8"),
                backend=default_backend()
            )
        except ValueError:
            correct_pass = False
    if (
        broken_paths == "" and key_dir_access
        and password_match and proper_keys
        and correct_pass
    ):
        return True
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        if not password_match:
            prompts.password_error()
        if not proper_keys:
            prompts.missing_keys(key_dir)
        if not correct_pass:
            prompts.wrong_pass()
        return False
    

def weak_dec(files, key_dir):
    """Return `True` if all of the conditions are valid
    for passwordless decryption. Otherwise, return
    `False` and prompt the user of the errors.

    Keyword arguments:
    files -- a tuple of filepaths
    key_dir -- the directory where the keys are located
    """
    broken_paths = ""
    rsa = True
    for fl in files:
        if not os.access(fl, os.W_OK):
            broken_paths += fl + "\n"
        with open(fl, "rb") as read_file:
            tag = read_file.read()[-1]
        if tag == 49:
            rsa = False
    key_dir_access = True if os.access(key_dir, os.W_OK) else False
    priv = key_dir + "/private_key.pem"
    sym = key_dir + "/symmetric_key.key"
    proper_keys = True if (rsa and os.path.exists(priv)) or (not rsa and os.path.exists(priv) and os.path.exists(sym)) else False
    if proper_keys:
        with open(priv, "rb") as priv_src:
            try:
                serialization.load_pem_private_key(
                    priv_src.read(),
                    password=None,
                    backend=default_backend()
                )
                need_pass = False
            except TypeError:
                need_pass = True
    else:
        need_pass = False
    if broken_paths == "" and key_dir_access and proper_keys and not need_pass:
        return True
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        if not proper_keys:
            prompts.missing_keys(key_dir)
        if need_pass:
            prompts.encrypted_keys()
        return False