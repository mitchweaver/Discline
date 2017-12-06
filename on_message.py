import re
from discord import MessageType
from ui import print_screen
from globals import *
from settings import *


async def trim_emoji(full_name, short_name, string):
    return string.replace(full_name, ":" + short_name + ":")

async def convert_bold(string):
    sections = string.split("**")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + term.white + left + " " + term.bold(target) + term.normal + \
            term.white + " " + right

async def convert_italic(string):
    sections = string.split("*")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + term.white +  left + " " + term.italic(target) + term.normal + \
            term.white + " " + right

async def convert_underline(string):
    sections = string.split("__")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + term.white + left + " " + term.underline(target) + term.normal + \
            term.white + " " + right

async def convert_code(string):
    sections = string.split("`")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + term.white +  left + " " + await get_color(CODE_BLOCK_COLOR) \
            + target  + term.normal \
            + term.white + " " + right

async def convert_code_block(string):
    sections = string.split("```")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + term.white +  left + " " + term.on_black(target) + term.normal + \
            term.white + " " + right

async def convert_url(string):
    formatted_line = []
    entities = string.split(" ")
    for entity in entities:
        if "http://" in entity or "https://" in entity or "www." in entity \
           or "ftp://" in entity or ".com" in entity:
            entity = get_color(URL_COLOR) + term.italic + term.underline + entity + term.normal
        formatted_line.append(entity)
    return " ".join(formatted_line)


async def calc_mutations(msg):

    # if the message is a file, extract the discord url from it
    try:
        json = str(msg.attachments[0]).split("'")
        msg.content = json[5]
        return msg
    
    # # otherwise it must not have any attachments and its a regular message
    except:
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

        # else it must be a regular message, nothing else
        return msg


async def on_incoming_message(msg):

    # TODO: make sure it isn't a private message

       
    # find the server/channel it belongs to and add it
    try: # (note: the try/except here is to be able to break out of the double for loop)
        for server_log in server_log_tree:
            if server_log.get_server() == msg.server:
                for channel_log in server_log.get_logs():
                    if channel_log.get_channel() == msg.channel:
                        # check if the message is a "user has pinned..." message
                        if msg.type != MessageType.pins_add:
                            channel_log.append(await calc_mutations(msg))
                        else: 
                            name = ""
                            if msg.author.nick is not None and \
                               msg.author.nick != "":
                                name = msg.author.nick
                            else: name = msg.author.name
                            msg.content = "📌 " + name + " has pinned a message to this channel."
                            channel_log.append(msg)

                        if channel_log.get_channel() is not client.get_current_channel():
                            channel_log.unread = True
                        raise Found
    except:
        # redraw the screen
        await print_screen()
