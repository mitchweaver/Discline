from os import system
from ui.ui import clear_screen, set_display
from utils.globals import gc, get_color
from utils.settings import settings

async def print_emojilist():
    if len(gc.client.servers) == 0:
        set_display(gc.term.red + "Error: You are not in any servers." + gc.term.normal)
        return

    server_name = gc.client.get_current_server_name()
    server_name = server_name.replace("'", "")
    server_name = server_name.replace('"', "")
    server_name = server_name.replace("`", "")
    server_name = server_name.replace("$(", "")

    emojis = []
    server_emojis = ""

    try: server_emojis = gc.client.get_current_server().emojis
    except: pass

    if server_emojis is not None and server_emojis != "":
        for emoji in server_emojis:
            name = emoji.name
            name = name.replace("'", "")
            name = name.replace('"', "")
            name = name.replace("`", "")
            name = name.replace("$(", "")
            emojis.append(gc.term.yellow + ":" + name + ":" + "\n")

    await clear_screen()
    system("echo '" + gc.term.magenta + "Available Emojis in: " + gc.term.cyan + server_name +"\n" + gc.term.normal \
        + "---------------------------- \n" \
        + "".join(emojis) \
        + gc.term.green + "~ \n" \
        + gc.term.green + "~ \n" \
        + gc.term.green + "(press q to quit this dialog) \n" \
        + "' | less -R")
