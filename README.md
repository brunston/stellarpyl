project: stellarPY
file: README
author: Brunston Poon
org: UH-IFA and SPS
For licensing information see LICENCE.txt.

##Summary:

This is stellar spectra reduction and analysis command-line software written
using the Python 3.4 version of the Anaconda Scientific Python distribution. It 
is work done for an internship at the Unversity of Hawaii in conjunction with 
the St. Paul's School Engineering Honors program.

It aims to provide a one-click workflow for analyzing uncompressed TIFF stellar
spectra images obtained from a DSLR through a diffraction grating. The goals of
the project are: to automatically crop the image; to perform background 
subtraction; to create an intensity plot of the spectrum (accounting for non-
orthogonal spectra); and to account for the use of a DSLR sensor by using either 
a relative response function or an absolute response function to normalize the 
intensity plot.

##Workflow:

Run ui.py in the command line:

> python ui.py

Be sure you are using Python3 and installed numpy and Python Imaging Library.
Alternatively, you can run this using the Python3 version of Anaconda.
If you do not satisfy these prerequisites, the program will not function
correctly.

You will be presented with a list of commands.

For a brand new image, run 'crop' first. Drag your file into the same directory
and enter the filename including the file extension. This program will accept
TIFF files, either in .tif or .tiff extension format. It will then ask you for a
threshold.

The threshold is used throughout the program to determine what data is relevant
and what parts of the image can be discarded without damaging the value of the
data. It needs to be an integer value between 0 and 765 as the threshold is
measured as the sum of the R, G, and B bin values in a pixel, therefore, 
each RGB value can be an integer from 0-255; total value can be from 0-765. If
you do not have a value you are already using for all of your images, you can
type 'pixel_d' at the command prompt to run a function that plots the
distribution of binned pixel values in your image.

The program will run the cropping algorithm and ask for a filename to give to
the new file.

The next command you should run is 'intensity_saa'. It will take an image file
and a threshold and automatically perform linear regression to find the y=mx+b
line on which the spectral trace lies. It will then step one pixel at a time
along the spectral trace and add up all intensity values occuring along that
line.

The program will graph this intensity plot, which can be saved using the tools
already provided by matplotlib.


##Command list:

###IMAGE PROCESSING
- 'autoProcess' (short 'auto') -
autoProcess will take care of cropping and doing intensity plotting for you.
just provide a filename. In order to use this feature you must first set
a default threshold to use by using the 'settings_threshold' command.

- 'pixel_d' (short 'pd') -
takes an image and shows the pixel distribution of the image over the intensity
of the pixels.

- 'crop' - 
takes an image and crop it based on your selected threshold.

- 'image_regression' (short 'imgreg') -
takes an image and finds the line which goes through the spectrum in that image.

- 'intensity_n' (short 'n') -
takes an image of a spectrum and converts it into an intensity plot using the
naive method of adding.

- 'intensity_saa' (short 'saa') -
takes an image of a spectrum and converts it into an intensity plot using
spatial anti-aliasing at a sub-sampling rate of one tenth of one pixel.

- 'show_threshold' -
see exactly what could be removed (assuming no crop stop has been set) using the
threshold that is currently set.

- 'show_regression' -
shows regressed line overlayed on the original (cropped) image.

- 'show_walks' -
shows walking lines overlayed on the original (cropped) image.

###PROGRAM

- 'about' -
displays information about this program

- 'functions' -
where you are now

- 'help' -
brings up sample workflow

- 'settings_cropoverride' -
sets manual overrides for automatic cropping on the top, bottom, and sides
of an image. The default value is -1 (which is equivalent to no override)
for all values.

- 'settings_default' -
returns ALL settings back to default:
    defaultThreshold = -1
    autoIntensity = saa
    manual overrides all to -1
    step = 1
    verbose = yes

- 'settings_intensity' -
sets default intensity processing method for the autoProcess feature.
The default setting is saa (for spatial anti-aliasing).

- 'settings_step'
sets default step value along the spectral trace (and thus resolution of
resulting intensity plot). default is 1 pixel-equivalence.

- 'settings_threshold' -
sets default threshold. Set to -1 if you would like the program to always ask.
The default setting is -1 (always asks).

- 'settings_verbose' -
sets verboseness. 'yes' to include debug statements, 'no' is default.

- 'view_settings' -
view your current settings

##Additional commands:

<table border="1" style="width:100%">
  <tr>
    <td>'jellyfish'</td>
    <td>who doesn't need a jellyfish?</td>
  </tr>
</table>