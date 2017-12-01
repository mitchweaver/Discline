from os import system
import sys
from blessings import Terminal
from line import Line
from settings import *
from discord import ChannelType
import discord
from userlist import print_userlist

# maximum number of lines that can be on the screen
# is updated every cycle as to allow automatic resizing
MAX_LINES = 0
# the index in the channel log the user is at
INDEX = 0
# buffer to allow for double buffering (stops screen flashing)
screen_buffer = []

def print_screen():
    # Get ready to redraw the screen
    left_bar_width = get_left_bar_width()
    clear_screen()

    # top bar
    # print_top_bar()
    # TEMP:
    screen_buffer.append("\n \n")

# -------- Print Main Screen ------------------------- #
    if server_log_tree is not None:
        print_channel_log(left_bar_width)
# ---------------------------------------------------- #

    # second line margin
    screen_buffer.append("\n")
    print_bottom_bar()

    # Print the buffer. NOTE: the end="" is to prevent it
    # printing a new line character, which would add whitespace
    # to the bottom of the terminal
    print(term.move(0,0) + "".join(screen_buffer), end="")

    print_left_bar(left_bar_width)

    print_top_bar()

def print_left_bar(left_bar_width):
    for i in range(2, term.height - MARGIN):
        print(term.move(i, left_bar_width) + get_color(SEPARATOR_COLOR) + "|" \
              + term.normal)

    buffer = []
    count = 0
    for channel in client.get_current_server().channels:
        text = channel.name
        if len(text) > left_bar_width:
            text = text[0:left_bar_width - 3]
            text = text + "..."
        if channel == client.get_current_channel():
            buffer.append(term.green + text + term.normal + "\n")
        else: buffer.append(text + "\n")
        count += 1
        # should the server have *too many channels!*, stop them
        # from spilling over the screen
        if count == term.height - 5: break

    with term.location(1, 2):
        print("".join(buffer))

def print_top_bar():
    # screen_buffer.append(" " + "Server: " + get_color(SERVER_DISPLAY_COLOR) \
    #                      + client.get_current_server_name() + term.normal + "\n")
    # screen_buffer.append("-" * term.width + "\n")

    with term.location(1, 0):
        print(" " + "Server: " + get_color(SERVER_DISPLAY_COLOR) \
            + client.get_current_server_name() + term.normal + "\n", end="")
    
    online_count = 0
    for member in client.get_current_server().members:
        if member is None: continue # happens if a member left the server
        if member.status is discord.Status.online:
            online_count +=1 
    
    topic = ""
    try: topic = client.get_current_channel().topic
    # null exception if it has no topic
    except: pass

    # if there is no channel topic, just print the channel name
    if topic is None: topic = client.get_current_channel().name

    with term.location(term.width // 2 - len(topic) // 2, 0):
        print(term.normal + topic, end="")

    text = "Users online: "
    online_count = str(online_count)
    length = len(text) + len(online_count)
    with term.location(term.width - 1 - length, 0):
        print(text + term.green + online_count + term.normal, end="")

    # top bar separator
    print(term.move(1, 0) + get_color(SEPARATOR_COLOR) + ("-" * term.width) + "\n" \
          + term.normal)

    
def print_bottom_bar():
    screen_buffer.append(get_color(SEPARATOR_COLOR) + ("-" * term.width) + "\n" \
                         + term.normal)

    if client.get_prompt() == DEFAULT_PROMPT:
            prompt = get_color(PROMPT_BORDER_COLOR) + "[" + " " \
                    + get_color(PROMPT_COLOR) + DEFAULT_PROMPT + " " \
                    + get_color(PROMPT_BORDER_COLOR) + "]: " + term.normal
    else:
        prompt = get_color(PROMPT_BORDER_COLOR) + "["  + \
                get_color(PROMPT_COLOR) + "#" + client.get_prompt() \
                + get_color(PROMPT_BORDER_COLOR) + "]: " + term.normal

    if len(input_buffer) > 0: screen_buffer.append(prompt + "".join(input_buffer))
    else: screen_buffer.append(prompt)

def clear_screen():

    # instead of "clearing", we're actually just overwriting
    # everything with white space. This mitigates the massive
    # screen flashing that goes on with "cls" and "clear"
    del screen_buffer[:]
    wipe = (" " * (term.width) + "\n") * term.height
    print(term.move(0,0) + wipe, end="")

def print_channel_log(left_bar_width):
    global INDEX
    
    # If the line would spill over the screen, we need to wrap it
    # NOTE: term.width is calculating every time this function is called.
    #       Meaning that this will automatically resize the screen.
    MAX_LENGTH = term.width - (left_bar_width + MARGIN*2) - 1
    # For wrapped lines, offset them to line up with the previous line
    offset = 0
    # List to put our *formatted* lines in, once we have OK'd them to print
    formatted_lines = []
 
    for server_log in server_log_tree:
        if server_log.get_name().lower() == client.get_current_server_name().lower():
            for channel_log in server_log.get_logs():
                if channel_log.get_name().lower() == client.get_current_channel_name().lower():

                    for msg in channel_log.get_logs():
                        # The lines of this unformatted message
                        msg_lines = []

                        color = ""
                        
                        try: 
                            r = msg.author.top_role
                            if r.name.lower() == "admin":
                                color = get_color(ADMIN_COLOR)
                            elif r.name.lower() == "mod": 
                                color = get_color(MOD_COLOR)
                            elif r.name.lower() == "bot": 
                                color = get_color(BOT_COLOR)
                            elif CUSTOM_ROLE is not None and r.name == CUSTOM_ROLE:
                                color = get_color(CUSTOM_ROLE_COLOR)
                            elif CUSTOM_ROLE_2 is not None and r.name == CUSTOM_ROLE_2:
                                color = get_color(CUSTOM_ROLE_2_COLOR)
                            elif CUSTOM_ROLE_3 is not None and r.name == CUSTOM_ROLE_3:
                                color = get_color(CUSTOM_ROLE_3_COLOR)
                            elif NORMAL_USER_COLOR is not None:
                                color = get_color(NORMAL_USER_COLOR)
                            else: color = term.green
                        # if this fails, the user either left or was banned
                        except: 
                            if NORMAL_USER_COLOR is not None:
                                color = get_color(NORMAL_USER_COLOR)
                            else: color = term.green

                        author_prefix = color + msg.author.display_name + ": "

                        proposed_line = author_prefix + term.white(msg.clean_content.strip())

                        # If our message actually consists of
                        # of multiple lines separated by new-line
                        # characters, we need to accomodate for this.
                        # --- Otherwise: msg_lines will just consist of one line
                        msg_lines = proposed_line.split("\n")

                        for line in msg_lines:

                            # strip leading spaces - LEFT ONLY
                            line = line.lstrip()

                            # If our line is greater than our max length,
                            # that means the author has a long-line comment
                            # that wasn't using new line chars...
                            # We must manually wrap it.
                            if len(line) > MAX_LENGTH:

                                # Loop through, wrapping the lines until it behaves
                                while len(line) > MAX_LENGTH:

                                    line = line.strip()

                                    # Take a section out of the line based on our max length
                                    sect = line[:MAX_LENGTH - offset]

                                    # Make sure we did not cut a word in half 
                                    sect = sect[:sect.strip().rfind(' ')]
                                    
                                    # If this section isn't the first line of the comment,
                                    # we should offset it to better distinguish it
                                    offset = 0
                                    if author_prefix not in sect:
                                        offset = len(msg.author.display_name) + 2

                                    # add in now formatted line!
                                    formatted_lines.append(Line(sect.strip(), offset))
                                
                                    # since we just wrapped a line, we need to make sure
                                    # we don't overwrite it next time

                                    # Split the line between what has been formatted, and
                                    # what still remains needing to be formatted
                                    if len(line) > len(sect):
                                        line = line.split(sect)[1]


                            # Once here, the string was either A: already short enough
                            # to begin with, or B: made through our while loop and has
                            # since been chopped down to less than our MAX_LENGTH
                            if len(line) > 0:
                                
                                offset = 0
                                if author_prefix not in line:
                                    offset = len(msg.author.display_name) + 2

                                formatted_lines.append(Line(line.strip(), offset))
                                
                    # Once all lines have been formatted, we may now print them
                    # the max number of lines that can be shown on the screen
                    MAX_LINES = get_max_lines()
                    # where we should start printing from
                    if INDEX < MAX_LINES: INDEX = MAX_LINES 

                    # ----- Trim out list to print out nicely ----- #
                    # trims off the front of the list, until our index
                    del formatted_lines[0:(len(formatted_lines) - INDEX)]
                    # retains the amount of lines for our screen, deletes remainder
                    del formatted_lines[MAX_LINES:]

                    step = MARGIN // 2
                    for line in formatted_lines:
                        # with term.location(left_bar_width + MARGIN + line.offset, step):
                        #     print(line.text)
   
                        screen_buffer.append(" " * (left_bar_width + MARGIN + line.offset) + line.text + "\n")
   
                        step += 1

                    # return as not to loop through all channels unnecessarily
                    return

def get_max_lines():
    return term.height - MARGIN * 2

def get_left_bar_width():
    left_bar_width = term.width // LEFT_BAR_DIVIDER
    if left_bar_width < 8:
        return  8
    else: return left_bar_width

def print_serverlist():

    if len(client.servers) == 0:
        print("Error: You are not in any servers.")
        return

    buffer = []
    for server in client.servers:
        buffer.append(server.name + "\n")
            
    clear_screen()
    system("echo '" + "Available Servers: \n" \
        + "---------------------------- \n \n" \
        + "".join(buffer) \
        + "\n \n" \
        + "(press \'q\' to quit this dialog) \n" \
        + "' | less")

def print_channellist():
    if len(client.servers) == 0:
        print("Error: You are not in any servers.")
        return
    
    if len(client.get_current_server().channels) == 0:
        print("Error: Does this server not have any channels?")
        return

    buffer = []
    for channel in client.get_current_server().channels:
        if channel.type == ChannelType.text:
            buffer.append(channel.name + "\n")

    clear_screen()
    system("echo '" + "Available Channels in " \
           + client.get_current_server_name() + ": \n" \
           + "---------------------------- \n \n" \
           + "".join(buffer) \
           + "\n \n" \
           + "(press \'q\' to quit this dialog) \n" \
           + "' | less")


# takes in a string, returns the appropriate term.color
def get_color(string):
    if string == "white":   return term.white
    if string == "black":   return term.black
    if string == "red":     return term.red
    if string == "blue":    return term.blue
    if string == "yellow":  return term.yellow
    if string == "cyan":    return term.cyan
    if string == "magenta": return term.magenta
    if string == "green":   return term.green
   
    # if we're here, someone has one of their settings.py
    # colors defined wrong. We'll be nice and just return white.
    return term.white
