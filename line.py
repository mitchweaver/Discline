class Line():

    # the text the line contains
    text = "" 
    # how offset from the [left_bar_width + MARGIN] it should be printed
    # this is to offset wrapped lines to better line up with the previous
    offset = 0
    # how many lines down from the top of the window we are printing at
    step = 0

    def __init__(self, text, offset, step):
        self.text = text
        self.offset = offset
        self.step = step
