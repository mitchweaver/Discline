import curses
import time
import logging
import asyncio
from discord import ChannelType
from ui.curses_utils import CursesBase, WrappedText, MessageEdit
from utils.globals import gc

async def start_ui():
    curses.wrapper(gc.ui.run)

async def print_screen():
    await print_channel_log()

async def print_top_bar(left_bar_width):
    # Prints server, topic, and members online
    topic = ""
    try:
        if gc.client.get_current_channel().topic is not None:
            topic = gc.client.get_current_channel().topic
    except:
        # if there is no channel topic, just print the channel name
        try: topic = gc.client.get_current_channel().name
        except: pass

async def set_display(string):
    # ???
    pass

async def print_left_bar(left_bar_width):
    # Lists channels
    pass

async def print_bottom_bar(left_bar_width):
    # Prints user input
    pass

async def clear_screen():
    # Wipes screen
    pass

#TODO: This first
async def print_channel_log():
    # Prints channel log (messages)
    MAX_LINES = gc.ui.contentPadAttribs[4]

    for server_log in gc.server_log_tree:
        if server_log.get_server() is gc.client.get_current_server():
            for channel_log in server_log.get_logs():
                if channel_log.get_channel() is gc.client.get_current_channel():
                    if channel_log.get_channel() not in gc.channels_entered:
                        await gc.client.populate_current_channel_log()
                        gc.channels_entered.append(channel_log.get_channel())
                    # if the server has a "category" channel named the same
                    # as a text channel, confusion will occur
                    # TODO: private messages are not "text" channeltypes
                    if channel_log.get_channel().type != ChannelType.text: continue
                    gc.ui.contentPad.clear()
                    if not gc.ui.areLogsRead:
                        for msg in channel_log.get_logs():
                            gc.ui.wrapText.addMessage(msg)
                        gc.ui.areLogsRead = True
                    else:
                        msg = channel_log.get_logs()[-1]
                        gc.ui.wrapText.addMessage(msg)
                    line = 0
                    formatted = "".join(gc.ui.wrapText.formatted)
                    normalText = None
                    boldText = None
                    if "\033[1m" in formatted:
                        split = formatted.split("\033[1m")
                        normalText = split[0]
                        boldText = split[1]
                    if boldText is not None:
                        gc.ui.contentPad.addstr(0,0, normalText)
                        gc.ui.contentPad.addstr(normalText, curses.A_BOLD)
                    else:
                        gc.ui.contentPad.addstr(0,0, formatted)
    nls = 0
    for msg in gc.ui.wrapText.formatted:
        nls += msg.count('\n')
    gc.ui.frameWins[0].refresh()
    gc.ui.setPadIndex(nls-MAX_LINES+1)
