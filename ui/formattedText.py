from utils.log import log
import curses
from collections import deque
from ui.textParser import parseText

class TokenContainer:
    def __init__(self, content, attrs):
        self.content = content
        self.clean_content = content
        self.attrs = attrs

class MessageContainer:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

class Line:
    def __init__(self, isFirst=False, user=None, topRole=None):
        self.words = []
        if isFirst:
            if user is None:
                raise Exception
        self.user = user
        self.topRole = topRole
        self.isFirst = isFirst

    def add(self, token):
        self.words.append(token)

class FormattedText:
    def __init__(self, w, maxlen=100, colors=0):
        self.width = w
        self.colors = colors

        self.messages = []
        self.messageBuffer = deque([], maxlen)

    def addMessage(self, msg):
        self.messages.append(msg)
        self.format(msg)

    def getLines(self):
        lines = []
        for message in self.messageBuffer:
            for line in message.lines:
                lines.append(line)
        return lines

    def refresh(self, newWidth=None):
        if newWidth is not None:
            self.width = newWidth
        self.messageBuffer.clear()
        for msg in self.messages:
            self.format(msg)

    def format(self, msg):
        chrPos = 0
        try:
            name = msg.author.display_name
        except:
            name = msg.author.name
            if name is None:
                name = "Unknown Author"
        topRole = ""
        if msg.author.__class__.__name__ == "Member":
            topRole = msg.author.top_role.name.lower()
        offset = len(name)+2
        width = self.width-offset

        # Tokens grouped by type (type tokens)
        ttokens = parseText(msg.clean_content, self.colors)
        # Separate tokens by word (word tokens)
        wtokens = []
        for tok_id, ttoken in enumerate(ttokens):
            # if '\n' is in segment but not JUST '\n'
            if ttoken[0] != '\n' and '\n' in ttoken[0] and len(ttoken[0]) < width:
                # Split ttoken into lines
                lines = ttoken[0].splitlines()
                for line_id, line in enumerate(lines):
                    # Only split line into words if it's not code
                    if ttoken[1] != curses.A_REVERSE:
                        for word in line.split(' '):
                            wtokens.append((word, ttoken[1]))
                    else:
                        wtokens.append((line, ttoken[1]))
                    wtokens.append(('\n', curses.A_NORMAL))
                continue
            words = ttoken[0].split(' ')
            for idx, word in enumerate(words):
                if len(word) < 1:
                    continue
                # if single word is longer than width
                if len(word) >= width:
                    iters = len(word)//(width-1)
                    if len(word)%(width-1) != 0:
                        iters += 1
                    for segid in range(iters):
                        if segid < iters-1:
                            rng = word[segid*(width-1):(segid+1)*(width-1)]
                            wtokens.append((rng, ttoken[1]))
                            wtokens.append(('\n', curses.A_NORMAL))
                        else:
                            rng = word[segid*(width-1):]
                            wtokens.append((rng, ttoken[1]))
                    continue
                wtokens.append((word, ttoken[1]))
        cpos = 0
        line = Line(True, name, topRole)
        ltokens = []
        for idx,wtoken in enumerate(wtokens):
            cpos += len(wtoken[0])+1
            if cpos > width or wtoken[0] == '\n':
                ltokens.append(line)
                line = Line()
                cpos = 0
                continue
            line.add(TokenContainer(wtoken[0].rstrip(), wtoken[1]))
            if idx == len(wtokens)-1:
                ltokens.append(line)
        mc = MessageContainer(name, ltokens)
        self.messageBuffer.append(mc)
