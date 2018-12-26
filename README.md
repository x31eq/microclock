## Binary clock for BBC micro:bit

I wrote this for my own amusement.  It shows a binary clock
on a BBC micro:bit.  You can set it from a serial console
or another micro:bit acting as a server.  There are a few
different modes (on button A) including a thermometer.

There are more things I could do to it but I probably won't.
It isn't a very good clock because it doesn't keep very good
time.  There's a test script that doesn't work now.

To install it, something like 
```
pip install uflash
pip install microfs
uflash stub.py /media/sdb
ufs put clock.py
```

The idea is that you can flash updated scripts without
copying a new firmware every time.

The clock format is based on <http://x31eq.com/clock.html>.
