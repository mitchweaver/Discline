import curses
from cursesContainer import CursesContainer

class WinSizeContainer(CursesContainer):
    def waitUntilUserExit(self):
        win = self.createWin(30,75)
        self.wins.append(win)
        win.box()
        self.refreshAll()
        while True:
            pass

if __name__ == "__main__":
    wsc = WinSizeContainer()
    curses.wrapper(wsc.run)
