# Terminal Discord
--------------------

![Image](https://0x0.st/soYP.png)


__**Warning**__: Currently Linux/Mac only, it may be a while before support for Windows comes back

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
* /channel to switch channel
* /server to switch server
* /nick to change nickname (per server)
* typing without a leading prefix will submit to current chat
* User customization via editing settings.py
* "<USER> is typing..." support
* private channels
* colored output, with user definable colors and custom roles
* Channel logs update when users edit messages
* /channels, /servers, /users to view information
* /game to update the "Now playing: " status
* use /help for more commands
* unicode emoji displayal support
* File uploading via path (ex: /file /path/to/file)
* italic, bold, and underline font support
* inline-code and \`code\` block support
* sending of __default__ unicode emojis in messages
* URL detection, highlighting in blue + italics
* automatic updating, fetching the latest master branch's commit

### Planned Features
---------------------------

* custom server emojis in messages
* emojis reactions
* comment editing and deletion
* private messaging
* message searching -- (working, but not at a useable speed)

## Dependencies
------------------------

* [Python 3.5+](https://www.python.org/downloads/)
* [discord.py](https://github.com/Rapptz/discord.py)
* [blessings.py](https://pypi.python.org/pypi/blessings/)
* asyncio

To install dependencies:

    `pip3 install asyncio discord blessings`


### Color Customization
------------------------

Almost all aspects of the client can be colored to
the user's wishes. You can set these colors from within
settings.py

### A Note On Emojis
-------------------------

Currently *most* of the standard unicode emojis
are displaying. Note your terminal must be able
to render these symbols *and* you must be using a font
set that contains them. Because some of the emojis
that discord uses are non-standard, they may not
display properly. Here is an example of a random
few.

![Image](https://images-ext-2.discordapp.net/external/iN52NdGOWqdWOxby88wiEGs8R81j33ndPjgKX8eKUNA/https/0x0.st/soIy.png?width=400&height=32)

### Note On Font Support
-------------------------

Like emojis, not all terminals and fonts support
italic/bold/underline and 'background' colors, (which are used for \`code\`).
If these features aren't working for you, odds are you are not using a 
support terminal/font. Experiment with different setups to see what works.

![Image](https://0x0.st/sHQ0.png)

*Letting me know what setups __don't__ work helps a lot!*

### Starting this with my token as an argument is such a pain!
--------------------------------------------------------

To make it easier, you can create a bash script to launch it for you.

Example:

```bash
#!/bin/bash

TOKEN="put your token here"

python3.6 /path/to/term_disc/main.py $TOKEN
```

### Dude this is awesome! How can I support the project?
--------------------------------------------------------

Star it! It helps to get it higher in GitHub's search results as well as
making me feel good inside. ;)

If you'd like to contribute, pull requests are __*always*__ welcome!

If you would like to get more info on what could be done or to discuss the
project in general, come join the discord server at: https://discord.gg/rBGQMTk

### FAQ
-------------------------

> Yet another discord cli?

I didn't like any of the implementations I found around github. Too buggy.
Too bloated. Bad UI. No customization. Some, after discord updates, 
no longer functioning at all.

> Why use a token and not email/password?

Discord's API __does__ allow for email/pass login, but if you were to have
2FA, (2 factor authentication), enabled on your account, Discord would
interpret this as a malicious attack against your account and disable it.

So, because *"Nobody reads the readme"*, I have disabled this.

> How should I submit a GitHub issue?

Try to include this format:

```
OS: Linux/Debian
Terminal: urxvt
Font: source code pro
Python Version: 3.6
How to reproduce: xxxxxx
```

### Misc Screenshots
--------------------------

![Image](https://0x0.st/sHjR.png)

![Image](https://0x0.st/sHer.png)

![Image](https://0x0.st/sHez.png)


### Known Bugs
--------------------------

> Sometimes when I submit a message the client crashes

This should(?) be fixed, but if it keeps happening, do let me know.

> Line wrapping sometimes doesn't work

This happens if there is too much formatting / coloring being done to the
message that contains that line. I'm looking for a work around.

> When I type many lines before hitting send, the UI sometimes bugs out
and/or the separators encroach upon different sections

Known. Looking for a work around.

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

As far as I know, nobody has been banned for using things like this before, 
but Discord might one day change their mind. With this said, I take **no** 
responsibility if this gets you banned.
