import sys
import curses
from binascii import hexlify
import logging
from tests.formattedText import WrappedText
from tests.utils import User, Message

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

def formattingTestLauncher():
    try:
        curses.wrapper(formattingTest)
    except Exception as e:
        logging.error(e)
        quit()

def formattingTest(screen):
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)

    user = User("NatOsaka")
    maxyx = screen.getmaxyx()
    win = curses.newwin(maxyx[0]-2, maxyx[1]-2, 1,1)
    win_maxyx = win.getmaxyx()
    wt = WrappedText(win_maxyx[1])
    while True:
        win.clear()
        buf = ['']
        screen.move(maxyx[0]-1,0)
        screen.clrtoeol()
        screen.move(maxyx[0]-1,0)
        while buf[-1] != '\n':
            ch = screen.getch()
            buf.append(chr(ch))
            if buf[-1] != '\n':
                screen.addch(ch)
        text_offset = 0
        wt.addMessage(Message(user, "".join(buf)))
        lines = wt.getLines()
        line_offset = 0
        if len(lines) > win_maxyx[0]:
            line_offset = len(lines)-win_maxyx[0]
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
                    win.addstr(" ", curses.A_NORMAL)
            win.refresh()
            line_offset = 0
            if len(lines) > win_maxyx[0]:
                line_offset = len(lines)-win_maxyx[0]
