import asyncio
import discord

from input.kbhit import KBHit
import ui.ui as ui 
from utils.globals import *
from utils.print_utils.help import print_help
from utils.print_utils.userlist import print_userlist
from utils.print_utils.serverlist import print_serverlist
from utils.print_utils.channellist import print_channellist
from settings import *
from commands.text_emoticons import check_emoticons
from commands.sendfile import send_file
from commands.channel_jump import channel_jump

kb = ""

def init_input():
    global kb
    kb = KBHit()

async def key_input():
    await client.wait_until_ready()
    
    global user_input, kb
    memory = ""
    key = ""
    while True:
        if await kb.kbhit() or memory == "[":
            key = await kb.getch()
            ordkey = ord(key)
            
            if memory == "[":
                if key == "6": # page down
                    client.get_current_channel_log().dec_index(SCROLL_LINES)
                    input_buffer.pop()
                elif key == "5": # page up
                    client.get_current_channel_log().inc_index(SCROLL_LINES)
                    input_buffer.pop()
            else:
                if ordkey == 10 or ordkey == 13: # enter key
                    user_input = "".join(input_buffer)
                    del input_buffer[:]
                elif ordkey == 127 or ordkey == 8: # backspace
                    if len(input_buffer) > 0:
                        del input_buffer[-1]             
                # elif ordkey == 27: kill() # escape # why are arrow keys doing this?
                
                # elif ordkey == 8 or ordkey == 72: # ctrl/shift  + h
                #     for i in range(0, 100):
                #         print("HHHHHH")
                # elif ordkey == 10 or ordkey == 74: # ctrl/shift  + j
                #     print("JJJJJ")
                # elif ordkey == 11 or ordkey == 75: # ctrl/shift  + k
                #     print("KKKK")
                # elif ordkey == 12 or ordkey == 76: # ctrl/shift  + l
                #     print("LLLL")

                elif ordkey >= 32 and ordkey <= 122:
                    input_buffer.append(key)
                elif ordkey == 9:
                    input_buffer.append(" " * 4) # tab key
                
            memory = key
            if key != "[":
                await ui.print_screen()

        if key != "[":
            await asyncio.sleep(0.015)

async def input_handler():
    await client.wait_until_ready()
   
    global user_input
    while True:

        # If input is blank, don't do anything
        if user_input == '': 
            await asyncio.sleep(0.05)
            continue

        # # check if input is a command
        if user_input[0] == PREFIX:
            # strip the PREFIX
            user_input = user_input[1:]

            # check if contains a space
            if ' ' in user_input:
                # split into command and argument
                command,arg = user_input.split(" ", 1)

                if command == "server" or command == 's':
                    
                    server_name = ""
                    # check if arg is a valid server, then switch
                    for servlog in server_log_tree:
                        if servlog.get_name().lower() == arg.lower():
                            server_name = servlog.get_name()
                            break

                    # if we didn't find an exact match, assume only partial
                    # Note if there are multiple servers containing the same
                    # word, this will only pick the first one. Better than nothing.
                    if server_name == "":
                        for servlog in server_log_tree:
                            if arg.lower() in servlog.get_name().lower():
                                server_name = servlog.get_name()
                                break

                    if server_name != "":
                        client.set_current_server(server_name)

                        # discord.py's "server.default_channel" is buggy.
                        # often times it will return 'none' even when
                        # there is a default channel. to combat this,
                        # we can just get it ourselves.
                        def_chan = ""
                        for chan in servlog.get_server().channels:
                            if chan.type is discord.ChannelType.text:
                                if chan.permissions_for(servlog.get_server().me).read_messages:
                                    if chan.position == 0:
                                        def_chan = chan
                                        break

                        client.set_current_channel(def_chan.name)
                        # and set the default channel as read
                        for chanlog in servlog.get_logs():
                            if chanlog.get_channel() is def_chan:
                                chanlog.unread = False
                                chanlog.mentioned_in = False
                                break
                    else:
                        ui.set_display(term.red + "Can't find server" + term.normal)


                elif command == "channel" or command == 'c':
                    # check if arg is a valid channel, then switch
                    for servlog in server_log_tree:
                        if servlog.get_server() is client.get_current_server():
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
                                client.set_current_channel(final_chanlog.get_name())
                                final_chanlog.unread = False
                                final_chanlog.mentioned_in = False
                                break
                            else:
                                ui.set_display(term.red + "Can't find channel" + term.normal)

                elif command == "nick":
                    try: 
                        await client.change_nickname(client.get_current_server().me, arg)
                    except: # you don't have permission to do this here
                        pass
                elif command == "game":
                    try: await client.change_presence(game=discord.Game(name=arg),status=None,afk=False)
                    except: pass
                elif command == "file":
                    await send_file(client, arg)

            # else we must have only a command, no argument
            else:
                command = user_input
                if command == "clear": await ui.clear_screen()
                elif command == "quit": kill()
                elif command == "exit": kill()
                elif command == "help": await print_help()
                elif command == "servers": await print_serverlist()
                elif command == "channels": await print_channellist()
                elif command == "users" or command == "members": 
                    await ui.clear_screen()
                    await print_userlist()
                elif command[0] == 'c':
                    try: 
                        if command[1].isdigit():
                            await channel_jump(command)
                    except IndexError: pass

                await check_emoticons(client, command)


        # this must not be a command...
        else: 
            # check to see if it has any custom-emojis, written as :emoji:
            # we will need to expand them.
            # these will look like <:emojiname:39432432903201>
            # check if there might be an emoji
            if user_input.count(":") >= 2:
                
                # if user has nitro, loop through *all* emojis
                if HAS_NITRO:
                    for emoji in client.get_all_emojis():
                        short_name = ':' + emoji.name + ':'
                        if short_name in user_input:
                            # find the "full" name of the emoji from the api
                            full_name = "<:" + emoji.name + ":" + emoji.id + ">"
                            user_input = user_input.replace(short_name, full_name)

                # else the user can only send from this server
                elif client.get_current_server().emojis is not None \
                and len(client.get_current_server().emojis) > 0:
                    for emoji in client.get_current_server().emojis:
                        short_name = ':' + emoji.name + ':'
                        if short_name in user_input:
                            # find the "full" name of the emoji from the api
                            full_name = "<:" + emoji.name + ":" + emoji.id + ">"
                            user_input = user_input.replace(short_name, full_name)

            # if we're here, we've determined its not a command,
            # and we've processed all mutations to the input we want
            # now we will try to send the message.
            try: 
                # sometimes this fails --- this could be due to occasional
                # bugs in the api, or there was a connection problem
                await client.send_message(client.get_current_channel(), user_input)
            except:
                try:
                    # we'll try to sleep 3s and resend, 2 more times
                    for i in range(0,1):
                        await asyncio.sleep(3)
                        await client.send_message(client.get_current_channel(), user_input)
                except:
                    # if the message failed to send 3x in a row, there's
                    # something wrong. notify the user.
                    ui.set_display(term.blink_red + "error: could not send message!")

        # clear our input as we've just sent it
        user_input = ""

        # update the screen
        await ui.print_screen()
        
        await asyncio.sleep(0.25)
