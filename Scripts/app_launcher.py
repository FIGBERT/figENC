from random import choice
import time
import threading
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
        self.progressbar = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
        self.progressbar.pack(side=tk.TOP)
        self.root.mainloop()
    
    def pick_tip(self):
        with open("tips.json") as source:
            self.tips = load(source)
        self.tip = "Tip: " + choice(self.tips)
        return self.tip

    def load(self):
        with open("settings.json") as read_file:
            self.settings_file = load(read_file)
        #Add something that checks the code against this link
        #https://github.com/therealFIGBERT/figENC/tree/master/Executables/figENC.app/Contents
        App(self.settings_file["font_size"], self.settings_file["scroll"])


Launcher()