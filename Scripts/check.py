import os, inspect, sys
import prompts

def password_check(first_pass, second_pass):
    if first_pass == second_pass:
        return True
    else:
        return False


# def find_path(filename):
#     """Return the filepath from the filename when running from a
#     pyinstaller application.
    
#     Keyword arguments:
#     filename -- the filename to convert to a filepath
#     """
#     if hasattr(sys, '_MEIPASS'):
#         # PyInstaller >= 1.6
#         os.chdir(sys._MEIPASS)
#         filename = os.path.join(sys._MEIPASS, filename)
#     elif '_MEIPASS2' in os.environ:
#         # PyInstaller < 1.6 (tested on 1.5 only)
#         os.chdir(os.environ['_MEIPASS2'])
#         filename = os.path.join(os.environ['_MEIPASS2'], filename)
#     else:
#         os.chdir(os.path.dirname(sys.argv[0]))
#         filename = os.path.join(os.path.dirname(sys.argv[0]), filename)
#     return filename


def find_path(file):
        """Return the correct filename if you are running it as a script"""
        return os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        ) + "/{}".format(file)


def key_enc(files, pass1, pass2, key_dir):
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
            prompts.password_error(pass1, pass2)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        return False


def weak_key_enc(files, key_dir):
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


def key(key_dir):
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
    if broken_paths == "" and key_dir_access and password_match and proper_keys:
        return True
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        if not password_match:
            prompts.password_error(pass1, pass2)
        if not proper_keys:
            prompts.missing_keys(key_dir)
        return False
    

def weak_dec(files, key_dir):
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
    if broken_paths == "" and key_dir_access and proper_keys:
        return True
    else:
        if broken_paths != "":
            prompts.file_access_error(broken_paths)
        if not key_dir_access:
            prompts.key_dir_error(key_dir)
        if not proper_keys:
            prompts.missing_keys(key_dir)
        return False