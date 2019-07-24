import requests

def update_available():
    git_import = int(requests.get("https://raw.githubusercontent.com/therealFIGBERT/figENC/master/Scripts/_version.py").text)
    with open("version.txt") as local:
        local_version = int(local.read())
    if local_version < git_import:
        return True
    else:
        return False