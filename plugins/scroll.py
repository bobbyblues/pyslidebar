import threading
import time
from pymouse import PyMouse


class Scroll:

    def __init__(self, sb, sink = "0"):
        self.sb = sb
        self.mouse = PyMouse()
        self.moving = False

    def init(self):
        self.sb.createParts(1)
        self.moving = True
        while self.sb.getPosition() < 0.42 or self.sb.getPosition() > 0.56:
            time.sleep(1. / 60.)

        self.moving = False

        # We specify that we started, so that the thread doesn't stop
        self.running = True

        # And we start the thread
        self.periodic_thread = threading.Thread(target = self.update)
        self.periodic_thread.start()

    def stop(self):
        self.running = False
        self.sb.removeParts()

    def keydown(self, event):
        return

    def keyup(self, event):
        return


    def update(self):
        while True:
            if not self.running:
                return

            if self.moving:
                time.sleep(1. / 60.)
                continue

            # We compute the distance
            position = self.sb.getPosition()
            if position < 0.4:
                distance = 0.4 - position
                distance = int(distance * 10.) + 1
                self.mouse.scroll(vertical=distance)

            elif position > 0.6:
                distance = position - 0.6
                distance = int(distance * 10.) + 1
                self.mouse.scroll(vertical=-distance)


            # print("scrolling:", distance)

            # self.mouse.scroll(vertical=distance)

            # print(self.sb.getPosition())
            # We repeat this process at a 60Hz frequency
            time.sleep(5. / 60.)

