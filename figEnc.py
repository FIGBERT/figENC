from initiate_key import rsa_key
from encrypt import rsa_enc
from decrypt import rsa_dec

exec_action = input("Are you encrypting or decrypting today (enc/dec)? ")
if exec_action == "enc":
    key_gen = input("Are you generating fresh keys (y/n)? ")
    if key_gen == "y":
        rsa_key()
        rsa_enc()
    elif key_gen == "n":
        rsa_enc()
elif exec_action == "dec":
    rsa_dec()