# Lego: Random Ideas and Tools for EV3 Brick Running ev3dev Linux

This repository stores my personal experiments with ev3 brick running ev3dev
linux. Most of it is not sufficiently general but it may still serve as a
source of ideas for others.

The files ``.history-*`` are my local bash histories, for finding how I ran
what.

## Connecting via Bluetooth

brickman:
Wireless->Bluetooth->scroll to my paired NB
Network Connection -> Connect
...Bluetooth icon gets green instead of white in Mate side panel
...but leads to GDBus.Error:net.connman.Error.Failed: Input/output error

Remove devices from both devices
Switch off both bluetooths.
Fire up brick BT, Make brick visible
Open BT devices on NB
Search
Click on ev3dev
Pair
Confirm pairing on both devices
Then scroll to NB-device in brickman
click Network Connection
click Connect (*not* connect directly)
On NB **CONFIRM**. The window gets often hidden somewhere, so this tends to timeout...
Brickman should go over Associating to Connecting to Connected



## Basic Commands

ssh robot@ev3dev.local
# heslo maker
python3
ev3.Sound.speak('Welcome!').wait()
m = ev3.LargeMotor('outB')
m.run_timed(time_sp=1000,speed_sp=500)


# upgrading only ev3dev-python:
sudo apt-get update
sudo apt-get install --only-upgrade python3-ev3dev

## Populating fresh robot card

git clone https://github.com/obo/lego.git
bash lego/environment/setup_environment.sh

## Interesting Ideas from ev3dev Python Demos

git clone https://github.com/ev3dev/ev3dev-lang-python-demo.git

ev3dev-lang-python-demo/robots/R3PTAR/r3ptar.py
... ukazuje vicevlaknovost
... cili tim by melo jit udelat rizeni a soucasne moznost zapnout sledovani cary

ev3dev-lang-python-demo/robots/EV3RSTORM/ev3rstorm.py
... zahrnuje kresleni na display! Cili tim by se dalo delat nejake malovani mapy, kudy projel

## Multipurpose Track3r Proposal

- vicevlaknova aplikace
- triggery na 4. kanalu IR pro ovladani nabidky
- tank na 1. kanalu
- pomalejsi tank na 2. kanalu
V nabidce:
- sleduj caru
  1. Rozhledne se vlevo a vpravo, tim pozna barvu cary a okoli, a taky tloustku cary.
  2. Vyrazi po care, zastavi na jakekoli jine barve nez cara nebo pozadi.


## Inspiring Youtube Videoss

http://www.mindcuber.com/mindcub3r/mindcub3r.html
http://www.mindcuber.com/mindcub3r/MindCub3r-v1p0.pdf


https://www.youtube.com/watch?v=JlWOKaxKrIE
...reptar a kocka

https://www.youtube.com/watch?v=uIPrN-b-Zb0
...spybot, dobry pasovy

https://www.youtube.com/watch?v=JOUGsgqYraE
...ruka

https://www.youtube.com/watch?v=bSmXZyNWm28
...tridic lentilek

https://www.youtube.com/watch?v=5VAhH7GUoks
...hledani veci

https://www.youtube.com/watch?v=cXgB3lIvPHI
...hraje na kytaru

https://www.youtube.com/watch?v=FCWNNk1G2UU
...had, slon

https://www.youtube.com/watch?v=6xCd55oSgO4
...hromska krabice

https://www.youtube.com/watch?v=dIgSKPzLC9g
...telegraf

https://www.youtube.com/watch?v=0d0ktACCwT4
...best of evdev

https://www.youtube.com/watch?v=LZYr646Ul4Q
...spirograph

## Other interesting links:

Camera: https://siyahodacom.wordpress.com/2017/10/01/adding-webcam-to-ev3-ev3dev/

Camera-based line tracking:
http://karandashsamodelkin.blogspot.cz/

Pixy-camera: http://www.ev3dev.org/docs/tutorials/using-pixy-camera/

lejos opencv face recognition:
http://thinkbricks.net/face-tracking-on-ev3-using-lejos-0-9-1/

https://github.com/Klabbedi/ev3
...a better line follower, PID algorithm
(but this will not work on red lines, because in reflected-light scanning, red led is used, so red is the same as white)

http://pazhong.net/code/number_detect/number_detect.py
... number detection and draw it on screen

https://github.com/dlech/ev3dev-photo-booth

and a similar tutorial in C++:
https://github.com/FrankBau/raspi-repo-manifest/wiki/OpenCV

http://www.ev3dev.org/docs/tutorials/using-ev3-lcd/

## Trying to get my old Logitech camera running

lsusb
Bus 001 Device 003: ID 046d:08ae Logitech, Inc. QuickCam for Notebooks

sudo hwinfo --usb
04: USB 00.0: 11200 TV Card
  [Created at usb.122]
  Unique ID: ADDn.elweGVRLXdD
  Parent ID: k4bc.BtRjRTLQ986
  SysFS ID: /devices/platform/ohci.0/usb1/1-1/1-1:1.0
  SysFS BusID: 1-1:1.0
  Hardware Class: tv card
  Model: "Logitech Camera"
  Hotplug: USB
  Vendor: usb 0x046d "Logitech, Inc."
  Device: usb 0x08ae "Camera"
  Revision: "1.00"
  Speed: 12 Mbps
  Module Alias: "usb:v046Dp08AEd0100dc00dsc00dp00icFFiscFFipFFin00"
  Driver Info #0:
    Driver Status: zc0301 is not active
    Driver Activation Cmd: "modprobe zc0301"
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #3 (Hub)

dmesg
[ 4957.057832] usb 1-1: USB disconnect, device number 2
[ 4968.794243] usb 1-1: new full-speed USB device number 3 using ohci
[ 4969.013560] usb 1-1: New USB device found, idVendor=046d, idProduct=08ae
[ 4969.013649] usb 1-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[ 4969.013705] usb 1-1: Product: Camera         

uname -r
4.4.87-22-ev3dev-ev3

The issue where I ask for help: https://github.com/ev3dev/ev3dev/issues/64

This is what could possibly help:
 I installed the kernel options: gspca (in v4l) and USB audio (in alsa USB devices) and then inserted the corresponding modules: zc3xx and snd_usb_audio. 


## Connecting via USB cable

There is a tutorial: http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/

But it didn't really work for me.

When brickman connected to wired connection and has shown me its IP address, I manually configured my NB for that network:

ifconfig enp0s20f0u3 169.254.214.1
 
ssh robot@169.254.214.149

On the robot:
  sudo ifconfig
  myip=$(sudo ifconfig | sed -n 's/.*inet \([0-9][0-9.]*\).*/\1/p' | grep -v 127.0.0.1)
  sudo /sbin/route add default gw $(echo $myip | cut -d. -f1-3).1
  echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf

And on my laptop: (this may have not been necessary, not sure)
echo 1 > /proc/sys/net/ipv4/ip_forward
sudo modprobe ip_tables
sudo modprobe ip_conntrack
sudo modprobe ip_conntrack_irc
sudo modprobe ip_conntrack_irc
sudo modprobe ip_conntrack_ftp
sudo iptables -t nat -A POSTROUTING -o wlp4s0 -j MASQUERADE
... to forward robot's network through my NB


### Still some problems:

[ 2540.370361] usb 1-1: new full-speed USB device number 2 using ohci-da8xx
[ 2540.643482] usb 1-1: New USB device found, idVendor=046d, idProduct=08ae
[ 2540.643546] usb 1-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[ 2540.643581] usb 1-1: Product: Camera         
[ 2542.272748] Linux video capture interface: v2.00
[ 2542.395353] gspca_main: v2.14.0 registered
[ 2542.471259] gspca_main: gspca_zc3xx-2.14.0 probing 046d:08ae
[ 2543.313943] input: gspca_zc3xx as /devices/platform/soc@1c00000/ohci-da8xx/usb1/1-1/input/input2
[ 2543.344797] usbcore: registered new interface driver gspca_zc3xx
[ 2544.366522] usbcore: registered new interface driver snd-usb-audio

robot@ev3dev:~/lego$ streamer -f jpeg -o image.jpeg
files / video: JPEG (JFIF) / audio: none
fifo max fill: audio 0/0, video 1/16, convert 1/16  


## Taking pictured from camera

streamer -f jpeg -o image.jpeg

## Recording sound through USB camera

arecord -D plughw:1,0 -t wav --duration=5 test.wav
... worked out of the box

http://ofalcao.pt/blog/2017/lego-voice-control-ev3


## OpenCV links

https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

https://thecodacus.com/opencv-object-tracking-colour-detection-python/#.WuB4pta-lUA

## Connecting via wifi

lsusb:
Bus 001 Device 003: ID 083a:4505 Accton Technology Corp. SMCWUSB-G 802.11bg

hwinfo --usb
07: USB 00.0: 0000 Unclassified device
  [Created at usb.122]
  Unique ID: lfzD.wkm1Arvlfj3
  Parent ID: ADDn._cOmnuCBvb4
  SysFS ID: /devices/platform/soc@1c00000/ohci-da8xx/usb1/1-1/1-1.1/1-1.1:1.0
  SysFS BusID: 1-1.1:1.0
  Hardware Class: unknown
  Model: "Accton SMCWUSB-G 802.11bg"
  Hotplug: USB
  Vendor: usb 0x083a "Accton"
  Device: usb 0x4505 "SMCWUSB-G 802.11bg"
  Revision: "48.10"
  Speed: 12 Mbps
  Module Alias: "usb:v083Ap4505d4810dcFFdscFFdpFFicFFisc00ip00in00"
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #8 (Hub)

ifconfig
usb1: flags=-28669<UP,BROADCAST,MULTICAST,DYNAMIC>  mtu 1500
        ether 22:16:53:5f:74:d2  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lsmod
Module                  Size  Used by
sr_mod                 12624  0
cdrom                  28732  1 sr_mod
snd_usb_audio         139864  0
snd_hwdep               5257  1 snd_usb_audio
snd_usbmidi_lib        19259  1 snd_usb_audio
snd_rawmidi            19974  1 snd_usbmidi_lib
snd_seq_device          4207  1 snd_rawmidi
gspca_zc3xx            41388  0
gspca_main             22080  1 gspca_zc3xx
v4l2_common             4978  1 gspca_main
videodev              127782  3 v4l2_common,gspca_zc3xx,gspca_main
iptable_nat             1728  0
nf_conntrack_ipv4       5927  1
nf_defrag_ipv4          1634  1 nf_conntrack_ipv4
nf_nat_ipv4             5140  1 iptable_nat
nf_nat                 14692  1 nf_nat_ipv4
nf_conntrack           87388  3 nf_conntrack_ipv4,nf_nat_ipv4,nf_nat
libcrc32c               1100  2 nf_conntrack,nf_nat
usb_f_rndis            15528  2
usb_f_ecm               6278  2
u_ether                12402  2 usb_f_ecm,usb_f_rndis
ev3_uart_sensor_ld      7767  2
ev3_uart_sensor        13506  1 ev3_uart_sensor_ld
nxt_i2c_sensor         35440  1 ev3_uart_sensor
servo_motor_class       6378  1 nxt_i2c_sensor
hci_uart               16410  0
serdev                  8117  1 hci_uart
suart_emu              23989  0
ev3_analog_sensor       5077  0
uinput                  8046  0
libcomposite           41550  16 usb_f_ecm,usb_f_rndis
configfs               28703  4 usb_f_ecm,usb_f_rndis,libcomposite
ip_tables              10235  1 iptable_nat
x_tables               19232  1 ip_tables


robot@ev3dev:~$ ev3dev-sysinfo -m
<!-- Copy everything between these lines -->
**System info (from `ev3dev-sysinfo`)**
```
Image file:         ev3dev-stretch-ev3-generic-2018-04-22
Kernel version:     4.14.35-ev3dev-2.0.0-ev3
Brickman:           0.10.0
ev3devKit:          0.5.2
Board:              board0
BOARD_INFO_HW_REV=8
BOARD_INFO_MODEL=LEGO MINDSTORMS EV3
BOARD_INFO_ROM_REV=6
BOARD_INFO_SERIAL_NUM=0016535F74D2
BOARD_INFO_TYPE=main
```
<!-- Copy everything between these lines -->


Brickman says Wifi: Not available


## connmanctl to connect to wifi:

http://www.ev3dev.org/docs/tutorials/setting-up-wifi-using-the-command-line/

## Mouse input?

ls /dev/input/by-id/
should say: usb-0461_USB_Optical_Mouse-event-mouse

Following mouse is implemented here:
follow_mouse:
  https://github.com/cavenel/ev3-print3rbot/blob/master/writer.py

## LCD

sudo openvt -s -w -- sudo --user <user> -- COMMAND
...this should allow me to run the COMMAND with access to the screen

https://sites.google.com/site/ev3python/learn_ev3_python/screen

My issue: https://github.com/ev3dev/ev3dev-lang-python/issues/463

## QR code reader:

https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/

http://aishack.in/tutorials/scanning-qr-codes-2/

https://gist.github.com/mohankumargupta/243aeb6787123cc17f1c10338bd4a82f
...this seems to be all combined into one script

## Simplest white balance:

https://gist.github.com/tomykaira/94472e9f4921ec2cf582
paper+code: http://www.ipol.im/pub/art/2011/llmps-scb/?utm_source=doi

## USB Camera button

https://unix.stackexchange.com/questions/398660/detecting-usb-camera-button-event

## Beacon Seeker

see random-bits/report-beacon-location.py

0 -128  ... means that no beacon is found
0 1     ... means that we are really really close

11 54   ... means that at "angle" 11, 54 "cm"

Note that it can't distinguish front and back, so we will have to realize that
when we try to roll towards but get further, we probably need to rotate...

Or put differently, we should first stabilize the angle and only then focus on the distance.

## Steering

steering3 doesn't work at all, ignores the change.

Course: 295.63783698408236 , Left: 40 , Right:  40.0
Course: 278.2177484737596 , Left: 40 , Right:  40.0
Course: 285.1530424270078 , Left: 40 , Right:  40.0
Course: 285.3336692939426 , Left: 40 , Right:  40.0
Course: 280.5610942447775 , Left: 40 , Right:  40.0
Course: 264.02855443500306 , Left: 40 , Right:  40.0
Course: 253.69647100177943 , Left: 40 , Right:  40.0
Course: 246.29642562886042 , Left: 40 , Right:  40.0
Course: 153.73717076689826 , Left: 40 , Right:  40.0
Course: 148.49593456078 , Left: 40 , Right:  40.0
Course: 160.43838775570993 , Left: 40 , Right:  40.0
Course: 203.88310612648385 , Left: 40 , Right:  40.0
Course: 162.86323496452164 , Left: 40 , Right:  40.0
Course: 118.7518368606886 , Left: 40 , Right:  40.0
Course: -27.32580003400672 , Left: -18.139359972794622 , Right:  40
Course: -193.01178484332874 , Left: 40.0 , Right:  40
Course: -208.61163282385814 , Left: 40.0 , Right:  40
Course: -199.13916193295287 , Left: 40.0 , Right:  40
Course: -167.95320071053493 , Left: 40.0 , Right:  40
Course: -145.75692942290914 , Left: 40.0 , Right:  40
Course: -150.46866580834674 , Left: 40.0 , Right:  40
Course: -166.23221224603807 , Left: 40.0 , Right:  40
Course: -172.32239497128228 , Left: 40.0 , Right:  40
Course: -206.31446988052232 , Left: 40.0 , Right:  40
Course: -235.97961153989553 , Left: 40.0 , Right:  40
Course: -229.70066500212323 , Left: 40.0 , Right:  40
Course: -213.9761825924693 , Left: 40.0 , Right:  40
Course: -203.31686643334615 , Left: 40.0 , Right:  40
Course: -193.18282078522884 , Left: 40.0 , Right:  40
Course: -184.6898381805486 , Left: 40.0 , Right:  40

## Testing new design of pen holder

>>> import ev3dev.ev3 as ev3
>>> from ev3dev.auto import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
>>> from ev3dev.helper import MediumMotor
>>> m=MediumMotor(OUTPUT_A)
>>> m.run_to_rel_pos(speed_sp=80, position_sp=-30, stop_action="hold")
...put pen
>>> m.run_to_rel_pos(speed_sp=80, position_sp=30, stop_action="hold")
...lift pen


