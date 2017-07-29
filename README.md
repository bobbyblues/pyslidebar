# pyslidebar

Python 3 implementation of the [slidekb](https://slidekb.com/) software.

# Prior to using the software

You need to have your slidebar accessible by python.
Usually, the slidebar will appear in your `/dev/` directory as `ttyUSB0`, if not, change the following commands according to your device name.

A temporary way of making the device accessible is to run:

    sudo chmod 666 /dev/ttyUSB0

However, this needs to be done after each restart.

TODO: explain how to use a udev rule.

# How to use

The slidebar.py class can be used to control the slidebar from other scripts, for example:

    import slidebar
    sb = slidebar.SlideBar("/dev/ttyUSB0")
    sb.setPosition(0.5) # Sets the slidebar in the center
    sb.vibrate(20) # Makes the slidebar vibrate for 20 arduino cycles

The software also comes with a set of modules and a module manager.
Those can be configured through a `config.json` file, and the manager launched as:

    python manager.py

For a simple start, you can use the sample configuration file provided:

	mv config-sample.json config.json

# Typewriter module

This module is the default one, running when no other is.
It makes the slider shift to the right at every keypress, and go back all the way to the left at every new line.
To enable or disable that module, change the value of the `typewriter` entry in the `config.json` file.

For this module to work, we use the pyxhook library from [JeffHoogland](https://github.com/JeffHoogland/pyxhook).
Those files are provided under the license specified in the pyxhook subdirectory.

Configuration:

 - typewriter: true or false to enable or disable the typewriter module

Known bugs:

 - Sometimes the slider moves all the way to the right instead of doing only one step, I don't know why yet

# Volume module

This module allows to control the volume using the slider.
By default, pressing the left windows key will set the slider at a position corresponding to the current volume (0% being all the way to the left, and 100% all the way to the right).
Moving the slider while still holding the windows key will change the volume accordingly.

To enable or disable that module, change the value of the `volume` entry in the `config.json` file.


To change which key is triggering this module, change the value of the `volume-modifier` entry in the `config.json` file.
The value should be the ascii value of the key you wish to use.

Know that this module works with pulseaudio only, and requires for pulseaudio-ctl to be installed.


Configuration:

 - volume: true or false to enable or disable the volume module
 - volume-modifier: ascii code of the key that will trigger the volume module
 - volume-sink: index of the pulse-audio sink you want the volume module to control
