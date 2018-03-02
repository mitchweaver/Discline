import sys
from os import system
from discord import ChannelType
from blessings import Terminal
from ui.line import Line
from ui.ui_utils import *
from utils.globals import gc, get_color
from utils.quicksort import quick_sort_channel_logs
from utils.settings import settings
from utils.print_utils.userlist import print_userlist

# maximum number of lines that can be on the screen
# is updated every cycle as to allow automatic resizing
MAX_LINES = 0
# buffer to allow for double buffering (stops screen flashing)
screen_buffer = []
# text that can be set to be displayed for 1 frame
display = ""
display_frames = 0

async def print_screen():
    # Get ready to redraw the screen
    left_bar_width = await get_left_bar_width()
    await clear_screen()

    if settings["show_top_bar"]:
        await print_top_bar(left_bar_width)

    if gc.server_log_tree is not None:
        await print_channel_log(left_bar_width)

    await print_bottom_bar(left_bar_width)

    # Print the buffer containing our message logs
    if settings["show_top_bar"]:
        if settings["show_separators"]:
            with gc.term.location(0, 2):
                print("".join(screen_buffer), end="")
        else:
            with gc.term.location(0, 1):
                print("".join(screen_buffer), end="")

    else:
        with gc.term.location(0, 0):
            print("".join(screen_buffer), end="")

    if settings["show_left_bar"]:
        await print_left_bar(left_bar_width)

    global display, display_frames
    if display != "": 
        print(display)
        display_frames -= 1
        if display_frames <=  0:
            display = ""

async def print_top_bar(left_bar_width):
    topic = ""
    try: 
        if gc.client.get_current_channel().topic is not None:
            topic = gc.client.get_current_channel().topic
    except: 
        # if there is no channel topic, just print the channel name
        try: topic = gc.client.get_current_channel().name
        except: pass

    
    text_length = gc.term.width - (36 + len(gc.client.get_current_server_name()))
    if len(topic) > text_length:
        topic = topic[:text_length]

    with gc.term.location(1,0):
        print("Server: " + await get_color(settings["server_display_color"]) \
                         + gc.client.get_current_server_name() + gc.term.normal, end="")

    with gc.term.location(gc.term.width // 2 - len(topic) // 2, 0):
        print(topic, end="")

    online_text = "Users online: "
    online_count = str(await gc.client.get_online())
    online_length = len(online_text) + len(online_count)

    with gc.term.location(gc.term.width - online_length - 1, 0):
        print(await get_color(settings["server_display_color"]) + online_text \
              + gc.term.normal + online_count, end="")

    if settings["show_separators"]:
        divider = await get_color(settings["separator_color"]) \
                + ("─" * gc.term.width) + "\n" + gc.term.normal

        with gc.term.location(0, 1):
            print(divider, end="")

        with gc.term.location(left_bar_width, 1):
            print(await get_color(settings["separator_color"]) + "┬", end="")


async def set_display(string):
    global display, display_frames
    loc = gc.term.width - 1 - len(string)
    escape_chars = "\e"
    for escape_chars in string:
        loc = loc - 5
    display = gc.term.move(gc.term.height - 1, loc) + string
    display_frames = 3

async def print_left_bar(left_bar_width):
    start = 0
    if settings["show_top_bar"]:
        start = 2

    if settings["show_separators"]:
        length = 0
        length = gc.term.height - settings["margin"]

        sep_color = await get_color(settings["separator_color"])
        for i in range(start, length):
            print(gc.term.move(i, left_bar_width) + sep_color + "│" \
                + gc.term.normal, end="")

    # Create a new list so we can preserve the server's channel order
    channel_logs = []

    for servlog in gc.server_log_tree:
        if servlog.get_server() is gc.client.get_current_server():
            for chanlog in servlog.get_logs():
                channel_logs.append(chanlog)
            break

    channel_logs = quick_sort_channel_logs(channel_logs)
   
    # buffer to print
    buffer = []
    count = 1
            
    for log in channel_logs:
        # don't print categories or voice chats
        # TODO: this will break on private messages
        if log.get_channel().type != ChannelType.text: continue
        text = log.get_name()
        length = len(text)

        if settings["number_channels"]:
            if count <= 9: length += 1
            else: length += 2

        if length > left_bar_width:
            if settings["truncate_channels"]:
                text = text[0:left_bar_width - 1]
            else:
                text = text[0:left_bar_width - 4] + "..."

        if log.get_channel() is gc.client.get_current_channel():
            if settings["number_channels"]:
                buffer.append(gc.term.normal + str(count) + ". " + gc.term.green + text + gc.term.normal + "\n")
            else: 
                buffer.append(gc.term.green + text + gc.term.normal + "\n")
        else: 
            if log.get_channel() is not channel_logs[0]:
                pass

            if log.get_channel() is not gc.client.get_current_channel():

                if log.unread and settings["blink_unreads"]: 
                    text = await get_color(settings["unread_channel_color"]) + text + gc.term.normal
                elif log.mentioned_in and settings["blink_mentions"]: 
                    text = await get_color(settings["unread_mention_color"]) + text + gc.term.normal
            
            if settings["number_channels"]:
                buffer.append(gc.term.normal + str(count) + ". " + text + "\n")
            else:
                buffer.append(text + "\n")
        
        count += 1
        # should the server have *too many channels!*, stop them
        # from spilling over the screen
        if count - 1  == gc.term.height - 2 - settings["margin"]: break

    with gc.term.location(0, start):
        print("".join(buffer))


async def print_bottom_bar(left_bar_width):
    if settings["show_separators"]:
        with gc.term.location(0, gc.term.height - 2):
            print(await get_color(settings["separator_color"]) + ("─" * gc.term.width) \
                + "\n" + gc.term.normal, end="")

        with gc.term.location(left_bar_width, gc.term.height - 2):
            print(await get_color(settings["separator_color"]) + "┴", end="")

    bottom = await get_prompt()
    if len(gc.input_buffer) > 0: bottom = bottom + "".join(gc.input_buffer)
    with gc.term.location(0, gc.term.height - 1):
        print(bottom, end="")

async def clear_screen():
    # instead of "clearing", we're actually just overwriting
    # everything with white space. This mitigates the massive
    # screen flashing that goes on with "cls" and "clear"
    del screen_buffer[:]
    wipe = (" " * (gc.term.width) + "\n") * gc.term.height
    print(gc.term.move(0,0) + wipe, end="")

async def print_channel_log(left_bar_width):
    global INDEX
    
    # If the line would spill over the screen, we need to wrap it
    # NOTE: gc.term.width is calculating every time this function is called.
    #       Meaning that this will automatically resize the screen.
    # note: the "1" is the space at the start
    MAX_LENGTH = gc.term.width - (left_bar_width + settings["margin"]) - 1
    # For wrapped lines, offset them to line up with the previous line
    offset = 0
    # List to put our *formatted* lines in, once we have OK'd them to print
    formatted_lines = []
 
    # the max number of lines that can be shown on the screen
    MAX_LINES = await get_max_lines()

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
                    
                    for msg in channel_log.get_logs():
                        # The lines of this unformatted message
                        msg_lines = []
           
                        HAS_MENTION = False
                        if "@" + gc.client.get_current_server().me.display_name in msg.clean_content:
                            HAS_MENTION = True

                        author_name = ""
                        try: author_name = msg.author.display_name
                        except:
                            try: author_name = msg.author.name
                            except: author_name = "Unknown Author"
                        
                        author_name_length = len(author_name)
                        author_prefix = await get_role_color(msg) + author_name + ": "

                        color = ""
                        if HAS_MENTION:
                            color = await get_color(settings["mention_color"])
                        else:
                            color = await get_color(settings["text_color"])
                        proposed_line = author_prefix + color + msg.clean_content.strip()

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
                                        offset = author_name_length + settings["margin"]
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
                            if len(line.strip()) > 0:
                                
                                offset = 0
                                if author_prefix not in line:
                                    offset = author_name_length + settings["margin"]

                                formatted_lines.append(Line(line.strip(), offset))
                                
                    # where we should start printing from
                    # clamp the index as not to show whitespace
                    if channel_log.get_index() < MAX_LINES: 
                        channel_log.set_index(MAX_LINES)
                    elif channel_log.get_index() > len(formatted_lines): 
                        channel_log.set_index(len(formatted_lines))

                    # ----- Trim out list to print out nicely ----- #
                    # trims off the front of the list, until our index
                    del formatted_lines[0:(len(formatted_lines) - channel_log.get_index())]
                    # retains the amount of lines for our screen, deletes remainder
                    del formatted_lines[MAX_LINES:]

                    # if user does not want the left bar, do not add margin
                    space = " "
                    if not settings["show_left_bar"]:
                        space = ""
                    
                    # add to the buffer!
                    for line in formatted_lines:
                        screen_buffer.append(space * (left_bar_width + \
                                settings["margin"] + line.offset) + line.text + "\n")

                    # return as not to loop through all channels unnecessarily
                    return
