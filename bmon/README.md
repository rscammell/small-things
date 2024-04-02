# bmon

**Written in Python 2 in 2001-2002. Unmaintained since then, but presented here for historic interest and potential usefulness. **

bmon grabs battery usage data from /proc/apm, and writes it to a file in two column format. 

The first column is the current battery charge in %, and the second is the (estimated) number of minutes remaining. The info in the file can be graphed using a system such as Gnuplot, which may permit users to gain a better understanding of how their system uses the battery under a given process load.