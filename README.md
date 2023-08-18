# NodeWall
### Graffiti Wall for BPQ
---
[MIT License](https://opensource.org/license/mit/)

NodeWall is a Graffiti Wall for Packet Radio.  It's made to work with the [BPQ32 Packet Switch from G8BPQ](https://www.cantab.net/users/john.wiseman/Documents/BPQ32.html).  It requires that you have a basic Python3 install which most everyone should who runs modern Linux.

NodeWall when running on your packet system will look like this:
```
*** Connected to WALL        
-=- Node Wall -=-

Showing entries 1-10 of 32:
(16-Aug 00:10) < PD1NL > I'm using Windows so i can see through walls
(15-Aug 09:32) < WW6Q > Just making my wall rounds.... carry on
(14-Aug 03:27) < AG7BI > This is cool! Have to add it to my node
(13-Aug 07:38) < PE1RRR > @BCX <3 thanks for the msg do you have a twitch channel?
(13-Aug 04:50) < YD0BCX-15 > Just passing by while streaming to twicth xixi
(12-Aug 16:15) < PE1RRR > @M0JQQ Thx for visiting, Robin :D Condx on 40 lately have been transient & turbulent!
(12-Aug 09:15) < M0JQQ > Morning Red. Yr mail received. This via MM3NDH. No connect via GB7IOW this morning. Will try later 73
(11-Aug 08:15) < WW6Q > Yes, this is where you share your kitty wittys.
(11-Aug 06:21) < EI2GYB > is this where i write somthing witty?
(06-Aug 22:04) < WW6Q > i tot i taw a puddy tat.

[P]ost a message [B]ack [F]orward [D]elete E[x]it
```

## Installation
Download and install NodeWall to your system:
```
git clone https://github.com/juniberry/NodeWall.git
```

Configure BPQ to connect to external application ports[^1]:
```
; Telnet Port
PORT
PORTNUM=15
 ID=Telnet
 DRIVER=TELNET
 ; ... etc ...
 CONFIG
  ; external application ports, zero indexed!
  CMDPORT=6000 6001 6002 6003 6004 6005 6006 6007 6008 6009 6010
ENDPORT

; Application Lines
APPLICATION 1,BBS,,N0CALL-1,CALBBS,255
APPLICATION 3,CHAT,,N0CALL-11,CALCHT,255

; External Applications
APPLICATION 10,WALL,C 15 HOST 1 S,N0CALL-14,CALWAL,255
```
Note: CMDPORT= ports are zero indexed, such that "C 15 HOST 1 S" will connect to port 15 (Telnet) in the example config, and then connect to local host on command port 1 which is the second port 6001 in the CMDPORT= list. **The "S" in the connect string is needed so that BPQ passes the users Callsign to NodeWall.**

You can run NodeWall from inet.d or xinet.d as a TCP service[^2]:
```
service wall
{
	disable		= no
	protocol	= tcp
	port		= 6001
	server		= /home/bpquser/wall.py
	user		= bpquser
	socket_type	= stream
	wait		= no
}
```

---
[^1]: [LinBPQ Applications Interface](https://www.cantab.net/users/john.wiseman/Documents/LinBPQ%20Applications%20Interface.html)
[^2]: [xinet.d](https://en.wikipedia.org/wiki/Xinetd)