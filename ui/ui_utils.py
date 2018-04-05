import sys
import math
from datetime import datetime, timedelta
import asyncio
import curses
import signal
import logging
import re
import io
from discord import MessageType
from utils.log import log
from utils.settings import settings

async def get_role_color(r, colors):
    color = ""
    try:
        for role in settings["custom_roles"]:
            if r == role["name"].lower():
                color = colors[role["color"]]

        if color is not "": # The user must have already been assigned a custom role
            pass
        elif settings["normal_user_color"] is not None:
            color = colors[settings["normal_user_color"]]
        else: color = colors["green"]
    # if this fails, the user either left or was banned
    except:
        if settings["normal_user_color"] is not None:
            color = colors[settings["normal_user_color"]]
        else: color = colors["green"]
    return color

async def calc_mutations(msg):
    try: # if the message is a file, extract the discord url from it
        json = str(msg.attachments[0]).split("'")
        for string in json:
            if string is not None and string != "":
                if "cdn.discordapp.com/attachments" in string:
                    msg.content = string
                    break
    except IndexError: pass

    # if message is blank and message's timestamp is within a second
    # of a member's join timestamp, it's a join message
    if not msg.content:
        timeDiff = msg.timestamp - msg.author.joined_at
        if timedelta(seconds=-1) <= timeDiff <= timedelta(seconds=1):
            msg.content = "**({} joined the server!)**".format(msg.author.display_name)

            return msg

    text = msg.content

    # check to see if it has any custom-emojis
    # These will look like <:emojiname:39432432903201>
    # We will recursively trim this into just :emojiname:
    if msg.server.emojis is not None and len(msg.server.emojis) > 0:
        for emoji in msg.server.emojis:
            full_name = "<:" + emoji.name + ":" + emoji.id + ">"

            while full_name in text:
                text = await trim_emoji(full_name, emoji.name, text)

        msg.content = text

    # Catch all of the non-server (nitro) emojis
    mat = re.match('<:\w*:\d*>', text)
    if mat is not None:
        full_name = mat.group(0)

        while full_name in text:
            text = await trim_emoji(full_name, full_name[1:-1].split(':')[1], text)

        msg.content = text

    # check if the message is a "user has pinned..." message
    if msg.type == MessageType.pins_add:
        msg.content = await convert_pin(msg)

    # else it must be a regular message, nothing else
    return msg

async def convert_pin(msg):
    name = ""
    if msg.author.nick is not None and msg.author.nick != "":
        name = msg.author.nick
    else: name = msg.author.name
    return "{} {} has pinned a message to this channel.".format(chr(0x1f4cc), name)

async def trim_emoji(full_name, short_name, string):
    return string.replace(full_name, ":" + short_name + ":")
