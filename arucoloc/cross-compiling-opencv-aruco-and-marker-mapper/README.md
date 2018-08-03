# Cross-Compiling OpenCV, Aruco and MarkerMapper for EV3

EV3 is **slow** and it has tiny memory. The only way that seems plausible is to cross-compile both tools for it. Here is how.

## Get ARM Linux Cross-Compiler

More details: https://www.acmesystems.it/arm9_toolchain

Get the tools:

```bash
sudo apt-get install libc6-armel-cross libc6-dev-armel-cross
sudo apt-get install binutils-arm-linux-gnueabi binutils-arm-linux-gnueabi
sudo apt-get install libncurses5-dev
sudo apt-get install gcc-arm-linux-gnueabi g++-arm-linux-gnueabi
sudo apt-get install cmake # will be needed shortly
```

Compile hello-world:

```bash
arm-linux-gnueabi-gcc hello.c -o hello
```

Copy to robot and run. This hello world app worked!


# Environment of Your Computer and EV3

I have a messy setup with various packages in various places. It would be probably better to put things somewhere nicely organized, e.g.:

```bash
mkdir sources
mkdir compiled-for-robot
```


# Cross-Compiling OpenCV

Get opencv sources:
  https://docs.opencv.org/3.4/d7/d9f/tutorial_linux_install.html

I used ``opencv-2.4.13.6``:

```bash
cd sources
wget https://github.com/opencv/opencv/archive/2.4.13.6.zip
unzip 2.4.13.6.zip
```


Patch cmake configs to use ``arm-linux-gnueabi-gcc`` and
``arm-linux-gnueabi-g++``:

```bash
patch -p 0 < opencv-2.4.13.6.patch
```

Build without GUI and 1394 camera support (these did not compile for me and I
don't need them):

```bash
cd opencv-2.4.13.6
mkdir build
cd build
cmake -DWITH_QT=OFF -DWITH_GTK=OFF -DWITH_1394=OFF \
  -DCMAKE_INSTALL_PREFIX:PATH=...full.path.to...compiled-for-robot/opencv \
  ..
make -j3
make install
```

# Cross-Compiling Aruco and MarkerMapper

The best documentation of Aruco and MarkerMapper is here:
- https://docs.google.com/document/d/1QU9KoBtjSM2kF6ITOjQ76xqL7H0TEtXriJX5kwi9Kgc/edit#heading=h.sxfg1jh7nibb
- I downloaded it as PDF here: ``ArUco_Library_Documentation.pdf``

Download Aruco and MarkerMapper:
- https://sourceforge.net/projects/aruco/files/?source=navbar
- https://sourceforge.net/projects/markermapper/files/?source=navbar


```bash
cd sources
# now obtain aruco-3.0.11.zip and marker_mapper1.0.12.zip
unzip aruco-3.0.11.zip
unzip marker_mapper1.0.12.zip
# patch both packages for my needs
patch -p 0 < ../aruco-3.0.11.patch
patch -p 0 < marker_mapper1.0.12.patch
# compile and install aruco to ~/opt/aruco-3.0.11
cd aruco-3.0.11
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=...full.path.to...compiled-for-robot/aruco
make
make install
cd ..
###### the rest has not been checked yet
# compile markermapper
cd marker_mapper1.0.12
mkdir build
cd build
export aruco_DIR=$HOME/opt/aruco-3.0.11/
cmake ..
make
```

