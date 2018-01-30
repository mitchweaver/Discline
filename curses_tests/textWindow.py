import curses
import logging
import math
import json
from cursesUtils import CursesContainer, WrappingText

class Message:
    def __init__(self, member: str, content: str):
        self.author = member
        self.content = content

class TextWinContainer(CursesContainer):
    def waitUntilUserExit(self):
        outerWin = self.createWin(30,75)
        self.wins.append(outerWin)
        outerWin.box()
        innerWin = self.createWin(28,73, 1,1)
        messages = None
        with open("lorem.json", 'r') as f:
            messages = json.loads(f.read())
        wt = WrappingText((0,0), (27,72))
        for msg in messages:
            wt.addMessage(msg)
        wt.formatText()
        innerWin.addstr(0,0, "".join(wt.formatted))
        self.refreshAll()
        while True:
            pass

if __name__ == "__main__":
    twc = TextWinContainer()
    curses.wrapper(twc.run)
