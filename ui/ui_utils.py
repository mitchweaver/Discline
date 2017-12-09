from utils.globals import term, client, get_color
from settings import *

async def get_prompt():
    left = await get_color(PROMPT_BORDER_COLOR) + "["
    right = await get_color(PROMPT_BORDER_COLOR) + "]: " + term.normal
    middle = ""
    if client.get_prompt() == DEFAULT_PROMPT:
        middle = " " + await get_color(PROMPT_COLOR) + DEFAULT_PROMPT + " "
    else:
        middle = await get_color(PROMPT_HASH_COLOR) + "#" \
                + await get_color(PROMPT_COLOR) + client.get_prompt()

    return left + middle + right


async def get_max_lines():
    return term.height - MARGIN * 2

async def get_left_bar_width():
    left_bar_width = term.width // LEFT_BAR_DIVIDER
    if left_bar_width < 8: return  8
    else: return left_bar_width

async def get_role_color(msg):
    color = ""
    try: 
        r = msg.author.top_role.name.lower()
        if r == "admin":
            color = await get_color(ADMIN_COLOR)
        elif r == "mod": 
            color = await get_color(MOD_COLOR)
        elif r == "bot": 
            color = await get_color(BOT_COLOR)
        elif CUSTOM_ROLE is not None and r == CUSTOM_ROLE.lower():
            color = await get_color(CUSTOM_ROLE_COLOR)
        elif CUSTOM_ROLE_2 is not None and r == CUSTOM_ROLE_2.lower():
            color = await get_color(CUSTOM_ROLE_2_COLOR)
        elif CUSTOM_ROLE_3 is not None and r == CUSTOM_ROLE_3.lower():
            color = await get_color(CUSTOM_ROLE_3_COLOR)
        elif NORMAL_USER_COLOR is not None:
            color = await get_color(NORMAL_USER_COLOR)
        else: color = term.green
    # if this fails, the user either left or was banned
    except: 
        if NORMAL_USER_COLOR is not None:
            color = await get_color(NORMAL_USER_COLOR)
        else: color = term.green
    return color

