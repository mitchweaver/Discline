import sys
import os

lorem = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " +
        "Nullam tempus, ex vel dignissim laoreet, ante diam auctor " +
        "augue, at posuere dui nibh at est. Vivamus auctor magna " +
        "vitae velit aliquam convallis.")
width = 50

def printRange(text, y, startPos, cursorPos):
    print("\033[{};0H{}".format(y, text[startPos:startPos+width]), end='')
    print("\033[{};{}H\u2588".format(y, cursorPos), end='', flush=True)

if __name__ == "__main__":
    os.system('clear')
    printRange(lorem, 1, 0, 0)
    printRange(lorem, 2, 25, 0)
    printRange(lorem, 3, 25, 25)
    print()

# startPos:startPos+width gives buffer
# cursorPos is relative to buffer
