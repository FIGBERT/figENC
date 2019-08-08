import os, inspect, requests, sys
from check import find_path

def update_available():
    try:
        git_import = requests.get(
            ("https://raw.githubusercontent.com/therealFIGBERT/figENC/"
            "master/Executables/figENC_MacOS/figENC.app/Contents/Resources"
            "/version.txt"
            )
        ).text
    except requests.exceptions.ConnectionError:
        return "offline"
    version_file = find_path("version.txt")
    with open(version_file) as local:
        local_version = local.read()
    if local_version < git_import:
        return "available"
    else:
        return "updated"