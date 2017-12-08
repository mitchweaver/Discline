from os import system
from discord import ChannelType
from ui.ui import clear_screen, set_display
from utils.globals import client,term

async def print_channellist():
    if len(client.servers) == 0:
        set_display(term.red + "Error: You are not in any servers.")
        return
    
    if len(client.get_current_server().channels) == 0:
        set_display(term.red + "Error: Does this server not have any channels?" + term.normal)
        return

    buffer = []
    for channel in client.get_current_server().channels:
        if channel.type == ChannelType.text:
            buffer.append(channel.name + "\n")

    await clear_screen()
    system("echo '" + term.cyan + "Available Channels in " \
           + term.magenta + client.get_current_server_name() + ": \n" \
           + "---------------------------- \n \n" \
           + term.yellow + "".join(buffer) \
           + term.green + "~ \n" \
           + term.green + "~ \n" \
           + term.green + "(press \'q\' to quit this dialog) \n" \
           + "' | less")

