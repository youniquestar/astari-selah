# ESP32 Bare-Metal Firmware (PlatformIO)

Bare-metal C++ firmware for the 5-DOF industrial robotic arm manipulator running on the ESP32 base microcontroller.

## Overview
- **Kinematics Engine**: Onboard forward and inverse kinematics using Denavit-Hartenberg parameters.
- **Actuation**: PCA9685 16-channel I2C PWM controller running at 50Hz, with trajectory ramping to prevent high current surges and mechanical jerk.
- **Sensor Feedback**: 12-bit ADC reading and exponential moving average (EMA) filtering of the FSR 402 pressure sensor located in the recessed pocket of the left gripper jaw.
- **Telemetry Loop**: 50Hz cyclic timer streaming joint states and force data to ROS 2 over USB-Serial (115200 baud).

## Directory Structure
```
firmware/
├── platformio.ini       # PlatformIO project configuration (esp32dev)
├── include/
│   ├── arm_config.h     # Pinouts, link dimensions, joint limits, PWM timings
│   ├── kinematics.h     # FK & IK analytical math definitions
│   ├── pca9685_driver.h # PCA9685 I2C driver & trajectory ramp
│   ├── fsr_sensor.h     # FSR 402 pressure sensor filtering
│   └── telemetry.h      # Serial streaming & command protocol
├── src/
│   ├── main.cpp         # 50Hz main task & hardware timer loop
│   ├── kinematics.cpp   # Analytical FK/IK solver
│   ├── pca9685_driver.cpp
│   ├── fsr_sensor.cpp
│   └── telemetry.cpp
└── test/
    └── test_kinematics.cpp
```

## Flashing Instructions
With PlatformIO Core or the VSCode PlatformIO extension installed:

```bash
# Build firmware
pio run

# Flash to connected ESP32
pio run --target upload --upload-port /dev/ttyUSB0

# Open serial monitor
pio device monitor --port /dev/ttyUSB0 --baud 115200
```
