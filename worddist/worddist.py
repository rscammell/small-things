#!/usr/bin/python
# worddist.py 1.0
# (C) 2001-2002 Rupert Scammell
# GNU General Public License.
#
# Description:
# worddist takes a text file as input, and generates word frequency histogram
# data, and stores it within a hash table inside a pickle file.  Words
# encountered are used as keys, with the individual frequency of occurence
# as values.

# Usage example:
# python worddist.py textfile_input.txt picklefile_output
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

import sys, string, re, fileinput, pickle

infile = sys.argv[1]
outfile = sys.argv[2]
dfile = open(outfile, 'w')
pickle_file = pickle.Pickler(dfile)

f_hash = {}
from_list = '!@#$%^&*()_-=+[]\|:;\'",.><?/'
to_list = ''
for i in range(len(from_list)):
	to_list = to_list + ' '
ttbl = string.maketrans(from_list, to_list)

for line in fileinput.input([infile]):
	line_tok = string.split(line)
	for i in range(len(line_tok)):
		lt = string.translate(line_tok[i], ttbl)

		if (f_hash.has_key(lt) == 1):
			f_hash[lt] = f_hash[lt] + 1 
		if (f_hash.has_key(line_tok[i]) == 0):
			f_hash[lt] = 0
		print lt, f_hash[lt]


pickle_file.dump(f_hash)
dfile.close()
