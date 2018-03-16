import curses

class MessageEdit:
    SCROLL = 10
    def __init__(self, maxWidth):
        self.maxWidth = maxWidth
        self.offset = 0
        self.curPos = 0
        self.inputBuffer = []

    def reset(self):
        self.offset = 0
        self.curPos = 0
        del(self.inputBuffer[:])

    def getCurrentData(self):
        if len(self.inputBuffer) < self.maxWidth:
            return ("".join(self.inputBuffer), self.curPos)
        else:
            return ("".join(self.inputBuffer[self.offset:self.offset+self.maxWidth]), self.curPos)

    def addKey(self, ch):
        # check if character is function character
        # Home, End, Left/Up, Right/Down, Enter
        if ch == curses.KEY_HOME or ch == curses.KEY_PPAGE:
            self.offset = 0
            self.curPos = 0
        elif ch == curses.KEY_END or ch == curses.KEY_NPAGE:
            # if inputBuffer fits into line
            if len(self.inputBuffer) < self.maxWidth:
                self.curPos = len(self.inputBuffer)
            else:
                self.offset = len(self.inputBuffer)-self.maxWidth+1
                self.curPos = self.maxWidth-1
        elif ch == curses.KEY_LEFT or ch == curses.KEY_UP:
            # curPos is greater than 0
            if self.curPos > 0:
                self.curPos -= 1
            # at beginning of line where offset is less than 0
            elif self.offset > 0 and self.curPos == 0:
                self.offset -= self.SCROLL
                self.curPos = self.maxWidth-self.SCROLL+1
        elif ch == curses.KEY_RIGHT or ch == curses.KEY_DOWN:
            # less than end of buffer and less than EOL
            if self.offset+self.curPos < len(self.inputBuffer) and\
                    self.curPos < self.maxWidth-1:
                self.curPos += 1
            # less than end of buffer and curPos equal to EOL
            elif self.offset+self.curPos < len(self.inputBuffer) and\
                    self.curPos == self.maxWidth-1:
                self.offset += self.SCROLL
                self.curPos -= self.SCROLL-1
        elif ch in (0x7f, ord('\b'), curses.KEY_BACKSPACE):
            if self.curPos > 0:
                self.inputBuffer.pop(self.offset+self.curPos-1)
                self.curPos -= 1
        elif ch == ord('\n'):
            return "".join(self.inputBuffer)
        # Normal text
        else:
            self.inputBuffer.insert(self.offset+self.curPos, chr(ch))
            if self.curPos != self.maxWidth-1:
                self.curPos += 1
            else:
                self.offset += self.SCROLL
                self.curPos -= self.SCROLL-1
