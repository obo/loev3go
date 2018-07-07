<img align="right" src="web/loev3go.svg"/>

# LoEV3go: A LOGO language interpreter for LEGO EV3 robot
Ondřej Bojar, bojar@ufal.mff.cuni.cz

This LOGO interpreter is based on [pylogo](http://pylogo.sourceforge.net/) ported to python3. It runs on the [EV3 intelligent brick](https://shop.lego.com/en-US/EV3-Intelligent-Brick-45500)
under Linux, [EV3DEV](http://ev3dev.org/). On the outside, it looks as a:

- IR-controlled turtle (pacifists don't play with tanks, do they).
  - with two felt-tip pens (switchable with the beacon button)
- Web server for entering a LOGO program.
  - After a preview, the robot turtle will draw the LOGO program on the <s>carpet</s> canvas underneath.

## Wishlist

- Precision, precision, precision. Obviously, precision is troublesome. I am now working on mousometry, but any global positioning is highly desirable.

- The robot could have "security" feature: the LOGO program will stop immediately
when the color sensor does not see enough white or when the touch sensor hits
something. Obviously, you can still damage your floor if the turtle runs
backwards...

- The robot could first scan the carpet to determine the white area and scale the image accordingly.

## Usage

(todo)

### Running without EV3 robot

### Using the web page

#### Preview, Scale, Dry Run, Draw

#### Loading and saving

#### Detailed settings
