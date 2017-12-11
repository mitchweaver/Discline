from yaml import safe_load
from blessings import Terminal
import os

def copy_skeleton():
    term = Terminal()
    try:
        from shutil import copyfile
        if not os.path.exists(os.getenv("HOME") + "/.config/Discline"):
            os.mkdir(os.getenv("HOME") + "/.config/Discline")
        
        if os.path.exists(os.getenv("HOME") + "/.config/Discline/config"):
            try: os.remove(os.getenv("HOME") + "/.config/Discline/config")
            except: pass

        copyfile("res/settings-skeleton.yaml", os.getenv("HOME") + "/.config/Discline/config", follow_symlinks=True) 
        print(term.green("Skeleton copied!" + term.normal))
        print(term.cyan("Your configuration file can be found at ~/.config/Discline"))

    except KeyboardInterrupt: 
        print("Cancelling...")
        quit()
    except SystemExit: quit()
    except:
        print(term.red("Error creating skeleton file."))
        quit()

import sys
arg = ""
try: arg = sys.argv[1]
except IndexError: pass
# Before we automatically load the settings, make sure we
# are actually trying to start the client
if arg != "--skeleton" and arg != "--copy-skeleton" \
   and arg != "--help" and arg != "--token" \
   and arg != "--store-token":

    # can't import globals.term due to globals.py needing settings
    term = Terminal()

    # This runs on the module import, before the client or main() starts
    os.system("clear")
    if not os.path.exists(os.getenv("HOME") + "/.config/Discline/config"):
        print(term.yellow("Configuration file not found, creating skeleton..."))
        copy_skeleton()
        print("\n")

    try:
        with open(os.getenv("HOME") + "/.config/Discline/config") as f:
            settings = safe_load(f)
    except:
        try:
            with open(os.getenv("HOME") + "/.Discline") as f:
                settings = safe_load(f)
        except:
            print(term.red("ERROR: could not get settings."))
            quit()

    # null it when we're done
    term = None
elif arg == "--skeleton" or arg == "--copy-skeleton":
    copy_skeleton()
    quit()
