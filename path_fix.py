import sys
import os

#Helper function for pyinstaller. Pyinstaller has different paths even when you send the exact path names.
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # If running from PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    # If running in dev mode
    return os.path.join(os.path.abspath("."), relative_path)