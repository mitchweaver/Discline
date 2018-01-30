import curses
import time

def main(screen):
    buf = None
    with open("lorem.txt", 'r') as f:
        buf = f.read()

    maxyx = screen.getmaxyx()

    win = curses.newwin(maxyx[0],maxyx[1])
    win.box()
    win.refresh()
    pad = curses.newpad(maxyx[0]*2-2,maxyx[1]-2)

    pad.addstr(0,0, buf)

    line = 0
    while True:
        pad.refresh(line,0, 1,1, maxyx[0]-2,maxyx[1]-2)
        line += 1
        time.sleep(0.25)

if __name__ == '__main__':
    curses.wrapper(main)
