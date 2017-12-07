import sys
from os import system
from time import sleep
from printutils import *
from client import Client
import ui
import asyncio
from serverlog import ServerLog
from channellog import ChannelLog
from kbhit import KBHit
import hidecursor
import discord
from help import print_help
from printutils import *
from settings import *
from globals import *
from sendfile import send_file
from on_message import on_incoming_message
from text_emoticons import check_emoticons

message_to_send = ""
user_input = ""
init_complete = False

try: 
    # git pull at start as to automatically update to master repo
    from subprocess import Popen,PIPE
    print("Checking for updates...")
    process = Popen(["git", "pull"], stdout=PIPE)
    output = process.communicate()[0].decode('utf-8').strip()

    if output != "Already up to date.":
        print("Updates downloaded! Please restart.")
        quit()
    else:
        print("Already up to date!" + "\n")
except:
    print("Error fetching automatic updates! Do you have git installed?")
    # They must not have git installed, no automatic updates for them!
    pass

print("Starting...")

@client.event
async def on_ready():
    await client.wait_until_login()

    # clear screen while the client loads
    system("clear")

    # completely hide the system's cursor
    await hidecursor.hide_cursor()

    # these values are set in settings.py
    if DEFAULT_PROMPT is not None:
        client.set_prompt(DEFAULT_PROMPT.lower())
    else: client.set_prompt('~')

    if DEFAULT_SERVER is not None:
        client.set_current_server(DEFAULT_SERVER)
        if DEFAULT_CHANNEL is not None:
            client.set_current_channel(DEFAULT_CHANNEL.lower())
            client.set_prompt(DEFAULT_CHANNEL.lower())

    if DEFAULT_GAME is not None:
        await client.change_presence(game=discord.Game(name=DEFAULT_GAME), \
                                     status=None,afk=False)

# --------------- INIT SERVERS --------------------------------------------- #
    print("Welcome to " + term.cyan + "Terminal Discord" + term.normal + "!")
    await print_line_break()
    await print_user()
    await print_line_break()
    print("Initializing... \n")
    try: sys.stdout.flush()
    except: pass

    # list to store our "ChannelLog" data type
    for server in client.servers:
        serv_logs = []
        count = 0
        print("loading " + term.magenta + server.name + term.normal + " ...")
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                if channel.permissions_for(server.me).read_messages:
                    try: # try/except in order to 'continue' out of multiple for loops
                        for serv_key in CHANNEL_IGNORE_LIST:
                            if serv_key.lower() == server.name.lower():
                                for name in CHANNEL_IGNORE_LIST[serv_key]:
                                    if channel.name.lower() == name.lower():
                                        raise Found

                        print("    loading " + term.yellow + channel.name + term.normal)
                        channel_log = []
                        try:
                            async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
                                count+=1
                                channel_log.insert(0, msg)
                            serv_logs.append(ChannelLog(channel, channel_log))
                        except:
                            print("Error loading logs from channel: " + \
                                channel.name + " in server: " + server.name)
                            continue
                    except: continue

        print("\n - Channels loaded! Found " + str(count) + " messages. \n")

        # add the channellog to the tree
        server_log_tree.append(ServerLog(server, serv_logs)) 
        
    if DEBUG:
        for slog in server_log_tree:
            for clog in slog.get_logs():
                print(slog.get_name() + " ---- " + clog.get_name())

    # Print initial screen
    await ui.print_screen()
  
    global init_complete
    init_complete = True

async def key_input():
    while not init_complete: await asyncio.sleep(0.25)


    kb = KBHit()
    global user_input, input_buffer
    while True:
        if await kb.kbhit():
            key = await kb.getch()
            ordkey = ord(key)
            if ordkey == 10 or ordkey == 13: # enter key
                user_input = "".join(input_buffer)
                del input_buffer[:]
            # elif ordkey == 27: kill() # escape # why are arrow keys doing this?
            elif ordkey == 127 or ordkey == 8: # backspace
                if len(input_buffer) > 0:
                    del input_buffer[-1]             
            else: input_buffer.append(key)
            await ui.print_screen()
        # This number could be adjusted, but it feels alright as is.
        # Too much higher lags the typing, but set it too low
        # and it will thrash the CPU
        await asyncio.sleep(0.0125)

async def is_typing_handler():
    while not init_complete: await asyncio.sleep(2)

    # user specified setting in settings.py
    if not SEND_IS_TYPING: return
    
    is_typing = False
    while True:
        # if typing a message, display '... is typing'
        if not is_typing:
            if len(input_buffer) > 0 and input_buffer[0] is not PREFIX:
                await client.send_typing(client.get_current_channel())
                is_typing = True
        elif len(input_buffer) == 0 or input_buffer[0] is PREFIX:
            is_typing = False
        
        await asyncio.sleep(0.5)


async def input_handler():
    global user_input, input_buffer
    await client.wait_until_ready()

    while not init_complete: await asyncio.sleep(0.25)
    
    while True:
        
        # If input is blank, don't do anything
        if user_input == '': 
            await asyncio.sleep(0.025)
            continue

        # Check if input is a command
        if user_input[0] == PREFIX:
            # Strip the prefix
            user_input = user_input[1:]

            # Check if contains a space
            if ' ' in user_input:
                # Split into command and argument
                command,arg = user_input.split(" ", 1)
                if command == "server" or command == 's':
                    # check if arg is a valid server, then switch
                    for servlog in server_log_tree:
                        if servlog.get_name().lower() == arg.lower():
                            client.set_current_server(arg.lower())
                            
                            # discord.py's "server.default_channel" is buggy.
                            # Often times it will return 'None' even when
                            # there IS a default channel. To combat this,
                            # we can just get it ourselves.
                            def_chan = ""
                            for chan in servlog.get_server().channels:
                                if chan.type == discord.ChannelType.text:
                                    if channel.permissions_for(server.me).read_messages:
                                        if chan.position == 0:
                                            def_chan = chan
                                            break

                            client.set_current_channel(def_chan.name.lower())
                            client.set_prompt(def_chan.name.lower())
                            # And set the default channel as read
                            for chanlog in servlog.get_logs():
                                if chanlog.get_channel() is def_chan:
                                    chanlog.unread = False
                                    break
                            break

                elif command == "channel" or command == 'c':
                    # check if arg is a valid channel, then switch
                    for servlog in server_log_tree:
                        if servlog.get_server() is client.get_current_server():
                            for chanlog in servlog.get_logs():
                                if chanlog.get_name().lower() == arg.lower():
                                    if chanlog.get_channel().type == discord.ChannelType.text:
                                        if channel.permissions_for(server.me).read_messages:
                                            client.set_current_channel(arg.lower())
                                            client.set_prompt(arg.lower())
                                            chanlog.unread = False
                                            break
                            break

                elif command == "nick":
                    try: 
                        await client.change_nickname(client.get_current_server().me, arg)
                    except: # you don't have permission to do this here
                        pass
                elif command == "game":
                    try:
                        await client.change_presence(game=discord.Game(name=arg),status=None,afk=False)
                    except: pass
                elif command == "file":
                    await send_file(client, arg)

            # Else we must have only a command, no argument
            else:
                command = user_input
                if command == "clear": await ui.clear_screen()
                elif command == "quit": kill()
                elif command == "exit": kill()
                elif command == "help": await print_help()
                elif command == "servers": await ui.print_serverlist()
                elif command == "channels": await ui.print_channellist()
                elif command == "users": await ui.print_userlist()
                elif command == "members": await ui.print_userlist()

                await check_emoticons(client, command)





        # This must not be a command...
        else: 
            # check to see if it has any custom-emojis, written as :emoji:
            # We will need to expand them.
            # These will look like <:emojiname:39432432903201>
            # check if there might be an emoji
            if user_input.count(":") >= 2:
                if client.get_current_server().emojis is not None \
                and len(client.get_current_server().emojis) > 0:


                    buffer = []
                    for emoji in client.get_current_server().emojis:
                        if ":" + emoji.name + ":" in user_input:
                            # find the "full" name of the emoji from the API
                            full_name = "<:" + emoji.name + ":" + emoji.id + ">"
                        
                            # split the input into sections
                            # ".split()" will swallow the :emojiname:
                            # we will then replace each instance with full_name
                            sections = user_input.split(':' + emoji.name + ':')

                            # check to see if the message wasn't just 1 emoji
                            if len(sections) > 1:
                                buffer.append(sections[0] + full_name) 
                            # if it wasn't there must not be more than 1 section
                            else:
                                buffer.append(full_name)
                                break
                            
                            # this creates a list of all sections except the first
                            # and last. We will append 'full_name' between each.
                            # Note: if their are only two sections, there will be
                            # no middle -- so we will simply append the second.
                            if len(sections) >= 3:
                                middle = sections[1:-1]
                                for sect in middle:
                                    buffer.append(sect + full_name) 
                            else:
                                # else this must be the second section, of
                                # which the emoji was inbetween
                                buffer.append(sections[1])
                                break
                        
                            
                            # Finally we will append the rightmost section
                            # Note: This should be safe as the two cases
                            # that would give us out-of-bound exceptions
                            # have been 'break'ed, (broke?), above
                            buffer.append(right)

                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                        # buffer = []
                            # target = []
                            # for c in list(user_input):
                            #     if c == ':':
                            #         if ':' in target: 
                            #             buffer = "".join(buffer) + full_name
                            #             buffer = list(buffer)
                            #             del target[:]
                            #         else:
                            #             target.append(c)
                            #     elif ':' not in target:
                            #         buffer.append(c)

                            #     else:
                            #         target.append(c)

                    # after formatting, assign it to our user_input
                    user_input = "".join(buffer)
            # If we're here, we've determined its not a command,
            # and we've processed all mutations to the input we want
            # Now we will try to send the message.
            try: 
                # sometimes this fails --- this could be due to occasional
                # bugs in the API, or there was a connection problem
                await client.send_message(client.get_current_channel(), user_input)
            except:
                try:
                    # we'll try to sleep 3s and resend, 2 more times
                    for i in range(0,1):
                        await asyncio.sleep(3)
                        await client.send_message(client.get_current_channel(), user_input)
                except:
                    # if the message failed to send 3x in a row, there's
                    # something wrong. Notify the user.
                    ui.set_display(term.blink_red + "Error: could not send message!")

        # clear our input as we've just sent it
        user_input = ""

        # Update the screen
        await ui.print_screen()

        # sleep while we wait for the screen to print and/or network
        await asyncio.sleep(0.1)

# called whenever the client receives a message (from anywhere)
@client.event
async def on_message(message):
    if not init_complete: return
    await on_incoming_message(message)

@client.event
async def on_message_edit(msg_old, msg_new):
    if not init_complete: return
    msg_new.content = msg_new.content + " *(edited)*"

    # redraw the screen
    await ui.print_screen()

@client.event
async def on_message_delete(msg):

    if not init_complete: return
    # TODO: PM's have 'None' as a server -- fix this later
    if msg.server is None: return

    try:
        for serverlog in server_log_tree:
            if serverlog.get_server() == msg.server:
                for channellog in serverlog.get_logs():
                    if channellog.get_channel()== msg.channel:
                        channellog.get_logs().remove(msg)
                        await ui.print_screen()
                        return
    except:
        # if the message cannot be found, an exception will be raised
        # this could be #1: if the message was already deleted,
        # (happens when multiple calls get excecuted within the same time)
        # or the user was banned, (in which case all their msgs disappear)
        pass

# --------------------------------------------------------------------------- #

# start our own coroutines
try: asyncio.get_event_loop().create_task(input_handler())
except SystemExit: pass
except KeyboardInterrupt: pass
try: asyncio.get_event_loop().create_task(key_input())
except SystemExit: pass
except KeyboardInterrupt: pass
try: asyncio.get_event_loop().create_task(is_typing_handler())
except SystemExit: pass
except KeyboardInterrupt: pass

# start the client coroutine
try: client.run(sys.argv[1], bot=False)
except SystemExit: pass
except KeyboardInterrupt: pass

# if we are here, the client's loop was cancelled or errored, or user exited
try: kill()
except: 
    # if our cleanly-exit kill function failed for whatever reason,
    # make sure we at least exit uncleanly
    quit()
