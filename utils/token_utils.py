import os
from utils.globals import term

def get_token():
    if os.path.exists(os.getenv("HOME") + "/.config/Discline/token"):
        token = ""
        try:
            f = open(os.getenv("HOME") + "/.config/Discline/token", "r")
            token = f.read()
            f.close()
        except: pass

        if token != "":
            return token
    
    from blessings import Terminal
    term = Terminal()
    print("\n" + term.red("Error reading token."))
    print("\n" + term.yellow("Are you sure you stored your token?"))
    print(term.yellow("Use --store-token to store your token."))
    quit()

def store_token():
    import sys
    from blessings import Terminal
    
    token = ""
    try: 
        token=sys.argv[2]
    except IndexError:
        print(Terminal().red("Error: You did not specify a token!"))
        quit()

    if not os.path.exists(os.getenv("HOME") + "/.config/Discline"):
        os.mkdir(os.getenv("HOME") + "/.config/Discline")

    if token is not None and token != "":
        # trim off quotes if user added them
        token = token.strip('"')
        token = token.strip("'")

    if token is None or len(token) < 59 or len(token) > 88:
        print(Terminal().red("Error: Bad token. Did you paste it correctly?"))
        quit()
    
    try:
        f = open(os.getenv("HOME") + "/.config/Discline/token", "w")
        f.write(token)
        f.close()
        print(Terminal().green("Token stored!"))
    except:
        print(Terminal().red("Error: Could not write token to file."))
        quit()
