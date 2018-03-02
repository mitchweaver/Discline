# Features
* Can receive and draw messages
* Can send messages
* Channel log: Old messages at top, new messages at bottom
* Can edit typing.

# Walk through
* Start Discline.py
* It initializes
* It displays a channel
* Start typing something, see text appear in editBar & cursor at end
* Press Left/Up, the cursor moves over to the left
* Press Right/Down, the cursor moves to the right
* Press backspace at end, the character before the cursor is deleted
* Press backspace anywhere, the character before the cursor is deleted
* Press left and start typing, see text inserted at point and displayed on screen
* Send new message
* See the sent message in channel log
* (Many messages later)
* Older messages float up/newer messages at bottom

# Control flow

```
Discline.py
	main:
		* start client
	on_ready:
		* wait until login
		* populate (server_log_tree) with (ServerLog)s with empty (ChannelLog)s
		* initialize UI
		* [async] create task key_input

input_handler.py
	key_input:
		* wait until ready
		* draw initial screen
		<loop>:
			* refresh (editBar)
			* get and process input
			if msgEdit still in editing state:
				* print msgEdit buffer to editBar
			else:
				* try to send message. On failure, try again 2 more times
			* reset msgEdit
			* redraw entire screen

Discline.py
		* draw initial screen
```
