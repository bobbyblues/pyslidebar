import slidebar
import subprocess
from subprocess import PIPE
import time

sb = slidebar.SlideBar("/dev/ttyUSB0")

# We get the current level
command = ["pulseaudio-ctl", "full-status"]
a = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
(cout, cerr) = a.communicate()
curr_volume = int(cout.decode("ascii").split(" ")[0])

curr_position = min(float(curr_volume) / 100.0, 1.0)
sb.setPosition(curr_position) # We set the slider position according to the current volume (but not more than 100%)

while True:
	# We check if the position of the slider changed:
	new_position = sb.getPosition()
	new_volume = new_position * 100.0
	# If the change is greater than 1%, then we update the volume
	# (We do that check as the position given by the slidebar changes slightly from time to time)
	if abs(new_volume - curr_volume) > 1:
		command = ["pulseaudio-ctl", "set", str(int(new_volume))]
		a = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
		(cout, cerr) = a.communicate()
		curr_volume = new_volume
	# We repeat this process at a 60Hz frequency
	time.sleep(1. / 60.)



