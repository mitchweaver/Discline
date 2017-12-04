async def send_file(client, filepath):
    try: 
        await client.send_file(client.get_current_channel(), filepath)
    except:
        Either a bad file path, the file was too large,
        or encountered a connection problem during upload
        pass
