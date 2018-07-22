# Global Positioning using Aruco Markers

The plan is to equip LoEV3go with global positioning using Aruco markers placed
around the canvas on which LoEV3go is drawing, as sketched here:

<img align="center" src="arucoloc-idea.png"/>

LoEV3go would start by turning around, perhaps moving to two locations,
taking e.g. 12--20 pictures and creating the map with Marker Mapper. Then at
runtime, LoEV3go would regularly take a
picture, run Aruco tools to find its true location based on the markers it sees
at
the moment and apply any necessary small movements to hopefully move to the
real location given its assumed location.

## Steps Needed

- Webcam running on EV3 [done]
- Webcam calibrated
- Aruco and MarkerMapper compiled on EV3 [in process]
- MarkerMapper speed tested on EV3
- Using MarkerMapper to create the map. [done]
- Using Aruco to find camera position given a new picture [done]
- Physical layout of markers around the canvas, number of pictures needed for
  the map.
- LoEV3go integration
  - Consider storing more pictures and re-generating the map as more are collected, could be useful esp. in corners.

## Webcam Calibration

[OpenCV Interactive calibration](https://docs.opencv.org/3.4.1/d7/d21/tutorial_interactive_calibration.html)

...except I don't understand where the actual application is in opencv.

## Aruco and MarkerMapper on EV3

Download Aruco and MarkerMapper:
- https://sourceforge.net/projects/aruco/files/?source=navbar
- https://sourceforge.net/projects/markermapper/files/?source=navbar

Compile and install Aruco without root access:

```bash
cd aruco
mkdir build
cd build
mkdir -p $HOME/opt/
cmake -DCMAKE_INSTALL_PREFIX:PATH=$HOME/opt/aruco-3.0.11 ..
make
make install
```

**Minor fix needed in Aruco**: replace ``#endifxx`` with ``#endif`` in
``aruco-3.0.11/utils_calibration/dirreader.h``, line 1168.


Compile MarkerMapper:

```bash
cd markermapper
mkdir build
cd build
export aruco_DIR=/home/bojar/opt/aruco-3.0.11/
cmake ..
make
```

**Minor fix needed in MarkerMapper**: Replace:
```C
  auto p2=center+vp*markersize/2;
```
with
```C
  auto p2=center+markersize/2 * vp;
```
in ``marker_mapper1.0.12/utils/sglviewer.h``, line 68.

## Creating Marker Map

Following [MarkerMapper Usage Instructions](http://www.uco.es/investiga/grupos/ava/node/57), I ran the following on the suggested [example dataset](https://sourceforge.net/projects/markermapper/files/test_data/).

```bash
marker_mapper1.0.12/build/utils/mapper_from_images \
  sample_markers_test sample_markers_test/cam.yml 0.123 ARUCO out
```

Args:
- ``sample_markers`` is the directory with images
- ``cam.yml`` is the camera calibration file.
- 0.123 is the physical size of the markers in whichever unit, here meters
- ``ARUCO`` is the dictionary of markers used
- ``out`` is the prefix for output files

A file called ``out.yml`` will be created, this is what we need and we will
call it ``marker_map.yml`` in the following.

The ``out.log`` reports camera locations for each used image in the format
described under [Ground Truth Trajectories](https://vision.in.tum.de/data/datasets/rgbd-dataset/file_formats).
I still need to figure out how to get the robot heading angle from the unit
quaternion notation but the location is straightforward.

One can hack the ``out.yml`` map and add fake markers to indicate the positions of the camera for each of the image.

## Using Aruco to Locate the Robot Given Marker Map

I simplified ``aruco/utils_markermap/aruco_test_markermap.cpp`` into ``aruco_locate_one.cpp`` for my needs.

```bash
../aruco_locate_one sample-with-markers.jpg marker_map.yml cam.yml -save sample-with-markers.annotated.jpg
```

This will emit the location of the camera and optionally the picture annotated
with the known markers found in it.

TODO: Consider adding ``-server`` mode in which it would listen to stdin and
for ever newline, read the camera picture again (from camera or a given
filename) to save some initialization time, if that time is significant.

## Camera Calibration

All the following is done in the subdirectory ``camera-calibration/``.

1. Print ``printed_pattern_chessboard.png`` on A4 sheet.
2. Run ``./calibrate-with-chessboard.py`` and show the sheet to the camera several times (10 by default).

When the calibration says "Calibrated", you will have a file ``calibration.yaml`` in the current directory.

Older description and boards to print:

https://docs.opencv.org/3.3.1/da/d13/tutorial_aruco_calibration.html

https://docs.opencv.org/3.1.0/df/d4a/tutorial_charuco_detection.html

https://longervision.github.io/2017/03/16/OpenCV/opencv-internal-calibration-chessboard/

https://longervision.github.io/2017/03/12/OpenCV/opencv-external-posture-estimation-ArUco-board/

## Thoughts on LoEV3go Global Positioning

- LoEV3go has to be aware of its assumed global position
  - Every LOGO command has to update the assumed position and heading.
- Take a picture only every once a while, e.g. between two LOGO commands after
  5 seconds or 3 rotation commands, whichever comes first.
- Store the assumed global position and heading when the picture was taken.
- Run subsequent LOGO commands while processing the picture, record the
  (assumed) displacement in position and heading since the picture was taken.
- Once location is calculated from the camera, compare it with the stored
  assumed global position and heading. Record the necessary adjustment.
- Modify the adjustment as if the adjustment was calculated after the
  additional LOGO commands we ran in the meantime.
- Fiddle with the next ``forward`` or ``backward`` command, surrounding it with
  rotations before and after to carry out the adjustment -- to go to a slightly
  different position, which should be the globally correct one, and to have a
  slightly different heading afterwards, which should be the globally correct
  one.

