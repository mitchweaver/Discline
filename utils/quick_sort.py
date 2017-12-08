def quick_sort_channel_logs(channel_logs):
    # sort channels to match the server's default chosen positions
    def quick_sort(channel_logs):
        if len(channel_logs) <= 1: return channel_logs
        else:
            return quick_sort([e for e in channel_logs[1:] \
                if e.get_channel().position <= channel_logs[0].get_channel().position]) + \
                [channel_logs[0]] + quick_sort([e for e in channel_logs[1:] \
                if e.get_channel().position > channel_logs[0].get_channel().position])

