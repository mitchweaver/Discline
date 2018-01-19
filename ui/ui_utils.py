from utils.globals import get_color, gc
from utils.settings import settings

async def get_prompt():
    left = await get_color(settings["prompt_border_color"]) + "["
    right = await get_color(settings["prompt_border_color"]) + "]: " + gc.term.normal
    middle = ""
    if gc.client.get_prompt() == settings["default_prompt"]:
        middle = " " + await get_color(settings["prompt_color"]) + settings["default_prompt"] + " "
    else:
        middle = await get_color(settings["prompt_hash_color"]) + "#" \
                + await get_color(settings["prompt_color"]) + gc.client.get_prompt()

    return left + middle + right


async def get_max_lines():
    num = 0
    if settings["show_top_bar"] and settings["show_separators"]:
        num = gc.term.height - settings["margin"] * 2
    elif settings["show_top_bar"] and not settings["show_separators"]:
        num = gc.term.height - settings["margin"]
    elif not settings["show_top_bar"] and not settings["show_separators"]:
        num = gc.term.height - 1
        
    return num

async def get_left_bar_width():
    if not settings["show_left_bar"]: return 0

    left_bar_width = gc.term.width // settings["left_bar_divider"]
    if left_bar_width < 8: return  8
    else: return left_bar_width

async def get_role_color(msg):
    color = ""
    try: 
        r = msg.author.top_role.name.lower()
        for role in settings["custom_roles"]:
            if r == role["name"].lower():
                color = await get_color(role["color"])

        if color is not "": # The user must have already been assigned a custom role
            pass
        elif settings["normal_user_color"] is not None:
            color = await get_color(settings["normal_user_color"])
        else: color = gc.term.green
    # if this fails, the user either left or was banned
    except: 
        if settings["normal_user_color"] is not None:
            color = await get_color(settings["normal_user_color"])
        else: color = gc.term.green
    return color

