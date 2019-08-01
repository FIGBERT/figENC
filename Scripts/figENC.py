import sys, os, inspect
import tkinter as tk
from random import choice
import json
import requests
from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec
import version_check
import check
from check import find_path
import update as up


class App():

    def __init__(self, root):
        """Create and hide the main window then open the launcher window
        
        Keyword arguments:
        root -- the Tk() frame for the main window
        """
        self.crypto_mode = ""
        self.show_pass = False
        self.settings_file = find_path("settings.json")
        self.tips_file = find_path("tips.json")

        with open(self.settings_file) as settings_file:
            settings = json.load(settings_file)

        root.wm_title("figENC")
        self.canvas = tk.Canvas(
            root,
            height=settings["win_height"],
            width=settings["win_width"]
        )
        if settings["scroll"]:
            self.vertical_scroll = tk.Scrollbar(
                root,
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
            font=("Arial", str(settings["font_size"] + 6)),
            bg="#643181",
            fg="#F2DAFF",
            pady="2"
        )
        self.subheader = tk.Label(
            self.frame,
            text="Industry leading encryption by FIGBERT",
            justify=tk.CENTER,
            font=("Arial", str(settings["font_size"])),
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
        self.action_list.pack(fill="both", pady="10")
        if sys.platform == "darwin":
            self.submit_action = tk.Button(
                self.action,
                text="Begin Process",
                font=("Arial", str(settings["font_size"] - 2)),
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
                font=("Arial", str(settings["font_size"] - 2)),
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
        self.file_input = tk.Entry(
            self.file_frame,
            font=("Arial", str(settings["font_size"] - 2)),
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
        self.save = tk.Frame(self.step_two, bg="#1A181C", pady="8")
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
        self.save_input = tk.Entry(
            self.save,
            font=("Arial", str(settings["font_size"] - 2)),
            justify=tk.CENTER,
            textvariable=tk.StringVar,
            bg="#1A181C",
            fg="#F2DAFF",
            highlightthickness=0,
            insertbackground="#F2DAFF"
        )
        if sys.platform == "darwin":
            self.submit = tk.Button(
                self.save,
                text="If you see this, the app broke",
                font=("Arial", str(settings["font_size"] - 2)),
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
                font=("Arial", str(settings["font_size"] - 2)),
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
        root.withdraw()
        self.launcher = tk.Toplevel()
        self.launcher.wm_title("figENC")
        self.canvas = tk.Canvas(
            self.launcher,
            height=100,
            width=450
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="Loading application...",
            font=("Arial", "12"),
            bg="#1A181C",
            fg="#F2DAFF",
            pady="5"
        )
        self.header.pack(side=tk.TOP)
        self.subheader = tk.Label(
            self.frame,
            text=self.pick_tip(),
            font=("Arial", "10"),
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
        else:
            self.launch_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                bg="#643181",
                text="Launch App",
                font=("Arial", "10"),
                command=lambda: self.launch_app(root)
            )
        if sys.platform == "darwin":
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

    def launch_app(self, root):
        root.deiconify()
        self.launcher.destroy()
        self.frame.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def open_settings(self, root):
        """Open the settings window and temporarily minimize the root window
        
        Keyword arguments:
        root -- the window to be minimized
        """
        root.withdraw()
        self.settings_window = tk.Toplevel(
            height=400,
            width=700,
            bg="#1A181C"
        )
        self.settings_window.wm_title("figENC - Settings")
        with open(self.settings_file) as settings_file:
            self.settings = json.load(settings_file)
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
            font=("Arial", str(self.settings["font_size"] + 2)),
            bg="#643181",
            fg="#F2DAFF",
            pady=2
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
        self.scroll_frame = tk.Frame(self.frame, bg="#1A181C")
        self.scroll_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.scroll_label = tk.Label(
            self.scroll_frame,
            text="Scrollbar: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.scroll_label.pack(side=tk.LEFT)
        self.scroll_options = ["Off", "On"]
        self.scroll_dropdown = tk.StringVar()
        self.scroll_dropdown.set("On" if self.settings["scroll"] else "Off")
        self.scroll_menu = tk.OptionMenu(
            self.scroll_frame,
            self.scroll_dropdown,
            *self.scroll_options,
            command=self.modify_scroll
        )
        self.scroll_menu.config(bg="#1A181C", fg="#643181")
        self.scroll_menu.pack(side=tk.LEFT)
        self.width_frame = tk.Frame(self.frame, bg="#1A181C")
        self.width_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.width_label = tk.Label(
            self.width_frame,
            text="Default window width: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.width_label.pack(side=tk.LEFT)
        self.width_options = [500, 700, 900, 1000, 1200, 1500]
        self.width_dropdown = tk.StringVar()
        self.width_dropdown.set(self.settings["win_width"])
        self.width_menu = tk.OptionMenu(
            self.width_frame,
            self.width_dropdown,
            *self.width_options,
            command=self.modify_width
        )
        self.width_menu.config(bg="#1A181C", fg="#643181")
        self.width_menu.pack(side=tk.LEFT)
        self.height_frame = tk.Frame(self.frame, bg="#1A181C")
        self.height_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.height_label = tk.Label(
            self.height_frame,
            text="Default window height: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.height_label.pack(side=tk.LEFT)
        self.height_options = [500, 700, 900, 1000, 1200, 1500]
        self.height_dropdown = tk.StringVar()
        self.height_dropdown.set(self.settings["win_width"])
        self.height_menu = tk.OptionMenu(
            self.height_frame,
            self.height_dropdown,
            *self.height_options,
            command=self.modify_height
        )
        self.height_menu.config(bg="#1A181C", fg="#643181")
        self.height_menu.pack(side=tk.LEFT)
        self.auto_frame = tk.Frame(self.frame, bg="#1A181C")
        self.auto_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.auto_label = tk.Label(
            self.auto_frame,
            text="Automatic Updates: ",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.auto_label.pack(side=tk.LEFT)
        self.auto_options = ["Off", "On"]
        self.auto_dropdown = tk.StringVar()
        self.auto_dropdown.set("On" if self.settings["auto_update"] else "Off")
        self.auto_menu = tk.OptionMenu(
            self.auto_frame,
            self.auto_dropdown,
            *self.auto_options,
            command=self.modify_auto
        )
        self.auto_menu.config(bg="#1A181C", fg="#643181")
        self.auto_menu.pack(side=tk.LEFT)
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
        self.update_bool = version_check.update_available()
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
        self.save_frame = tk.Frame(self.frame, bg="#1A181C")
        self.save_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=5, padx=5)
        if sys.platform == "darwin":
            self.save_button = tk.Button(
                self.save_frame,
                fg="#643181",
                text="Save",
                font=("Arial", str(self.settings["font_size"] - 2)),
                highlightbackground="#1A181C",
                padx=5,
                command=lambda: self.export(self.settings_window, root)
            )
        else:
            self.save_button = tk.Button(
                self.save_frame,
                fg="#B494C7",
                bg="#643181",
                text="Save",
                font=("Arial", str(self.settings["font_size"] - 2)),
                padx=5,
                command=lambda: self.export(self.settings_window, root)
            )
        self.save_button.pack(side=tk.LEFT)
        self.settings_window.mainloop()
    
    def pick_tip(self):
        """Return a random string from the tips.json file"""
        with open(self.tips_file) as source:
            self.tips = json.load(source)
        self.tip = "Tip: " + choice(self.tips)
        return self.tip

    def reset(self):
        """Hide all elements of the app GUI and reset the entered text"""
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
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
            self.frame.update()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

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
            print("1. Quick check works")
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
                print("2. Reached function call")
                rsa_dec(target_file, save_folder, passkey)
            elif mode == "just_key" and check.password_check(passkey,
                                                                passcheck):
                rsa_key(passkey, save_folder)
            elif mode == "weak_key":
                rsa_key(passkey, save_folder)

    def export(self, settings_window, root):
        """Export the data contained in the modified settings variable
        derived from the file settings.json, delete the settings window
        and restore the launcher window.
        
        Keyword arguments:
        settings_window -- the window of the app to destory
        root -- the window of the app to deiconify()
        """
        with open(self.settings_file, "w") as write_file:
            json.dump(self.settings, write_file, indent=4, sort_keys=True)
        settings_window.destroy()
        root.deiconify()
    
    def modify_font(self, value):
        """Change the value of the font_size key in the self.settings variable
        
        Keyword arguments:
        value -- the int to which the self.settings variable will change
        """
        self.settings["font_size"] = value
        self.frame.update()

    def modify_scroll(self, value):
        """Change the value of the scroll key in the self.settings variable
        
        Keyword arguments:
        value -- a string, "on" or "off", to be converted to a boolean
        """
        bool_val = True if value is "On" else False
        self.settings["scroll"] = bool_val
        self.frame.update()

    def modify_auto(self, value):
        """Change the value of the auto_update key in the self.settings
        variable
        
        Keyword arguments:
        value -- a string, "on" or "off" to be converted to a boolean
        """
        bool_val = True if value is "On" else False
        self.settings["auto_update"] = bool_val
        self.frame.update()

    def modify_width(self, value):
        """Change the value of the win_width key in the self.settings
        variable
        
        Keyword arguments:
        value -- an int represeting the new width of the window
        """
        self.settings["win_width"] = value
        self.frame.update()

    def modify_height(self, value):
        """Change the value of the win_height key in the self.settings
        variable
        
        Keyword arguments:
        value -- an int represeting the new height of the window
        """
        self.settings["win_height"] = value
        self.frame.update()

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


if __name__ == "__main__":
    up.check_for_updates()
    root = tk.Tk()
    App(root)
    root.mainloop()