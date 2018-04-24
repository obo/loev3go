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
  sudo /sbin/route add default gw 169.254.214.1
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

## Taking pictured from camera

streamer -f jpeg -o image.jpeg

## Recording sound through USB camera

arecord -D plughw:1,0 -t wav --duration=5 test.wav
... worked out of the box

http://ofalcao.pt/blog/2017/lego-voice-control-ev3


## OpenCV links

https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
