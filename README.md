# Terminal Discord
--------------------

### Current Features
--------------------------

* login via token
* connect to default server/channel
* upon init, download all logs from what the client can see
* /channel to switch channel
* /server to switch server
* /help to display help, (note: may not be current)
* /clear to clear screen, (in case of graphical glitches)
* typing without a leading prefix will submit to current chat
* User customization via editing settings.py

### Planned Features
---------------------------

* emoji displaying and reaction
* file/image uploading via path
* /giphy support (submitting first result)
* comment editing and deletion
* message searching
* "<USER> is typing..." support
* private messaging
* private channels, (currently not working)

## Dependencies
------------------------

* Python 3.5+
* discord.py
* blessings.py
* asyncio
* pynput

To install dependencies:

    pip3 install discord blessings asyncio pynput


### Known Bugs
--------------------------

> Sometimes I my screen doesn't update upon receiving a message

This is due to the input loop waiting on user input and therefore not
freeing up CPU time for the other background loops via asyncio. 
Currently working on an alternative input method as a workaround.

> Sometimes when I submit a message the client crashes

No idea as of yet. Looking for a workaround.
