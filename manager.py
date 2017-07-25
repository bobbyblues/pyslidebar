import json
from pyxhook import pyxhook
import slidebar
import time

from plugins import typewriter
from plugins import volume

class Manager:

	def __init__(self):
		# Loading the configuration file
		config = json.load(open("config.json",'r'))

		self.slidebar_device = config["slidebar"]
		self.has_typewriter = config["typewriter"]
		self.has_volume = config["volume"]
		self.volume_modifier = config["volume-modifier"]

		# Creating the slidebar
		self.sb = slidebar.SlideBar(self.slidebar_device)
		self.sb.reverse()
		self.sb.setPosition(0.0)

		# Creating the plugins
		if self.has_typewriter:
			self.typewriter = typewriter.TypeWriter(self.sb)
			self.typewriter.init()

		if self.has_volume:
			self.volume = volume.Volume(self.sb)

		# Booleans to know which plugins are active
		self.is_active_typewriter = True
		self.is_active_volume = False


	def keydown(self, event):
		# We check if the key down is one of the modifiers
		if event.Ascii == self.volume_modifier and self.has_volume:
			self.is_active_volume = True
			self.is_active_typewriter = False
			if self.has_typewriter:
				self.typewriter.stop()
			self.volume.init()

		# We send the event to the proper plugin
		if self.has_typewriter and self.is_active_typewriter:
			self.typewriter.keydown(event)

		if self.has_volume and self.is_active_volume:
			self.volume.keydown(event)

	def keyup(self, event):
		# We check if the key up is one of the modifiers
		if event.Ascii == self.volume_modifier and self.is_active_volume:
			self.is_active_volume = False
			self.is_active_typewriter = True
			if self.has_volume:
				self.volume.stop()
			if self.has_typewriter:
				self.typewriter.init()

		# We send the event to the proper plugin
		if self.has_typewriter and self.is_active_typewriter:
			self.typewriter.keyup(event)

		if self.has_volume and self.is_active_volume:
			self.volume.keyup(event)


def kbevent_down(event):
	'''
	Function called whenever a key is pressed
	'''
	global manager
	manager.keydown(event)

def kbevent_up(event):
	global manager
	manager.keyup(event)


# The following code is shamelessly stolen from the example.py file at
# https://github.com/JeffHoogland/pyxhook

# Create Manager
manager = Manager()

# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent_down
hookman.KeyUp = kbevent_up
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


