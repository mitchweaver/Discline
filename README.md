# Terminal Discord
--------------------

![Image](https://0x0.st/soYP.png)


### WARNING: Currently Mac/Linux only until I find a fix!


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
* colored output, with user definable colors and custom roles
* Log updates when users edit messages
* /channels, /servers, /users to view information
* /game to update the "Now playing: " status
* use /help for more commands

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
* asyncio

To install dependencies:

    `pip3 install asyncio discord blessings`


### FAQ
-------------------------

> Yet another discord cli?

I didn't like any of the implementations I found around github. Too buggy.
Too bloated. Bad UI. No customization. Some, after discord updates, 
no longer functioning at all.

> Why use a token and not email/password?

Discord's API does allow for email/pass login, but if you were to have
2FA, (2 factor authentication), enabled on your account, Discord would
interpret this as a malicious attack against your account and disable it.

So, because *"Nobody reads the readme"*, I have disabled this.

### Known Bugs
--------------------------

> Sometimes when I submit a message the client crashes

No idea as of yet. Looking for a workaround.

> \<some feature\> isn't working right on Windows!

The fact the client works at all cross-platform is surprising
enough, but I'm working on it. If something breaks in windows,
post a github issue and I will try and work it out.

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
API for 3rd party clients is allowed or not. They *have* said that using
their API to make "self-bots" is against their ToS. By self-bots, it is
my understanding they mean automating non-bot accounts as bots.
My code has no automated functions, or any on_events that provide features
not included in the official client. 

Nobody has been banned for using things like this before, but Discord
might one day change their mind. With this said, I take **no** responsibility
if this gets you banned.
