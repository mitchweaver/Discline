def quick_sort_channel_logs(channel_logs):
    # sort channels to match the server's default chosen positions
    if len(channel_logs) <= 1: return channel_logs
    else:
        return quick_sort_channel_logs([e for e in channel_logs[1:] \
            if e.get_channel().position <= channel_logs[0].get_channel().position]) + \
            [channel_logs[0]] + quick_sort_channel_logs([e for e in channel_logs[1:] \
            if e.get_channel().position > channel_logs[0].get_channel().position])
