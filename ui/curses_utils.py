import sys
import math
import asyncio
import curses
import signal
import logging
import re

class StringGroup:
    NORMAL = 0
    BOLD   = 1
    def __init__(self, posRange, strFmt):
        self.posRange = position
        self.strFmt = strFmt

class CursesBase:
    def __init__(self):
        signal.signal(signal.SIGINT, self.destroyAndExit)
        self.frameWins = []
        self.contentWins = []
        self.contentPad = None

    def initScreen(self):
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.screen.clear()

    def waitUntilUserExit(self):
        pass

    def run(self, screen):
        self.screen = screen
        self.initScreen()
        maxyx = self.screen.getmaxyx()
        self.max_y = maxyx[0]
        self.max_x = maxyx[1]
        self.waitUntilUserExit()
        #self.destroy()

    def destroy(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def destroyAndExit(self, signal=None, frame=None):
        self.destroy()
        sys.exit(0)

    def createBoxedWin(self, h,w, y=0,x=0):
        frameWin = curses.newwin(h,w, y,x)
        self.frameWins.append(frameWin)
        frameWin.box()
        contentPad = curses.newpad(512,w-2)
        self.contentPad = contentPad
        self.contentPadAttribs = (0,0, y+1,x+1, y+h-2,x+w-2)

        return contentPad

    def setPadIndex(self, index):
        cpa = self.contentPadAttribs
        self.contentPadAttribs = (index,cpa[1], cpa[2],cpa[3], cpa[4],cpa[5])
        self.contentPad.refresh(*self.contentPadAttribs)

    def clearLine(self, win, y):
        win.hline(y,0, ' ',self.max_x)

    def refreshAll(self):
        self.screen.noutrefresh()
        for win in self.contentWins:
            win.noutrefresh()
        curses.doupdate()

# Creates formatted string lists from Messages
class WrappedText:
    def __init__(self, h,w, y=0,x=0):
        self.height = h
        self.width = w
        self.y = y
        self.x = x

        self.oldMsgs = []
        self.formatted = [] #String list

    def addMessage(self, msg):
        self.format(msg)

    def resize(self):
        for msg in self.oldMsgs:
            format(msg, resize=True)

    def format(self, msg, resize=False):
        fmtBuf = []
        chrPos = 0
        lines = 0
        name = msg.author.name
        if msg.author.nick is not None:
            name = msg.author.nick

        if not resize:
            self.oldMsgs.append(msg)
        for c in name:
            fmtBuf.append(c)
            chrPos += 1
        for c in ": ":
            fmtBuf.append(c)
            chrPos += 1
        text = parseFormatting(msg.content)
        for c in text:
            if chrPos > self.width-1:
                nameOffset = len(name)+2
                fmtBuf.append('\n' + ' '*nameOffset)
                lines += 1
                chrPos = nameOffset
            fmtBuf.append(c)
            chrPos += 1
        fmtBuf.append('\n')
        chrPos = 0
        self.formatted.append(fmtStr)

    def parseFormatting(self, text):
        if "**" in text:
            # bold
            

class MessageEdit:
    AWAITING = 0
    SENT     = 1
    def __init__(self, maxWidth):
        self.startPos = 0
        self.cursorPos = 0

        self.maxWidth = maxWidth

        self.inputBuffer = []

    def calcPos(self):
        if self.cursorPos > (self.maxWidth-6):
            # cursorPos approaches maxWidth
            self.startPos += (self.maxWidth-10)
            self.cursorPos = 5
        elif self.startPos+self.cursorPos > len(self.inputBuffer):
            self.cursorPos -= 1
        elif self.cursorPos < 0 and self.startPos > 0:
            # cursorPos < 0 and startPos > 0
            self.startPos -= (self.maxWidth-10)
            self.cursorPos = (self.maxWidth-5)
        elif self.cursorPos < 0:
            # cursorPos < 0 and startPos >= 0
            self.cursorPos = 0

    def clear(self):
        del(self.inputBuffer[:])
        self.cursorPos = self.startPos = 0

    def goToStart(self):
        self.cursorPos = self.startPos = 0

    def goToEnd(self):
        self.startPos = math.floor(len(self.inputBuffer)/self.maxWidth)
        self.cursorPos = len(self.inputBuffer)%self.maxWidth

    def moveLeft(self):
        self.cursorPos -= 1
        self.calcPos()

    def moveRight(self):
        self.cursorPos += 1
        self.calcPos()

    def backspace(self):
        if self.cursorPos != 0 or self.startPos != 0:
            del(self.inputBuffer[-1])
            self.cursorPos -= 1
        self.calcPos()

    def append(self, msg):
        self.inputBuffer.append(msg)
        self.cursorPos += 1
        self.calcPos()

    def insert(self, index, msg):
        self.inputBuffer.insert(index, msg)
        self.cursorPos += 1
        self.calcPos()

    def addKey(self, ch):
        if ch == curses.KEY_HOME:
            self.goToStart()
        elif ch == curses.KEY_END:
            self.goToEnd()
        elif ch == curses.KEY_LEFT or ch == curses.KEY_UP:
            self.moveLeft()
        elif ch == curses.KEY_RIGHT or ch == curses.KEY_DOWN:
            self.moveRight()
        elif ch in (0x7f, ord('\b'), curses.KEY_BACKSPACE):
            self.backspace()
        elif ch == ord('\n'):
            return self.SENT
        else:
            # must be a normal character
            if self.startPos+self.cursorPos == len(self.inputBuffer):
                # at end, append to inputBuffer
                self.append(chr(ch))
            else:
                # in middle/beginning, insert in inputBuffer
                # at startPos+cursorPos
                self.insert(self.startPos+self.cursorPos, chr(ch))
        return self.AWAITING
