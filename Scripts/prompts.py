from tkinter import messagebox


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

def file_access_error(broken_paths):
    messagebox.showwarning(
        "Filepath Access Failure",
        (
            "figENC can't access some of the files provided:\n\n"
            "Broken Paths:\n%s"%broken_paths
        )
    )

def key_dir_error(folder):
    messagebox.showwarning(
        "Directory Access Failure",
        (
            "The key directory provided cannot be accessed by figENC."
            " Please try again with a new directory.\n\nDirectory"
            " provided:\n%s"%folder
        )
    )

def missing_keys(folder):
    messagebox.showwarning(
        "Directory Missing Keys",
        (
            "The directory provided is missing keys critical to encrypting"
            " files. Please correct and try again.\n\nDirectory provided:"
            "\n%s"%folder
        )
    )