import os
import sys
import termios
import atexit
from select import select

class KBHit:
    
    def __init__(self):
        self.fd = sys.stdin.fileno()
        if self.fd is not None:
            self.fd = os.fdopen(os.dup(self.fd))

        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)
    
    def set_normal_term(self):
        ''' Resets to normal terminal. '''
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    async def getch(self):
        return self.fd.read(1)
                        
    async def kbhit(self):
        ''' Returns if keyboard character was hit '''
        dr,dw,de = select([self.fd], [], [], 0)
        return dr != []
