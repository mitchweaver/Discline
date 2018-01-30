import curses
import math
import time
from cursesUtils import CursesContainer, WrappingText, EditableMessage

class TextContainer(CursesContainer):
    def waitUntilUserExit(self):
        prefix = "Nat: "
        lenPrefix = len(prefix)
        win = self.createBoxedWin(self.max_y-1, self.max_x)
        self.screen.move(self.max_y-1,0)
        self.screen.addstr(prefix)
        max_y = win.getmaxyx()[0]
        max_x = win.getmaxyx()[1]
        em = EditableMessage(max_x-lenPrefix)
        wt = WrappingText(max_y,max_x-1)
        self.refreshAll()
        while True:
            self.screen.refresh()
            ch = self.screen.getch()
            ret = em.addKey(ch)
            if ret == em.AWAITING:
                self.clearLine(self.screen, self.max_y-1)
                self.screen.addstr(prefix)
                self.screen.addstr("".join(
                    em.inputBuffer[em.startPos:em.startPos+max_x]))
            else:
                win.hline(0,0, ' ',max_x)
                wt.addMessage({'name':"Nat", 'content':"".join(em.inputBuffer)})
                win.addstr(0,0, "".join(
                    wt.formatted))
                em.clear()
                self.clearLine(self.screen, self.max_y-1)
                self.screen.addstr(prefix)
            self.screen.move(self.max_y-1,lenPrefix+em.cursorPos)
            self.refreshAll()

if __name__ == '__main__':
    cc = TextContainer()
    curses.wrapper(cc.run)
