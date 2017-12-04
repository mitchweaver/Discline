import sys
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

message_to_send = ""
user_input = ""
init_complete = False

@client.event
async def on_ready():
    await client.wait_until_login()

    # completely hide the system's cursor
    await hidecursor.hide_cursor()

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
    await print_line_break()
    await print_user()
    await print_line_break()
    print("Initializing... \n")
    sys.stdin.flush()

    # list to store our "ChannelLog" data type
    logs = []
    for server in client.servers:
        count = 0
        print("loading " + term.magenta + server.name + term.normal + " ...")
        for channel in server.channels:
            
            if channel.name == "black_metal": continue
            elif channel.name == "death_metal": continue
            elif channel.name == "punk_core_grind_slam": continue
            elif channel.name == "kvlt_memes": continue
            elif channel.name == "non_metal": continue
            elif channel.name == "new_releases": continue
            elif channel.name == "kvlt_pics": continue
            elif channel.name == "kvltness": continue
            elif channel.name == "music_pick_ups": continue
            elif channel.name == "admin_chat": continue
            elif channel.name == "other_pickups": continue
            elif channel.name == "kvlt_speak": continue
            elif channel.name == "dungeon_synth": continue
            elif channel.name == "heavy_power_speed_trad": continue
            elif channel.name == "musicians_talk": continue
            elif channel.name == "doom_drone_metal": continue
            elif channel.name == "merch_pick_ups": continue
            elif channel.name == "prog_avantgarde_djent": continue
            elif channel.name == "thrash_crossover": continue
            elif channel.name == "pin_board": continue

            if channel.type == discord.ChannelType.text:
                print("    loading " + term.yellow + channel.name + term.normal)
                channel_log = []
                try:
                    async for msg in client.logs_from(channel, limit=MAX_LOG_ENTRIES):
                        count+=1
                        channel_log.insert(0, msg)
                    logs.append(ChannelLog(server, channel, channel_log))
                except:
                    # https forbidden exception, you don't have priveleges for
                    # this channel!
                    continue
    

        print("\n - Channels loaded! Found " + str(count) + " messages. \n")

        # add the channellog to the tree
        server_log_tree.append(ServerLog(server, logs)) 

 
    # Print initial screen
    await ui.print_screen()
  
    global init_complete
    init_complete = True

async def key_input():
    global user_input, input_buffer

    while not init_complete: await asyncio.sleep(0.25)

    kb = KBHit()

    while True:
        if kb.kbhit():
            key = kb.getch()
            ordkey = ord(key)
            if ordkey == 10 or ordkey == 13: # enter key
                user_input = "".join(input_buffer)
                del input_buffer[:]
            # elif ordkey == 27: kill() # escape # why are arrow keys doing this?
            elif ordkey == 127 or ordkey == 8: 
                if len(input_buffer) > 0:
                    del input_buffer[-1] # backspace
            else: input_buffer.append(key)
            await ui.print_screen()
        await asyncio.sleep(0.01)

async def input_handler():
    global user_input, input_buffer
    await client.wait_until_ready()

    while not init_complete: await asyncio.sleep(0.25)
    
    while True:

        # If input is blank, don't do anything
        if user_input == '': 
            await asyncio.sleep(0.05)
            continue

        # if typing a message, display '... is typing'
        if SEND_IS_TYPING:
            if len(input_buffer) > 0:
                if input_buffer[0] is not PREFIX:
                    try: await client.send_typing(client.get_current_channel())
                    except: pass


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
                    for serv in client.servers:
                        if serv.name.lower() == arg.lower():
                            client.set_current_server(arg)
                            client.set_current_channel(client.get_server(arg).default_channel)
                            break
                elif command == "channel" or command == 'c':
                    # check if arg is a valid channel, then switch
                    for channel in client.get_current_server().channels:
                        if channel.name.lower() == arg.lower():
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
        await ui.print_screen()

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
    # note: PM's have 'None' as a server -- fix this later
    if msg.server is None: return

    for serverlog in server_log_tree:
        if serverlog.get_server() == msg.server:
            for channellog in serverlog.get_logs():
                if channellog.get_channel()== msg.channel:
                    channellog.get_logs().remove(msg)
                    await ui.print_screen()
                    return

# --------------------------------------------------------------------------- #

# start our own coroutines
try: asyncio.get_event_loop().create_task(input_handler())
except: pass
try: asyncio.get_event_loop().create_task(key_input())
except: pass

# start the client coroutine
try: client.run(sys.argv[1], bot=False)
except SystemExit: pass

# if we are here, the client's loop was cancelled or errored
try: kill()
except: quit()
