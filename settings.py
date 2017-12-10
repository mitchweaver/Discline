""" -----------------------------------------------------------------------
        You can edit these to your preferences. Note: anything silly
        like MAX_MESSAGES=-1 will break the client. Duh.
--------------------------------------------------------------------------- """

# the default server which will be joined upon startup - CASE SENSITIVE!
DEFAULT_SERVER="term_disc"

# the default channel which will be joined upon startup - CASE SENSITIVE!
DEFAULT_CHANNEL="test_bed"

# the leading character used for commands
PREFIX = '/'

# whether you have discord "Nitro" -- this enables external emojis
HAS_NITRO = False

# the default prompt when not in a channel
DEFAULT_PROMPT = "~"

# the default 'playing ' status in discord
DEFAULT_GAME = ""

# used for various things, your preference
ARRAYS_START_AT_ZERO = False

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

# Determines whether the left bar 'truncates' the channels or 
# appends "..." to the end when the screen is too small to display them
TRUNCATE_CHANNELS = False

# the amount of lines to scroll up/down on each trigger
SCROLL_LINES = 1

# ---------------- COLOR SETTINGS ------------------------------------ #
# Available colors are: "white", "red", "blue", "black"
#                       "green", "yellow", "cyan", "magenta"
# Or: you can say "on_<color>" to make it the background (ex: 'on_red')
# Or: you can say "blink_<color>" to have it flash (ex: 'blink_blue')
SEPARATOR_COLOR="white"
SERVER_DISPLAY_COLOR = "cyan"
PROMPT_COLOR = "white"
PROMPT_HASH_COLOR = "white"
PROMPT_BORDER_COLOR = "red"
ADMIN_COLOR = "magenta"
MOD_COLOR = "blue"
BOT_COLOR = "yellow"
NORMAL_USER_COLOR = "green"

# the "default" text color for messages and other things
TEXT_COLOR = "white"

CODE_BLOCK_COLOR="on_black"
URL_COLOR="cyan"
CHANNEL_LIST_COLOR="white"
CURRENT_CHANNEL_COLOR="green"

# colors for the channels in the left bar upon unreads
UNREAD_CHANNEL_COLOR="blink_yellow"
UNREAD_MENTION_COLOR="blink_red"

# whether channels should blink when they have unread messages
BLINK_UNREADS=True
# same as above, but for @mentions 
BLINK_MENTIONS=True

# here you can define your own custom roles - NOTE: text must match exactly!
# These for example could be "helper" or "trusted", whatever roles
# your servers use that aren't the default 'admin/mod/bot'
CUSTOM_ROLE = ""
CUSTOM_ROLE_COLOR = ""
CUSTOM_ROLE_2 = ""
CUSTOM_ROLE_2_COLOR = ""
CUSTOM_ROLE_3 = ""
CUSTOM_ROLE_3_COLOR = ""

# Channel ignore list - This stops the channel from being loaded.
# Effectively like the "mute" + "hide" feature on the official client,
# However with the added benefit that this means these channels won't
# be stored in RAM.    
# Follow the format as below. 
CHANNEL_IGNORE_LIST = {

    "server_name": ('some_channel', 'some_other_channel'), 
    "another_server_name": ('foo', 'bar', 'they_can_be_separated_nicely', \
                            'using_the_\_operator', 'i_think_you_get_it_now'),

    "DisKvlt": ("black_metal", "death_metal", "punk_core_grind_slam", \
                "kvlt_memes", "non_metal", "new_releases", "kvlt_pics", \
                "kvltness", "music_pick_ups", "admin_chat", "other_pickups", \
                "kvlt_speak", "dungeon_synth", "heavy_power_speed_trad", \
                "musicians_talk", "doom_drone_metal", "merch_pick_ups", \
                "prog_avantgarde_djent", "thrash_crossover", "pin_board")

}

# ignore this unless you know what you're doing
DEBUG = False
