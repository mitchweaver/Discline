from yaml import safe_load

try:
    with open(os.getenv("HOME") + "/.config/Discline/config") as f:
        settings = safe_load(f)
except:
    try:
        with open(os.getenv("HOME") + "/.Discline") as f:
            settings = safe_load(f)
    except:
        try:
            with open("res/settings-skeleton.yaml") as f:
                settings = safe_load(f)
        except:
            print("ERROR: could not get settings.")
            quit()
