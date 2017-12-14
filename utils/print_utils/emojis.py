from os import system
from ui.ui import clear_screen, set_display
from utils.globals import client, term, server_log_tree, get_color
from utils.settings import settings

async def print_emojilist():
    if len(client.servers) == 0:
        set_display(term.red + "Error: You are not in any servers." + term.normal)
        return

    server_name = client.get_current_server_name()
    server_name = server_name.replace("'", "")
    server_name = server_name.replace('"', "")
    server_name = server_name.replace("`", "")

    emojis = []
    server_emojis = ""

    try: server_emojis = client.get_current_server().emojis
    except: pass

    if server_emojis is not None and server_emojis != "":
        for emoji in server_emojis:
            name = emoji.name
            name = name.replace("'", "")
            name = name.replace('"', "")
            name = name.replace("`", "")
            emojis.append(term.yellow + ":" + name + ":" + "\n")

    await clear_screen()
    system("echo '" + term.magenta + "Available Emojis in: " + term.cyan + server_name +"\n" + term.normal \
        + "---------------------------- \n" \
        + "".join(emojis) \
        + term.green + "~ \n" \
        + term.green + "~ \n" \
        + term.green + "(press q to quit this dialog) \n" \
        + "' | less -R")
