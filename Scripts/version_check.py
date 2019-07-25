import requests
import subprocess

def update_available():
    try:
        git_import = requests.get(
            ("https://raw.githubusercontent.com/therealFIGBERT/figENC/master"
            "/Scripts/version.txt"
            )
        ).text
    except requests.exceptions.ConnectionError:
        return "offline"
    with open("version.txt") as local:
        local_version = local.read()
    if local_version < git_import:
        return "available"
    else:
        return "updated"

def update_and_replace():
    pass