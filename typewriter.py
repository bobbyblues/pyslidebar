import slidebar
from pyxhook import pyxhook
import subprocess
from subprocess import PIPE
import time

# Initializing the slidebar
sb = slidebar.SlideBar("/dev/ttyUSB0")
sb.reverse()
sb.setPosition(0.0)

# We don't want the slider to start moving until it's back to the beginning
going_back = False

def kbevent(event):
	'''
	Function called whenever a key is pressed
	'''
	# We get the global variables
	global running
	global sb
	global going_back

	# We check if we are currently going back to the beginning of the line
	if going_back:
		# If so we verify if we reached the beginning yet
		if sb.getPosition() <= 0.01:
			# If so, we can start moving right again
			going_back = False
		else:
			# Else, we wait for the slider to finish moving
			sb.setPosition(0.0)
			return

	# If the key pressed is return, go back to the beginning
	if event.Ascii == 13:
		going_back = True
		sb.setPosition(0.0)
	# if the key pressed is backspace, we move left
	elif event.Ascii == 8:
		sb.moveLeft()
	# Otherwise, we move right
	else:
		sb.moveRight()


# The following code is shamelessly stolen from the example.py file at
# https://github.com/JeffHoogland/pyxhook

# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
# Hook the keyboard
hookman.HookKeyboard()
# Start our listener
hookman.start()

# Create a loop to keep the application running
running = True
while running:
    time.sleep(0.1)

# Close the listener when we are done
hookman.cancel()





