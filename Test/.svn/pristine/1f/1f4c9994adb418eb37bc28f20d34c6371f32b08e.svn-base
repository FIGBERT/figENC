import os
import requests
import subprocess
import tkinter as tk

def update_script():
    subprocess.run(
        [
            "svn", 
            "checkout",
            "https://github.com/therealFIGBERT/figENC/trunk/Test"
        ],
        shell=False
    )

#This line is only on GitHub
root = tk.Tk()
root.wm_title("GitHub")
button = tk.Button(root, text="Update", command=update_script)
button.pack()
root.mainloop()