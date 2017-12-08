from os import system
from ui.ui import clear_screen, set_display
from utils.globals import client, term

async def print_serverlist():

    if len(client.servers) == 0:
        set_display(term.red + "Error: You are not in any servers." + term.normal)
        return

    buffer = []
    for server in client.servers:
        buffer.append(server.name + "\n")
            
    await clear_screen()
    system("echo '" + term.magenta + "Available Servers: \n" \
        + "---------------------------- \n \n" \
        + term.cyan + "".join(buffer) \
        + term.green + "~ \n" \
        + term.green + "~ \n" \
        + term.green + "(press \'q\' to quit this dialog) \n" \
        + "' | less -R")
