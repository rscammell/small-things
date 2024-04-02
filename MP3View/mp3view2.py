#!/usr/bin/python
# ----------------------------------------------------
# A console based MP3 playlist system.
# http://hobbiton.thisside.net/mp3view
# Author: Rupert Scammell (rupe@sbcglobal.net)
# 2001-04-09
# Version history:
# 1.0 - 2001-03-21 - Initial version.  Many bugs.
# 2.0 - 2001-04-09 - Modularize code.  Change c_vol
# (default starting volume) to be 110 rather than 63.
# Modularize some functions.
# Add speech cues for startup, shutdown, and problems.
#
# 2004-06-01: Update website and contact information,
# but don't increment the version.
#
# MP3View is made available under the GNU General Public License:
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
# ----------------------------------------------------
#
# Program notes:
# This script is designed for use with a 32 col, 13
# line terminal (4x6 font on the VTTerm terminal
# on the Cybiko).  MP3 names are displayed as 26 chars,
# after the removal of path information.
# The playlist format simply consists of a CR separated list
# of filenames (find /home/foo/mp3dir/ -print > playlist).
#
# mp3_loc, aumix_loc, and dreamplay_loc contain the locations 
# of mpg123, aumix, and dreamplay (a wav file player).
# Both mpg123 and aumix are required, and dreamplay (or 
# another wav file player) are needed to play speech cues.
# Modify these variables appropriately for your environment.
# -------------------------------------------------------

import os, sys, string, thread, termios, TERMIOS, re, time

# Read all of the filenames from a playlist file.
# Input: playlist filename (string)
# Output: playlist (list)

# Some nice global variables:

# Set to 1 to run with sound cues:
dreamplay_active = 1

playlist_len = 0
block_start = 0
block_end = 13
cursor_pos = 0
a = [] # the playlist
c = '' # Keypress character
c_vol = 110 
nx = None

mp3_loc = "/usr/bin/mpg123 -q "
aumix_loc = "/usr/bin/aumix -v "
dreamplay_loc = "/usr/bin/dreamplay "
soundfile_loc = "/home/rupe/car-sounds/"
path_strip = re.compile(r"^(.*)/([^/]+)")

# Define a hash table that maps events to sound filenames:
sndtbl = {}
sndtbl["on"] = dreamplay_loc + soundfile_loc + "mp3software2.wav"
sndtbl["off"] = dreamplay_loc + soundfile_loc + "mp3softwaredeact.wav"
sndtbl["problem"] = dreamplay_loc + soundfile_loc + "mp3problems.wav"
sndtbl["randomplay"] = dreamplay_loc + soundfile_loc + "randomplay2.wav"
sndtbl["seqplay"] = dreamplay_loc + soundfile_loc + "mp3sequential3.wav"

# Set the volume to level vol, using a call to the aumix program.

def volume(vol):
	volcom = aumix_loc + str(vol)
	os.system(volcom)

# Play a sound, using a prebuilt command from the sndtbl hash.

def sndplay(event):
	global sndtbl
	if (dreamplay_active == 1):
		killsound()
		time.sleep(1)
		volume(c_vol)
		os.system(sndtbl[event])

# Hack to kill any playing mp3 files.

def killsound():
	os.system("killall -9 mpg123 2&>1 /dev/null")

# Load the initial playlist into a list in memory.
 
def load_playlist(pfile):
	p_h = open(pfile,"r")
	for line in p_h.readlines():
		# Do a bit of formatting with the line we get back.
		# Assume 4x6 font on the VTTerm app for the Cybiko head
		# end that we're using.
		# Format is | > blah blah blah.mp3 with maxlen 30
		# So effective length of any filename is 26 chars.
		songname = string.strip(line)
		a.append(songname)
	return a

# Start a new thread with mpg123 to play a selected MP3.

def play_mp3(song):
	# Bad hack to make sure no other songs are playing...
        killsound()	
	command = mp3_loc + "\"" + string.strip(song) + "\"" + " 2&>1 /dev/null"
	cl = command,
	thread.start_new_thread(os.system,cl)


# Draw the interface window, given a playlist range, and cursor location.		
def draw_screen(cursor_pos, block_start, block_end):
	bs = block_start
	print "CyMP3 1.0" + "-"*22
	while (bs != block_end):
		ret = path_strip.search(a[bs])
		if (ret != nx):
			filename = str(ret.group(2))
		if (ret == nx):
			filename = a[bs]
		
		if (len(filename) > 26):
			filename = filename[:25] + "~"
		if (bs == cursor_pos):
			draw_line = "| > " + str(filename)
			print string.strip(draw_line)
		if (bs != cursor_pos):
			draw_line = "|   " + str(filename)
			print string.strip(draw_line)
		bs = bs + 1
	diff = block_end - block_start
	if (diff < 11):
		while (diff < 11):
			print "|  "
			diff = diff + 1	
	print str(cursor_pos) + "/" + str(len(a))+ " songs vol: " + str(c_vol) +" " + "-"*11

# Keypress catching code by Andrew Kuchling:
def event_handler():
	global cursor_pos
	global block_start
	global block_end
	global c_vol
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
	new[6][TERMIOS.VMIN] = 1
	new[6][TERMIOS.VTIME] = 0
	termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
	while 1:
		#print 'starting keypress capture.'
		c = os.read(fd, 1)
		if (c != ''):
			if (c == '\n'):
				mp3list=a[cursor_pos],
				thread.start_new_thread(play_mp3,mp3list)
			if (c == 'q'):
				# Announce shutdown
				sndplay("off")
				os.system("reset")
				sys.exit(1)
			
			if (c == ' '):
				# Are we at the end of the playlist?
				# If not, we can move...	
				if (cursor_pos != len(a)):
				# If we're just moving within the current block
				# simply move the cursor without changing the
				# displayed block of songs.

					if (cursor_pos != block_end):
						cursor_pos = cursor_pos + 1
						draw_screen(cursor_pos,block_start, block_end)
						moved = 1
				# Are we at the bottom of the current 
				# block of songs?
					if (cursor_pos == block_end and moved != 1):
						block_start = block_start + 1
						block_end = block_end + 1
						cursor_pos = cursor_pos + 1
						draw_screen(cursor_pos, block_start, block_end)
					moved = 0

					
								
			if (c == '='):
				# Are we at the top of the playlist?
				# If not, we can move...
				if (cursor_pos != 0):
			# Are we at the top of the current block of
				# songs? If not, just move within the block. 
					if (cursor_pos != block_start):
						cursor_pos = cursor_pos - 1
						draw_screen(cursor_pos, block_start, block_end)
						moved = 1
					
					# If we haven't moved already, 
					# move the cursor and the block.
					if (cursor_pos == block_start and moved != 1):
						cursor_pos = cursor_pos - 1
						block_start = block_start - 1
						block_end = block_end - 1
						draw_screen(cursor_pos, block_start, block_end)
					moved = 0	
			if (c == ','):
				# Move the main volume down 3 notches.
				c_vol = c_vol - 3
				volume(c_vol)

			if (c == '.'):
				# Move the main volume up 3 notches.
				c_vol = c_vol + 3
				volume(c_vol)

			if (c == '1'):
				# Move down 11 songs (one screen).
				move_inc = 11
				# If we're less than a screen away
				# from the bottom, just go there.
				if (len(a) - block_end < 11):
					move_inc = len(a) - block_end
				block_start = block_start + move_inc
				block_end = block_end + move_inc
				cursor_pos = cursor_pos + move_inc
				draw_screen(cursor_pos, block_start, block_end)

			if (c == '2'):
				# Move up 11 songs (one screen).
				move_inc = 11
				# If we're less than a screen from the top
				# just go there.
				if (block_start < 11):
					move_inc = block_start
				block_start = block_start - move_inc
				block_end = block_end - move_inc
				cursor_pos = cursor_pos - move_inc
				draw_screen(cursor_pos, block_start, block_end)

# Set the volume to c_vol:
# Announce that the software was started.
sndplay("on")

# Turn the volume down to the default, c_vol (usually 80)
volume(c_vol)
	
load_playlist(sys.argv[1])
block_start = 0 # Start of the playlist
block_end = len(a) # Length of the playlist
# Truncate to 11 songs if there are more than that in the playlist...
if (block_end > 11):
	block_end = 11

# Do the initial draw.
draw_screen(cursor_pos,block_start,block_end)

# Start event handler.
try:
	event_handler()
except IndexError:
	print "\n\nA problem occurred.  Terminating application.\n\n"
	os.system("reset")
	sndplay("problem")	
