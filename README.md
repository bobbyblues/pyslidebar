# pyslidebar

Python 3 implementation of the [slidekb](https://slidekb.com/) software.

# Example of use

    import slidebar
    sb = slidebar.SlideBar("/dev/ttyUSB0")
    sb.setPosition(0.5) # Sets the slidebar in the center
    sb.vibrate(20) # Makes the slidebar vibrate for 20 arduino cycles

# Typewriter module

For this module to work, we use the pyxhook library from [JeffHoogland](https://github.com/JeffHoogland/pyxhook).
Those files are provided under the license specified in the pyxhook subdirectory.

Simply launch the module, and start typing.

There is currently a bug where the slider will move big spaces to the right, I am still not sure why.

# SlideBar as a volume control

For this module to work, you need to use pulseaudio, and have pulseaudio-ctl installed.
Make sure the proper device is written in volume.py (/dev/ttyUSB0 in my case), and run:
    
     python volume.py

The slider should move to the current volume position (caped to 100%).
Then, moving the slider should update your volume.
