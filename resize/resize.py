#!/usr/bin/python
# resize.py version 1.2
# (C) 2002 Rupert Scammell <rupe@sbcglobal.net>
# GNU General Public License.
# 2002-04-29 / 1.0 / Initial version.
# 2002-05-07 / 1.1 / Add some more verbosity, check for images to convert.
# 2002-05-08 / 1.2 / Smarter file extension handling, exclude non-image files.
#
# Description:
# A script to batch resize images, using the UNIX convert program,
# which ships as part of the ImageMagick image manipulation package.
# Currently, the program renames resized files numerically, in order
# of where they appear within a directory listing.  This helps to
# restore sanity to filenames mangled by Microsoft.  You may wish to
# change this if this behavior isn't what you want.
#
"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import os, sys, re

file_extension = re.compile("(.+)\.(.+)")

print '\nresize v1.1 - Batch image resizing utility.'
print '(C) 2002 Rupert Scammell <rupe@arrow.yak.net>'
print 'GNU General Public License.\n'


if (len(sys.argv) == 1):
	imdir = raw_input('Original image directory: ')
	rfactor = raw_input('Resize factor (%): ')
	odir = raw_input('Resized image output directory (%): ')
else:
	imdir = sys.argv[1]
	rfactor = sys.argv[2]
	odir = sys.argv[3]

print 'Getting file list from %s ...' % imdir
dirlist = os.listdir(imdir)
print dirlist
print '%i files found.' % len(dirlist)

# Make sure that there are actually files to work with.
if (len(dirlist) == 0):
	print 'Sorry, couldn\'t find any files to convert in %s .' % imdir
	sys.exit(1)

# Check to see if the convert utility exists on the system.
if (os.path.isfile('/usr/bin//convert') == 0):
	print 'Sorry, I couldn\'t locate the convert utility in /usr/bin/.'
	print 'The utility is provided as part of the ImageMagick package.'
	print 'See http://www.imagemagick.org/ for details.'
	sys.exit(1)

print 'Starting image conversion...'
for i in range(len(dirlist)):
        fex_handle = file_extension.search(dirlist[i])
        if (fex_handle != None):
	        cur_fex = '.' + fex_handle.group(2)
	else:
	        cur_fex = ''

	# Make sure we're not dealing with a dot file, or some other obvious non-image formats.
	if (dirlist[i][0] != '.' \
	and cur_fex != '.txt' \
	and cur_fex != '.tar' \
	and cur_fex != '.html' \
	and cur_fex != '.tar.gz' \
	and cur_fex != '.gz' \
	and cur_fex != '.mov' \
	and cur_fex != '.py' \
	and cur_fex != '.c' \
	and cur_fex != '.java' \
	and cur_fex != '.pdf' \
	and cur_fex != '.rpm' \
	and cur_fex != '.mp3' \
	and cur_fex != '.wav'):
		convert_command = '/usr/bin/convert -geometry ' \
				  + str(rfactor) + '% ' \
				  + os.path.join(imdir, dirlist[i]) +  \
				  ' ' + os.path.join(odir, str(i)) + cur_fex
		print 'Converting file %s (image %i of %i)' % (dirlist[i], i+1, len(dirlist))
		os.system(convert_command)

print 'Conversion complete. %i files converted. ' % len(dirlist)
