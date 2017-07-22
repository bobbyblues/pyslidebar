class TypeWriter:

	def __init__(self, sb):
		self.sb = sb
		self.going_back = False

	def init(self):
		self.sb.setPosition(0.0)

	def stop(self):
		return


	def keydown(self, event):
		# We check if we are currently going back to the beginning of the line
		if self.going_back:
			# If so we verify if we reached the beginning yet
			if self.sb.getPosition() <= 0.01:
				# If so, we can start moving right again
				self.going_back = False
			else:
				# Else, we wait for the slider to finish moving
				self.sb.setPosition(0.0)
				return

		# If the key pressed is return, go back to the beginning
		if event.Ascii == 13:
			self.going_back = True
			self.sb.setPosition(0.0)
		# if the key pressed is backspace, we move left
		elif event.Ascii == 8:
			self.sb.moveLeft()
		# Otherwise, we move right
		else:
			self.sb.moveRight()

	def keyup(self, event):
		return

