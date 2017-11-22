# Terminal Discord
--------------------

![Image](https://0x0.st/s-JP.png)


## How to use:
-------------------------

1. Clone the repo
    
    `git clone https://github.com/mitchweaver/terminal-discord`
    
2. Find your discord "token"
   
    This can be found by going to https://discordapp.com/channels/@me,
    and opening your browser developer console. This is normally `F12` or
    `CTRL-SHIFT-I`. Now click on "storage", (may be called something different),
    and look for the discord url. Clicking this will show you a list of
    variables. Look for a line that looks like:
    
    `"token = 322332r093fwaf032f90323f32f903f23wfa"`

3. Edit settings.py to your choosing.

4. Launch with python3, using your token as an argument

    `python3 main.py $TOKEN`


### Current Features
--------------------------

* login via token
* connect to default server/channel
* upon init, download all logs from what the client can see
* /channel to switch channel
* /server to switch server
* /nick to change nickname (per server)
* /help to display help, (note: may not be current)
* /clear to clear screen, (in case of graphical glitches)
* typing without a leading prefix will submit to current chat
* User customization via editing settings.py
* "<USER> is typing..." support
* private channels

### Planned Features
---------------------------

* emoji displaying and reaction
* file/image uploading via path
* /giphy support (submitting first result)
* comment editing and deletion
* message searching
* private messaging

## Dependencies
------------------------

* [Python 3.5+](https://www.python.org/downloads/)
* [discord.py](https://github.com/Rapptz/discord.py)
* [blessings.py](https://pypi.python.org/pypi/blessings/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)

To install dependencies:

    `pip3 install discord blessings asyncio pynput`


### Known Bugs
--------------------------

> Sometimes when I submit a message the client crashes

No idea as of yet. Looking for a workaround.

> \<some feature\> isn't working right on Windows!

The fact the client works at all cross-platform is surprising
enough, but I'm working on it.

> My bug isn't listed here, how can I voice my problem?

If you have a specific issue that isn't listed here or in the
wiki, post a github issue with a detailed explanation and I can
try to get it fixed.

### License
-------------------------------

Licensed under GNU-GPLv3


### Legal Disclaimer
--------------------------------

Discord hasn't put out any official statement on whether using their 
API for 3rd party clients is allowed or not. Nobody has been banned
for using such things before, but they might one day change their mind.
With this said, I take no responsibility if this gets you banned.

Also, this client uses your token to log in. There is a reason for this.
Do **NOT** try and edit the code to use client.login("email", "pass") instead
of the token. This is deprecated and WILL get you banned. You have been warned.
