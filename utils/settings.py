import os
import sys
from yaml import safe_load
from blessings import Terminal

settings = ""

def copy_skeleton():
    term = Terminal()
    try:
        from shutil import copyfile
        if not os.path.exists(os.getenv("HOME") + "/.config/Discline"):
            os.mkdir(os.getenv("HOME") + "/.config/Discline")
        
        if os.path.exists(os.getenv("HOME") + "/.config/Discline/config"):
            try:
                os.remove(os.getenv("HOME") + "/.config/Discline/config")
            except:
                pass

        copyfile("res/settings-skeleton.yaml", os.getenv("HOME") + "/.config/Discline/config", follow_symlinks=True) 
        print(term.green("Skeleton copied!" + term.normal))
        print(term.cyan("Your configuration file can be found at ~/.config/Discline"))

    except KeyboardInterrupt: 
        print("Cancelling...")
        quit()
    except SystemExit:
        quit()
    except:
        print(term.red("Error creating skeleton file."))
        quit()

def load_config(path):
    global settings
    with open(path) as f:
        settings = safe_load(f)
 
arg = ""
try: 
    arg = sys.argv[1]
except IndexError: 
    pass

if arg == "--store-token" or arg == "--token":
    pass
elif arg == "--skeleton" or arg == "--copy-skeleton":
    copy_skeleton()
    quit()
elif arg == "--config":
    try:
        load_config(sys.argv[2])
    except IndexError:
        print("No path provided?")
        quit()
    except:
        print("Invalid path to config entered.")
        quit()
else:
    try:
        load_config(os.getenv("HOME") + "/.config/Discline/config")
    except:
        try:
            load_config(os.getenv("HOME") + "/.Discline")
        except:
            print(term.red("ERROR: could not get settings."))
            quit()
