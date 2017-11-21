from pynput import mouse, keyboard
from settings import *
import ui

def on_move(x, y):
    # print('Pointer moved to {0}'.format(
    #     (x, y)))
    pass

def on_click(x, y, button, pressed):
    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False
    pass

def on_scroll(x, y, dx, dy):
    pass
    # if ui.INDEX < ui.MAX_LINES: ui.INDEX = ui.MAX_LINES
    # if dy > 0: ui.INDEX += 10
    # else: ui.INDEX -= 10
    # ui.print_screen(client, channel_log)

def on_press(key):
    pass
    # if ui.INDEX < ui.MAX_LINES: ui.INDEX = ui.MAX_LINES
    # ui.INDEX += 10
    # ui.print_screen(client, channel_log)
    # try:
    #     print('{0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

def on_release(key):
    pass
    # print('{0} released'.format(
    #     key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False

mlis = mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll)
klis = keyboard.Listener(on_press=on_press,on_release=on_release)
mlis.start()
klis.start()
