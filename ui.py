import os
from blessings import Terminal

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

    print_left_bar(left_bar_width)
    print_bottom_bar()
    print_prompt(client.get_prompt())
    if channel_log is not None:
        print_channel_log(channel_log, left_bar_width)

def print_left_bar(left_bar_width):
    for i in range(0, term.height - MARGIN):
        with term.location(left_bar_width, i):
            print('|')

def print_bottom_bar():
    for i in range(0, term.width):
        with term.location(i, term.height - MARGIN):
            print('-')

def print_prompt(prompt):
    with term.location(1, term.height - 1):
        print(term.red("[ ") + prompt + term.red(" ]: "))

def clear_screen():
    term.clear()
    os.system('cls' if os.name == 'nt' else 'clear')

def print_channel_log(channel_log, left_bar_width):
    step = MARGIN
    offset = 0

    for msg in channel_log:

        # check if we've filled the term window, if so, stop printing!
        if step + MARGIN*2 >= term.height: break

        # Our line, filled with hope to be printed
        author_prefix = term.green(msg.author.display_name + ": ")
        proposed_line = author_prefix + term.white(msg.clean_content.strip())

        # If our input line actually consists of
        # of multiple lines separated by new-line
        # characters, we need to accomodate for this.
        # --- Otherwise: lines will just be the one line
        lines = proposed_line.split("\n")

        for line in lines:

            # strip leading spaces - LEFT ONLY
            line = line.lstrip()

            # If the line would spill over the screen, we need to wrap it
            max_length = term.width - (left_bar_width + MARGIN*2) - 1
            # if our line is greater than our max length,
            # that means the author has a long-line comment
            # that wasn't using new line chars... We must
            # manually wrap it.
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


                    with term.location(left_bar_width + MARGIN + offset, step):
                        print(sect.lstrip())
                   
                    # since we just wrapped a line, we need to make sure
                    # we don't overwrite it
                    step += 1

                    # Split the line between what has been printed, and
                    # what still remains needing to be printed
                    line = line.split(sect)[1]


            # Once here, the string was either A: already short enough
            # to begin with, or B: made through our while loop and has
            # since been chopped down to less than our max_length
            if len(line) > 0:
                
                offset = 0
                if author_prefix not in line:
                    offset = len(msg.author.display_name) + 2

                with term.location(left_bar_width + MARGIN + offset, step):
                    print(line.strip())
                
                step += 1
