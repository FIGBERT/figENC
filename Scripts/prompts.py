from tkinter import messagebox
from random import choice


def overwrite_prompt():
    """Opens a tkinter messagebox asking if the user wants to
    overwrite the previously generated keys detected in the provided
    savefolder. Returns `True` if the user clicks ok, `False` if they
    click cancel.
    """
    return messagebox.askokcancel(
        "Overwrite Warning",
        (
            "The directory selected contains previously generated keys."
            " If you choose to continue, these keys will be overwritten"
            " and any files encrypted using these keys will be lost forever."
            "\n\nContinue?"
        )
    )

def password_error():
    """"Raise an error informing the user that the provided passwords
    do not match.
    """
    messagebox.showwarning(
        "Passwords Do Not Match",
        "The passwords provided do not match. Please try again."
    )

def encrypted_keys():
    messagebox.showwarning(
        "Keys are Password Locked",
        (
            "The keys provided are encrypted, and require a password to "
            "function. Please attempt decryption again with a password."
        )
    )

def file_access_error(broken_paths):
    """Raise an error informing the user that some files aren't
    accessible by figENC.

    Keyword arguments:
    broken_paths -- a string with newlines seperating filepaths
    """
    messagebox.showwarning(
        "Filepath Access Failure",
        (
            "figENC can't access some of the files provided:\n\n"
            "Broken Paths:\n%s"%broken_paths
        )
    )

def key_dir_error(folder):
    """Raise an error informing the user that the key directory isn't
    accessible by figENC.

    Keyword arguments:
    folder -- a directory filepath string
    """
    messagebox.showwarning(
        "Directory Access Failure",
        (
            "The key directory provided cannot be accessed by figENC."
            " Please try again with a new directory.\n\nDirectory"
            " provided:\n%s"%folder
        )
    )

def missing_keys(folder):
    """Raise an error informing the user that some keys are missing
    from the passed directory

    Keyword arguments:
    folder -- a directory filepath string
    """
    messagebox.showwarning(
        "Directory Missing Keys",
        (
            "The directory provided is missing keys critical to encrypting"
            " files. Please correct and try again.\n\nDirectory provided:"
            "\n%s"%folder
        )
    )

def wrong_pass():
    messagebox.showwarning(
        "Incorrect Password",
        "The password provided is incorrect. Please try again."
    )

def success(mode):
    """Inform the user of the processes succesful completion
    with a fun message/reference.
    """
    if "enc" in mode or "key" in mode:
        lst = "enc"
    else:
        lst = "dec"
    fun_messages = {
        "enc": [
            "Proceed into cyberspace with confidence.",
            "*applause*",
            "Congratulations, prince of darkness.",
            "Don't delete the .dat file",
            "You can remove your hoodie now.",
            "D*ck pic hidden.",
            "Time to take over the world.",
            "Mainframe secured.",
            "Don't steal my nuts!",
            "Probably a little overkill"
        ],
        "dec": [
            "Proceed into cyberspace with confidence.",
            "*applause*",
            "Congratulations, prince of darkness.",
            "Don't delete the .dat file",
            "You can remove your hoodie now.",
            "From nothing to something.",
            "Time to take over the world.",
            "Mainframe secured.",
            "Don't steal my nuts!",
            ("Like pulling a rabbit from a hat, but with lots of math,"
            " computers, and it's actually nothing like pulling a rabbit"
            " from a hat.")
        ]
    }
    messagebox.showinfo(
        "Success",
        "The operation was complete. %s"%choice(fun_messages[lst])
    )