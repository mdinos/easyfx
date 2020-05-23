# EasyFX

EasyFX is a custom pedal-board software application. Patches are loaded via Pure Data and the graphical interface allows easy control over it.

How to run:

```shell
./init.sh # this assumes you have git and pip installed
./entry.py
```

Pyenv recomended for python version management (hence .python-version file).

## Creating patches for importing to EasyFX

There are two simple steps to take in prior to importing an effect into EasyFX.

Firstly, your patch must be designed as an [abstraction](http://write.flossmanuals.net/pure-data/abstractions/),
with `inlet` and `outlet` objects not `adc` or `dac` objects.

Secondly, any parameters that you wish to be adjustable by slider should have their values input with a *single* 
[netrecieve](http://write.flossmanuals.net/pure-data/send-and-receive/) object,  multiple parameters should take
input from the same *single* netrecieve object, on a port which is unique among those found in any other patches
that may be loaded into the application. Parameters should be named $1, $2, $3 etc in your parameterised objects.
For an example, please see the `/patches` folder.

Finally, open up EasyFX and press the 'import' button (The last button on the toolbar!) and follow the steps. 
Remember what order your parameters are in, as this is important when filling in the form which adds the information
about your patch to the program.

If you experience any issues, remember there are always backup patch and patch metadata files in the /patches/backup 
folder.

### Additional Credits

Ward, James (2018) for the Delay Patch

[Phasor patch](https://guitarextended.wordpress.com/2011/12/28/phaserchorus-effect-with-pure-data/)

Icons located in /img made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from www.flaticon.com"
