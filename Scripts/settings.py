from sys import platform
import tkinter as tk
import json

class SettingsApp():

    def __init__(self):
        with open("settings.json") as settings_file:
            self.settings = json.load(settings_file)
        self.root = tk.Tk()
        self.root.wm_title("figENC - Settings")
        self.canvas = tk.Canvas(
            self.root,
            height=400,
            width=700
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


        self.save_frame = tk.Frame(self.frame, bg="#1A181C")
        self.save_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=5, padx=5)
        if platform == "darwin":
            self.save_button = tk.Button(
                self.save_frame,
                fg="#643181",
                text="Save",
                font=("Arial", str(self.settings["font_size"] - 2)),
                highlightbackground="#1A181C",
                padx=5,
                command=lambda: self.export(self.root)
            )
        else:
            self.save_button = tk.Button(
                self.save_frame,
                fg="#B494C7",
                bg="#643181",
                text="Save",
                font=("Arial", str(self.settings["font_size"] - 2)),
                padx=5,
                command=lambda: self.export(self.root)
            )
        self.save_button.pack(side=tk.LEFT)

        self.root.mainloop()

    def export(self, root):
        with open("settings.json", "w") as write_file:
            json.dump(self.settings, write_file, indent=4, sort_keys=True)
        root.destroy()
    
    def modify_font(self, value):
        self.settings["font_size"] = value
        self.frame.update()

    def modify_scroll(self, value):
        bool_val = True if value is "On" else False
        self.settings["scroll"] = bool_val
        self.frame.update()


SettingsApp()