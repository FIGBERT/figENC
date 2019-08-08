import sys, json
import tkinter as tk
from tkinter import filedialog
from random import choice
import key, check
from encrypt import enc_manager
from decrypt import dec_manager
import version_check as vc
from check import find_path


class App():

    def __init__(self, root):
        """Create and hide the main window then open the launcher window
        
        Keyword arguments:
        root -- the Tk() frame for the main window
        """
        self.crypto_mode = ""
        self.show_pass = False
        self.crypto_filepaths = ()
        self.key_dir = ""
        
        self.settings_file = find_path("settings.json")
        self.tips_file = find_path("tips.json")
        with open(self.settings_file) as settings_file:
            settings = json.load(settings_file)
        self.main_app(root, settings)

        self.launcher = tk.Toplevel()
        self.launcher.wm_title("figENC")
        self.canvas = tk.Canvas(
            self.launcher,
            height=settings["win_height"]/6,
            width=settings["win_width"]/1.5
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="Loading application...",
            font=("Arial", (
                settings["font_size"]-2 if settings["font_size"]-2 > 0 else 2
                )
            ),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=5
        )
        self.header.pack(side=tk.TOP)
        self.subheader = tk.Label(
            self.frame,
            text=self.pick_tip(),
            font=("Arial", (
                settings["font_size"]-4 if settings["font_size"]-4 > 0 else 1
                )
            ),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.subheader.pack(side=tk.TOP)
        self.button_frame = tk.Frame(self.frame, bg="#1A181C", pady=5)
        self.button_frame.pack(side=tk.TOP)
        if sys.platform == "darwin":
            self.launch_button = tk.Button(
                self.button_frame,
                fg="#643181",
                text="Launch App",
                font=("Arial", "10"),
                highlightthickness=5,
                highlightbackground="#1A181C",
                command=lambda: self.launch_app(root)
            )
            self.settings_button = tk.Button(
                self.button_frame,
                fg="#643181",
                text="Settings",
                font=("Arial", "10"),
                highlightbackground="#1A181C",
                highlightthickness=5,
                command=lambda: self.open_settings(self.launcher)
            )
        else:
            self.launch_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                bg="#643181",
                text="Launch App",
                font=("Arial", "10"),
                command=lambda: self.launch_app(root)
            )
            self.settings_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                bg="#643181",
                text="Settings",
                font=("Arial", "10"),
                command=lambda: self.open_settings(self.launcher)
            )
        self.launch_button.pack(side=tk.LEFT)
        self.settings_button.pack(side=tk.RIGHT)
        
        root.mainloop()

    def main_app(self, root, settings):
        """Create the main app widgets in the passed root variable, and then
        minimize the root window.

        Keyword arguments:
        root -- the main app window
        settings -- a dictionary of settings used to build the widget
        """
        root.wm_title("figENC")
        self.canvas = tk.Canvas(
            root,
            height=settings["win_height"],
            width=settings["win_width"]
        )
        self.canvas.pack(fill="both", expand=True, side=tk.LEFT)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="figENC",
            justify=tk.CENTER,
            font=("Arial", str(settings["font_size"] + 6)),
            bg="#643181",
            fg="#F2DAFF",
            pady=2
        )
        self.subheader = tk.Label(
            self.frame,
            text="Industry leading encryption by FIGBERT",
            justify=tk.CENTER,
            font=("Arial", str(settings["font_size"])),
            bg="#643181",
            fg="#F2DAFF",
            pady=2
        )
        self.header.pack(fill="x", side=tk.TOP)
        self.subheader.pack(fill="x", side=tk.TOP)
        self.action = tk.Frame(self.frame, bg="#1A181C", pady=5)
        self.action.pack(fill="both")
        self.action_label = tk.Label(
            self.action,
            text="Action:",
            justify=tk.LEFT,
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
        )
        self.action_label.pack()
        self.action_list = tk.Listbox(
            self.action,
            justify=tk.CENTER,
            font=("Arial", str(settings["font_size"] - 2)),
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
        self.action_list.pack(fill="both", pady=10)
        if sys.platform == "darwin":
            self.submit_action = tk.Button(
                self.action,
                text="Begin Process",
                font=("Arial", str(settings["font_size"] - 2)),
                fg="#643181",
                highlightthickness=0,
                highlightbackground="#1A181C",
                command=lambda: self.setup(self.action_list.curselection())
            )
        else:
            self.submit_action = tk.Button(
                self.action,
                text="Begin Process",
                font=("Arial", str(settings["font_size"] - 2)),
                bg="#643181",
                fg="#B494C7",
                command=lambda: self.setup(self.action_list.curselection())
            )
        self.submit_action.pack()
        self.step_two = tk.Frame(self.frame, bg="#1A181C")
        self.step_two.pack(fill="both")
        self.file_frame = tk.Frame(self.step_two, bg="#1A181C", pady=8)
        self.file_label = tk.Label(
            self.file_frame,
            text="If you see this, the app broke",
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.file_instructions = tk.Label(
            self.file_frame,
            text="Separate filepaths with colons (:)",
            font=("Arial", str(settings["font_size"] - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        if sys.platform == "darwin":
            self.file_input = tk.Button(
                self.file_frame,
                text="Select File/s",
                font=("Arial", str(settings["font_size"] - 2)),
                fg="#643181",
                highlightthickness=0,
                highlightbackground="#1A181C",
                command=self.select_filepaths
            )
        else:
            self.file_input = tk.Button(
                self.file_frame,
                text="Select File/s",
                font=("Arial", str(settings["font_size"] - 2)),
                bg="#643181",
                fg="#B494C7",
                command=self.select_filepaths
            )
        self.passcode_frame = tk.Frame(self.step_two, bg="#1A181C", pady=8)
        self.passcode_label = tk.Label(
            self.passcode_frame,
            text="If you see this, the app broke",
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.passcode_instructions = tk.Label(
            self.passcode_frame,
            text="If you see this, the app broke",
            font=("Arial", str(settings["font_size"] - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.passcode_input = tk.Entry(
            self.passcode_frame,
            font=("Arial", str(settings["font_size"] - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            show="*",
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        self.passcode_input.bind("<Button-2>", self.toggle_pass)
        self.confirm_label = tk.Label(
            self.passcode_frame,
            text="Confirm passkey",
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.confirm_instructions = tk.Label(
            self.passcode_frame,
            text="Re-enter the provided passkey",
            font=("Arial", str(settings["font_size"] - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.confirm_input = tk.Entry(
            self.passcode_frame,
            font=("Arial", str(settings["font_size"] - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            show="*",
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        self.confirm_input.bind("<Button-2>", self.toggle_pass)
        self.save = tk.Frame(self.step_two, bg="#1A181C", pady=8)
        self.save_label = tk.Label(
            self.save,
            text="Save location for keys",
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.save_instructions = tk.Label(
            self.save,
            text="If you see this, the app broke",
            font=("Arial", str(settings["font_size"] - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        if sys.platform == "darwin":
            self.save_input = tk.Button(
                self.save,
                text="Select Directory",
                font=("Arial", str(settings["font_size"] - 2)),
                fg="#643181",
                highlightthickness=0,
                highlightbackground="#1A181C",
                command=self.select_key_dir
            )
        else:
            self.save_input = tk.Button(
                self.save,
                text="Select Directory",
                font=("Arial", str(settings["font_size"] - 2)),
                bg="#643181",
                fg="#B494C7",
                command=self.select_key_dir
            )
        self.type_frame = tk.Frame(self.step_two, bg="#1A181C", pady=8)
        self.type_label = tk.Label(
            self.type_frame,
            text="Type of keys to generate",
            font=("Arial", str(settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF"
        )
        self.type_instructions = tk.Label(
            self.type_frame,
            text=("Selecting RSA will generate a public and private key,\nbut"
            " selecting Mixed will also generate a symmetric key."
            ),
            font=("Arial", str(settings["font_size"] - 2)),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.type_button_frame = tk.Frame(self.type_frame, bg="#1A181C")
        self.type_control = tk.IntVar()
        self.rsa_radiobutton = tk.Radiobutton(
            self.type_button_frame,
            text="RSA",
            bg="#1A181C",
            fg="#F2DAFF",
            variable=self.type_control,
            value=0
        )
        self.mixed_radiobutton = tk.Radiobutton(
            self.type_button_frame,
            text="Mixed",
            bg="#1A181C",
            fg="#F2DAFF",
            variable=self.type_control,
            value=1
        )
        if sys.platform == "darwin":
            self.submit = tk.Button(
                self.step_two,
                text="If you see this, the app broke",
                font=("Arial", str(settings["font_size"] - 2)),
                fg="#643181",
                highlightbackground="#1A181C",
                highlightthickness=0,
                command=lambda: self.go(
                    mode=self.crypto_mode,
                    key_dir=self.key_paths,
                    target_files=self.crypto_filepaths,
                    passkey=self.passcode_input.get(),
                    passcheck=self.confirm_input.get()
                )
            )
        else:
            self.submit = tk.Button(
                self.step_two,
                text="If you see this, the app broke",
                font=("Arial", str(settings["font_size"] - 2)),
                bg="#643181",
                fg="#B494C7",
                command=lambda: self.go(
                    mode=self.crypto_mode,
                    key_dir=self.key_paths,
                    target_files=self.crypto_filepaths,
                    passkey=self.passcode_input.get(),
                    passcheck=self.confirm_input.get()
                )
            )
        root.withdraw()

    def open_settings(self, root):
        """Open the settings window and temporarily minimize the root window
        
        Keyword arguments:
        root -- the window to be minimized
        """
        root.withdraw()
        with open(self.settings_file) as settings_file:
            self.settings = json.load(settings_file)
        self.settings_window = tk.Toplevel(
            height=self.settings["win_height"],
            width=self.settings["win_width"],
            bg="#1A181C"
        )
        self.settings_window.wm_title("figENC - Settings")
        self.canvas = tk.Canvas(
            self.settings_window,
            height=self.settings["win_height"],
            width=self.settings["win_width"]
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="Settings",
            justify=tk.CENTER,
            font=("Arial", str(self.settings["font_size"] + 4)),
            bg="#643181",
            fg="#F2DAFF",
            pady=6
        )
        self.header.pack(fill=tk.X)
        self.font_frame = tk.Frame(self.frame, bg="#1A181C")
        self.font_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.font_label = tk.Label(
            self.font_frame,
            text="Font Size: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.font_label.pack(side=tk.LEFT)
        self.font_options = [12, 14, 16, 18, 20, 24, 32]
        self.font_dropdown = tk.StringVar()
        self.font_dropdown.set(self.settings["font_size"])
        self.font_menu = tk.OptionMenu(
            self.font_frame,
            self.font_dropdown,
            *self.font_options,
            command=self.modify_font
        )
        self.font_menu.config(bg="#1A181C", fg="#643181")
        self.font_menu.pack(side=tk.LEFT)
        self.dim_frame = tk.Frame(self.frame, bg="#1A181C")
        self.dim_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.dim_label = tk.Label(
            self.dim_frame,
            text="Default window dimension: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.dim_label.pack(side=tk.LEFT)
        self.dim_options = [
            "500x500",
            "700x700",
            "900x900",
            "1000x1000",
            "1200x1200",
            "1500x1500"
        ]
        self.dim_dropdown = tk.StringVar()
        self.dim_dropdown.set(
            str(self.settings["win_width"])
            + "x"
            + str(self.settings["win_height"])
        )
        self.dim_menu = tk.OptionMenu(
            self.dim_frame,
            self.dim_dropdown,
            *self.dim_options,
            command=self.modify_dim
        )
        self.dim_menu.config(bg="#1A181C", fg="#643181")
        self.dim_menu.pack(side=tk.LEFT)
        self.update_frame = tk.Frame(self.frame, bg="#1A181C")
        self.update_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.update_label = tk.Label(
            self.update_frame,
            text="Update Status: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.update_label.pack(side=tk.LEFT)
        self.update_bool = vc.update_available()
        if self.update_bool == "available":
            self.update_text = "Available"
            self.update_color = "#84D373"
        elif self.update_bool == "updated":
            self.update_text = "Up to date!"
            self.update_color = "#B1A5B8"
        else:
            self.update_text = "Connection failed"
            self.update_color = "#FC142F"
        self.update_status = tk.Label(
            self.update_frame,
            text=self.update_text,
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg=self.update_color,
            pady=2
        )
        self.update_status.pack(side=tk.LEFT)
        self.settings_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_settings(self.settings_window, root)
        )
        self.settings_window.mainloop()

    def launch_app(self, root):
        """Deiconifies the passed root window, destroys the launcher
        window and updates the frame
        
        Keyword arguments:
        root -- the main app window
        """
        root.deiconify()
        self.launcher.destroy()
        self.frame.update()


    def reset(self):
        """Hide all elements of the main app GUI and reset the entered text"""
        self.file_frame.pack_forget()
        self.file_instructions.pack_forget()
        self.file_label.pack_forget()
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
        self.save_input.pack_forget()
        self.type_frame.pack_forget()
        self.type_label.pack_forget()
        self.type_instructions.pack_forget()
        self.type_button_frame.pack_forget()
        self.rsa_radiobutton.pack_forget()
        self.mixed_radiobutton.pack_forget()
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
            self.save_input.pack(fill="x")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady=10)
            self.crypto_mode = "key_enc"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady=10)
            self.crypto_mode = "weak_key_enc"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.submit.config(text="Encrypt file/s")
            self.submit.pack(pady=10)
            self.crypto_mode = "enc"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.submit.config(text="Decrypt file/s")
            self.submit.pack(pady=10)
            self.crypto_mode = "dec"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.submit.config(text="Decrypt file/s")
            self.submit.pack(pady=10)
            self.crypto_mode = "weak_dec"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.type_frame.pack()
            self.type_label.pack()
            self.type_instructions.pack()
            self.type_button_frame.pack()
            self.rsa_radiobutton.pack(side=tk.LEFT)
            self.mixed_radiobutton.pack(side=tk.LEFT)
            self.submit.config(text="Create keys")
            self.submit.pack(pady=10)
            self.crypto_mode = "just_key"
            self.frame.update()
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
            self.save_input.pack(fill="x")
            self.type_frame.pack()
            self.type_label.pack()
            self.type_instructions.pack()
            self.type_button_frame.pack()
            self.rsa_radiobutton.pack(side=tk.LEFT)
            self.mixed_radiobutton.pack(side=tk.LEFT)
            self.submit.config(text="Create keys")
            self.submit.pack(pady=10)
            self.crypto_mode = "weak_key"
            self.frame.update()

    def go(
        self,
        mode,
        key_dir=None,
        target_files=None,
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
        if mode == "key_enc" and check.key_enc(
            target_files,
            passkey,
            passcheck,
            key_dir
        ):
            key.key_manager(target_files, key_dir, passkey)
            enc_manager(target_files, key_dir)
        elif mode == "weak_key_enc" and check.weak_key_enc(
            target_files,
            key_dir
        ):
            key.key_manager(target_files, key_dir, passkey)
            enc_manager(target_files, key_dir)
        elif mode == "enc" and check.enc(target_files, key_dir):
            enc_manager(target_files, key_dir)
        elif mode == "dec" and check.dec(
            target_files,
            passkey,
            passcheck,
            key_dir
        ):
            dec_manager(target_files, key_dir, passkey)
        elif mode == "weak_dec" and check.weak_dec(target_files, key_dir):
            dec_manager(target_files, key_dir, passkey)
        elif mode == "just_key" and check.key(key_dir):
            key.just_key_manager(self.type_control.get(), key_dir, passkey)
        elif mode == "weak_key" and check.key(key_dir):
            key.just_key_manager(self.type_control.get(), key_dir, passkey)

    def pick_tip(self):
        """Return a random string from the tips.json file"""
        with open(self.tips_file) as source:
            self.tips = json.load(source)
        self.tip = "Tip: " + choice(self.tips)
        return self.tip

    def close_settings(self, settings_window, root):
        """Destroy the settings toplevel and deiconify the root window
        
        Keyword arguments:
        settings_window -- the window of the app to destory
        root -- the window of the app to deiconify()
        """
        settings_window.destroy()
        root.deiconify()

    def modify_font(self, value):
        """Change the value of the font_size key in the self.settings variable
        and export settings to file.
        
        Keyword arguments:
        value -- the int to which the self.settings variable will change
        """
        self.settings["font_size"] = value
        with open(self.settings_file, "w") as fl:
            json.dump(self.settings, fl, indent=4, sort_keys=True)

    def modify_dim(self, value):
        """Change the value of the win_width key in the self.settings
        variable and export settings to file.
        
        Keyword arguments:
        value -- an int represeting the new width of the window
        """
        width = int(value.split("x")[0])
        height = int(value.split("x")[1])
        self.settings["win_width"] = width
        self.settings["win_height"] = height
        with open(self.settings_file, "w") as fl:
            json.dump(self.settings, fl, indent=4, sort_keys=True)

    def toggle_pass(self, *args):
        """Toogle the password fields between showing the characters and
        hiding them.
        """
        if self.show_pass:
            self.passcode_input.config(show="")
            self.confirm_input.config(show="")
            self.show_pass = not self.show_pass
        else:
            self.passcode_input.config(show="*")
            self.confirm_input.config(show="*")
            self.show_pass = not self.show_pass
    
    def select_filepaths(self):
        self.crypto_filepaths = filedialog.askopenfilenames()

    def select_key_dir(self):
        self.key_paths = filedialog.askdirectory()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()