import requests

def update_available():
    git_import = requests.get("https://raw.githubusercontent.com/therealFIGBERT/figENC/master/Scripts/version.txt").text
    with open("version.txt") as local:
        local_version = local.read()
    if local_version < git_import:
        return True
    else:
        return False