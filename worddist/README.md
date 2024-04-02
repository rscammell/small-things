# worddist

**Written in Python 2 in 2001-2002. Unmaintained since then, but presented here for historic interest and potential usefulness. **

worddist takes a text file as input, and generates word frequency histogram data, and stores it within a hash table inside a pickle file. Words encountered are used as keys, with the individual frequency of occurence as values.

Usage example:
```
python worddist.py textfile_input.txt picklefile_output
```
