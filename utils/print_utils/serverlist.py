from os import system
from ui.ui import clear_screen, set_display
from utils.globals import client, term, server_log_tree, get_color
from settings import settings

async def print_serverlist():
    pass

    if len(client.servers) == 0:
        set_display(term.red + "Error: You are not in any servers." + term.normal)
        return

    buffer = []
    for slog in server_log_tree:
        if slog.get_server() is client.get_current_server():
            buffer.append(await get_color(settings["current_channel_color"]) + slog.get_name() + term.normal + "\n")
            continue

        string = ""
        for clog in slog.get_logs():
            if clog.mentioned_in:
                string = await get_color(settings["unread_mention_color"]) + slog.get_name() + term.normal + "\n"
                break
            elif clog.unread:
                string = await get_color(settings["unread_channel_color"]) + slog.get_name() + term.normal + "\n"
                break
        
        if string == "":
            string = await get_color(settings["text_color"]) + slog.get_name() + term.normal + "\n"

        buffer.append(string)
            
    await clear_screen()
    system("echo '" + term.magenta + "Available Servers: \n" + term.normal \
        + "---------------------------- \n \n" \
        + "".join(buffer) \
        + term.green + "~ \n" \
        + term.green + "~ \n" \
        + term.green + "(press \'q\' to quit this dialog) \n" \
        + "' | less -R")
