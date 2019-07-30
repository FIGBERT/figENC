import os
import requests
import tkinter as tk

def update_script():
    git_data = requests.get("https://raw.githubusercontent.com/therealFIGBERT/figENC/master/Test/test.py").text
    with open(os.getcwd() + "test.py", "w") as write:
        write.write(git_data)

#This line is only on GitHub
root = tk.Tk()
root.wm_title("GitHub")
button = tk.Button(root, text="Update", command=update_script)
button.pack()
root.mainloop()