import curses
import logging
from curses_utils import CursesBase

class TestCurses(CursesBase):
    def __init__(self):
        super().__init__()

    def waitUntilUserExit(self):
        while True:
            c = self.screen.getch()
            if c == ord('q'):
                break
            logging.info(c)

if __name__ == '__main__':
    logging.basicConfig(filename="test.log", filemode='w', level=logging.INFO)
    tc = TestCurses()
    curses.wrapper(tc.run)
