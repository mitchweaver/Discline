import sys
import time
import curses
import discord
import logging
import asyncio
from utils.settings import settings
from utils.token_utils import get_token

scr = None
client = discord.Client()
serverName = ""
channelName = ""
channel = None

@client.event
async def on_message(msg):
    await client.wait_until_ready()
    clear()
    if serverName != msg.server.name or channelName != msg.channel.name:
        return
    offset = len(msg.author.name)+2
    scr.addstr(0,0, msg.author.name + ": ", curses.A_BOLD)
    scr.addstr(0,offset, msg.content)
    scr.move(nlines-1,0)
    scr.refresh()

@client.event
async def on_ready():
    clear()
    scr.addstr(0,0, "Ready!")
    scr.refresh()
    time.sleep(2)
    clear()
    scr.refresh()
    global serverName, channelName, channel
    serverName = settings["default_server"]
    channelName = settings["default_channel"]
    for svr in client.servers:
        if serverName == svr.name:
            server = svr
            for chl in server.channels:
                if chl.name == channelName:
                    channel = chl
    if not channel:
        logging.info("Server and/or channel are undefined")
        sys.exit(0)

async def input_handler():
    await client.wait_until_ready()
    nlines = scr.getmaxyx()[0]
    while True:
        await asyncio.sleep(0.1)
        buf = ['']
        scr.move(nlines-1,0)
        try:
            while buf[-1] != '\n':
                ch = scr.getch()
                if ch == -1:
                    await asyncio.sleep(0.05)
                    continue
                buf.append(chr(ch))
                if chr(ch) != '\n':
                    scr.addch(ch)
        except KeyboardInterrupt:
            sys.exit(0)
        del buf[-1]
        clear()
        await client.send_message(channel, "".join(buf))

def clear():
    for line in range(5):
        scr.move(line,0)
        scr.clrtoeol()
    scr.move(scr.getmaxyx()[0]-1,0)
    scr.clrtoeol()

def sendrecvTestLauncher():
    curses.wrapper(sendrecvTest)

def sendrecvTest(screen):
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)
    screen.nodelay(True)
    screen.addstr(0,0, "Loading. Please wait.")
    screen.refresh()
    global scr
    scr = screen
    token = get_token()
    asyncio.get_event_loop().create_task(input_handler())
    client.run(token, bot=False)
