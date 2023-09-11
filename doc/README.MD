# Python Electronic Table Saw Fence

## Introduction
Heavily influenced by:
* xx
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

## Assumptions
*   TODO: The working side of the fence is always to the left - this is needed to simplify the backlash compensation (i.e. it only needs to compensate on one side)


## Resources
*   Timing belt calculator (https://www.technobotsonline.com/timing-pulley-distance-between-centres-calculator.html)
*   Stepper driver https://www.omc-stepperonline.com/download/DM556T.pdf
