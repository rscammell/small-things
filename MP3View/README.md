# MP3View

**Written in Python 2 in 2001. Unmaintained since then, but presented here for historic interest and potential usefulness. **

MP3View is a Python application to display and play MP3 files from a playlist, using a [Cybiko PDA](https://en.wikipedia.org/wiki/Cybiko), or any VT100/TTY terminal. MP3View 2.0 has the capability to play sound cues when the application is started, stopped, or encounters a problem. 
The program has several dependencies for operation, specifically [mpg123](https://mpg123.de/) for MP3 decoding, [aumix](https://web.archive.org/web/20160621151434/http://www.jpj.net/~trevor/aumix.html) for volume control and mixing, and [dreamplay](https://sourceforge.net/projects/dreamplay/) for WAV file playback. If desired, these programs could be substituted for modern equivalents fairly easily. Paths to these dependencies are specified within the script.

Running in a small dimension terminal like a Cybiko, MP3View looks like this:

```
CyMP3 1.0----------------------
| > 01-Bohemian_Rhapsody.mp3
|   02-Another_one_bites_the_~
|   03-Killer_Queen.mp3
|   04-Fat_bottomed_girls.mp3
|   05-Bicycle_race.mp3
|   06-You_re_my_best_friend.~
|   07-Don_t_stop_me_now.mp3
|   08-Save_me.mp3
|   09-Crazy_little_thing_cal~
|   10-Somebody_to_love.mp3
|   11-Now_I_m_here.mp3
0/35 songs vol: 63 -----------
```

**Using MP3View**

    \n (Enter key) - Plays the selected song
    (space) - Selects the next song in the list
    = - Selects the previous song in the list
    1 - Goes forward 1 page in the list (11 songs)
    2 - Goes back 1 page in the list (11 songs)
    , - Lowers the volume 3 levels using aumix
    . - Raises the volume 3 levels using aumix
    q - Quits the program 

**Starting and Stopping MP3View**

There are two variants of MP3View. mp3view2 is designed to run in a small dimension terminal of 32x13. mp3view2.1-console is designed to run on a standard 80x24 TTY or VT100 terminal, using the same interface
To start MP3View, run the appropriate script with python, and provide the name of the playlist file that you wish to use, e.g.

```python mp3view2.py playlist.txt```

To exit, type 'q'. Don't Ctrl-C the application, as doing so will leave the terminal in a state where characters are not echoed back to the terminal. If this happens, type 'reset' (blindly) and hit Enter... this should fix the problem. Hitting 'q' to quit does this for you. 