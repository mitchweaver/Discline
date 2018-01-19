import discord
from utils.globals import gc

async def print_servers():
    print("Available servers: ")
    print_line_break();
    for server  in  gc.client.servers:
        print(server.name)

async def print_user():
    print('Logged in as: ' + gc.term.green + gc.client.user.name + gc.term.normal)

async def print_line_break():
    print("-" * int(gc.term.width * 0.45))

async def print_channels(server):
    print("Available channels:")
    print_line_break();
    for channel in  server.channels:
        print(channel.name)
