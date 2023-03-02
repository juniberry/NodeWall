# NodeWall
BBS Style Graffiti Wall made for BPQ Application

I put this together for my BPQ Node.  It runs from xinet.d, I've included the xinet.d file....and yeah, here is how you should configure it in bpq32.conf.

bpq32.conf appl line:
APPLICATION 10,WALL,C 15 HOST 1 S

Where 15 is your Telnet port and 1 is the port number (zero indexed) from the following list:
CMDPORT=6000 6001 6002 6003 6004

which would be port 6001 and you can define this in the CONFIG pragma of the Telnet PORT definition.


Enjoy!

