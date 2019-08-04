import errno
import os
from os import makedirs, path
import tempfile
import inspect
import sys
from sys import platform
import tkinter as tk
from tkinter import messagebox

#Windows-specific error code indicating an invalid pathname
ERROR_INVALID_NAME = 123


def is_pathname_valid(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname for the current
    OS, and `False` otherwise. If the pathname provided is either not a string
    or is a string but is empty, return `False`.
    '''
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        #Strips this pathname's Windows-specific drive specifier (e.g., `C:\`)
        #if any.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True


def is_path_creatable(pathname: str) -> bool:
    '''
    Return `True` if the current user has sufficient permissions to create the
    passed pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname for the current
    OS and either currently exists or is hypothetically createable; `False
    otherwise.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False


def is_path_sibling_creatable(pathname: str) -> bool:
    '''
    Return `True` if the current user has sifficient permissions to create
    siblings (arbitrary files in the parent directory) of the passed pathname,
    and `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        # Opening and immediately closing the temporary file
        with tempfile.TemporaryFile(dir=dirname): pass
        return True
    # All exceptions fall under the EnvironmentError subclass
    except EnvironmentError:
        return False


def is_path_exists_or_creatable_portable(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname on the current OS
    and either currently exists or is hypothetically creatable in a
    cross-platform manner optimized for POSIX-unfriendly filesystems; `False`
    otherwise.
    Never raises errors.
    '''
    try:
        # Calls is_pathname_valid() first to prevent "os" module from raising
        # undesirable exceptions on invalid pathnames
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_sibling_creatable(pathname))
    except OSError:
        pass


def overwrite():
    """Raise an error informing the user that the provided folder
    where they wish to write the keys has keys in that will be
    overwritten if they continue. Returns `True` if they wish to
    overwrite the keys, `False` otherwise.
    """
    return messagebox.askokcancel(
        "Overwrite Keys",
        (
        "The savefolder provided already has keys stored. If you continue, "
        "these keys will be overwritten and any files encrypted with them "
        "will be lost forever.\n\nContinue?"
        )
    )


def missing_key_error(save_folder):
    """Raise an error informing the user that the provided folder
    where the keys should be stored is missing the required keys.
    """
    messagebox.showwarning(
        "Missing Keys",
        (
        "The savefolder provided is missing the required keys to perform "
        "the requested operation. Please correct this and try again."
        "\n\nFolder Provided:\n%s" % save_folder
        )
    )


def path_error(paths):
    """Raise an error informing the user that the provided pathnames
    are invalid.

    Arguments:
    paths -- all of the broken filepaths
    """
    messagebox.showwarning(
        "Path Error",
        (
        "One or more of the filepaths provided are invalid."
        "\nCheck that the filepath was entered correctly, or that the user "
        "has permission to edit the file."
        "\n\nBroken Filepaths:\n%s" % paths
        )
    )

def password_error(one, two):
    """"Raise an error informing the user that the provided passwords
    do not match.
    """
    messagebox.showwarning(
        "Passwords Do Not Match",
        ("The passwords provided do not match. Please Try again."
        "\n\nFirst: {}\nSecond: {}".format(one, two)
        )
    )

def password_check(first_pass, second_pass):
    if first_pass == second_pass:
        return True
    else:
        password_error(first_pass, second_pass)
        return False


def find_path(filename):
    """Return the filepath from the filename when running from a
    pyinstaller onefile application.
    
    Keyword arguments:
    filename -- the filename to convert to a filepath
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller >= 1.6
        os.chdir(sys._MEIPASS)
        filename = os.path.join(sys._MEIPASS, filename)
    elif '_MEIPASS2' in os.environ:
        # PyInstaller < 1.6 (tested on 1.5 only)
        os.chdir(os.environ['_MEIPASS2'])
        filename = os.path.join(os.environ['_MEIPASS2'], filename)
    else:
        os.chdir(os.path.dirname(sys.argv[0]))
        filename = os.path.join(os.path.dirname(sys.argv[0]), filename)
    return filename


# def find_path(file):
#         """Return the correct filename if you are running it as a script"""
#         return os.path.dirname(
#             os.path.abspath(
#                 inspect.getfile(
#                     inspect.currentframe()
#                 )
#             )
#         ) + "/{}".format(file)


def quick_check(mode, target_file_raw=None, save_folder=None):
    """Return `True` only if both the target file and save folder provided
    by the user are valid pathnames (If the save folder is createable but does
    not exist, it will be created). Otherwise, return `False` and notify the
    user with an error messagebox.
    
    Keyword arguments:
    target_file_raw -- a string list of pathnames
    save_folder -- a string pathname to a directory
    """
    save_folder += "/" if save_folder[-1] is not "/" else ""
    if mode is not "just_key" or mode is not "weak_key":
        target_file_list = target_file_raw.split(":")
        targets_exist = True
        broken_paths = ""
        for target_file in target_file_list:
            if targets_exist:
                if not os.path.exists(target_file):
                    target_file = False
                    broken_paths += (target_file + "\n")
            else:
                if not os.path.exists(target_file):
                    broken_paths += (target_file + "\n")
        if not targets_exist:
            path_error(broken_paths)
            return False
    if (
        mode is "just_key"
        or mode is "weak_key"
        or mode is "key_enc"
        or mode is "weak_key_enc"
    ):
        if platform is "win32":
            if is_path_exists_or_creatable_portable(save_folder):
                try:
                    os.makedirs(save_folder)
                    return True
                except OSError:
                    if (
                        os.path.exists(save_folder + "symmetric_key.key")
                        or os.path.exists(save_folder + "private_key.pem")
                        or os.path.exists(save_folder + "public_key.pem")
                    ):
                        return overwrite()
                    else:
                        return True
            else:
                return False
        else:
            if is_path_exists_or_creatable(save_folder):
                try:
                    os.makedirs(save_folder)
                    return True
                except OSError:
                    if (
                        os.path.exists(save_folder + "symmetric_key.key")
                        or os.path.exists(save_folder + "private_key.pem")
                        or os.path.exists(save_folder + "public_key.pem")
                    ):
                        return overwrite()
                    else:
                        return True
            else:
                return False
    elif mode is "dec" or mode is "weak_dec":
        encryption_type = ""
        for target_file in target_file_list:
            with open(target_file, "rb") as read_file:
                content = read_file.read()
            if (
                content[-1] == b"1"
                and (encryption_type is "" or encryption_type is "SYM")
            ):
                encryption_type = "SYM"
            elif (
                content[-1] == b"1"
                and (encryption_type is "RSA" or encryption_type is "MIX")
            ):
                encryption_type = "MIX"
            elif (
                content[-1] == b"0"
                and (encryption_type is "" or encryption_type is "RSA")
            ):
                encryption_type = "RSA"
            elif (
                content[-1] == b"0"
                and (encryption_type is "SYM" or encryption_type is "MIX")
            ):
                encryption_type = "MIX"
        if encryption_type is "RSA":
            if platform is "win32":
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
            else:
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
        else:
            if platform is "win32":
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                        and os.path.exists(save_folder + "symmetric_key.key")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
            else:
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                        and os.path.exists(save_folder + "symmetric_key.key")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
    else:
        encryption_type = ""
        for target_file in target_file_list:
            if (
                os.path.getsize(target_file) > 446
                and (encryption_type is "" or encryption_type is "SYM")
            ):
                encryption_type = "SYM"
            elif (
                os.path.getsize(target_file) > 446
                and (encryption_type is "RSA" or encryption_type is "MIX")
            ):
                encryption_type = "MIX"
            elif (
                os.path.getsize(target_file) <= 446
                and (encryption_type is "" or encryption_type is "RSA")
            ):
                encryption_type = "RSA"
            elif (
                os.path.getsize(target_file) <= 446
                and (encryption_type is "SYM" or encryption_type is "MIX")
            ):
                encryption_type = "MIX"
        if encryption_type is "RSA":
            if platform is "win32":
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
            else:
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
        else:
            if platform is "win32":
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                        and os.path.exists(save_folder + "symmetric_key.key")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False
            else:
                if os.path.exists(save_folder):
                    if (
                        os.path.exists(save_folder + "private_key.pem")
                        and os.path.exists(save_folder + "public_key.pem")
                        and os.path.exists(save_folder + "symmetric_key.key")
                    ):
                        return True
                    else:
                        missing_key_error(save_folder)
                        return False
                else:
                    return False