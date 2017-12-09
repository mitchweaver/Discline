import sys
from os import system
from discord import ChannelType
from blessings import Terminal
from ui.line import Line
from ui.ui_utils import *
from utils.globals import *
from utils.quicksort import quick_sort_channel_logs
from settings import *
from utils.print_utils.userlist import print_userlist

# maximum number of lines that can be on the screen
# is updated every cycle as to allow automatic resizing
MAX_LINES = 0
# the index in the channel log the user is at
INDEX = 0
# buffer to allow for double buffering (stops screen flashing)
screen_buffer = []
# text that can be set to be displayed for 1 frame
display = ""

async def print_screen():
    global display
    # Get ready to redraw the screen
    left_bar_width = await get_left_bar_width()
    await clear_screen()

    await print_top_bar()

    if server_log_tree is not None:
        await print_channel_log(left_bar_width)

    await print_bottom_bar()

    # Print the buffer containing our message logs
    with term.location(0, 2):
        print("".join(screen_buffer), end="")

    await print_left_bar(left_bar_width)

    if display is not None: 
        print(display)
        display = ""

async def print_top_bar():
    topic = ""
    try: 
        if client.get_current_channel().topic is not None:
            topic = client.get_current_channel().topic
    except: 
        # if there is no channel topic, just print the channel name
        try: topic = client.get_current_channel().name
        except: pass

    with term.location(1,0):
        print("Server: " + await get_color(SERVER_DISPLAY_COLOR) \
                         + client.get_current_server_name() + term.normal, end="")

    with term.location(term.width // 2 - len(topic) // 2, 0):
        print(topic, end="")

    online_text = "Users online: "
    online_count = str(await client.get_online())
    online_length = len(online_text) + len(online_count)

    with term.location(term.width - online_length - 1, 0):
        print(await get_color(SERVER_DISPLAY_COLOR) + online_text \
              + term.normal + online_count, end="")

    divider = await get_color(SEPARATOR_COLOR) \
            + ("-" * term.width) + "\n" + term.normal

    with term.location(0, 1):
        print(divider, end="")

async def set_display(string):
    global display
    display = string

async def print_left_bar(left_bar_width):
    sep_color = await get_color(SEPARATOR_COLOR)
    for i in range(2, term.height - MARGIN):
        print(term.move(i, left_bar_width) + sep_color + "|" \
              + term.normal, end="")

    # Create a new list so we can preserve the server's channel order
    channel_logs = []

    for servlog in server_log_tree:
        if servlog.get_server() is client.get_current_server():
            for chanlog in servlog.get_logs():
                channel_logs.append(chanlog)
            break

    channel_logs = quick_sort_channel_logs(channel_logs)
   
    # buffer to print
    buffer = []
    count = 0
            
    for log in channel_logs:
        # don't print categories or voice chats
        # TODO: this will break on private messages
        if log.get_channel().type != ChannelType.text: continue
        text = log.get_name()
        if len(text) > left_bar_width:
            if TRUNCATE_CHANNELS:
                text = text[0:left_bar_width - 1]
            else:
                text = text[0:left_bar_width - 4] + "..."
        if log.get_channel() is client.get_current_channel():
            buffer.append(term.green + text + term.normal + "\n")
        else: 
            if log.get_channel() is not channel_logs[0]:
                pass

            if log.unread and log.get_channel() is not client.get_current_channel():
                text = term.blink_red + text + term.normal
            
            buffer.append(text + "\n")
        
        count += 1
        # should the server have *too many channels!*, stop them
        # from spilling over the screen
        if count == term.height - 2 - MARGIN: break

    with term.location(0, 2):
        print("".join(buffer))


async def print_bottom_bar():
  
    with term.location(0, term.height - 2):
        print(await get_color(SEPARATOR_COLOR) + ("-" * term.width) \
            + "\n" + term.normal, end="")

    bottom = await get_prompt()
    if len(input_buffer) > 0: bottom = bottom + "".join(input_buffer)
    with term.location(0, term.height - 1):
        print(bottom, end="")

async def clear_screen():
    # instead of "clearing", we're actually just overwriting
    # everything with white space. This mitigates the massive
    # screen flashing that goes on with "cls" and "clear"
    del screen_buffer[:]
    wipe = (" " * (term.width) + "\n") * term.height
    print(term.move(0,0) + wipe, end="")

async def print_channel_log(left_bar_width):
    global INDEX
    
    # If the line would spill over the screen, we need to wrap it
    # NOTE: term.width is calculating every time this function is called.
    #       Meaning that this will automatically resize the screen.
    # note: the "1" is the space at the start
    MAX_LENGTH = term.width - (left_bar_width + MARGIN) - 1
    # For wrapped lines, offset them to line up with the previous line
    offset = 0
    # List to put our *formatted* lines in, once we have OK'd them to print
    formatted_lines = []
 
    for server_log in server_log_tree:
        if server_log.get_server() is client.get_current_server():
            for channel_log in server_log.get_logs():
                if channel_log.get_channel() is client.get_current_channel():
                    # if the server has a "category" channel named the same
                    # as a text channel, confusion will occur
                    # TODO: private messages are not "text" channeltypes
                    if channel_log.get_channel().type != ChannelType.text: continue
                    # check to make sure the user can read the logs

                    for msg in channel_log.get_logs():
                        # The lines of this unformatted message
                        msg_lines = []
           
                        author_name = ""
                        try: author_name = msg.author.display_name
                        except:
                            try: author_name = msg.author.name
                            except: author_name = "Unknown Author"
                        
                        author_name_length = len(author_name)
                        author_prefix = await get_role_color(msg) + author_name + ": "

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

                                                        

                            line_length = len(line)
                            # Loop through, wrapping the lines until it behaves
                            while line_length > MAX_LENGTH:

                                line = line.strip()

                                # Take a section out of the line based on our max length
                                sect = line[:MAX_LENGTH - offset]

                                # Make sure we did not cut a word in half 
                                sect = sect[:sect.strip().rfind(' ')]
                                
                                # If this section isn't the first line of the comment,
                                # we should offset it to better distinguish it
                                offset = 0
                                if author_prefix not in sect:
                                    if line is not msg_lines[0]:
                                        offset = author_name_length + MARGIN
                                # add in now formatted line!
                                formatted_lines.append(Line(sect.strip(), offset))
                            
                                # since we just wrapped a line, we need to 
                                # make sure we don't overwrite it next time

                                # Split the line between what has been formatted, and
                                # what still remains needing to be formatted
                                if len(line) > len(sect):
                                    line = line.split(sect)[1]
                                    
                                # find the "real" length of the line, by subtracting
                                # any escape characters it might have. It would
                                # be wasteful to loop through all of the possibilities
                                # so instead we will simply subtract the length
                                # of the shortest for each that it has.
                                line_length = len(line)
                                target = "\e"
                                for target in line:
                                    line_length -= 5


                            # Once here, the string was either A: already short enough
                            # to begin with, or B: made through our while loop and has
                            # since been chopped down to less than our MAX_LENGTH
                            if len(line) > 0:
                                
                                offset = 0
                                if author_prefix not in line:
                                    offset = author_name_length + MARGIN

                                formatted_lines.append(Line(line.strip(), offset))
                                
                    # the max number of lines that can be shown on the screen
                    MAX_LINES = await get_max_lines()
                    
                    # where we should start printing from
                    # clamp the index as not to show whitespace
                    if INDEX < MAX_LINES: INDEX = MAX_LINES 

                    # ----- Trim out list to print out nicely ----- #
                    # trims off the front of the list, until our index
                    del formatted_lines[0:(len(formatted_lines) - INDEX)]
                    # retains the amount of lines for our screen, deletes remainder
                    del formatted_lines[MAX_LINES:]

                    for line in formatted_lines:
                        screen_buffer.append(" " * (left_bar_width + \
                                MARGIN + line.offset) + line.text + "\n")

                    # return as not to loop through all channels unnecessarily
                    return
