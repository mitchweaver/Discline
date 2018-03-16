import curses
import random
import logging
from tests.utils import User, Message
from tests.formattedText import WrappedText

async def scrollingTestLauncher():
    curses.wrapper(scrollingTest)

def scrollingTest(screen):
    users = [
            User("NatOsaka"),
            User("mitch"),
            User("E5ten"),
            User("Nep")
    ]

    maxyx = screen.getmaxyx()
    screen.box()
    screen.refresh()
    win = curses.newwin(maxyx[0]-2, maxyx[1]-2, 1,1)
    win.keypad(True)
    win_maxyx = win.getmaxyx()
    wt = WrappedText(win_maxyx[1], 100)

    with open("tests/loremSample.txt", 'r') as f:
        for line in f:
            wt.addMessage(Message(random.choice(users), line.rstrip()))
        wt.addMessage(Message(users[0], "Last message"))
        lines = wt.getLines()
        line_offset = 0
        if len(lines) > win_maxyx[0]:
            line_offset = len(lines)-win_maxyx[0]
        while True:
            win.clear()
            text_offset = 0
            for idx, line in enumerate(lines[line_offset:line_offset+win_maxyx[0]]):
                if line.isFirst:
                    win.addstr(idx,0, line.user + ": ", curses.A_BOLD)
                    text_offset = len(line.user) + 2
                win.move(idx,text_offset)
                for idx, token in enumerate(line.words):
                    if len(line.words)-1 != idx and token.attrs == line.words[idx+1].attrs:
                        win.addstr(token.content + " ", token.attrs)
                    else:
                        win.addstr(token.content, token.attrs)
                win.refresh()
            ch = win.getch()
            if chr(ch) == 'q':
                break
            elif ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            elif ch == curses.KEY_PPAGE:
                line_offset -= 5
            elif ch == curses.KEY_NPAGE:
                line_offset += 5
            if line_offset < 0:
                line_offset = 0
            elif line_offset > (len(lines)-win_maxyx[0]):
                line_offset = len(lines)-win_maxyx[0]
