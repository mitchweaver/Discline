# Behavior
* Start typing something, see text appear in editBar & cursor at end
* Press Left/Up, the cursor moves over to the left
* Press Right/Down, the cursor moves to the right
* Press backspace at end, the character before the cursor is deleted
* Press backspace anywhere, the character before the cursor is deleted
* Press left and start typing, see text inserted at point and displayed on screen

## Cursor movements
### Left
* Pressing left when curPos > 0
	* Cursor moves left
* Pressing left when curPos == 0 and offset == 0
	* No action
* Pressing left when curPos == 0 and offset > 0
	* curPos = maxWidth-SCROLL
	* offset -= SCROLL
### Right
* Pressing right when offset+curpos < len(inputBuffer)-1 and curPos < maxWidth-1
	* Cursor moves right
* Pressing right when len(inputBuffer) == 0
	* No action
* Pressing right when offset+curPos == len(inputBuffer)-1
	* No action
* Pressing/typing right when curPos == maxWidth-1 and offset+curPos < len(inputBuffer)-1
	* curPos -= SCROLL
	* offset += SCROLL

# Component requirements
* Input buffer
* Cursor position

# Method
* Initialize class
* <Loop>
	* Get character from input
	* Check if character is alphanumeric or not
	* If alphanumeric, add character to buffer
	* If non-alphanumeric, call associated function
	* If character is '\n', return str and clear buffer, set curPos to 0
