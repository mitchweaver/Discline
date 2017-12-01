from os import system

def print_help():
    system("clear")
    system("echo " + term.green \
        + "'Available Commands: \n" + term.red \
        + "---------------------------------- \n" + term.normal \
        + "/channel  - switch to channel - (alias: 'c') \n" \
        + "/server   - switch server     - (alias: 's') \n" \
        + "\n" \
        + "/servers  - list available servers \n" \
        + "/channels - list available channels \n" \
        + "/users    - list servers users \n" \
        + "\n" \
        + "/nick     - change server nick name \n" \
        + "/game     - change your game status \n" \
        + "/quit     - exit cleanly \n" \
        + "\n \n" \
        + term.green + "(press q to quit this dialog) \n" \
        + "' | less")
