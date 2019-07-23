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
            text="Font Size:",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.font_label.pack(side=tk.LEFT)
        self.font_options_selector = tk.Menubutton(
            self.font_frame,
            font=("Arial", str(self.settings["font_size"] - 2)),
            text=str(self.settings["font_size"]),
            bg="#1A181C"
        )
        self.font_options = tk.Menu(
            self.font_options_selector,
            tearoff=0,
            title=str(self.settings["font_size"])
        )
        self.font_options.add_radiobutton(label="12", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="14", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="16", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="18", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="20", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="24", variable=tk.IntVar())
        self.font_options.add_radiobutton(label="32", variable=tk.IntVar())
        self.font_options_selector.pack(side=tk.LEFT)
        self.font_options_selector["menu"] = self.font_options

        scroll_bool = "on" if self.settings["scroll"] else "off"
        self.scroll_frame = tk.Frame(self.frame, bg="#1A181C")
        self.scroll_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10)
        self.scroll_label = tk.Label(
            self.scroll_frame,
            text="Scrollbar:",
            justify=tk.LEFT,
            font=("Arial", str(self.settings["font_size"])),
            bg="#1A181C",
            fg="#F2DAFF",
            pady=2
        )
        self.scroll_label.pack(side=tk.LEFT)
        self.scroll_options_selector = tk.Menubutton(
            self.scroll_frame,
            font=("Arial", str(self.settings["font_size"] - 2)),
            text=scroll_bool,
            bg="#1A181C"
        )
        self.scroll_options = tk.Menu(
            self.scroll_options_selector,
            tearoff=0,
            title=scroll_bool
        )
        self.scroll_options.add_radiobutton(
            label="off",
            variable=tk.IntVar(),
            value=False
        )
        self.scroll_options.add_radiobutton(
            label="on",
            variable=tk.IntVar(),
            value=True
        )
        self.scroll_options_selector.pack(side=tk.LEFT)
        self.scroll_options_selector["menu"] = self.scroll_options

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
        print(self.settings)
        root.destroy()

#SettingsApp()