from yaml import safe_load
from os import getenv

try:
    with open(getenv("HOME") + "/.config/Discline/config") as f:
        settings = safe_load(f)
except:
    try:
        with open(getenv("HOME") + "/.Discline") as f:
            settings = safe_load(f)
    except:
        try:
            with open("res/settings-skeleton.yaml") as f:
                settings = safe_load(f)
        except:
            print("ERROR: could not get settings.")
            quit()
