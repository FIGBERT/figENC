import os
import sys
import requests
import subprocess
import zipfile
from check import find_path

SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
RETRY_LIMIT = 2


def download_update():
    if sys.platform is "win32":
        download_url = "https://github.com/therealFIGBERT/figENC/blob/master/Executables/figENC.exe?raw=true"
        #something
    else:
        download_url = "https://github.com/therealFIGBERT/figENC/trunk/Executables/figENC.app/Contents"
        output_dir = "/".join(SCRIPTDIR.split("/")[:-1])
        subprocess.run(["svn", "checkout", download_url, output_dir], shell=False)

def check_for_updates():
    with open(find_path("version.txt")) as read_version:
        local_version = read_version.read()
    git_version = requests.get("https://raw.githubusercontent.com/therealFIGBERT/figENC/master/Scripts/version.txt").text
    if git_version > local_version:
        download_update()