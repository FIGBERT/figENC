from sys import platform
from random import choice
from json import load
import tkinter as tk
from tkinter import ttk
from figENC import App

class Launcher():

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("figENC")
        self.canvas = tk.Canvas(
            self.root,
            height=125,
            width=450
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.frame = tk.Frame(self.canvas, bg="#1A181C")
        self.frame.place(relwidth=1, relheight=1)
        self.header = tk.Label(
            self.frame,
            text="Loading application...",
            font=("Arial", "10"),
            bg="#1A181C",
            fg="#F2DAFF",
            pady="5"
        )
        self.header.pack(side=tk.TOP)
        self.subheader = tk.Label(
            self.frame,
            text=self.pick_tip(),
            font=("Arial", "8"),
            bg="#1A181C",
            fg="#B494C7"
        )
        self.subheader.pack(side=tk.TOP)
        self.progressbar = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
        self.progressbar.pack(side=tk.TOP)
        self.button_frame = tk.Frame(self.frame, bg="#1A181C", pady=10)
        self.button_frame.pack(side=tk.TOP)
        if platform == "darwin":
            self.launch_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                text="Launch App",
                font=("Arial", "8"),
                highlightthickness=0,
                highlightbackground="#1A181C"
            )
        else:
            self.launch_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                bg="#643181",
                text="Launch App",
                font=("Arial", "8")
            )
        if platform == "darwin":
            self.settings_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                text="Settings",
                font=("Arial", "8"),
                highlightthickness=0,
                highlightbackground="#1A181C"
            )
        else:
            self.settings_button = tk.Button(
                self.button_frame,
                fg="#B494C7",
                bg="#643181",
                text="Settings",
                font=("Arial", "8")
            )
        self.launch_button.pack(side=tk.LEFT)
        self.settings_button.pack(side=tk.RIGHT)
        self.root.mainloop()
    
    def pick_tip(self):
        with open("tips.json") as source:
            self.tips = load(source)
        self.tip = "Tip: " + choice(self.tips)
        return self.tip

    def open_settings(self):
        pass
    
    def launch_app(self):
        pass


Launcher()