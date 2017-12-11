from yaml import safe_load
import utils.globals as globals
import os

def copy_skeleton():
    try:
        from shutil import copyfile
        if not os.path.exists(os.getenv("HOME") + "/.config/Discline"):
            os.mkdir(os.getenv("HOME") + "/.config/Discline")
        
        copyfile("res/settings-skeleton.yaml", os.getenv("HOME") + "/.config/Discline/config", follow_symlinks=True) 
        print(globals.term.green("Skeleton copied!" + globals.term.normal))
    except:
        print(globals.term.red("Error creating skeleton file."))
        quit()

# This runs on the module import, before the client or main() starts
os.system("clear")
if not os.path.exists(os.getenv("HOME") + "/.config/Discline"):
    print(globals.term.yellow("Configuration file not found, creating skeleton..."))
    copy_skeleton()
    print(globals.term.cyan("Your configuration file can be found at ~/.config/Discline"))
    print("\n")

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
            print(globals.term.red("ERROR: could not get settings."))
            quit()
