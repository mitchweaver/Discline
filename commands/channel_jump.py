from utils.globals import server_log_tree, client
from utils.quicksort import quick_sort_channel_logs
from settings import ARRAYS_START_AT_ZERO

async def channel_jump(arg):
    logs = []

    num = int(arg[1:]) - 1

    # sub one to allow for "/c0" being the top channel
    if ARRAYS_START_AT_ZERO:
        num -= 1
   
    # in case someone tries to go to a negative index
    if num <= -1:
        num = 0

    for slog in server_log_tree:
        if slog.get_server() is client.get_current_server():
            for clog in slog.get_logs():
                logs.append(clog)

    logs = quick_sort_channel_logs(logs)


    if num > len(logs):
        if ARRAYS_START_AT_ZERO:
            num = len(logs) - 1
        else: num = len(logs)

    client.set_current_channel(logs[num].get_name()) 
    logs[num].unread = False
