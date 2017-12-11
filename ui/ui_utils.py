from utils.globals import term, client, get_color
from utils.settings import settings

async def get_prompt():
    left = await get_color(settings["prompt_border_color"]) + "["
    right = await get_color(settings["prompt_border_color"]) + "]: " + term.normal
    middle = ""
    if client.get_prompt() == settings["default_prompt"]:
        middle = " " + await get_color(settings["prompt_color"]) + settings["default_prompt"] + " "
    else:
        middle = await get_color(settings["prompt_hash_color"]) + "#" \
                + await get_color(settings["prompt_color"]) + client.get_prompt()

    return left + middle + right


async def get_max_lines():
    num = 0
    if settings["show_top_bar"]:
        num = term.height - settings["margin"] * 2
    else:
        num = term.height - settings["margin"]

    if not settings["show_separators"]:
        num += 2
        
    return num

async def get_left_bar_width():
    if not settings["show_left_bar"]: return 0

    left_bar_width = term.width // settings["left_bar_divider"]
    if left_bar_width < 8: return  8
    else: return left_bar_width

async def get_role_color(msg):
    color = ""
    try: 
        r = msg.author.top_role.name.lower()
        if r == "admin":
            color = await get_color(settings["admin_color"])
        elif r == "mod": 
            color = await get_color(settings["mod_color"])
        elif r == "bot": 
            color = await get_color(settings["bot_color"])
        elif settings["custom_role"] is not None and r == settings["custom_role"].lower():
            color = await get_color(settings["custom_role_color"])
        elif settings["custom_role_2"] is not None and r == settings["custom_role_2"].lower():
            color = await get_color(settings["custom_role_2_color"])
        elif settings["custom_role_3"] is not None and r == settings["custom_role_3"].lower():
            color = await get_color(settings["custom_role_3_color"])
        elif settings["normal_user_color"] is not None:
            color = await get_color(settings["normal_user_color"])
        else: color = term.green
    # if this fails, the user either left or was banned
    except: 
        if settings["normal_user_color"] is not None:
            color = await get_color(settings["normal_user_color"])
        else: color = term.green
    return color

