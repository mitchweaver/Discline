from os import system
from ui.ui import clear_screen, set_display
from utils.globals import get_color, gc
from utils.settings import settings

async def print_serverlist():
    if len(gc.client.servers) == 0:
        set_display(gc.term.red + "Error: You are not in any servers." + gc.term.normal)
        return

    buffer = []
    for slog in gc.server_log_tree:
        name = slog.get_name()
        name = name.replace("'", "")
        name = name.replace('"', "")
        name = name.replace("`", "")
        name = name.replace("$(", "")

        if slog.get_server() is gc.client.get_current_server():
            buffer.append(await get_color(settings["current_channel_color"]) + name + gc.term.normal + "\n")
            continue

        string = ""
        for clog in slog.get_logs():
            if clog.mentioned_in:
                string = await get_color(settings["unread_mention_color"]) + name + gc.term.normal + "\n"
                break
            elif clog.unread:
                string = await get_color(settings["unread_channel_color"]) + name + gc.term.normal + "\n"
                break
        
        if string == "":
            string = await get_color(settings["text_color"]) + name + gc.term.normal + "\n"

        buffer.append(string)
            
    await clear_screen()
    system("echo '" + gc.term.magenta + "Available Servers: \n" + gc.term.normal \
        + "---------------------------- \n \n" \
        + "".join(buffer) \
        + gc.term.green + "~ \n" \
        + gc.term.green + "~ \n" \
        + gc.term.green + "(press q to quit this dialog) \n" \
        + "' | less -R")
