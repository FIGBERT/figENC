import requests, sys
from path import find_path

def update_available():
    """Check against the current app version for
    update availability. Return "available" if there's
    an update available, "updated" if there's none available,
    and "offline" if figENC can't establish a connection.
    """
    try:
        if sys.platform == "darwin":
            git_import = requests.get(
                ("https://raw.githubusercontent.com/therealFIGBERT/figENC/"
                "master/Executables/figENC_MacOS/figENC.app/Contents/Resources"
                "/version.txt?token=AEAWGCM6DNTALDSEJWBNUTC5UTU74"
                )
            ).text
        else:
            git_import = requests.get(
                ("https://raw.githubusercontent.com/therealFIGBERT/figENC/"
                "master/Executables/figENC_Windows/version.txt?token=AEAWGCM6DNTALDSEJWBNUTC5UTU74"
                )
            ).text
    except requests.exceptions.ConnectionError:
        return "offline"
    version_file = find_path("version.txt")
    with open(version_file) as local:
        local_version = local.read()
    if local_version < git_import:
        return "available"
    elif local_version > git_import:
        return "dev"
    else:
        return "updated"