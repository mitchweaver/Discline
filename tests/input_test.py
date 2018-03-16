import asyncio
import logging
import curses
from tests.messageEdit import MessageEdit

def inputTestLauncher():
    try:
        curses.wrapper(inputTest)
    except Exception as e:
        logging.critical(e)
        quit()

def inputTest(screen):
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)
    edit = MessageEdit(screen.getmaxyx()[1])
    while True:
        ch = screen.getch()
        ret = edit.addKey(ch)
        if ret is not None:
            for i in range(5):
                screen.move(i+1,0);screen.clrtoeol()
            screen.addstr(1,0, ret)
            edit.reset()
        else:
            data = edit.getCurrentData()
            screen.move(0,0);screen.clrtoeol()
            screen.addstr(0,0, data[0])
            screen.move(0,data[1])
