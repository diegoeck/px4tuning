# px4tuning

Data-driven controller tuning for UAV firmware PX4

## Description

This Python Toolbox provides commands to design feedback controllers using the method Virtual Reference Feedback Tuning for the PX4 Firmware.
The algorithms compute automatically PID gains for Pitch Rate, Roll Rate, Yaw Rate, Pitch Angle, Roll Angle and Yaw Angle.

## Install:

Use PIP to install:

```bash
pip instal px4tuning
```

## Use:

The toolbox provides a bash interface to directly compute the gains using the *log file*:

```bash
px4att file.ulg --plot
```

## Contributors

Diego Eckhard - diegoeck@ufrgs.br - @diegoeck
