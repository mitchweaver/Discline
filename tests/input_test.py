import asyncio
import time
import logging
import curses
from blessings import Terminal
from input.messageEdit import MessageEdit

scr = None

def inputTestLauncher():
    try:
        curses.wrapper(inputTest)
    except Exception as e:
        logging.critical(e)
        quit()

async def print_bottom_bar():
    editBar = scr
    editBar.clear()
    # TODO: Add colors
    editBar.addstr(0,0, "[#{}]: ".format("general"))

def inputTest(screen):
    global scr
    scr = screen
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doWork())

async def doWork():
    offset = len("general")+5
    curses.cbreak()
    curses.noecho()
    scr.keypad(True)
    scr.nodelay(True)
    edit = MessageEdit(scr.getmaxyx()[1])
    await print_bottom_bar()
    while True:
        ch = scr.getch()
        if ch == -1:
            asyncio.sleep(0.01)
            continue
        ret = edit.addKey(ch)
        if ret is not None:
            logging.info(ret)
            await print_bottom_bar()
            edit.reset()
        else:
            data = edit.getCurrentData()
            scr.clear()
            await print_bottom_bar()
            scr.addstr(0,offset, data[0])
            scr.move(0,offset+data[1])
