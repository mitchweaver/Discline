import re
from discord import MessageType
from utils.settings import settings
from utils.globals import gc, get_color
import utils

async def calc_mutations(msg):

    try: # if the message is a file, extract the discord url from it
        json = str(msg.attachments[0]).split("'")
        for string in json:
            if string is not None and string != "":
                if "cdn.discordapp.com/attachments" in string:
                    msg.content = string
                    break
    except IndexError: pass
    
    # otherwise it must not have any attachments and its a regular message
    text = msg.content


    # check for in-line code blocks
    if text.count("```") > 1:
        while("```") in text:
            text = await convert_code_block(text)

        msg.content = text

    # TODO: if there are asterics or __'s in the code, then
    # this will not stop them from being formatted
    # check for in-line code marks
    if text.count("`") > 1:
        while("`") in text:
            text = await convert_code(text)

        msg.content = text

    # check to see if it has any custom-emojis
    # These will look like <:emojiname:39432432903201>
    # We will recursively trim this into just :emojiname:
    if msg.server.emojis is not None and len(msg.server.emojis) > 0:
        for emoji in msg.server.emojis:
            full_name = "<:" + emoji.name + ":" + emoji.id + ">" 
                                
            while full_name in text:
                text = await trim_emoji(full_name, emoji.name, text)

        msg.content = text

    # check for boldened font
    if text.count("**") > 1:
        while("**") in text:
            text = await convert_bold(text)            

        msg.content = text

    # check for italic font
    if text.count("*") > 1:
        while("*") in text:
            text = await convert_italic(text)            

        msg.content = text

    # check for underlined font 
    if text.count("__") > 1:
        while("__") in text:
            text = await convert_underline(text)            

        msg.content = text

    # check for urls
    if "http://" in text or "https://" in text or "www." in text \
        or "ftp://" in text or ".com" in text:

        msg.content = await convert_url(text)

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
    return "📌 " + str(name) + " has pinned a message to this channel."


async def trim_emoji(full_name, short_name, string):
    return string.replace(full_name, ":" + short_name + ":")

async def convert_bold(string):
    sections = string.split("**")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return gc.term.normal + gc.term.white + left + " " + gc.term.bold(target) + gc.term.normal + \
            gc.term.white + " " + right

async def convert_italic(string):
    sections = string.split("*")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return gc.term.normal + gc.term.white +  left + " " + gc.term.italic(target) + gc.term.normal + \
            gc.term.white + " " + right

async def convert_underline(string):
    sections = string.split("__")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return gc.term.normal + gc.term.white + left + " " + gc.term.underline(target) + gc.term.normal + \
            gc.term.white + " " + right

async def convert_code(string):
    sections = string.split("`")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return gc.term.normal + gc.term.white +  left + " " + await get_color(settings["code_block_color"]) \
            + target  + gc.term.normal \
            + gc.term.white + " " + right

async def convert_code_block(string):
    sections = string.split("```")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return gc.term.normal + gc.term.white +  left + " " + gc.term.on_black(target) + gc.term.normal + \
            gc.term.white + " " + right

async def convert_url(string):
    formatted_line = []
    entities = []
    if " " in string:
        entities = string.split(" ")
    else:
        entities.append(string)

    for entity in entities:
        if "http://" in entity or "https://" in entity or "www." in entity \
           or "ftp://" in entity or ".com" in entity:
            entity = await get_color(settings["url_color"]) + gc.term.italic + gc.term.underline + entity + gc.term.normal
        formatted_line.append(entity)

    return " ".join(formatted_line)


