import os, inspect, sys

# def find_path(filename):
#     """Return the correct filepath if you are running
#     figENC as a bundled application
    
#     Keyword arguments:
#     filename -- the filename to convert to a filepath
#     """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, filename)

def find_path(file):
        """Return the correct filepath if you are running
        figENC as a script

        Keyword arguments:
        file -- the filename to convert to a filepath
        """
        return os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        ) + "/{}".format(file)