import serial
import threading
import time

class SlideBar:

	def __init__(self, port):

		self.ser = serial.Serial(port,  115200)

		# Waiting for the slider to initialize
		time.sleep(2)

		# Centering the slider
		self.vibrate(3)
		self.last_pos = 0.5
		self.ID = 'NONE'
		self.ser.write("2424]".encode("ascii")) # The reader thread will pick up the new ID as soon as it has been sent back
		self.reversed = False
		self.setPosition(0.5)

		# Starting a reader thread that will read the slidebar output constantly
		self.periodic_thread = threading.Thread(target = self.reader)
		self.periodic_thread.start()

	def reader(self):
		while(True):
			read_bytes = self.ser.read_all()
			read_str = read_bytes.decode("ascii")
			read_values = read_str.split("\r\n")
			for value in read_values:
				if 'l' in value:
					# It seems that slidebarID follow the format l[0-9]n[0-9]+
					# By checking if it contains a 'l', we know if we are reading the ID
					self.ID = value
				elif len(value) > 1:
					# Debug
					try:
						tmp = float(value)
					except Exception as e:
						print("[ERROR] When converting value:", value)
					pos_float = float(value) / 1023.0
					if self.reversed:
						self.last_pos = 1.0 - pos_float
					else:
						self.last_pos = pos_float
			time.sleep(1. / 60.)



	def setPosition(self, position):
		'''
		Sets the position of the slider between 0 and 1.
		@param position: position value between 0.0 and 1.0
		'''
		if self.reversed:
			position = 1.0 - position
		if (position >= 0.0 and position <= 1.0):
			int_pos = int(position * 1023.0)
			str_pos = str(int_pos).zfill(4)
			str_setPosition = str_pos + "]"
			self.ser.write(str_setPosition.encode("ascii"))

	def vibrate(self, time):
		'''
		Makes the slidebar vibrate for a given amount of time.
		@param time: vibration time in arduino cycles between 0 and 999
		'''
		if (time >= 0 and time <= 999):
			str_time = str(time).zfill(3)
			str_vibrate = "6" + str_time + "]"
			self.ser.write(str_vibrate.encode("ascii"))

	def getPosition(self):
		'''
		Returns the position of the slider between 0.0 and 1.0
		'''
		return self.last_pos


	def getID(self):
		'''
		Returns the ID of the slider (or "NONE" if it has not been read already)
		'''
		return self.ID

	def setReverse(self, reversed=True):
		'''
		Allows to change the orientation of the slider
		@param reversed: slider is reversed if parameter is set to True, normal otherwise
		'''
		self.reversed = reversed

	def moveRight(self, steps = 1, step_size = 0.02):
		'''
		Moves the slider one or more steps to the right
		@param steps: number of steps to move
		@param step_size: size of the step (anything less than 0.02 will have no effect)
		'''
		new_pos = self.last_pos + steps * step_size
		if new_pos > 1.0:
			new_pos = 1.0
		self.setPosition(new_pos)

	def moveLeft(self, steps = 1, step_size = 0.02):
		'''
		Moves the slider one or more steps to the left
		@param steps: number of steps to move
		@param step_size: size of the step (anything less than 0.02 will have no effect)
		'''
		new_pos = self.last_pos - steps * step_size
		if new_pos < 0.0:
			new_pos = 0.0
		self.setPosition(new_pos)

	def createParts(self, number_of_parts):
		'''
		Create parts in the slider:
		 - the slider will automatically be at the center of a part
		 - the slider will offer resistance when trying to move from one part to the other
		@param number_of_patrs: number of parts to be created between 0 and 50 (0 makes the slider go back to "normal" mode)
		'''
		if number_of_parts > 50:
			print("[ERROR] Cannot have more than 50 parts")
		if number_of_parts < 0:
			print("[ERROR] Number of parts needs to be at least 0")

		str_pos = str(2000 + number_of_parts)
		str_createParts = str_pos + "]"
		self.ser.write(str_createParts.encode("ascii"))

	def removeParts(self):
		self.createParts(0)


