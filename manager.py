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

		# Creating the slidebar
		self.sb = slidebar.SlideBar(self.slidebar_device)
		self.sb.reverse()
		self.sb.setPosition(0.0)

		# We start we no modules
		self.do_typewriter = False
		self.typewriter_is_running = False
		self.modules = [] # Existing modules
		self.modules_modifier = [] # Modifiers keys activating modules
		self.modules_running = [] # Boolean to know if a module is running

		# To keep track of keys currently pressed
		self.pressed_keys = []

		# Loading modules
		for module in config["plugins"]:
			self.loadModule(module)


	def keydown(self, event):
		# We append the key to the keys currently being pressed
		if event.Ascii not in self.pressed_keys:
			self.pressed_keys.append(event.Ascii)

		# We check if any module needs to start
		for i in range(len(self.modules)):
			key = self.modules_modifier[i]
			running = self.modules_running[i]
			# If that module has its key down and is not already running
			if key in self.pressed_keys and not running:
				# We stop the typewriter if any
				if self.typewriter_is_running:
					self.typewriter.stop()
					self.typewriter_is_running = False
				# We indicate that the module is running
				self.modules_running[i] = True
				# We start the module
				self.modules[i].init()

		# Finally we send the key event to the appropriate modules
		for i in range(len(self.modules)):
			if self.modules_running[i]:
				self.modules[i].keydown(event)

		if self.typewriter_is_running:
			self.typewriter.keydown(event)


	def keyup(self, event):
		# We remove the key from the list of keys being pressed
		if event.Ascii in self.pressed_keys:
			self.pressed_keys.remove(event.Ascii)

		# We check if any module needs to stop
		for i in range(len(self.modules)):
			key = self.modules_modifier[i]
			running = self.modules_running[i]
			# If that module is running but its key is not pressed anymore
			if running and key not in self.pressed_keys:
				# We stop the module
				self.modules[i].stop()
				self.modules_running[i] = False

		# We check if we need to start the typewriter module again
		if self.do_typewriter and not self.typewriter_is_running and True not in self.modules_running:
			self.typewriter_is_running = True
			self.typewriter.init()

		# Finally we send the key event to the appropriate modules
		for i in range(len(self.modules)):
			if self.modules_running[i]:
				self.modules[i].keyup(event)

		if self.typewriter_is_running:
			self.typewriter.keyup(event)



	def loadModule(self, module):
		if not module["enabled"]:
			return

		module_name = module["name"]

		if module_name == "typewriter":
			self.do_typewriter = True
			if self.do_typewriter:
				self.typewriter = typewriter.TypeWriter(self.sb)
				self.typewriter_is_running = True
				self.typewriter.init()

		elif module_name == "volume":
			# Reading parameters
			volume_sink = module["sink"]
			volume_modifier = module["modifier"]

			# Initializing module
			self.modules.append(volume.Volume(self.sb, volume_sink))
			self.modules_modifier.append(volume_modifier)
			self.modules_running.append(False)

		else:
			print("Unknown module:", module)


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


