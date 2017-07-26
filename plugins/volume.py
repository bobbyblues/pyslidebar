import subprocess
from subprocess import PIPE
import threading
import time
import os, sys

class Volume:

    def __init__(self, sb):
        self.sb = sb

    def init(self):
        # We specify that we started
        self.running = True

        # We get the current level
        command = ["./plugins/getVolume.sh"]
        a = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
        (cout, cerr) = a.communicate()
        self.curr_volume = int(cout.strip())

        # We set the slider at the proper position
        curr_position = min(float(self.curr_volume) / 100.0, 1.0)
        self.sb.setPosition(curr_position) # We set the slider position according to the current volume (but not more than 100%)

        # We wait for the slider to be at the righ position
        while abs(self.sb.getPosition() - curr_position) > 0.01:
            time.sleep(1. / 60.)


        self.periodic_thread = threading.Thread(target = self.update)
        self.periodic_thread.start()

    def stop(self):
        self.running = False

    def keydown(self, event):
        return

    def keyup(self, event):
        return

    def setVolume(self, volume):
        command = ["pactl", "set-sink-volume", "0", str(int(volume)) + "%"]
        a = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
        (cout, cerr) = a.communicate()
        self.curr_volume = volume

    def update(self):
        while True:
            if not self.running:
                return
            # We check if the position of the slider changed:
            new_position = self.sb.getPosition()
            new_volume = new_position * 100.0

            if new_volume < 2.0 and self.curr_volume != 0.0:
                self.setVolume(0.0)

            # If the change is greater than 1%, then we update the volume
            # (We do that check as the position given by the slidebar changes slightly from time to time)
            elif new_volume > 2 and abs(new_volume - self.curr_volume) > 1:
                self.setVolume(new_volume)
                
            # We repeat this process at a 60Hz frequency
            time.sleep(1. / 60.)

