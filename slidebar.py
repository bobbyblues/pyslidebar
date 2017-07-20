import serial

class SlideBar:

	def __init__(self, port):
		self.ser = serial.Serial(port,  115200)
		# Trying to read the ID — somehow that fails
		# self.ser.read_all()
		# self.ser.write("2424]".encode("ascii"))
		# pos = self.ser.readline() # It seems the slider sends its position first
		# self.id = self.ser.readline() # Then we can read the ID
		# print("Slidebar ID:", self.id)

	def setPosition(self, position):
		'''
		Sets the position of the slider between 0 and 1.
		@param position: position value between 0.0 and 1.0
		'''
		if (position >= 0.0 and position <= 1.0):
			int_pos = int(position * 1023.0)
			str_pos = str(int_pos).zfill(4)
			str_setPosition = str_pos + "]"
			self.ser.write(str_setPosition.encode("ascii"))

	def vibrate(self, time):
		'''
		Makes the slidebar vibrate for a given amount of time.
		@param time: vibration time in arduino cycles between 0 and 999 where 
		'''
		if (time >= 0 and time <= 999):
			str_time = str(time).zfill(3)
			str_vibrate = "6" + str_time + "]"
			self.ser.write(str_vibrate.encode("ascii"))


