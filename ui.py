import os
import sys
from blessings import Terminal
from line import Line
from settings import *

# maximum number of lines that can be on the screen
# is updated every cycle as to allow automatic resizing
MAX_LINES = 0
# the index in the channel log the user is at
INDEX = 0
# buffer to allow for double buffering (stops screen flashing)
screen_buffer = []


"""
TODO: put current server in a top bar - with current channel description
"""

def print_screen():
    # Get ready to redraw the screen
    left_bar_width = term.width // 7
    clear_screen()

    # initial line margin
    screen_buffer.append("\n")

    if server_log_tree is not None:
        print_channel_log(left_bar_width)

    # second line margin
    screen_buffer.append("\n")
    print_bottom_bar()

    # Print the buffer. NOTE: the end="" is to prevent it
    # printing a new line character, which would add whitespace
    # to the bottom of the terminal
    print("".join(screen_buffer), end="")

    print_left_bar(left_bar_width)

def print_left_bar(left_bar_width):
    for i in range(0, term.height - MARGIN - MARGIN//2):
        with term.location(left_bar_width, i):
            print('|')

def print_bottom_bar():
    
    # with term.location(0, term.height - MARGIN + MARGIN // 2):
    #     print("-" * term.width)

    screen_buffer.append("-" * term.width + "\n")

    # print prompt + input_buffer
    with term.location(1, term.height):
        if client.get_prompt() == DEFAULT_PROMPT:
            prompt = term.red("[") + " " + DEFAULT_PROMPT + " " + term.red("]: ")
        else:
            prompt = term.red("[") + "#" + client.get_prompt() + term.red("]: ")
        
        # if len(input_buffer) > 0: print(prompt + "".join(input_buffer))
        # else: print(prompt)
        
        if len(input_buffer) > 0: screen_buffer.append(prompt + "".join(input_buffer))
        else: screen_buffer.append(prompt)

def clear_screen():
    # term.clear()
    # os.system('cls' if os.name == 'nt' else 'clear')
    del screen_buffer[:]
    
    lines = []
    for i in range(0, term.height + 1):
        lines.append(" " * term.width + "\n")
    with term.location(0,0):
        print("".join(lines))

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
        if server_log.get_name() == client.get_current_server_name():
            for channel_log in server_log.get_logs():
                if channel_log.get_name() == client.get_current_channel_name():

                    for msg in channel_log.get_logs():
                        # The lines of this unformatted message
                        msg_lines = []

                        author_prefix = term.green(msg.author.display_name + ": ")
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
                    MAX_LINES = term.height - MARGIN * 2
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
