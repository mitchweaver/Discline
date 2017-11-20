import sys
from blessings import Terminal
from printutils import *
from client import Client
from help import *
import ui

# await client.login('zemajujo@axsup.net', 'testpassword')

TOKEN = sys.argv[1]
MAX_MESSAGES=100
MAX_LOG_ENTRIES=200
client = Client(max_messages=MAX_MESSAGES)
term = Terminal()
prefix = '/'
default_prompt = "~"

@client.event
async def on_ready():
    client.wait_until_login()

    client.set_prompt(default_prompt)

    ##### init for debugging ###################
    client.set_current_server("DisKvlt")
    client.set_current_channel("terminal_discord")
    #############################################

     # Print initial screen
    ui.print_screen(client, None)

    while True:
        # messages = client.messages
        # for m in messages: print(m.content)

        # Clear channel log
        channel_log = []

        # Note: input() needs to be set at 1 line higher than the prompt
        with term.location(len(client.get_prompt()) + 7, term.height - 2):
            user_input = input().rstrip()

        # If input is blank, don't do anything
        if user_input == '': continue

        # Check if input is a command
        elif user_input[0] == prefix:
            # Strip the prefix
            user_input = user_input[1:]

            # Check if contains a space
            if ' ' in user_input:
                # Split into command and argument
                command,arg = user_input.split(" ", 1)
                if command == "server":
                    # TODO: check if arg is a valid server
                    client.set_current_server(arg)
                    client.set_current_channel(client.get_server(arg).default_channel)
                    ui.clear_screen()
                elif command == "channel":
                    # TODO: check if arg is a valid channel
                    client.set_current_channel(arg)
                    client.set_prompt(arg)
            
            # Else we must have only a command, no argument
            else:
                command = user_input
                # if command == "help": print_help()
                if command == "clear": ui.clear_screen()
                if command == "quit": kill()
                if command == "exit": kill()
        
        # This must not be a command...
        else: 
            # If all options have been exhausted, it must be chat
            await client.send_message(client.getCurrentChannel(), user_input)
            
        # Fill the log
        if client.get_current_channel is not None:
            async for msg in client.logs_from(client.get_current_channel(), limit=MAX_LOG_ENTRIES):
                channel_log.insert(0, msg)

        # Update the screen
        ui.print_screen(client, channel_log)


# kills the program and all its elements gracefully
def kill():
    ui.clear_screen()
    quit()


client.run(TOKEN, bot=False)
