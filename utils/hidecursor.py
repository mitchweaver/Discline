from sys import stdout
from os import name

# completely hides the system cursor
async def hide_cursor():
    stdout.write("\033[?25l")
    stdout.flush()
