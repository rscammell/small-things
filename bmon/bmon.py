#!/usr/bin/python
# bmon.py version 2.0
# (C) 2001-2002 Rupert Scammell <rupe@arrow.yak.net>
# GNU General Public License.
# 2001-09-24 / Written on a 747 over the Pacific Ocean :)
# 2002-04-23 / Additions and updates
# 
# Description:
# bmon grabs battery usage data from /proc/apm, and writes it to
# a file in two column format.  The first column is the current 
# battery charge in %, and the second is the (estimated) number 
# of minutes remaining.
# The info in the file can be graphed using a system such as Gnuplot,
# which may permit users to gain a better understanding of how their
# system uses the battery under a given process load.
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

import os, sys, string, time, re

# Global variables:
# Interval between sampling (seconds):
sample_int = 10
 
dfile = '/tmp/bat_data'


# Group 2 = battery %
# Group 4 = time remaining

apm_cap = re.compile("(.*) ([0-9]+)(\% )([0-9]+)(.*)")

data_file = open(dfile,"w")
print 'Collecting battery usage data to %s ...' % dfile
while 1:
	apm_f = open("/proc/apm","r")
	fline = str(apm_f.readlines())
	print fline
	if (apm_cap.search(fline) != None):
		b_p = apm_cap.search(fline).group(2)
		t_r = apm_cap.search(fline).group(4)
		print time.time()
		print "%s percent , %s minutes remaining" % (b_p, t_r)
		dfile_preproc = b_p + " " + t_r +  "\n"
		data_file.write(dfile_preproc)
		data_file.flush()

	apm_f.close()
	time.sleep(sample_int)