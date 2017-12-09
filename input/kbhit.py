import os
import sys
import termios
import atexit
from select import select
from utils.globals import term, kill

class KBHit:
    
    def __init__(self):
        self.fd = os.fdopen(os.dup(sys.stdin.fileno()))
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
                        

    # async def getarrow(self):
    #     ''' Returns an arrow-key code after kbhit() has been called. Codes are
    #     0 : up
    #     1 : right
    #     2 : down
    #     3 : left
    #     Should not be called in the same program as getch(). '''
        
    #     c = self.fd.read(3)[2]
    #     vals = [65, 67, 66, 68]
        
    #     return vals.index(ord(c.decode('utf-8')))
        

    async def kbhit(self):
        ''' Returns if keyboard character was hit '''
        dr,dw,de = select([self.fd], [], [], 0)
        return dr != []
