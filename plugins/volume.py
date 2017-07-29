import subprocess
from subprocess import PIPE
import threading
import time
import os, sys

class Volume:

    def __init__(self, sb, sink = "0"):
        self.sb = sb
        self.sink = str(sink)
        self.running = False
        self.moving = False

    def init(self):

        # We check if we don't have a previous call to Volume still running
        # (otherwise, causes bug when people press and release the volume modifier key very quickly)
        while self.running or self.moving:
            time.sleep(1. / 60.)

        # We get the current level
        self.curr_volume = self.getVolume()

        # We set the slider at the proper position
        curr_position = min(float(self.curr_volume) / 100.0, 1.0)
        self.moving = True # We set a flag saying we are moving, so that the update function doesn't update the volume
        self.sb.setPosition(curr_position) # We set the slider position according to the current volume (but not more than 100%)

        # We wait for the slider to be at the righ position
        while abs(self.sb.getPosition() - curr_position) > 0.02:
            time.sleep(1. / 60.)

        # We are done moving, we can actually update the volume
        self.moving = False

        # We specify that we started, so that the thread doesn't stop
        self.running = True

        # And we start the thread
        self.periodic_thread = threading.Thread(target = self.update)
        self.periodic_thread.start()

    def stop(self):
        self.running = False

    def keydown(self, event):
        return

    def keyup(self, event):
        return

    def getVolume(self):
        command = ["pactl", "list", "sinks"]
        a = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
        (cout, cerr) = a.communicate()

        volume = int(cout.decode("ascii").split("SINK #" + str(self.sink))[-1].split('/ ')[1].split('%')[0])

        return volume


    def setVolume(self, volume):
        command = ["pactl", "set-sink-volume", "2", str(int(volume)) + "%"]
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

            if not self.moving:
                # If the slider is low enough, we set the volume to 0.
                # (We need to do that because of the not perfect precision of the slider)
                if new_volume < 2.0 and self.curr_volume != 0.0:
                    self.setVolume(0.0)

                # Similarly, if the slider is high enough, we set the volume to the max.
                elif new_volume > 98.0 and self.curr_volume != 100.0:
                    self.setVolume(100.0)

                # If the change is greater than 1%, then we update the volume
                # (We do that check as the position given by the slidebar changes slightly from time to time)
                elif new_volume > 2.0 and new_volume < 98.0 and abs(new_volume - self.curr_volume) > 1:
                    self.setVolume(new_volume)
                
            # We repeat this process at a 60Hz frequency
            time.sleep(1. / 60.)

