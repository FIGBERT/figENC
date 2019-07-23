from sys import platform
import tkinter as tk
from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec
import check


class App():

    def __init__(self, head_font, scroll_bool):
        self.crypto_mode = ""

        self.root = tk.Tk()
        self.root.wm_title("figENC")
        self.canvas = tk.Canvas(
            self.root,
            height=700,
            width=700
        )
        if scroll_bool:
            self.vertical_scroll = tk.Scrollbar(
                self.root,
                command=self.canvas.yview
            )
            self.canvas.config(yscrollcommand=self.vertical_scroll.set)
            self.vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill="both", expand=True, side=tk.LEFT)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="figENC",
            justify=tk.CENTER,
            font=("Arial", str(head_font + 6)),
            bg="#643181",
            fg="#F2DAFF",
            pady="2"
        )
        self.subheader = tk.Label(
            self.frame,
            text="Industry leading encryption by FIGBERT",
            justify=tk.CENTER,
            font=("Arial", str(head_font)),
            bg="#643181",
            fg="#F2DAFF",
            pady="2"
        )
        self.header.pack(fill="x", side=tk.TOP)
        self.subheader.pack(fill="x", side=tk.TOP)
        self.action = tk.Frame(self.frame, bg="#1A181C", pady="5")
        self.action.pack(fill="both")
        self.action_label = tk.Label(
            self.action,
            text="Action:",
            justify=tk.LEFT,
            font=("Arial", str(head_font)),
            bg="#1A181C",
            fg="#F2DAFF",
        )
        self.action_label.pack()
        self.action_list = tk.Listbox(
            self.action,
            justify=tk.CENTER,
            font=("Arial", str(head_font - 2)),
            bg="#1A181C",
            fg="#ACA0B2",
            selectbackground="#643181",
            selectmode=tk.SINGLE,
            relief=tk.SUNKEN,
            height=7
        )
        self.action_list.insert(
            1,
            "Encrypt with fresh keys (password locked)"
        )
        self.action_list.insert(2, "Encrypt with fresh keys (no password)")
        self.action_list.insert(3, "Encrypt with generated keys")
        self.action_list.insert(
            4,
            "Decrypt with generated keys (password locked)"
        )
        self.action_list.insert(
            5,
            "Decrypt with generated keys (no password)"
        )
        self.action_list.insert(6, "Only create fresh keys (password locked)")
        self.action_list.insert(7, "Only create fresh keys (no password)")
        self.action_list.pack(fill="both", pady="10")
        if platform == "darwin":
            self.submit_action = tk.Button(
                self.action,
                text="Begin Process",
                font=("Arial", str(head_font - 2)),
                fg="#643181",
                highlightthickness=0,
                highlightbackground="#1A181C",
                pady="3",
                command=lambda: self.setup(self.action_list.curselection())
            )
        else:
            self.submit_action = tk.Button(
                self.action,
                text="Begin Process",
                font=("Arial", str(head_font - 2)),
                bg="#643181",
                fg="#B494C7",
                command=lambda: self.setup(self.action_list.curselection())
            )
        self.submit_action.pack()
        self.step_two = tk.Frame(self.frame, bg="#1A181C")
        self.step_two.pack(fill="both")
        self.file_frame = tk.Frame(self.step_two, bg="#1A181C", pady="8")
        self.file_label = tk.Label(
            self.file_frame,
            text="If you see this, the app broke",
            font=("Arial", str(head_font)),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.file_instructions = tk.Label(
            self.file_frame,
            text="Separate filepaths with colons (:)",
            font=("Arial", str(head_font - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.file_input = tk.Entry(
            self.file_frame,
            font=("Arial", str(head_font - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        self.passcode_frame = tk.Frame(self.step_two, bg="#1A181C", pady="8")
        self.passcode_label = tk.Label(
            self.passcode_frame,
            text="If you see this, the app broke",
            font=("Arial", str(head_font)),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.passcode_instructions = tk.Label(
            self.passcode_frame,
            text="If you see this, the app broke",
            font=("Arial", str(head_font - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.passcode_input = tk.Entry(
            self.passcode_frame,
            font=("Arial", str(head_font - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            show="*",
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        self.confirm_label = tk.Label(
            self.passcode_frame,
            text="Confirm passkey",
            font=("Arial", str(head_font)),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.confirm_instructions = tk.Label(
            self.passcode_frame,
            text="Re-enter the provided passkey",
            font=("Arial", str(head_font - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.confirm_input = tk.Entry(
            self.passcode_frame,
            font=("Arial", str(head_font - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            show="*",
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        self.save = tk.Frame(self.step_two, bg="#1A181C", pady="8")
        self.save_label = tk.Label(
            self.save,
            text="Save location for keys",
            font=("Arial", str(head_font)),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.save_instructions = tk.Label(
            self.save,
            text="If you see this, the app broke",
            font=("Arial", str(head_font - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.save_input = tk.Entry(
            self.save,
            font=("Arial", str(head_font - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        if platform == "darwin":
            self.submit = tk.Button(
                self.save,
                text="If you see this, the app broke",
                font=("Arial", str(head_font - 2)),
                fg="#643181",
                highlightbackground="#1A181C",
                highlightthickness=0,
                pady="3",
                command=lambda: self.go(
                    mode=self.crypto_mode,
                    save_folder=self.save_input.get(),
                    target_file=self.file_input.get(),
                    passkey=self.passcode_input.get(),
                    passcheck=self.confirm_input.get()
                )
            )
        else:
            self.submit = tk.Button(
                self.save,
                text="If you see this, the app broke",
                font=("Arial", str(head_font - 2)),
                bg="#643181",
                fg="#B494C7",
                pady="3",
                command=lambda: self.go(
                    mode=self.crypto_mode,
                    save_folder=self.save_input.get(),
                    target_file=self.file_input.get(),
                    passkey=self.passcode_input.get(),
                    passcheck=self.confirm_input.get()
                )
            )
        self.root.mainloop()
    
    def reset(self):
        self.file_frame.pack_forget()
        self.file_instructions.pack_forget()
        self.file_label.pack_forget()
        self.reset_text(self.file_input)
        self.file_input.pack_forget()
        self.passcode_frame.pack_forget()
        self.passcode_label.pack_forget()
        self.passcode_instructions.pack_forget()
        self.reset_text(self.passcode_input)
        self.passcode_input.pack_forget()
        self.confirm_label.pack_forget()
        self.confirm_instructions.pack_forget()
        self.reset_text(self.confirm_input)
        self.confirm_input.pack_forget()
        self.save.pack_forget()
        self.save_label.pack_forget()
        self.save_instructions.pack_forget()
        self.reset_text(self.save_input)
        self.save_input.pack_forget()
        self.submit.pack_forget()

    def reset_text(self, entry_widget):
        """Reset the string value of a tk.Entry object to an empty string
        
        Keyword arguments:
        entry_widget -- a tk.Entry object
        """
        entry_widget.delete(0,tk.END)
        entry_widget.insert(0,"")

    def setup(self, mode):
        """"Change the GUI to match the app mode,
        based on the user's action_list selection.

        Keyword arguments:
        mode -- an int (0-6) corresponding with the action_list selection
        """
        mode = mode[0]
        if mode == 0: #Encrypt with fresh keys (password locked)
            self.reset()
            self.file_frame.pack(fill="both")
            self.file_label.config(text="Filepath/s to the file/s to encrypt")
            self.file_label.pack()
            self.file_instructions.pack()
            self.file_input.pack(fill="x")
            self.passcode_frame.pack(fill="both")
            self.passcode_label.config(text="Set private key passcode")
            self.passcode_label.pack()
            self.passcode_instructions.config(
                text=(
                    "CRITICAL: DO NOT FORGET YOUR"
                    "PASSCODE.\nWITHOUT IT, "
                    "YOUR DATA WILL BE LOST."
                )
            )
            self.passcode_instructions.pack()
            self.passcode_input.pack(fill="x")
            self.confirm_label.pack()
            self.confirm_instructions.pack()
            self.confirm_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Save location for keys")
            self.save_label.pack()
            self.save_instructions.config(
                text=(
                    "Save the keys to an empty folder, "
                    "and store them somewhere secure\n"
                    "If other key files exist in the same"
                    "folder, they will be overwritten"
                )
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady="10")
            self.crypto_mode = "key_enc"
        elif mode == 1: #Encrypt with fresh keys (no password)
            self.reset()
            self.file_frame.pack(fill="both")
            self.file_label.config(text="Filepath/s to the file/s to encrypt")
            self.file_label.pack()
            self.file_instructions.pack()
            self.file_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Save location for keys")
            self.save_label.pack()
            self.save_instructions.config(
                text=(
                    "Save the keys to an empty folder, "
                    "and store them somewhere secure\n"
                    "If other key files exist in the same"
                    "folder, they will be overwritten"
                )
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady="10")
            self.crypto_mode = "weak_key_enc"
        elif mode == 2: #Encrypt with generated keys
            self.reset()
            self.file_frame.pack(fill="both")
            self.file_label.config(text="Filepath/s to the file/s to encrypt")
            self.file_label.pack()
            self.file_instructions.pack()
            self.file_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Key location")
            self.save_label.pack()
            self.save_instructions.config(
                text="Filepath to matching key trio"
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady="10")
            self.crypto_mode = "enc"
        elif mode == 3: #Decrypt with generated keys (password locked)
            self.reset()
            self.file_frame.pack(fill="both")
            self.file_label.config(text="Filepath/s to the file/s to decrypt")
            self.file_label.pack()
            self.file_instructions.pack()
            self.file_input.pack(fill="x")
            self.passcode_frame.pack(fill="both")
            self.passcode_label.config(text="Private key passcode")
            self.passcode_label.pack()
            self.passcode_instructions.config(
                text=(
                    "Passcode must be the same "
                    "passcode used when the keys were created"
                )
            )
            self.passcode_instructions.pack()
            self.passcode_input.pack(fill="x")
            self.confirm_label.pack()
            self.confirm_instructions.pack()
            self.confirm_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Key location")
            self.save_label.pack()
            self.save_instructions.config(
                text="Filepath to matching key trio"
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Decrypt file/s")
            self.submit.pack(pady="10")
            self.crypto_mode = "dec"
        elif mode == 4: #Decrypt with generated keys (no password)
            self.reset()
            self.file_frame.pack(fill="both")
            self.file_label.config(text="Filepath/s to the file/s to decrypt")
            self.file_label.pack()
            self.file_instructions.pack()
            self.file_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Key location")
            self.save_label.pack()
            self.save_instructions.config(
                text="Filepath to matching key trio"
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Decrypt file/s")
            self.submit.pack(pady="10")
            self.crypto_mode = "weak_dec"
        elif mode == 5: #Only create fresh keys (password locked)
            self.reset()
            self.passcode_frame.pack(fill="both")
            self.passcode_label.config(text="Set private key passcode")
            self.passcode_label.pack()
            self.passcode_instructions.config(
                text=(
                    "CRITICAL: DO NOT FORGET YOUR PASSCODE.\nWITHOUT IT, "
                    "YOUR DATA WILL BE LOST."
                )
            )
            self.passcode_instructions.pack()
            self.passcode_input.pack(fill="x")
            self.confirm_label.pack()
            self.confirm_instructions.pack()
            self.confirm_input.pack(fill="x")
            self.save.pack(fill="both")
            self.save_label.config(text="Save location for keys")
            self.save_label.pack()
            self.save_instructions.config(
                text=(
                    "Save the keys to an empty folder, "
                    "and store them somewhere secure\n"
                    "If other key files exist in the same"
                    "folder, they will be overwritten"
                )
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Create keys")
            self.submit.pack(pady="10")
            self.crypto_mode = "just_key"
        elif mode == 6: #Only create fresh keys (no password)
            self.reset()
            self.save.pack(fill="both")
            self.save_label.config(text="Save location for keys")
            self.save_label.pack()
            self.save_instructions.config(
                text=(
                    "Save the keys to an empty folder, "
                    "and store them somewhere secure\n"
                    "If other key files exist in the same"
                    "folder, they will be overwritten"
                )
            )
            self.save_instructions.pack()
            self.save_input.pack(fill="both")
            self.submit.config(text="Create keys")
            self.submit.pack(pady="10")
            self.crypto_mode = "weak_key"

    def go(
        self,
        mode,
        save_folder=None,
        target_file=None,
        passkey=None,
        passcheck=None
    ):
        """Perform the action corresponding to the mode,
        using the input data from the user, after checking the validity
        of the filepaths.

        Keyword arguments:
        mode -- the mode defined by setup() from action_list
        save_folder -- the folder where the keys are or will be stored
        target_file -- the file to encrypt or decrypt
        passkey - the access code to the RSA keys that have them
        passcheck - the access code to the RSA keys that have them confirmed,
        to prevent spelling errors.
        """
        if check.quick_check(
            mode=mode,
            target_file_raw=target_file,
            save_folder=save_folder
        ):
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
            elif mode == "just_key" and check.password_check(passkey,
                                                                passcheck):
                rsa_key(passkey, save_folder)
            elif mode == "weak_key":
                rsa_key(passkey, save_folder)


#App(14, False)