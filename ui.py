import os
from blessings import Terminal
from line import Line

term = Terminal()

# Margins for inside the terminal and between elements
MARGIN = 2

# Index of where the user is at in the channel message log
index = 0

def print_screen(client, channel_log):
    # Get ready to redraw the screen
    left_bar_width = int(term.width / 7)

    # Begin Drawing
    clear_screen()

    if channel_log is not None:
        print_channel_log(channel_log, left_bar_width)
    print_left_bar(left_bar_width)
    print_bottom_bar()
    print_prompt(client.get_prompt())

def print_left_bar(left_bar_width):
    for i in range(0, term.height - MARGIN):
        with term.location(left_bar_width, i):
            print('|')

def print_bottom_bar():
    for i in range(0, term.width):
        with term.location(i, term.height - MARGIN):
            print('-')

def print_prompt(prompt):
    with term.location(1, term.height - MARGIN//2):
        print(term.red("[") + "#" + prompt + term.red("]:"))

def clear_screen():
    term.clear()
    os.system('cls' if os.name == 'nt' else 'clear')

def print_channel_log(channel_log, left_bar_width):

    # start the first line at our margin
    step = MARGIN
    # If the line would spill over the screen, we need to wrap it
    # NOTE: term.width is calculating every time this function is called.
    #       Meaning that this will automatically resize the screen.
    max_length = term.width - (left_bar_width + MARGIN*2) - 1
    # For wrapped lines, offset them to line up with the previous line
    offset = 0
    # List to put our *formatted* lines in, once we have OK'd them to print
    formatted_lines = []
    
    for msg in channel_log:
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
            if len(line) > max_length:

                # Loop through, wrapping the lines until it behaves
                while len(line) > max_length:

                    line = line.strip()

                    # Take a section out of the line based on our max length
                    sect = line[:max_length - offset]

                    # Make sure we did not cut a word in half 
                    sect = sect[:sect.strip().rfind(' ')]
                    
                    # If this section isn't the first line of the comment,
                    # we should offset it to better distinguish it
                    offset = 0
                    if author_prefix not in sect:
                        offset = len(msg.author.display_name) + 2

                    # add in now formatted line!
                    formatted_lines.append(Line(sect.strip(), offset, step))
                   
                    # since we just wrapped a line, we need to make sure
                    # we don't overwrite it next time
                    step += 1

                    # Split the line between what has been formatted, and
                    # what still remains needing to be formatted
                    line = line.split(sect)[1]


            # Once here, the string was either A: already short enough
            # to begin with, or B: made through our while loop and has
            # since been chopped down to less than our max_length
            if len(line) > 0:
                
                offset = 0
                if author_prefix not in line:
                    offset = len(msg.author.display_name) + 2

                formatted_lines.append(Line(line.strip(), offset, step))
                
                step += 1

    # Once all lines have been formatted, we may now print them
    for line in formatted_lines:
        with term.location(left_bar_width + MARGIN + line.offset, line.step):
            print(line.text)
