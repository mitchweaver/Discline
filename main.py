import sys
from time import sleep
from printutils import *
from settings import *
from client import Client
import ui
from threading import Thread
import asyncio
from serverlog import ServerLog
from channellog import ChannelLog
from kbhit import KBHit
import hidecursor
import discord
from help import print_help
from printutils import *

message_to_send = ""
user_input = ""
init_complete = False

@client.event
async def on_ready():
    await client.wait_until_login()

    # completely hide the system's cursor
    hidecursor.hide_cursor()

    # these values are set in settings.py
    if DEFAULT_PROMPT is not None:
        client.set_prompt(DEFAULT_PROMPT)
    else: client.set_prompt('~')

    if DEFAULT_SERVER is not None:
        client.set_current_server(DEFAULT_SERVER)
        if DEFAULT_CHANNEL is not None:
            client.set_current_channel(DEFAULT_CHANNEL)
            client.set_prompt(DEFAULT_CHANNEL)

    if DEFAULT_GAME is not None:
        await client.change_presence(game=discord.Game(name=DEFAULT_GAME), \
                                     status=None,afk=False)

# --------------- INIT SERVERS --------------------------------------------- #
    print("Welcome to " + term.cyan + "Terminal Discord" + term.normal + "!")
    print_line_break()
    print_user()
    print_line_break()
    print("Initializing... \n")
    sys.stdin.flush()

    logs = []
    count = 0
    for server in client.servers:
        print("loading " + term.magenta + server.name + term.normal + " ...")
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                print("    loading " + term.yellow + channel.name + term.normal)
                channel_log = []
                try:
                    async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
                        count+=1
                        channel_log.insert(0, msg)
                    logs.append(ChannelLog(server.name, channel.name, channel_log))
                except:
                    # https forbidden exception, you don't have priveleges for
                    # this channel!
                    continue

        # add it to the tree
        server_log_tree.append(ServerLog(server.name, logs)) 

    print("Channels loaded! Found " + str(count) + " messages.")
 
    # Print initial screen
    ui.print_screen()
  
    global init_complete
    init_complete = True

def key_input():
    global user_input, input_buffer

    kb = KBHit()

    while True:
        if kb.kbhit():
            key = kb.getch()
            ordkey = ord(key)
            if ordkey == 10 or ordkey == 13: # enter key
                user_input = "".join(input_buffer)
                del input_buffer[:]
            elif ordkey == 27: kill() # escape
            elif ordkey == 127 or ordkey == 8: 
                if len(input_buffer) > 0:
                    del input_buffer[-1] # backspace
                else: 
                    sleep(0.0075)
                    continue
            else: input_buffer.append(key)
            ui.print_screen()
        sleep(0.01)

async def is_typing_handler():
    # Wait until all servers/channels are loaded
    while not init_complete: await asyncio.sleep(1)
    
    while True:
        if len(input_buffer) > 0:
            if input_buffer[0] is not "/":
                try: await client.send_typing(client.get_current_channel())
                except: pass
        try: await asyncio.sleep(0.2)
        except: pass

async def input_handler():
    global user_input
    await client.wait_until_ready()

    # Wait until all servers/channels are loaded
    while not init_complete: await asyncio.sleep(0.5)
   
    # Start our input thread
    t = Thread(target=key_input)
    t.daemon = True # thread will die upon main thread exiting
    t.start()

    while True:

        # If input is blank, don't do anything
        if user_input == '': 
            # while we wait for our input thread to get
            # some input, let discord.py's coroutines listen
            # for new events
            await asyncio.sleep(0.2)
            continue

        # Check if input is a command
        if user_input[0] == prefix:
            # Strip the prefix
            user_input = user_input[1:]

            # Check if contains a space
            if ' ' in user_input:
                # Split into command and argument
                command,arg = user_input.split(" ", 1)
                if command == "server" or command == 's':
                    # check if arg is a valid server, then switch
                    for serv in client.servers:
                        if serv.name == arg:
                            client.set_current_server(arg)
                            client.set_current_channel(client.get_server(arg).default_channel)
                            break
                elif command == "channel" or command == 'c':
                    # check if arg is a valid channel, then switch
                    for channel in client.get_current_server().channels:
                        if channel.name == arg:
                            client.set_current_channel(arg)
                            client.set_prompt(arg)
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

            # Else we must have only a command, no argument
            else:
                command = user_input
                if command == "clear": ui.clear_screen()
                elif command == "quit": kill()
                elif command == "exit": kill()
                elif command == "help": print_help()
                elif command == "servers": ui.print_serverlist()
                elif command == "channels": ui.print_channellist()
                elif command == "users": ui.print_userlist()
                elif command == "members": ui.print_userlist()
                elif command == "welcome": pass



                elif command == "shrug": 
                    try: await client.send_message(client.get_current_channel(), "¯\_(ツ)_/¯")
                    except: pass
                elif command == "tableflip": 
                    try: await client.send_message(client.get_current_channel(), "(╯°□°）╯︵ ┻━┻")
                    except: pass
                elif command == "unflip":
                    try: await client.send_message(client.get_current_channel(), "┬──┬ ノ( ゜-゜ノ)")
                    except: pass
                elif command == "zoidberg": 
                    try: await client.send_message(client.get_current_channel(), "(/) (°,,°) (/)")
                    except: pass
                elif command == "lenny": 
                    try: await client.send_message(client.get_current_channel(), "( ͡° ͜ʖ ͡°)")
                    except: pass
                elif command == "lennyx5": 
                    try: await client.send_message(client.get_current_channel(), "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)")
                    except: pass
                elif command == "glasses": 
                    try: await client.send_message(client.get_current_channel(), "(•_•) ( •_•)>⌐■-■ (⌐■_■)")
                    except: pass
                elif command == "walking_my_mods": 
                    try: await client.send_message(client.get_current_channel(), "⌐( ͡° ͜ʖ ͡°) ╯╲___卐卐卐卐")
                    except: pass

        
        # This must not be a command...
        else: 
            # If all options have been exhausted, it must be character
            try: await client.send_message(client.get_current_channel(), user_input)
            except:
                try: await client.send_message(client.get_current_channel(), user_input)
                except: print("Error: could not send message!")

        user_input = ""

        # Update the screen
        ui.print_screen()

        await asyncio.sleep(0.1)

# called whenever the client receives a message (from anywhere)
@client.event
async def on_message(message):
    if not init_complete: return

    # find the server/channel it belongs to and add it
    for server_log in server_log_tree:
        if server_log.get_name() == message.server.name:
            for channel_log in server_log.get_logs():
                if channel_log.get_name() == message.channel.name:
                    channel_log.append(message)
                    break

    # redraw the screen
    ui.print_screen()

@client.event
async def on_message_edit(msg_old, msg_new):
    if not init_complete: return
    msg_new.content = msg_new.content + " *(edited)*"

    # redraw the screen
    ui.print_screen()


# --------------------------------------------------------------------------- #

# start our own coroutines
try: asyncio.get_event_loop().create_task(input_handler())
except: pass
# SystemExit: pass
try: asyncio.get_event_loop().create_task(is_typing_handler())
except: pass
# SystemExit: pass

# start the client coroutine
try: client.run(sys.argv[1], bot=False)
except SystemExit: pass

# if we are here, the client's loop was cancelled or errored
try: kill()
except: quit()
