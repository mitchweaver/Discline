from client import Client
from blessings import Terminal

""" ----------------------------------------------------------
You can edit these to your preferences. Note: anything silly
like MAX_MESSAGES=-1 will break the client. Duh.
-------------------------------------------------------------- """

# the default server which will be joined upon startup - CASE SENSITIVE!
DEFAULT_SERVER="DisKvlt"

# the default channel which will be joined upon startup - CASE SENSITIVE!
DEFAULT_CHANNEL="terminal_discord"

# the leading character used for commands
prefix = '/'

# the default prompt when not in a channel
DEFAULT_PROMPT = "~"

# Margins for inside the terminal and between elements. NOTE: must be >= 2
# NOTE: some ratios have weird glitches. Just experiment.
MARGIN = 2

# the max amount of messages to be downloaded + kept
MAX_MESSAGES=101

# the max amount of entries in each channel log to be downloaded + kept
MAX_LOG_ENTRIES=200

# Colors - Available options:
# "white", "red", "blue", "green", "yellow", "cyan", "magenta", "black"
ADMIN_COLOR = "magenta"
MOD_COLOR = "blue"
BOT_COLOR = "yellow"
NORMAL_USER_COLOR = "green"

# here you can define your own custom roles - NOTE: text must match exactly!
CUSTOM_ROLE = ""
CUSTOM_ROLE_COLOR = ""
CUSTOM_ROLE_2 = ""
CUSTOM_ROLE_2_COLOR = ""
CUSTOM_ROLE_3 = ""
CUSTOM_ROLE_3_COLOR = ""



# ----------- Internal-Use Variables Below ----------------- #
""" ----------------------------------------------------------
DO NOT EDIT THESE - SERIOUSLY, DON'T DO IT.
-------------------------------------------------------------- """
client = Client(max_messages=MAX_MESSAGES)
term = Terminal()
server_log_tree = []
input_buffer = []
# kills the program and all its elements gracefully
def kill():
    import asyncio
    try: client.close()
    except: pass
    try: asyncio.get_event_loop().close()
    except: pass
    quit()
