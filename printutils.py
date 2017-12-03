import discord
from settings import term, client

async def print_servers():
    print("Available servers: ")
    print_line_break();
    for server  in  client.servers:
        print(server.name)

async def print_user():
    print('Logged in as: ' + term.green + client.user.name + term.normal)

async def print_line_break():
    print("-" * int(term.width * 0.45))

async def print_channels(server):
    print("Available channels:")
    print_line_break();
    for channel in  server.channels:
        print(channel.name)
