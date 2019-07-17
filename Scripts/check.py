import errno
import os
from os import makedirs, path
import tempfile
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


def path_error(*args):
    """Raise an error informing the user that the provided pathnames
    are invalid.

    Arguments:
    *args -- all of the broken filepaths
    """
    errors = ""
    num_errors = 0
    for arg in args:
        errors += (str(arg) + "\n")
        num_errors += 1
    messagebox.showwarning(
        "Path Error",
        (
        "One or more of the filepaths provided are invalid."
        "\nCheck that the filepath was entered correctly, or that the user "
        "has permission to edit the file."
        "\n\nBroken Filepaths:\n%s" % errors
        )
    )


def quick_check(mode, target_file=None, save_folder=None):
    """Return `True` only if both the target file and save folder provided
    by the user are valid pathnames (If the save folder is createable but does
    not exist, it will be created). Otherwise, return `False` and notify the
    user with an error messagebox.
    
    Keyword arguments:
    target_file -- a string pathname to a single file
    save_folder -- a string pathname to a directory
    """
    if mode is "just_key" or mode is "weak_key":
        if platform is "win32":
            if (is_path_exists_or_creatable_portable(save_folder)):
                try:
                    makedirs(save_folder)
                    return True
                except OSError:
                    if save_folder[-1] != "/":
                        save_folder += "/"
                    if (
                        path.exists(save_folder + "private_key.pem")
                        or path.exists(save_folder + "public_key.pem")
                        or path.exists(save_folder + "symmetric_key.key")
                    ):
                        return overwrite()
                    else:
                        return True
            else:
                return False
        else:
            if (is_path_exists_or_creatable(save_folder)):
                try:
                    makedirs(save_folder)
                    return True
                except OSError:
                    if save_folder[-1] != "/":
                        save_folder += "/"
                    if (
                        path.exists(save_folder + "private_key.pem")
                        or path.exists(save_folder + "public_key.pem")
                        or path.exists(save_folder + "symmetric_key.key")
                    ):
                        return overwrite()
                    else:
                        return True
            else:
                return False
    elif mode is "dec" or mode is "weak_dec" or mode is "enc":
        if (
            path.exists(target_file)
            and path.exists(save_folder)
        ):
            if save_folder[-1] is not "/":
                save_folder += "/"
            if mode is "enc":
                if (
                    path.exists(save_folder + "public_key.pem")
                    and path.exists(save_folder + "symmetric_key.key")
                ):
                    return True
                else:
                    missing_key_error(save_folder)
                    return False
            else:
                if (
                    path.exists(save_folder + "private_key.pem")
                    and path.exists(save_folder + "symmetric_key.key")
                ):
                    return True
                else:
                    missing_key_error(save_folder)
                    return False
        elif (
            path.exists(target_file)
            and not path.exists(save_folder)
        ):
            path_error(save_folder)
            return False
        elif (
            not path.exists(target_file)
            and path.exists(save_folder)
        ):
            path_error(target_file)
            return False
        elif (
            not path.exists(target_file)
            and not path.exists(save_folder)
        ):
            path_error(target_file, save_folder)
            return False
    else:
        if platform is "win32":
            if (
                path.exists(target_file)
                and is_path_exists_or_creatable_portable(save_folder)
            ):
                try:
                    makedirs(save_folder)
                    return True
                except OSError:
                    if save_folder[-1] != "/":
                        save_folder += "/"
                    if (
                        path.exists(save_folder + "private_key.pem")
                        or path.exists(save_folder + "public_key.pem")
                        or path.exists(save_folder + "symmetric_key.key")
                    ):
                        return overwrite()
                    else:
                        return True
            elif (
                path.exists(target_file)
                and not is_path_exists_or_creatable_portable(
                    save_folder
                )
            ):
                path_error(save_folder)
                return False
            elif (
                not path.exists(target_file)
                and is_path_exists_or_creatable_portable(save_folder)
            ):
                path_error(target_file)
                return False
            elif (
                not path.exists(target_file)
                and not is_path_exists_or_creatable_portable(
                    save_folder
                )
            ):
                path_error(target_file, save_folder)
                return False
        else:
            if (
                path.exists(target_file)
                and is_path_exists_or_creatable(save_folder)
            ):
                try:
                    makedirs(save_folder)
                    return True
                except OSError:
                    if save_folder[-1] != "/":
                        save_folder += "/"
                    if (
                        path.exists(save_folder + "private_key.pem")
                        or path.exists(save_folder + "public_key.pem")
                        or path.exists(save_folder + "symmetric_key.key")
                    ):
                        return overwrite()
                    else:
                        return True
            elif (
                path.exists(target_file)
                and not is_path_exists_or_creatable(save_folder)
            ):
                path_error(save_folder)
                return False
            elif (
                not path.exists(target_file)
                and is_path_exists_or_creatable(save_folder)
            ):
                path_error(target_file)
                return False
            elif (
                not path.exists(target_file)
                and not is_path_exists_or_creatable(save_folder)
            ):
                path_error(target_file, save_folder)
                return False

def password_check(first_pass, second_pass):
    if first_pass == second_pass:
        return True
    else:
        password_error(first_pass, second_pass)
        return False

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