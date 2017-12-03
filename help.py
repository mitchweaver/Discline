from os import system
from settings import term

async def print_help():
    system("clear")
    system("echo '" + term.green \
        + "Available Commands: \n" + term.red \
        + "--------------------------------------------- \n" \
        + get_line("/channel", "   - ", "switch to channel - (alias: 'c')") \
        + get_line("/server", "    - ", "switch server     - (alias: 's')") \
        + "\n" \
        + get_line("/servers", "   - ", "list available servers") \
        + get_line("/channels", "  - ", "list available channels") \
        + get_line("/users", "     - ", "list servers users") \
        + "\n" \
        + get_line("/nick", "      - ", "change server nick name") \
        + get_line("/game", "      - ", "change your game status") \
        + "\n" \
        + get_line("clear", "      - ", "force clearing of screen") \
        + get_line("/quit", "      - ", "exit cleanly") \
        + "\n \n" \
        + term.green + "(press q to quit this dialog)" \
        + "' | less -R")



def get_line(command, div, desc):
    return term.yellow + command + term.cyan + div + term.normal + desc + "\n"
