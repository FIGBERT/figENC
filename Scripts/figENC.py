from sys import platform
import tkinter as tk
from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec

crypto_mode = ""


def setup(mode):
    """"Change the GUI to match the app mode,
    based on the user's action_list selection.

    Keyword arguments:
    mode -- an int (0-6) corresponding with the action_list selection
    """
    mode = mode[0]
    global crypto_mode
    if mode == 0: #Encrypt with fresh keys (password locked)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        file_frame.pack(fill = "both")
        file_label.config(text = "Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill = "x")
        passcode_frame.pack(fill = "both")
        passcode_label.config(text = "Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text = (
                "CRITICAL: DO NOT FORGET YOUR"
                "PASSCODE.\nWITHOUT IT, "
                "YOUR DATA WILL BE LOST."
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Save location for keys")
        save_label.pack()
        save_instructions.config(
            text = (
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                "folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Encrypt file/s")
        submit.pack(pady = "10")
        crypto_mode = "key_enc"
    elif mode == 1: #Encrypt with fresh keys (no password)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        file_frame.pack(fill = "both")
        file_label.config(text = "Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Save location for keys")
        save_label.pack()
        save_instructions.config(
            text = (
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                "folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Encrypt file/s")
        submit.pack(pady = "10")
        crypto_mode = "weak_key_enc"
    elif mode == 2: #Encrypt with generated keys
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        file_frame.pack(fill = "both")
        file_label.config(text = "Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Key location")
        save_label.pack()
        save_instructions.config(text = "Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Encrypt file/s")
        submit.pack(pady = "10")
        crypto_mode = "enc"
    elif mode == 3: #Decrypt with generated keys (password locked)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        file_frame.pack(fill = "both")
        file_label.config(text = "Filepath/s to the file/s to decrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill = "x")
        passcode_frame.pack(fill = "both")
        passcode_label.config(text = "Private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text = (
                "Passcode must be the same "
                "passcode used when the keys were created"
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Key location")
        save_label.pack()
        save_instructions.config(text = "Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Decrypt file/s")
        submit.pack(pady = "10")
        crypto_mode = "dec"
    elif mode == 4: #Decrypt with generated keys (no password)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        file_frame.pack(fill = "both")
        file_label.config(text = "Filepath/s to the file/s to decrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Key location")
        save_label.pack()
        save_instructions.config(text =" Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Decrypt file/s")
        submit.pack(pady = "10")
        crypto_mode = "weak_dec"
    elif mode == 5: #Only create fresh keys (password locked)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        passcode_frame.pack(fill = "both")
        passcode_label.config(text = "Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text = (
                "CRITICAL: DO NOT FORGET YOUR PASSCODE.\nWITHOUT IT, "
                "YOUR DATA WILL BE LOST."
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill = "x")
        save.pack(fill = "both")
        save_label.config(text = "Save location for keys")
        save_label.pack()
        save_instructions.config(
            text = (
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                "folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Create keys")
        submit.pack(pady = "10")
        crypto_mode = "just_key"
    elif mode == 6: #Only create fresh keys (no password)
        file_frame.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        reset_text(file_input)
        file_input.pack_forget()
        passcode_frame.pack_forget()
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        reset_text(passcode_input)
        passcode_input.pack_forget()
        save.pack_forget()
        save_label.pack_forget()
        save_instructions.pack_forget()
        reset_text(save_input)
        save_input.pack_forget()
        submit.pack_forget()
        save.pack(fill = "both")
        save_label.config(text = "Save location for keys")
        save_label.pack()
        save_instructions.config(
            text = (
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                "folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill = "both")
        submit.config(text = "Create keys")
        submit.pack(pady = "10")
        crypto_mode = "weak_key"


def reset_text(entry_widget):
    """Reset the string value of a tk.Entry object to an empty string
    
    Keyword arguments:
    entry_widget -- a tk.Entry object
    """
    entry_widget.delete(0,tk.END)
    entry_widget.insert(0,"")


def go(mode, save_folder=None, target_file=None, passkey=None):
    """Perform the action corresponding to the mode,
    using the input data from the user

    Keyword arguments:
    mode -- the mode defined by setup() from action_list
    save_folder -- the folder where the keys are or will be stored (OPTIONAL)
    target_file -- the file to encrypt or decrypt (OPTIONAL)
    passkey - the access code to the RSA keys that have them (OPTIONAL)
    """
    if mode == "key_enc":
        rsa_key(passkey, save_folder)
        rsa_enc(target_file, save_folder)
    elif mode == "weak_key_enc":
        rsa_key(passkey, save_folder)
        rsa_enc(target_file, save_folder)
    elif mode == "enc":
        rsa_enc(target_file, save_folder)
    elif mode == "dec":
        rsa_dec(target_file, save_folder, passkey)
    elif mode == "weak_dec":
        rsa_dec(target_file, save_folder, passkey)
    elif mode == "just_key":
        rsa_key(passkey, save_folder)
    elif mode == "weak_key":
        rsa_key(passkey, save_folder)


root = tk.Tk()
root.wm_title("figENC")
canvas = tk.Canvas(root, height = 700, width = 500)
canvas.pack()
frame = tk.Frame(root, bg = "#1A181C")
frame.place(relwidth = 1, relheight = 1)

header = tk.Label(
    frame,
    text = "figENC",
    justify = tk.CENTER,
    font = ("Arial", "24"),
    bg = "#643181",
    fg = "#B494C7"
)
subheader = tk.Label(
    frame,
    text = "Industry leading encryption by FIGBERT",
    justify = tk.CENTER,
    font = ("Arial", "18"),
    bg = "#643181",
    fg = "#B494C7",
    pady = "5"
)
header.pack(fill = "x", side = "top")
subheader.pack(fill = "x", side = "top")

action = tk.Frame(frame, bg = "#1A181C", pady = "5")
action.pack(fill = "both")
action_label = tk.Label(
    action,
    text = "Action:",
    justify = tk.LEFT,
    font = ("Arial", "14"),
    bg = "#1A181C",
    fg = "#ACA0B2",
)
action_label.pack()
action_list = tk.Listbox(
    action,
    font = ("Arial", "12"),
    bg = "#1A181C",
    fg = "#B494C7",
    selectbackground = "#643181",
    selectmode = tk.SINGLE,
    height = 7,
    relief = tk.SUNKEN
)
action_list.insert(1, "Encrypt with fresh keys (password locked)")
action_list.insert(2, "Encrypt with fresh keys (no password)")
action_list.insert(3, "Encrypt with generated keys")
action_list.insert(4, "Decrypt with generated keys (password locked)")
action_list.insert(5, "Decrypt with generated keys (no password)")
action_list.insert(6, "Only create fresh keys (password locked)")
action_list.insert(7, "Only create fresh keys (no password)")
action_list.pack(fill = "both", pady = "10")
if platform == "darwin":
    submit_action = tk.Button(
        action,
        text = "Begin Process",
        font = ("Arial", "12"),
        fg = "#643181",
        highlightthickness = 0,
        highlightbackground = "#1A181C",
        pady = "3",
        command = lambda: setup(action_list.curselection())
    )
else:
    submit_action = tk.Button(
        action,
        text = " Begin Process",
        font = ("Arial", "12"),
        bg = "#643181",
        fg = "#B494C7",
        command = lambda: setup(action_list.curselection())
    )
submit_action.pack()

step_two = tk.Frame(frame, bg = "#1A181C")
step_two.pack(fill = "both")
file_frame = tk.Frame(step_two, bg = "#1A181C", pady = "8")
file_label = tk.Label(
    file_frame,
    text = "If you see this, the app broke",
    font = ("Arial", "14"),
    bg = "#1A181C",
    fg = "#ACA0B2"
)
file_instructions = tk.Label(
    file_frame,
    text = "Separate filepaths with colons (:)",
    font = ("Arial", "11"),
    bg = "#1A181C",
    fg = "#B494C7"
)
file_input = tk.Entry(
    file_frame,
    font = ("Arial", "12"),
    justify = tk.CENTER,
    textvariable = tk.StringVar,
    bg = "#1A181C",
    fg = "#ACA0B2",
    insertbackground = "#ACA0B2",
    relief = tk.SUNKEN
)
passcode_frame = tk.Frame(step_two, bg = "#1A181C", pady = "8")
passcode_label = tk.Label(
    passcode_frame,
    text = "If you see this, the app broke",
    font = ("Arial", "14"),
    bg = "#1A181C",
    fg = "#ACA0B2"
)
passcode_instructions = tk.Label(
    passcode_frame,
    text = "If you see this, the app broke",
    font = ("Arial", "11"),
    bg = "#1A181C",
    fg = "#B494C7"
)
passcode_input = tk.Entry(
    passcode_frame,
    font = ("Arial", "12"),
    justify = tk.CENTER,
    textvariable = tk.StringVar,
    relief = tk.SUNKEN,
    show = "*",
    bg = "#1A181C",
    fg = "#ACA0B2",
    insertbackground = "#ACA0B2"
)
save = tk.Frame(step_two, bg = "#1A181C", pady = "8")
save_label = tk.Label(
    save,
    text = "Save location for keys",
    font = ("Arial", "14"),
    bg = "#1A181C",
    fg = "#ACA0B2"
)
save_instructions = tk.Label(
    save,
    text = "If you see this, the app broke",
    font = ("Arial", "11"),
    bg = "#1A181C",
    fg = "#B494C7"
)
save_input = tk.Entry(
    save,
    font = ("Arial", "12"),
    justify = tk.CENTER,
    textvariable = tk.StringVar,
    bg = "#1A181C",
    fg = "#ACA0B2",
    insertbackground = "#ACA0B2",
    relief = tk.SUNKEN
)
if platform == "darwin":
    submit = tk.Button(
        save,
        text = "If you see this, the app broke",
        font = ("Arial", "12"),
        fg = "#643181",
        highlightbackground = "#1A181C",
        highlightthickness = 0,
        pady = "3",
        command = lambda: go(
            mode = crypto_mode,
            save_folder = save_input.get(),
            target_file = file_input.get(),
            passkey = passcode_input.get()
        )
    )
else:
    submit = tk.Button(
        save,
        text = "If you see this, the app broke",
        font = ("Arial", "12"),
        bg = "#643181",
        fg = "#B494C7",
        pady = "3",
        command = lambda: go(
            mode = crypto_mode,
            save_folder = save_input.get(),
            target_file = file_input.get(),
            passkey = passcode_input.get()
        )
    )

root.mainloop()