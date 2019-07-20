from sys import platform
import tkinter as tk
from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec
import check


class AutoScrollbar(tk.Scrollbar):
    """Create a scrollbar that hides iteself if it's not needed. Only
    works if you use the pack geometry manager from tkinter.
    """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
        else:
            if self.cget("orient") == tk.HORIZONTAL:
                self.pack(fill=tk.X, side=tk.BOTTOM)
            else:
                self.pack(fill=tk.Y, side=tk.RIGHT)
        tk.Scrollbar.set(self, lo, hi)
    def grid(self, **kw):
        raise tk.TclError("cannot use grid with this widget")
    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")


class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


crypto_mode = ""


def reset():
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
    confirm_label.pack_forget()
    confirm_instructions.pack_forget()
    reset_text(confirm_input)
    confirm_input.pack_forget()
    save.pack_forget()
    save_label.pack_forget()
    save_instructions.pack_forget()
    reset_text(save_input)
    save_input.pack_forget()
    submit.pack_forget()


def setup(mode):
    """"Change the GUI to match the app mode,
    based on the user's action_list selection.

    Keyword arguments:
    mode -- an int (0-6) corresponding with the action_list selection
    """
    mode = mode[0]
    global crypto_mode
    if mode == 0: #Encrypt with fresh keys (password locked)
        reset()
        file_frame.pack(fill=tk.BOTH)
        file_label.config(text="Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill=tk.X)
        passcode_frame.pack(fill=tk.BOTH)
        passcode_label.config(text="Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text=(
                "CRITICAL: DO NOT FORGET YOUR"
                "PASSCODE.\nWITHOUT IT, "
                "YOUR DATA WILL BE LOST."
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill=tk.X)
        confirm_label.pack()
        confirm_instructions.pack()
        confirm_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Save location for keys")
        save_label.pack()
        save_instructions.config(
            text=(
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                " folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Encrypt file/s")
        submit.pack(pady="10")
        crypto_mode = "key_enc"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 1: #Encrypt with fresh keys (no password)
        reset()
        file_frame.pack(fill=tk.BOTH)
        file_label.config(text="Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Save location for keys")
        save_label.pack()
        save_instructions.config(
            text=(
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                " folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Encrypt file/s")
        submit.pack(pady="10")
        crypto_mode = "weak_key_enc"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 2: #Encrypt with generated keys
        reset()
        file_frame.pack(fill=tk.BOTH)
        file_label.config(text="Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Key location")
        save_label.pack()
        save_instructions.config(text="Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Encrypt file/s")
        submit.pack(pady="10")
        crypto_mode = "enc"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 3: #Decrypt with generated keys (password locked)
        reset()
        file_frame.pack(fill=tk.BOTH)
        file_label.config(text="Filepath/s to the file/s to decrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill=tk.X)
        passcode_frame.pack(fill=tk.BOTH)
        passcode_label.config(text="Private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text=(
                "Passcode must be the same "
                "passcode used when the keys were created"
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill=tk.X)
        confirm_label.pack()
        confirm_instructions.pack()
        confirm_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Key location")
        save_label.pack()
        save_instructions.config(text="Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Decrypt file/s")
        submit.pack(pady="10")
        crypto_mode = "dec"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 4: #Decrypt with generated keys (no password)
        reset()
        file_frame.pack(fill=tk.BOTH)
        file_label.config(text="Filepath/s to the file/s to decrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Key location")
        save_label.pack()
        save_instructions.config(text="Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Decrypt file/s")
        submit.pack(pady="10")
        crypto_mode = "weak_dec"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 5: #Only create fresh keys (password locked)
        reset()
        passcode_frame.pack(fill=tk.BOTH)
        passcode_label.config(text="Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(
            text=(
                "CRITICAL: DO NOT FORGET YOUR PASSCODE.\nWITHOUT IT, "
                "YOUR DATA WILL BE LOST."
            )
        )
        passcode_instructions.pack()
        passcode_input.pack(fill=tk.X)
        confirm_label.pack()
        confirm_instructions.pack()
        confirm_input.pack(fill=tk.X)
        save.pack(fill=tk.BOTH)
        save_label.config(text="Save location for keys")
        save_label.pack()
        save_instructions.config(
            text=(
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                " folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Create keys")
        submit.pack(pady="10")
        crypto_mode = "just_key"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))
    elif mode == 6: #Only create fresh keys (no password)
        reset()
        save.pack(fill=tk.BOTH)
        save_label.config(text="Save location for keys")
        save_label.pack()
        save_instructions.config(
            text=(
                "Save the keys to an empty folder, "
                "and store them somewhere secure\n"
                "If other key files exist in the same"
                " folder, they will be overwritten"
            )
        )
        save_instructions.pack()
        save_input.pack(fill=tk.BOTH)
        submit.config(text="Create keys")
        submit.pack(pady="10")
        crypto_mode = "weak_key"
        frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))


def reset_text(entry_widget):
    """Reset the string value of a tk.Entry object to an empty string
    
    Keyword arguments:
    entry_widget -- a tk.Entry object
    """
    entry_widget.delete(0,tk.END)
    entry_widget.insert(0,"")


def go(mode, save_folder=None, target_file=None, passkey=None, passcheck=None):
    """Perform the action corresponding to the mode,
    using the input data from the user, after checking the validity
    of the filepaths.

    Keyword arguments:
    mode -- the mode defined by setup() from action_list
    save_folder -- the folder where the keys are or will be stored (OPTIONAL)
    target_file -- the file to encrypt or decrypt (OPTIONAL)
    passkey - the access code to the RSA keys that have them (OPTIONAL)
    passcheck - the access code to the RSA keys that have them confirmed,
    to prevent spelling errors.
    """
    if check.quick_check(mode=mode, target_file_raw=target_file, save_folder=save_folder):
        if mode == "key_enc" and check.password_check(passkey, passcheck):
            rsa_key(passkey, save_folder)
            rsa_enc(target_file, save_folder)
        elif mode == "weak_key_enc":
            rsa_key(passkey, save_folder)
            rsa_enc(target_file, save_folder)
        elif mode == "enc":
            rsa_enc(target_file, save_folder)
        elif mode == "dec" and check.password_check(passkey, passcheck):
            rsa_dec(target_file, save_folder, passkey)
        elif mode == "weak_dec":
            rsa_dec(target_file, save_folder, passkey)
        elif mode == "just_key" and check.password_check(passkey, passcheck):
            rsa_key(passkey, save_folder)
        elif mode == "weak_key":
            rsa_key(passkey, save_folder)


root = tk.Tk()
vscrollbar = AutoScrollbar(root)
canvas = ResizingCanvas(root, yscrollcommand=vscrollbar.set, highlightthickness=0, bg="pink", height=700, width=700)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
vscrollbar.config(command=canvas.yview)
frame = tk.Frame(canvas, bg="#1A181C")
canvas.create_window(0, 0, anchor=tk.NW, window=frame)

header = tk.Label(
    frame,
    text="figENC",
    justify=tk.CENTER,
    font=("Arial", "22"),
    bg="#643181",
    fg="#F2DAFF",
    pady="2"
)
subheader = tk.Label(
    frame,
    text="Industry leading encryption by FIGBERT",
    justify=tk.CENTER,
    font=("Arial", "16"),
    bg="#643181",
    fg="#F2DAFF",
    pady="2"
)
header.pack(fill=tk.X, side="top")
subheader.pack(fill=tk.X, side="top")

action = tk.Frame(frame, bg="#1A181C", pady="5")
action.pack(fill=tk.BOTH)
action_label = tk.Label(
    action,
    text="Action:",
    justify=tk.LEFT,
    font=("Arial", "16"),
    bg="#1A181C",
    fg="#F2DAFF",
)
action_label.pack()
action_list = tk.Listbox(
    action,
    justify=tk.CENTER,
    font=("Arial", "14"),
    bg="#1A181C",
    fg="#ACA0B2",
    selectbackground="#643181",
    selectmode=tk.SINGLE,
    relief=tk.SUNKEN,
    height=7
)
action_list.insert(1, "Encrypt with fresh keys (password locked)")
action_list.insert(2, "Encrypt with fresh keys (no password)")
action_list.insert(3, "Encrypt with generated keys")
action_list.insert(4, "Decrypt with generated keys (password locked)")
action_list.insert(5, "Decrypt with generated keys (no password)")
action_list.insert(6, "Only create fresh keys (password locked)")
action_list.insert(7, "Only create fresh keys (no password)")
action_list.pack(fill=tk.BOTH, pady="10")
if platform == "darwin":
    submit_action = tk.Button(
        action,
        text="Begin Process",
        font=("Arial", "14"),
        fg="#643181",
        highlightthickness=0,
        pady="3",
        command=lambda: setup(action_list.curselection())
    )
else:
    submit_action = tk.Button(
        action,
        text="Begin Process",
        font=("Arial", "14"),
        bg="#643181",
        fg="#B494C7",
        command=lambda: setup(action_list.curselection())
    )
submit_action.pack()

step_two = tk.Frame(frame, bg="#1A181C")
step_two.pack(fill=tk.BOTH)
file_frame = tk.Frame(step_two, bg="#1A181C", pady="8")
file_label = tk.Label(
    file_frame,
    text="If you see this, the app broke",
    font=("Arial", "16"),
    bg="#1A181C",
    fg="#F2DAFF"
)
file_instructions = tk.Label(
    file_frame,
    text="Separate filepaths with colons (:)",
    font=("Arial", "14"),
    bg="#1A181C",
    fg="#B494C7"
)
file_input = tk.Entry(
    file_frame,
    font=("Arial", "14"),
    justify=tk.CENTER,
    textvariable=tk.StringVar,
    bg="#1A181C",
    fg="#F2DAFF",
    highlightthickness=0,
    insertbackground="#F2DAFF"
)

passcode_frame = tk.Frame(step_two, bg="#1A181C", pady="8")
passcode_label = tk.Label(
    passcode_frame,
    text="If you see this, the app broke",
    font=("Arial", "16"),
    bg="#1A181C",
    fg="#F2DAFF"
)
passcode_instructions = tk.Label(
    passcode_frame,
    text="If you see this, the app broke",
    font=("Arial", "14"),
    bg="#1A181C",
    fg="#B494C7"
)
passcode_input = tk.Entry(
    passcode_frame,
    font=("Arial", "14"),
    justify=tk.CENTER,
    textvariable=tk.StringVar,
    show="*",
    bg="#1A181C",
    fg="#F2DAFF",
    highlightthickness=0,
    insertbackground="#F2DAFF"
)
confirm_label = tk.Label(
    passcode_frame,
    text="Confirm passkey",
    font=("Arial", "16"),
    bg="#1A181C",
    fg="#F2DAFF"
)
confirm_instructions = tk.Label(
    passcode_frame,
    text="Re-enter the provided passkey",
    font=("Arial", "14"),
    bg="#1A181C",
    fg="#B494C7"
)
confirm_input = tk.Entry(
    passcode_frame,
    font=("Arial", "14"),
    justify=tk.CENTER,
    textvariable=tk.StringVar,
    show="*",
    bg="#1A181C",
    fg="#F2DAFF",
    highlightthickness=0,
    insertbackground="#F2DAFF"
)

save = tk.Frame(step_two, bg="#1A181C", pady="8")
save_label = tk.Label(
    save,
    text="Save location for keys",
    font=("Arial", "16"),
    bg="#1A181C",
    fg="#F2DAFF"
)
save_instructions = tk.Label(
    save,
    text="If you see this, the app broke",
    font=("Arial", "14"),
    bg="#1A181C",
    fg="#B494C7"
)
save_input = tk.Entry(
    save,
    font=("Arial", "14"),
    justify=tk.CENTER,
    textvariable=tk.StringVar,
    bg="#1A181C",
    fg="#F2DAFF",
    highlightthickness=0,
    insertbackground="#F2DAFF"
)
if platform == "darwin":
    submit = tk.Button(
        save,
        text="If you see this, the app broke",
        font=("Arial", "14"),
        fg="#643181",
        highlightthickness=0,
        pady="3",
        command=lambda: go(
            mode=crypto_mode,
            save_folder=save_input.get(),
            target_file=file_input.get(),
            passkey=passcode_input.get(),
            passcheck=confirm_input.get()
        )
    )
else:
    submit = tk.Button(
        save,
        text="If you see this, the app broke",
        font=("Arial", "14"),
        bg="#643181",
        fg="#B494C7",
        pady="3",
        command=lambda: go(
            mode=crypto_mode,
            save_folder=save_input.get(),
            target_file=file_input.get(),
            passkey=passcode_input.get(),
            passcheck=confirm_input.get()
        )
    )

frame.update()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()