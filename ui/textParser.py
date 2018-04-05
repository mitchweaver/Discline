import re
from utils.log import log
import sys
import curses
from io import StringIO
from mistletoe.block_token import (BlockToken, Paragraph as _Paragraph,
        CodeFence)
from mistletoe.block_tokenizer import tokenize as blockTokenize
from mistletoe.span_token import (RawText, SpanToken, InlineCode,
        Strong, Emphasis,_first_not_none_group)
from mistletoe.span_tokenizer import tokenize as spanTokenize
from ui.ui_utils import convert_pin, trim_emoji

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

# Output: A list of tuples whose members are 1) raw text; and 2) attributes
# Example: [
#              ("Some text that is ", curses.A_NORMAL),
#              ("bold\n", curses.A_BOLD),
#              ("and across multiple ", curses.A_NORMAL),
#              ("lines.", curses.A_UNDERLINE)
#          ]

# Possible objects:
#  * List (Block token, OR Span token, OR RawText token)
#  * Paragraph token (.children is a list of span tokens)
#  * Span token (.chilren is a list of RawText)
#  * RawText token (.content is content)
#  * Content
# What we need:
#  * Content
#  * Attributes

def rectifyText(obj):
    text = obj
    if type(text) != str:
        text = obj.read()
    lines = []
    for line in text.splitlines():
        if '```' in line and line != '```':
            if line.startswith('```'):
                # Line contains ``` at beginning or middle
                lines.append('```')
                lines.append(line.replace('```', '').lstrip())
            elif line.endswith('```'):
                # Line ends with ```
                lines.append(line.replace('```', ''))
                lines.append('```')
            else:
                split = line.split('```')
                lines.append(split[0])
                lines.append('```')
                lines.append(split[1])
            continue
        lines.append(line)
    rectMsg = '\n'.join(lines)
    if len(rectMsg) > 0 and rectMsg[-1] != '\n':
        rectMsg = rectMsg + '\n'
    return rectMsg

def parseText(msg, colors):
    spanTokens = []
    # Needed for the markdown to parse correctly
    msg = StringIO(rectifyText(msg))
    doc = Document(msg)
    blockTokens = doc.children
    # FIXME: BlankLine sometimes at beginning of tokens
    if blockTokens[0].__class__.__name__ == "BlankLine":
        blockTokens = blockTokens[1:]
    for tokid, blockToken in enumerate(blockTokens):
        # These are blockToken objects
        # A blockToken object has a LIST of children
        attrs = curses.A_NORMAL
        for child in blockToken.children:
            if blockToken.__class__.__name__ == "CodeFence":
                spanTokens.append((child.content, curses.A_REVERSE))
                continue
            elif blockToken.__class__.__name__ == "BlankLine":
                spanTokens.append(('\n', curses.A_NORMAL))
                continue
            className = child.__class__.__name__
            # Child can be either a formatted token or a raw token
            if className in ("URL", "Strong", "Emphasis",
                    "StrongEmphasis", "Underlined",
                    "InlineCode"):
                # These have a single child with RawText inside
                if className == "Strong":
                    attrs = curses.A_BOLD
                elif className == "Emphasis":
                    if hasItalic:
                        attrs = curses.A_ITALIC
                    else:
                        attrs = curses.A_UNDERLINE
                elif className == "StrongEmphasis":
                    if hasItalic:
                        attrs = curses.A_BOLD | curses.A_ITALIC
                    else:
                        attrs = curses.A_BOLD | curses.A_UNDERLINE
                elif className == "Underlined":
                    attrs = curses.A_UNDERLINE
                elif className == "URL":
                    attrs = curses.A_UNDERLINE | colors["blue"]
                elif className == "InlineCode":
                    attrs = curses.A_REVERSE
                spanTokens.append((child.children[0].content, attrs))
            elif className == "RawText":
                spanTokens.append((child.content, curses.A_NORMAL))
            else:
                log("We shouldn't be here")

    return spanTokens

class Document(BlockToken):
    """
    Document token.
    """
    def __init__(self, lines):
        self.footnotes = {}
        # Document tokens have immediate access to first-level block tokens.
        # Useful for footnotes, etc.
        self._children = tuple(blockTokenize(lines, [CodeFence, Paragraph, BlankLine], root=self))

def tokenize_inner(content):
    return spanTokenize(content, token_types, RawText)

def return_whole_group(match_obj):
    return next(group for group in (match_obj.group(), None) if group is not None)

class URL(SpanToken):
    """
    URL tokens. ("http://example.com")
    """
    pattern = re.compile("(http(s)?:\\/\\/.)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)")
    def __init__(self, match_obj):
        self._children = (RawText(match_obj.group()),)

class Underlined(SpanToken):
    """
    Underlined tokens. ("__some text__")
    """
    pattern = re.compile(r"\_\_([^\s*].*?)\_\_|\b__([^\s_].*?)__\b")
    def __init__(self, match_obj):
        self._children = tokenize_inner(_first_not_none_group(match_obj))

class StrongEmphasis(SpanToken):
    """
    Strong-Emphasis tokens. ("***some text***")
    """
    pattern = re.compile(r"\*\*\*([^\s*].*?)\*\*\*|\b___([^\s_].*?)___\b")
    def __init__(self, match_obj):
        self._children = tokenize_inner(_first_not_none_group(match_obj))

class BlankLine(BlockToken):
    def __init__(self, lines):
        self._children = (RawText(''.join(lines)),)

    @staticmethod
    def start(line):
        return line == '\n'

    @staticmethod
    def read(lines):
        return []

class Paragraph(_Paragraph):
    def __init__(self, lines):
        content = ''.join(lines)
        BlockToken.__init__(self, content, tokenize_inner)

token_types = [URL, Underlined, StrongEmphasis, Strong, Emphasis, InlineCode]
