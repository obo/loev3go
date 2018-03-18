# Lego: Random Ideas and Tools for EV3 Brick Running ev3dev Linux

This repository stores my personal experiments with ev3 brick running ev3dev
linux. Most of it is not sufficiently general but it may still serve as a
source of ideas for others.

The files ``.history-*`` are my local bash histories, for finding how I ran
what.

## Basic Commands

ssh robot@ev3dev.local
# heslo maker
python3
ev3.Sound.speak('Welcome!').wait()
m = ev3.LargeMotor('outB')
m.run_timed(time_sp=1000,speed_sp=500)

## Interesting Ideas from ev3dev Python Demos

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
