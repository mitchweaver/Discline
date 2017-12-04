""" -----------------------------------------------------------------------
        You can edit these to your preferences. Note: anything silly
        like MAX_MESSAGES=-1 will break the client. Duh.
--------------------------------------------------------------------------- """

# the default server which will be joined upon startup - CASE SENSITIVE!
DEFAULT_SERVER="DisKvlt"

# the default channel which will be joined upon startup - CASE SENSITIVE!
DEFAULT_CHANNEL="terminal_discord"

# the leading character used for commands
PREFIX = '/'

# the default prompt when not in a channel
DEFAULT_PROMPT = "~"

# the default 'playing ' status in discord
DEFAULT_GAME = ""

# Margins for inside the terminal and between elements. NOTE: must be >= 2
# NOTE: some ratios have weird glitches. Just experiment.
MARGIN = 2

# the max amount of messages to be downloaded + kept
# NOTE: minimum = 100! This is normally safe to increase.
MAX_MESSAGES=100

# the max amount of entries in each channel log to be downloaded + kept
# NOTE: minimum = 100! The larger this is, the slower the client will start.
MAX_LOG_ENTRIES=100

# Whether to send "... is typing" when the input buffer is not blank or '/'
SEND_IS_TYPING = True

# Whether to show in-line emojis in messages
SHOW_EMOJIS = True

# the denominator used to calculate the width of the "left bar"
# NOTE: larger number here, the smaller the bar will be,
#       (although there is still a minimum of 8 chars...) 
LEFT_BAR_DIVIDER = 9

# ---------------- COLOR SETTINGS ------------------------------------ #
# Available colors are: "white", "red", "blue", "black"
#                       "green", "yellow", "cyan", "magenta"
SEPARATOR_COLOR="white"
SERVER_DISPLAY_COLOR = "cyan"
PROMPT_COLOR = "white"
PROMPT_BORDER_COLOR = "red"
ADMIN_COLOR = "magenta"
MOD_COLOR = "blue"
BOT_COLOR = "yellow"
NORMAL_USER_COLOR = "green"

# here you can define your own custom roles - NOTE: text must match exactly!
# These for example could be "helper" or "trusted", whatever roles
# your servers use that aren't the default 'admin/mod/bot'
CUSTOM_ROLE = ""
CUSTOM_ROLE_COLOR = ""
CUSTOM_ROLE_2 = ""
CUSTOM_ROLE_2_COLOR = ""
CUSTOM_ROLE_3 = ""
CUSTOM_ROLE_3_COLOR = ""
