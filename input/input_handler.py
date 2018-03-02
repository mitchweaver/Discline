import asyncio
import discord
from input.kbhit import KBHit
import ui.ui as ui
from utils.globals import gc, kill
from utils.print_utils.help import print_help
from utils.print_utils.userlist import print_userlist
from utils.print_utils.serverlist import print_serverlist
from utils.print_utils.channellist import print_channellist
from utils.print_utils.emojis import print_emojilist
from utils.settings import settings
from commands.text_emoticons import check_emoticons
from commands.sendfile import send_file
from commands.channel_jump import channel_jump

kb = ""

def init_input():
    global kb
    kb = KBHit()

async def key_input():
    await gc.client.wait_until_ready()

    global kb
    memory = ""
    key = ""
    while True:
        if await kb.kbhit() or memory == "[":
            key = await kb.getch()

            ordkey = ord(key)

            if memory == "[":
                if key == "6": # page down
                    gc.client.get_current_channel_log().dec_index(settings["scroll_lines"])
                    del gc.input_buffer[-1]
                elif key == "5": # page up
                    gc.client.get_current_channel_log().inc_index(settings["scroll_lines"])
                    del gc.input_buffer[-1]
            else:
                if ordkey == 10 or ordkey == 13: # enter key
                    gc.user_input = "".join(gc.input_buffer)
                    del gc.input_buffer[:]
                elif ordkey == 127 or ordkey == 8: # backspace
                    if len(gc.input_buffer) > 0:
                        del gc.input_buffer[-1]

                elif ordkey >= 32 and ordkey <= 256: # all letters and special characters
                    if not (ordkey == 126 and (memory == "5" or memory == "6")): # tilde left over from page up/down
                        gc.input_buffer.append(key)
                elif ordkey == 9:
                    gc.input_buffer.append(" " * 4) # tab key

            memory = key
            if key != "[":
                await ui.print_screen()

        if key != "[":
            await asyncio.sleep(0.015)
        elif key == "~":
            await asyncio.sleep(0.1)

async def input_handler():
    await gc.client.wait_until_ready()

    while True:

        # If input is blank, don't do anything
        if gc.user_input == '':
            await asyncio.sleep(0.05)
            continue

        # # check if input is a command
        if gc.user_input[0] == settings["prefix"]:
            # strip the PREFIX
            gc.user_input = gc.user_input[1:]

            # check if contains a space
            if ' ' in gc.user_input:
                # split into command and argument
                command,arg = gc.user_input.split(" ", 1)

                if command == "server" or command == 's':

                    server_name = ""
                    # check if arg is a valid server, then switch
                    for servlog in gc.server_log_tree:
                        if servlog.get_name().lower() == arg.lower():
                            server_name = servlog.get_name()
                            break

                    # if we didn't find an exact match, assume only partial
                    # Note if there are multiple servers containing the same
                    # word, this will only pick the first one. Better than nothing.
                    if server_name == "":
                        for servlog in gc.server_log_tree:
                            if arg.lower() in servlog.get_name().lower():
                                server_name = servlog.get_name()
                                break

                    if server_name != "":
                        gc.client.set_current_server(server_name)

                        # discord.py's "server.default_channel" is buggy.
                        # often times it will return 'none' even when
                        # there is a default channel. to combat this,
                        # we can just get it ourselves.
                        def_chan = ""

                        lowest = 999
                        for chan in servlog.get_server().channels:
                            if chan.type is discord.ChannelType.text:
                                if chan.permissions_for(servlog.get_server().me).read_messages:
                                    if chan.position < lowest:
                                        try:
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
                                # and set the default channel as read
                                for chanlog in servlog.get_logs():
                                    if chanlog.get_channel() is def_chan:
                                        chanlog.unread = False
                                        chanlog.mentioned_in = False
                                        break
                            # TODO: Bug: def_chan is sometimes ""
                            except: continue
                    else:
                        ui.set_display(gc.term.red + "Can't find server" + gc.term.normal)


                elif command == "channel" or command == 'c':
                    # check if arg is a valid channel, then switch
                    for servlog in gc.server_log_tree:
                        if servlog.get_server() is gc.client.get_current_server():
                            final_chanlog = ""
                            for chanlog in servlog.get_logs():
                                if chanlog.get_name().lower() == arg.lower():
                                    if chanlog.get_channel().type is discord.ChannelType.text:
                                        if chanlog.get_channel().permissions_for(servlog.get_server().me).read_messages:
                                            final_chanlog = chanlog
                                            break

                            # if we didn't find an exact match, assume partial
                            if final_chanlog == "":
                                for chanlog in servlog.get_logs():
                                    if chanlog.get_channel().type is discord.ChannelType.text:
                                        if chanlog.get_channel().permissions_for(servlog.get_server().me).read_messages:
                                            if arg.lower() in chanlog.get_name().lower():
                                                final_chanlog = chanlog
                                                break

                            if final_chanlog != "":
                                gc.client.set_current_channel(final_chanlog.get_name())
                                final_chanlog.unread = False
                                final_chanlog.mentioned_in = False
                                break
                            else:
                                ui.set_display(gc.term.red + "Can't find channel" + gc.term.normal)

                elif command == "nick":
                    try:
                        await gc.client.change_nickname(gc.client.get_current_server().me, arg)
                    except: # you don't have permission to do this here
                        pass
                elif command == "game":
                    await gc.client.set_game(arg)
                elif command == "file":
                    await send_file(gc.client, arg)
                elif command == "status":
                    status = arg.lower()
                    if status == "away" or status == "afk":
                        status = "idle"
                    elif "disturb" in status:
                        status = "dnd"

                    if status == "online" or status == "offline" \
                       or status == "idle" or status == "dnd":
                        await gc.client.set_status(status)

            # else we must have only a command, no argument
            else:
                command = gc.user_input
                if command == "clear": await ui.clear_screen()
                elif command == "quit": kill()
                elif command == "exit": kill()
                elif command == "help" or command == "h": print_help(gc)
                elif command == "servers" or command == "servs": await print_serverlist()
                elif command == "channels" or command == "chans": await print_channellist()
                elif command == "emojis": await print_emojilist()
                elif command == "users" or command == "members":
                    await ui.clear_screen()
                    await print_userlist()
                elif command[0] == 'c':
                    try:
                        if command[1].isdigit():
                            await channel_jump(command)
                    except IndexError:
                        pass

                await check_emoticons(gc.client, command)


        # this must not be a command...
        else:
            # check to see if it has any custom-emojis, written as :emoji:
            # we will need to expand them.
            # these will look like <:emojiname:39432432903201>
            # check if there might be an emoji
            if gc.user_input.count(":") >= 2:

                # if user has nitro, loop through *all* emojis
                if settings["has_nitro"]:
                    for emoji in gc.client.get_all_emojis():
                        short_name = ':' + emoji.name + ':'
                        if short_name in gc.user_input:
                            # find the "full" name of the emoji from the api
                            full_name = "<:" + emoji.name + ":" + emoji.id + ">"
                            gc.user_input = gc.user_input.replace(short_name, full_name)

                # else the user can only send from this server
                elif gc.client.get_current_server().emojis is not None \
                and len(gc.client.get_current_server().emojis) > 0:
                    for emoji in gc.client.get_current_server().emojis:
                        short_name = ':' + emoji.name + ':'
                        if short_name in gc.user_input:
                            # find the "full" name of the emoji from the api
                            full_name = "<:" + emoji.name + ":" + emoji.id + ">"
                            gc.user_input = gc.user_input.replace(short_name, full_name)

            # if we're here, we've determined its not a command,
            # and we've processed all mutations to the input we want
            # now we will try to send the message.
            text_to_send = gc.user_input
            if "@" in gc.user_input:
                sections = gc.user_input.lower().strip().split(" ")
                sects_copy = []
                for sect in sections:
                    if "@" in sect:
                        for member in gc.client.get_current_server().members:
                            if member is not gc.client.get_current_server().me:
                                if sect[1:] in member.display_name.lower():
                                    sect = "<@!" + member.id + ">"
                    sects_copy.append(sect)
                text_to_send = " ".join(sects_copy)

            # sometimes this fails --- this could be due to occasional
            # bugs in the api, or there was a connection problem
            # So we will try it 3 times, sleeping a bit inbetween
            for i in range(0,3):
                try:
                    await gc.client.send_message(gc.client.get_current_channel(), text_to_send)
                    break
                except:
                    await asyncio.sleep(3)
                    if i == 2:
                        ui.set_display(gc.term.blink_red + "error: could not send message")

        # clear our input as we've just sent it
        gc.user_input = ""

        # update the screen
        await ui.print_screen()

        await asyncio.sleep(0.25)
