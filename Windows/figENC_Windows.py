from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec
import tkinter as tk

crypto_mode = ""
def setup(mode):
    mode = mode[0]
    global crypto_mode
    if mode == 0:
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        passcode_input.pack_forget()
        file_label.config(text="Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill='x')
        passcode_label.config(text="Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(text="CRITICAL: DO NOT FORGET YOUR PASSCODE.\nWITHOUT IT, YOUR DATA WILL BE LOST.")
        passcode_instructions.pack()
        passcode_input.pack(fill='x')
        save_label.pack()
        save_instructions.pack()
        save_input.pack(fill="both")
        submit.config(text="Encrypt file/s")
        submit.pack()
        crypto_mode = "key_enc"
    elif mode == 1:
        file_label.config(text="Filepath/s to the file/s to encrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill='x')
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        passcode_input.pack_forget()
        save_label.config(text="Key location")
        save_label.pack()
        save_instructions.config(text="Filepath to matching key trio")
        save_instructions.pack()
        save_input.pack(fill="both")
        submit.config(text="Encrypt file/s")
        submit.pack()
        crypto_mode = "enc"
    elif mode == 2:
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        passcode_input.pack_forget()
        file_label.config(text="Filepath/s to the file/s to decrypt")
        file_label.pack()
        file_instructions.pack()
        file_input.pack(fill='x')
        passcode_label.config(text="Private key passcode")
        passcode_label.pack()
        passcode_instructions.config(text="Passcode must be the same passcode used when the keys were created")
        passcode_instructions.pack()
        passcode_input.pack(fill='x')
        save_label.pack()
        save_instructions.pack()
        save_input.pack(fill="both")
        submit.config(text="Decrypt file/s")
        submit.pack()
        crypto_mode = "dec"
    elif mode == 3:
        passcode_label.pack_forget()
        passcode_instructions.pack_forget()
        passcode_input.pack_forget()
        file_label.pack_forget()
        file_instructions.pack_forget()
        file_input.pack_forget()
        passcode_label.config(text="Set private key passcode")
        passcode_label.pack()
        passcode_instructions.config(text="CRITICAL: DO NOT FORGET YOUR PASSCODE.\nWITHOUT IT, YOUR DATA WILL BE LOST.")
        passcode_instructions.pack()
        passcode_input.pack(fill='x')
        save_label.pack()
        save_instructions.pack()
        save_input.pack(fill="both")
        submit.config(text="Create keys")
        submit.pack()
        crypto_mode = "just_key"

def go(mode, save_folder, target_file, passkey=None):
    if mode == "key_enc":
        rsa_key(passkey, save_folder)
        rsa_enc(target_file, save_folder)
    elif mode == "enc":
        rsa_enc(target_file, save_folder)
    elif mode == "dec":
        rsa_dec(target_file, save_folder, passkey)
    elif mode == "just_key":
        rsa_key(passkey, save_folder)

root = tk.Tk()
root.wm_title("figENC")
canvas = tk.Canvas(root, height=700, width=650)
canvas.pack()
frame = tk.Frame(root)
frame.place(relwidth=1, relheight=1)

header = tk.Label(frame, text="figENC\nIndustry leading encryption by FIGBERT", justify="center", font=("Arial", "24"), relief=tk.RAISED)
header.pack(fill="x", side="top", ipady="5")

action = tk.Frame(frame)
action.pack(fill='both')
action_label = tk.Label(action, text="Action:", justify='left', font=("Arial", "14"))
action_label.pack()
action_list = tk.Listbox(action, selectmode="single", font=("Arial", "12"), height=4, bd=1, relief=tk.SUNKEN)
action_list.insert(1, "Encrypt with fresh keys")
action_list.insert(2, "Encrypt with generated keys")
action_list.insert(3, "Decrypt with generated keys")
action_list.insert(4, "Only create fresh keys")
action_list.pack(fill='both')
submit_action = tk.Button(action, text="Begin Process", font=("Arial", "12"), command=lambda: setup(action_list.curselection()))
submit_action.pack()

step_two =tk.Frame(frame)
step_two.pack(fill="both")

modifiers = tk.Frame(step_two)
modifiers.pack(fill="both")
file_label = tk.Label(modifiers, text="If you see this, the app broke", font=("Arial", "14"))
file_instructions = tk.Label(modifiers, text="Separate filepaths with colons (:)", font=("Arial", "11"))
file_input = tk.Entry(modifiers, font=("Arial", "12"), justify=tk.CENTER, textvariable=tk.StringVar, relief=tk.SUNKEN)
passcode_label = tk.Label(modifiers, text="If you see this, the app broke", font=("Arial", "14"))
passcode_instructions = tk.Label(modifiers, text="If you see this, the app broke", font=("Arial", "11"))
passcode_input = tk.Entry(modifiers, font=("Arial", "12"), justify=tk.CENTER, textvariable=tk.StringVar, relief=tk.SUNKEN)

save = tk.Frame(step_two)
save.pack(fill='both')
save_label = tk.Label(save, text="Save location for keys", font=("Arial", "14"))
save_instructions = tk.Label(save, text="Save the keys to an empty folder, and store them somewhere secure\nIf other key files exist in the same folder, they will be overwritten", font=("Arial", "11"))
save_input = tk.Entry(save, font=("Arial", "12"), justify=tk.CENTER, textvariable=tk.StringVar, relief=tk.SUNKEN)
submit = tk.Button(save, text="If you see this, the app broke", font=("Arial", "12"), command=lambda: go(mode=crypto_mode, save_folder=save_input.get(), target_file=file_input.get(), passkey=passcode_input.get()))

root.mainloop()