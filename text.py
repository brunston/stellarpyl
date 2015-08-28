# -*- coding: utf-8 -*-
"""
stellarPYL - python stellar spectra processing software
Copyright (c) 2015 Brunston Poon
@file: text
This program comes with absolutely no warranty.
"""
import time

def welcome():
	print("""
Welcome to stellarPYL, Copyright (C) 2015 Brunston Poon, type 'licence' for info

Type 'quit' or 'exit' to leave the program. Use ctrl-c to force-interrupt.

TO VIEW HELP, WHICH WILL DESCRIBE A TYPICAL WORKFLOW SCENARIO, TYPE 'help'.
TO VIEW A LIST OF AVAILABLE FUNCTIONS & COMMANDS, TYPE 'commands'.
TO LEARN MORE ABOUT THIS PROGRAM, TYPE 'about'.

Help and information is also available online at http://st.bpbp.xyz/
or by viewing README.md
            """)
	return None

def firstrun():
	print("""
SINCE this is your first time running the program, please take the time to read
the about, help, and commands documentation to familiarize yourself with this
program. For your convenience, I'm loading the commands below.
        """)
	return None

def about():
	print("""
This is stellar spectra reduction and analysis command-line software written
using the Python 3.4 version of the Anaconda Scientific Python distribution. It 
is work done for an internship at the Unversity of Hawaii in conjunction with 
the St. Paul's School Engineering Honors program.

It aims to provide a simplified workflow for analyzing uncompressed TIFF stellar
spectra images obtained from a DSLR through a diffraction grating. The goals of
the project are: to automatically crop the image; to perform background 
subtraction; to create an intensity plot of the spectrum (accounting for non-
orthogonal spectra); and to account for the use of a DSLR sensor by using either
a relative response function or an absolute response function to normalize the 
intensity plot.

It is written by Brunston Poon. 
            """)
	return None

def help():
	print("""

AS AN ALTERNATIVE TO THE BELOW, make sure you set a default threshold using
'settings_threshold', and then simply type 'auto' to have the program do
the majority of the work.

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

A typical threshold may be in the range from 100-130.

The program will run the cropping algorithm and ask for a filename to give to
the new file.

The next command you should run is 'intensity_saa'. It will take an image file
and a threshold and automatically perform linear regression to find the y=mx+b
line on which the spectral trace lies. It will then step one pixel at a time
along the spectral trace and add up all intensity values occuring along that
line.

The program will graph this intensity plot, which can be saved using the tools
already provided by matplotlib.

            """)
	return None

def commands():
	print("""
            ---IMAGE PROCESSING---
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

- 'dev_cgrowth' -
plots curve of growth

            ---PROGRAM---

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
    showthresh = yes

- 'settings_intensity' -
sets default intensity processing method for the autoProcess feature.
The default setting is saa (for spatial anti-aliasing).

- 'settings_margin' -
sets margin for cropping. default is 5 pixels.

- 'settings_showthreshold' -
showThreshold takes a while to run. Set to 'no' for a faster autoProcess
run time. Default is 'yes'

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

            """)
	return None

def rehash():
	print("""
Type 'quit' or 'exit' to leave this program. Alternately, you may use
ctrl-c to force-interrupt at any time. Type 'help' for sample workflow,
'commands' for a list of functions and commands, and 'about' for more info.
            """)
	return None

def viewSettings(config):
	print("Current settings:")
	print("default threshold: ", config['CONTROL']['defaultthreshold'])
	print("autoIntensity: ", config['CONTROL']['autointensity'])
	print("manual override top crop:", config['CONTROL']['manualtop'])
	print("manual override bottom crop:", config['CONTROL']['manualbot'])
	print("manual override left crop:", config['CONTROL']['manualleft'])
	print("manual override right crop:", config['CONTROL']['manualright'])
	print("step:", config['CONTROL']['r'])
	print("verbose:", config['CONTROL']['verbose'])
	print("showthresh:", config['CONTROL']['showthresh'])
	print("margin:",config['CONTROL']['margin'])
	return None

def licence():
  print("""
This program comes with absolutely no warranty. This is libre/gratis software,
and you are welcome to redistribute it under certain conditions.
    """)
  time.sleep(3)
  print("""

      stellarPYL is copyright (c) 2015 Brunston Poon

                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

  THE REST OF THE LICENCE TEXT IS VIEWABLE IN LICENCE.txt
  stellarPYL is copyright (c) 2015 Brunston Poon.
    """)

  return None

def jellyfish():
	print("""
                
                                        (hello!)
                                      .'
                                     '
                      _ -- ~~~ -- _      _______
                  .-~               ~-.{__-----. :
                /                       \      | |
               :         O     O         :     | |
               /\                       /------' j
              { {/~-.      \__/      .-~\~~~~~~~~~
               \/ /  |~:- .___. -.~\  \  \.
              / /\ \ | | { { \ \  } }  \  \.
             { {   \ \ |  \ \  \ \ /    } }
              \ \   /\ \   \ \  /\ \   { {
               } } { { \ \  \ \/ / \ \  \ \.
              / /   } }  \ \ }{ {    \ \ } }
             / /   { {     \ \{\ \    } { {
            / /     } }     } } \  / / \ \ \.
           `-'     { {     `-'\ \`-'/ /   `-'
                    `-'        `-' `-'

                    unknown artist
                """)
	return "jellyfish"