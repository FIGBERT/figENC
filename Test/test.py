import os
import requests
import tkinter as tk

def find_path(file):
        """Return the correct filename if you are running it as a script"""
        return os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        ) + "/{}".format(file)

def update_script():
    git_data = requests.get("https://raw.githubusercontent.com/therealFIGBERT/figENC/master/Test/test.py").text
    print("File read")
    with open(find_path("test.py")) as write:
        write.write(git_data)
    print("File written")

#This line is only on GitHub
root = tk.Tk()
root.wm_title("GitHub")
button = tk.Button(root, text="Update", command=update_script)
button.pack()
root.mainloop()