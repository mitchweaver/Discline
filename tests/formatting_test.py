import sys
import curses
import time
from binascii import hexlify
from utils.log import log
from ui.formattedText import FormattedText
from tests.utils import Role, User, Message

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

def formattingTestLauncher():
    curses.wrapper(formattingTest)

def formattingTest(screen):
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)

    user = User("mitch", Role("moderator"))
    maxyx = screen.getmaxyx()
    win = curses.newwin(maxyx[0]-2, maxyx[1]-2, 1,1)
    win.keypad(True)
    win_maxyx = win.getmaxyx()
    for f in [open("tests/test.txt", 'r'), open("tests/test2.txt", 'r')]:
        ft = FormattedText(win_maxyx[1])
        win.clear()
        text_offset = 0
        contents = f.read()
        ft.addMessage(Message(user, contents))
        lines = ft.getLines()
        line_offset = 0
        if len(lines) > win_maxyx[0]:
            line_offset = len(lines)-win_maxyx[0]
        for idx, line in enumerate(lines[line_offset:line_offset+win_maxyx[0]]):
            if line.isFirst:
                win.addstr(idx,0, line.user + ": ")
                text_offset = len(line.user) + 2
            win.move(idx,text_offset)
            for idy, word in enumerate(line.words):
                if len(line.words)-1 != idy and word.attrs == line.words[idy+1].attrs:
                    win.addstr(word.content + " ", word.attrs)
                else:
                    win.addstr(word.content, word.attrs)
                    win.addstr(" ", curses.A_NORMAL)
            win.refresh()
            line_offset = 0
            if len(lines) > win_maxyx[0]:
                line_offset = len(lines)-win_maxyx[0]
        win.getch()
