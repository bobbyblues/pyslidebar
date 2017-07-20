# pyslidebar
Python implementation of the slidekb software.

# Example of use

    import slidebar
    sb = slidebar.SlideBar("/dev/ttyUSB0")
    sb.setPosition(0.5) # Sets the slidebar in the center
    sb.vibrate(20) # Makes the slidebar vibrate for 20 arduino cycles