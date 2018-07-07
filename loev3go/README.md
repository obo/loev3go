<img align="right" src="loev3go.svg"/>

# LoEV3go: A LOGO language interpreter for LEGO EV3 robot

This LOGO interpreter is based on the pylogo. It runs on the EV3 brick
(under Linux, EV3DEV) and on the outside, it looks as a:

- IR-controlled turtle (pacifists don't play with tanks, do they)
  - with two felt-tip pens (switchable with the beacon button)
- Web server for entering a LOGO program
  - Once confirmed, the robot turtle will draw the LOGO program on the <s>carpet</s>canvas underneath.

## TODO

The robot could have "security" feature: the LOGO program will stop immediately
when the color sensor does not see enough white or when the touch sensor hits
something. Obviously, you can still damage your floor if the turtle runs
backwards...


## 2018-05-25 Navrh zastavitelneho weboveho interpretru loga

- webserver:
  - stale nabizi kod k editaci
  - stale nabizi "Test draw", kdy to nakresli a vrati jako obrazek
  - kdyz nebezi vlakno malovani, nabizi "Test run" (bez pera) a "Real run" (s
    perem)
  - kdyz bezi vlakno, tak to naopak nabizi jen "Stop current program"
  - tlacitko na robotovi udela taky stop
  - kdyz vyjede mimo bile, tak to taky stopne
  - infra se da jezdit nezavisle, ale smysl to ma jen, kdyz nebezi program
