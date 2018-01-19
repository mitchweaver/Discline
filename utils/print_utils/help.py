from os import system
from utils.globals import gc

def print_help(gc):
    system("clear")
    system("echo '" + gc.term.normal \
        + gc.term.green("Launch Arguments: \n") + gc.term.red \
        + "--------------------------------------------- \n" \
        + get_line("--copy-skeleton ", " --- ", "copies template settings") \
        + gc.term.cyan("This file can be found at ~/.config/Discline/config \n") \
        + "\n"
        + get_line("--store-token", " --- ", "stores your token") \
        + gc.term.cyan("This file can be found at ~/.config/Discline/token \n") \
        + "\n"
        + gc.term.green("Available Commands: \n") + gc.term.red \
        + "--------------------------------------------- \n" \
        + get_line("/channel", "   - ", "switch to channel - (alias: 'c')") \
        + get_line("/server", "    - ", "switch server     - (alias: 's')") \
        + gc.term.cyan + "Note: these commands can now fuzzy-find! \n" \
        + "\n" \
        + get_line("/servers", "   - ", "list available servers") \
        + get_line("/channels", "  - ", "list available channels") \
        + get_line("/users", "     - ", "list servers users") \
        + get_line("/emojis", "     - ", "list servers custom emojis") \
        + "\n" \
        + get_line("/nick", "      - ", "change server nick name") \
        + get_line("/game", "      - ", "change your game status") \
        + get_line("/file", "      - ", "upload a file via path") \
        + get_line("/status", "    - ", "change online presence") \
        + gc.term.cyan + "This can be either 'online', 'offline', 'away', or 'dnd' \n" \
        + gc.term.cyan + "(dnd = do not disturb) \n" \
        + "\n" \
        + get_line("/cX", "        - ", "shorthand to change channel (Ex: /c1)") \
        + gc.term.cyan("This can be configured to start at 0 in your config") \
        + "\n" \
        + "\n" \
        + get_line("/quit", "      - ", "exit cleanly") \
        + "\n \n" \
        + gc.term.magenta + "Note: You can send emojis by using :emojiname: \n" \
        + gc.term.cyan("Nitro emojis do work! Make sure you have \n") \
        + gc.term.cyan("nitro enabled in your config. \n") \
        + "\n"
        + gc.term.yellow + "You can scroll up/down in channel logs \n" \
        + gc.term.yellow + "by using PageUp/PageDown. \n" \
        + gc.term.green + "~ \n" \
        + gc.term.green + "~ \n" \
        + gc.term.green + "~ \n" \
        + gc.term.green + "(press q to quit this dialog)" \
        + "' | less -R")



def get_line(gc, command, div, desc):
    return gc.term.yellow(command) + gc.term.cyan(div) + gc.term.normal + desc + "\n"
