import sys
import curses
from binascii import hexlify
import logging
from tests.formattedText import WrappedText

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

class User:
    def __init__(self, name):
        self.name = name
        self.nick = name

class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content

async def formattingTestLauncher():
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
        buf = ['']
        screen.move(maxyx[0]-1,0)
        while buf[-1] != '\n':
            ch = screen.getch()
            buf.append(chr(ch))
            if buf[-1] != '\n':
                screen.addch(ch)
        screen.move(maxyx[0]-1,0);screen.clrtoeol()
        wt.addMessage(Message(user, "".join(buf)))
        for count, msg in enumerate(wt.getMsgs()):
            offset = len(msg.name)+2 #": "
            win.addstr(count,0, msg.name + ": ")
            win.move(count,offset)
            flag_nl = False
            num_nl = 0
            for line in msg.tokens:
                logging.info(line)
                for token in line:
                    win.addstr(token.content + " ", token.attrs)
                num_nl += 1
                win.move(count+num_nl,offset)
            win.refresh()
