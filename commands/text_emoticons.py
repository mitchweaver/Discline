async def check_emoticons(client, cmd):
    if cmd == "shrug": 
        try: await client.send_message(client.get_current_channel(), "¯\_(ツ)_/¯")
        except: pass
    elif cmd == "tableflip": 
        try: await client.send_message(client.get_current_channel(), "(╯°□°）╯︵ ┻━┻")
        except: pass
    elif cmd == "unflip":
        try: await client.send_message(client.get_current_channel(), "┬──┬ ノ( ゜-゜ノ)")
        except: pass
    elif cmd == "zoidberg": 
        try: await client.send_message(client.get_current_channel(), "(/) (°,,°) (/)")
        except: pass
    elif cmd == "lenny": 
        try: await client.send_message(client.get_current_channel(), "( ͡° ͜ʖ ͡°)")
        except: pass
    elif cmd == "lennyx5": 
        try: await client.send_message(client.get_current_channel(), "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)")
        except: pass
    elif cmd == "glasses": 
        try: await client.send_message(client.get_current_channel(), "(•_•) ( •_•)>⌐■-■ (⌐■_■)")
        except: pass
    elif cmd == "walking_my_mods": 
        try: await client.send_message(client.get_current_channel(), "⌐( ͡° ͜ʖ ͡°) ╯╲___卐卐卐卐")
        except: pass

