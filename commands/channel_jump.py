from utils.globals import gc
from utils.quicksort import quick_sort_channel_logs
from utils.settings import settings

async def channel_jump(arg):
    logs = []

    num = int(arg[1:]) - 1

    # sub one to allow for "/c0" being the top channel
    if settings["arrays_start_at_zero"]:
        num -= 1
   
    # in case someone tries to go to a negative index
    if num <= -1:
        num = 0

    for slog in gc.server_log_tree:
        if slog.get_server() is gc.client.get_current_server():
            for clog in slog.get_logs():
                logs.append(clog)

    logs = quick_sort_channel_logs(logs)


    if num > len(logs): num = len(logs) - 1

    gc.client.set_current_channel(logs[num].get_name()) 
    logs[num].unread = False
    logs[num].mentioned_in = False
