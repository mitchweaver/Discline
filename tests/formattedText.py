import logging
import curses
from collections import deque
from tests.textParser import parseText

class TokenContainer:
    def __init__(self, content, attrs):
        self.content = content
        self.attrs = attrs

class MessageContainer:
    def __init__(self, name, tokens):
        self.name = name
        self.tokens = tokens

class Line:
    def __init__(self, isFirst=False, user=None):
        self.words = []
        if isFirst:
            if user is None:
                raise Exception
        self.user = user
        self.isFirst = isFirst

    def add(self, token):
        self.words.append(token)

class WrappedText:
    def __init__(self, w, maxlen=100):
        self.width = w

        self.oldMsgs = []
        self.messages = deque([], maxlen) #TextContainer list

    def addMessage(self, msg):
        self.format(msg)

    def getLines(self):
        lines = []
        for message in self.messages:
            for line in message.tokens:
                lines.append(line)
        return lines

    def resize(self):
        for msg in self.oldMsgs:
            format(msg, resize=True)

    def format(self, msg, resize=False):
        chrPos = 0
        lines = 0
        name = msg.author.name
        if msg.author.nick is not None:
            name = msg.author.nick
        offset = len(name)+2
        width = self.width-offset

        ptokens = parseText(msg.content)
        # Separate tokens by word
        # Create new token for each word
        wtokens = []
        for ptoken in ptokens:
            words = ptoken[0].split(' ')
            for idy, word in enumerate(words):
                if len(word) < 1:
                    continue
                elif len(word) >= width:
                    iters = int(len(word)/width)
                    if len(word)%width != 0:
                        iters += 1
                    for segid in range(iters):
                        if segid == iters-1:
                            rng = word[segid*width:]
                        else:
                            rng = word[segid*width:(segid+1)*width]
                        wtokens.append((rng, ptoken[1]))
                    continue
                wtokens.append((word, ptoken[1]))
        cpos = 0
        line = Line(True, name)
        ltokens = []
        for idx,wtoken in enumerate(wtokens):
            cpos += len(wtoken[0])+1
            if cpos > width+1:
                ltokens.append(line)
                line = Line()
                cpos = 0
            line.add(TokenContainer(wtoken[0], wtoken[1]))
            if idx == len(wtokens)-1:
                ltokens.append(line)
        mc = MessageContainer(name, ltokens)
        self.messages.append(mc)
