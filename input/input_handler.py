import asyncio
import curses
import logging
from utils.log import log
import discord
from input.kbhit import KBHit
import ui.ui as ui
from utils.globals import gc, kill
from utils.settings import settings
from commands.text_emoticons import check_emoticons
from commands.sendfile import send_file
from commands.channel_jump import channel_jump
from input.messageEdit import MessageEdit

async def key_input():
    # if the next two aren't here, input does not work
    curses.cbreak()
    curses.noecho()
    editBar = gc.ui.editBar
    edit = gc.ui.edit
    await ui.draw_bottom_bar()
    while True:
        prompt = gc.client.get_prompt()
        ch = editBar.getch()
        if ch == -1 or not gc.ui.displayPanel.hidden():
            await asyncio.sleep(0.01)
            continue
        if chr(ch) != '\n':
            gc.typingBeingHandled = True
        if ch == curses.KEY_PPAGE:
            gc.ui.channel_log_offset -= settings["scroll_lines"]
            gc.ui.doUpdate = True
            while gc.ui.doUpdate:
                await asyncio.sleep(0.01)
            continue
        elif ch == curses.KEY_NPAGE:
            gc.ui.channel_log_offset += settings["scroll_lines"]
            gc.ui.doUpdate = True
            while gc.ui.doUpdate:
                await asyncio.sleep(0.01)
            continue
        await ui.draw_bottom_bar()
        ret = edit.addKey(ch)
        if ret is not None:
            await input_handler(ret)
            edit.reset()
        await ui.draw_bottom_bar()

async def typing_handler():
    if not settings["send_is_typing"]: return

    while True:
        if gc.typingBeingHandled:
            await gc.client.send_typing(gc.client.get_current_channel())
            await asyncio.sleep(5)
            gc.typingBeingHandled = False
        await asyncio.sleep(0.1)

async def input_handler(text):
    # Must be a command
    if text.startswith(settings["prefix"]):
        text = text[1:]
        arg = None
        if ' ' in text:
            command,arg = text.split(" ", 1)
        elif not text:
            return
        else:
            command = text
            arg = None
        await parseCommand(command, arg)
    # Must be text
    else:
        # Emoji
        if text.count(':')%2 == 0:
            text = await parseEmoji(text)
        if '@' in text:
            sections = text.lower().strip().split()
            secs_copy = []
            for sect in sections:
                if '@' in sect:
                    for member in gc.client.get_current_server().members:
                        if member is not gc.client.get_current_server().me and \
                                sect[1:] in member.display_name.lower():
                            sect = "<@!" + member.id + ">"
                sects_copy.append(sect)
            text = " ".join(sects_copy)
        sent = False
        for i in range(0,3):
            try:
                await gc.client.send_message(gc.client.get_current_channel(), text)
                sent = True
                break
            except:
                await asyncio.sleep(3)

async def parseCommand(command, arg=None):
    if command in ("server", 's'):
        server_name = ""
        server_log = None
        for servlog in gc.server_log_tree:
            if arg.lower() in servlog.get_name().lower():
                server_name = servlog.get_name()
                server_log = servlog
                break
        if server_name:
            gc.client.set_current_server(server_name)
            def_chan = ""

            lowest = 999
            for chan in server_log.get_server().channels:
                if chan.type is discord.ChannelType.text and \
                        chan.permissions_for(server_log.get_server().me).read_messages and \
                        chan.position < lowest:
                    try:
                        # Skip over ignored channels
                        for serv_key in settings["channel_ignore_list"]:
                            if serv_key["server_name"].lower() == server_name:
                                for name in serv_key["ignores"]:
                                    if chan.name.lower() == name.lower():
                                        raise Found
                    except:
                        continue
                    lowest = chan.position
                    def_chan = chan
                try:
                    gc.client.set_current_channel(def_chan.name)
                    for chanlog in servlog.get_logs():
                        if chanlog.get_channel() is def_chan:
                            chanlog.unread = False
                            chanlog.mentioned_in = False
                            break
                except: continue
            log("changed server")
            gc.ui.channel_log_offset = -1
            gc.ui.doUpdate = True
            while gc.ui.doUpdate:
                await asyncio.sleep(0.01)
        else:
            log("Can't find server", logging.error)
    elif command in ("channel", 'c'):
        for servlog  in gc.server_log_tree:
            if servlog.get_server() is gc.client.get_current_server():
                final_chanlog = ""
                for chanlog in servlog.get_logs():
                    if arg.lower() in chanlog.get_name().lower()and \
                            chanlog.get_channel().type is discord.ChannelType.text and \
                            chanlog.get_channel().permissions_for(
                                    servlog.get_server().me).read_messages:
                        final_chanlog = chanlog
                        break
                if final_chanlog:
                    gc.client.set_current_channel(final_chanlog.get_name())
                    final_chanlog.unread = False
                    final_chanlog.mentioned_in = False
                    gc.ui.doUpdate = True
                    while gc.ui.doUpdate:
                        await asyncio.sleep(0.01)
                else:
                    log("Can't find channel", logging.error)
    elif command == "nick":
        try:
            await gc.client.change_nickname(gc.client.get_current_server().me, arg)
        except:
            pass
    elif command == "game":
        await gc.client.set_game(arg)
    elif command == "file":
        await send_file(gc.client, arg)
    elif command == "status":
        status = arg.lower()
        if status in ("away", "afk"):
            status = "idle"
        elif "disturb" in status:
            status = "dnd"

        if status in ("online", "offline", "idle", "dnd"):
            await gc.client.set_status(status)

    if arg is None:
        if command == "refresh":
            gc.ui.doUpdate = True
            while gc.ui.doUpdate:
                await asyncio.sleep(0.01)
            log("Manual update done", logging.info)
        elif command in ("quit", "exit"): kill()
        elif command in ("help", 'h'): await ui.draw_help()
        elif command in ("servers", "servs"): await ui.draw_serverlist()
        elif command in ("channels", "chans"): await ui.draw_channellist()
        elif command == "emojis": await ui.draw_emojilist()
        elif command in ("users", "members"): await ui.draw_userlist()
        elif command[0] == 'c':
            try:
                if command[1].isdigit():
                    await channel_jump(command)
            except IndexError:
                pass
        await check_emoticons(gc.client, command)

async def parseEmoji(text):
    if settings["has_nitro"]:
        for emoji in gc.client.get_all_emojis():
            short_name = ':' + emoji.name + ':'
            if short_name in text:
                full_name = "<:{}:{}>".format(emoji.name, emoji.id)
                text = text.replace(short_name, full_name)
    elif gc.client.get_current_server().emojis is not None and \
            len(gc.client.get_current_server().emojis) > 0:
        for emoji in gc.client.get_current_server().emojis:
            short_name = ':' + emoji.name + ':'
            if short_name in text:
                full_name = "<:{}:{}>".format(emoji.name, emoji.id)
                text = text.replace(short_name, full_name)

    return text
