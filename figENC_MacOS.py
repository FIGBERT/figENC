from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec
import tkinter as tk

root = tk.Tk()
root.wm_title("figENC")
canvas = tk.Canvas(root, height=700, width=500)
canvas.pack()
frame = tk.Frame(root, bg='white')
frame.place(relwidth=1, relheight=1)

header = tk.Label(frame, text="figENC\nIndustry leading encryption by FIGBERT", bg="gray", fg="black", justify="center", font=("Arial", "18"))
header.pack(fill="x", side="top", ipady="5")

action = tk.Frame(frame, bg="white")
action.pack(fill='both')
action_label = tk.Label(action, text="Action:", bg="white", justify='left', font=("Arial", "14"))
action_label.pack()
action_list = tk.Listbox(action, bg="white", selectmode="single", font=("Arial", "12"), height=3, bd=1)
action_list.insert(1, "Encrypt with fresh keys")
action_list.insert(2, "Encrypt with generated key")
action_list.insert(3, "Decrypt with generated key")
action_list.pack(fill='both')
submit_action = tk.Button(action, text="Begin Process", font=("Arial", "12"))
submit_action.pack()

modifiers = tk.Frame(frame, bg="white")
modifiers.pack(fill="both")
file_label_text = "If you see this, the app broke"
file_instructions_text = "Separate filepaths with colons (:)"
file_label = tk.Label(modifiers, text=file_label_text, font=("Arial", "14"))
file_label.pack()
file_instructions = tk.Label(modifiers, text=file_instructions_text, font=("Arial", "11"))
file_instructions.pack()
file_input = tk.Entry(modifiers, font=("Arial", "12"), justify=tk.LEFT)
file_input.pack(fill=tk.X)
passcode_label_text = "If you see this, the app broke"
passcode_instructions_text = "CRITICAL: DO NOT FORGET YOUR PASSCODE. WITHOUT IT, YOUR DATA IS LOST."
passcode_label = tk.Label(modifiers, text=passcode_label_text, font=("Arial", "14"))
passcode_label.pack()
passcode_instructions = tk.Label(modifiers, text=passcode_instructions_text, font=("Arial", "11"))
passcode_instructions.pack()
passcode_input = tk.Entry(modifiers, font=("Arial", "12"), justify=tk.LEFT)
passcode_input.pack(fill=tk.X)

root.mainloop()