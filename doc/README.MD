# Python Electronic Table Saw Fence

## Introduction
Heavily influenced by:
* https://www.airspayce.com/mikem/arduino/AccelStepper/ stepper library, the micro-python port of the C library was from here https://github.com/pedromneto97/AccelStepper-MicroPython - my huge thanks to the respective authors both for their work and releasing the code.  I am as such releasing this code under a similar license.
* yy


## Design goals
* Minimise backlash by preloading the fence to ensure repeatable cuts
* Simple design from of shelf parts, available in the UK (i.e. without needing the larger market place of say the US)
* Python based to simplify community extension (vs Arduino which has a steeper learning curve)
* Rigid / accurate enough to support a commercial use scenario (at least from an accuracy perspective)
* Safe to use (inclusion of crash detection / eStop etc) - collision detection may be a stretch for v1

## Hardware used for v1
*   8080 aluminium extrusion
*   20mm linear guide rail (Vevor)
*   2.4Nm stepper, Nema 23
*   Mod1 rack / pinion (BearingBoys in the UK sell long lengths of the rack)
*   267-3M-15 HTD 3M Timing Belt (89 tooth
)

## Assumptions
*   TODO: The working side of the fence is always to the left - this is needed to simplify the backlash compensation (i.e. it only needs to compensate on one side)


## Resources
*   Timing belt calculator (https://www.technobotsonline.com/timing-pulley-distance-between-centres-calculator.html)
*   Stepper driver https://www.omc-stepperonline.com/download/DM556T.pdf
*   The original data used in the acceleration calcs https://www.embedded.com/generate-stepper-motor-speed-profiles-in-real-time/
*   How to debug remotely https://github.com/gloveboxes/Remote-debug-Python-on-Raspberry-Pi-from-Visual-Studio-Code
* Code (https://github.com/Robocraze/MPU6050) and blog (https://robocraze.com/blogs/post/mpu6050-accelerometer-tutorial.htmlhttps://robocraze.com/blogs/post/mpu6050-accelerometer-tutorial.html) for interfacing with the MPU6050


## Installation
*   On the raspberry pi, install tkinter: sudo apt-get install python3-tk
*   For osx install XQuartz: https://www.xquartz.org/
*   to debug: ssh -YX ip-address-here
*   to run: python3 main.py

If you want to remote develop, the following resources may be useful:
* https://jakemakes.eu/setting-up-sshfs-on-raspberry-pi/

