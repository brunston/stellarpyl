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

<table border="1" style="width:100%">
  <tr>
    <td>'pixel_d' (short 'pd')</td>
    <td>takes an image and shows the pixel distribution of the\
	image over the intensity of the pixels</td>
  </tr>
  <tr>
    <td>'image_regression' (short 'imgreg')</td>
    <td>takes an image and finds the line which goes\
	through the spectrum in that image</td>
  </tr>
  <tr>
    <td>'intensity_n' (short 'n')</td>
    <td>takes an image of a spectrum and converts it into an\
	intensity plot using the naive method of adding</td>
  </tr>
  <tr>
    <td>'intensity_saa' (short 'saa')</td>
    <td>takes an image of a spectrum and converts it into\
	an intensity plot using spatial anti-aliasing at a sub-sampling rate\
	of one tenth of one pixel</td>
  </tr>
  <tr>
    <td>'crop'</td>
    <td>takes an image and crop it based on your selected threshold.</td>
  </tr>
</table>

##Additional commands:

<table border="1" style="width:100%">
  <tr>
    <td>'jellyfish'</td>
    <td>who doesn't need a jellyfish?</td>
  </tr>
</table>