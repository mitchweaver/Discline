import re
import sys
import curses
from mistletoe.span_token import (RawText, SpanToken,
        _first_not_none_group)
from mistletoe.span_tokenizer import tokenize

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

def parseText(msg):
    tokens = []
    for token in tokenize(msg, token_types, RawText):
        attrs = curses.A_NORMAL
        if token.__class__.__name__ == "Strong": attrs=curses.A_BOLD
        elif token.__class__.__name__ == "Emphasis":
            if hasItalic: attrs=curses.A_ITALIC
            else: attrs=curses.A_UNDERLINE
        elif token.__class__.__name__ == "StrongEmphasis":
            if hasItalic: attrs=curses.A_BOLD|curses.A_ITALIC
            else: attrs=curses.A_BOLD|curses.A_UNDERLINE
        elif token.__class__.__name__ == "Underlined": attrs=curses.UNDERLINE
        if attrs == curses.A_NORMAL:
            tokens.append((token.content, attrs))
        else:
            tokens.append((token.children[0].content, attrs))

    return tokens

def tokenize_inner(content):
    return tokenize(content, token_types, RawText)

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

class Strong(SpanToken):
    """
    Strong tokens. ("**some text**")
    """
    pattern = re.compile(r"\*\*([^\s*].*?)\*\*|\b__([^\s_].*?)__\b")
    def __init__(self, match_obj):
        self._children = tokenize_inner(_first_not_none_group(match_obj))


class Emphasis(SpanToken):
    """
    Emphasis tokens. ("*some text*")
    """
    pattern = re.compile(r"\*([^\s*].*?)\*|\b_([^\s_].*?)_\b")
    def __init__(self, match_obj):
        self._children = tokenize_inner(_first_not_none_group(match_obj))


class InlineCode(SpanToken):
    """
    Inline code tokens. ("`some code`")
    """
    pattern = re.compile(r"`(.+?)`")
    def __init__(self, match_obj):
        self._children = (RawText(match_obj.group(1)),)

token_types = [Underlined, StrongEmphasis, Strong, Emphasis, InlineCode]
