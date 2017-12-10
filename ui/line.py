class Line():

    # the text the line contains
    text = "" 
    # how offset from the [left_bar_width + MARGIN] it should be printed
    # this is to offset wrapped lines to better line up with the previous
    offset = 0

    def __init__(self, text, offset):
        self.text = text
        self.offset = offset

    def length(self):
        return len(self.text)
