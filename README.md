# Astari Selah — 5-DOF Articulated Robotic Manipulator

A complete, production-grade robotics workspace unifying **ESP32 bare-metal embedded C++ firmware**, **ROS 2 Humble configurations**, and **mechanical 3D CAD assets** for a 5-DOF industrial manipulator with 550 mm reach and tactile FSR force sensing.

## Directory Structure & Subsystem Layout

```
astari_selah/
├── README.md                          # Master project documentation
├── docs/                              # System specifications and math derivations
│   ├── ARCHITECTURE.md                # System topology and ROS 2 <-> ESP32 division
│   ├── HARDWARE_SPECS.md              # Physical dimensions, link lengths, reach verification
│   ├── PINOUT_AND_WIRING.md           # Dual power distribution (XL4016/LM2596) and pin map
│   ├── KINEMATICS.md                  # Analytical D-H parameter tables and IK derivation
│   └── PROJECT_SPECS.md               # Slicing tolerances and pocket constraints
│
├── firmware/                          # ESP32 Bare-Metal Embedded C++ (PlatformIO)
│   ├── COLCON_IGNORE                  # Excludes firmware from ROS 2 colcon builds
│   ├── platformio.ini                 # PlatformIO project configuration (esp32dev)
│   ├── include/
│   │   ├── arm_config.h               # Hardware pinouts, joint limits, PWM timings
│   │   ├── kinematics.h               # Onboard analytical FK & IK solvers
│   │   ├── pca9685_driver.h           # 16-channel I2C PWM driver with trajectory ramping
│   │   ├── fsr_sensor.h               # FSR 402 pressure sensor analog filtering (EMA)
│   │   └── telemetry.h                # 50Hz serial protocol manager
│   ├── src/
│   │   ├── main.cpp                   # Deterministic 50Hz execution loop
│   │   ├── kinematics.cpp             # D-H mathematical implementation
│   │   ├── pca9685_driver.cpp         # Servo pulse width generation & interpolation
│   │   ├── fsr_sensor.cpp             # Analog ADC processing
│   │   └── telemetry.cpp              # ROS 2 serial packet serialization
│   └── test/
│       └── test_kinematics.cpp        # Standalone kinematics unit tests
│
├── ros2/                              # ROS 2 Packages & Middleware
│   └── astari_selah_description/      # Description package (ament_cmake)
│       ├── package.xml                # ROS 2 package manifest
│       ├── CMakeLists.txt             # Build instructions installing launch, urdf, meshes
│       ├── urdf/
│       │   ├── astari_selah.urdf.xacro# Master kinematic model (reach: 550mm)
│       │   ├── materials.xacro        # Visual color definitions matching CAD
│       │   └── astari_selah.gazebo.xacro # Gazebo physics properties
│       ├── meshes/
│       │   ├── visual/*.stl           # High-precision visual meshes for RViz
│       │   └── collision/*.stl        # Optimized collision geometry
│       ├── launch/
│       │   ├── display.launch.py      # RViz2 visualization with GUI joint sliders
│       │   └── hardware.launch.py     # Live hardware bridge execution
│       ├── rviz/
│       │   └── display.rviz           # Pre-configured RobotModel & TF layout
│       ├── scripts/
│       │   └── esp32_bridge.py        # 50Hz serial bridge node (ROS 2 <-> ESP32)
│       └── config/
│           └── joint_limits.yaml      # Software joint limits and velocity bounds
│
└── cad/                               # 3D Mechanical CAD & Modeling Subsystem
    ├── COLCON_IGNORE                  # Excludes CAD solids from ROS 2 colcon builds
    ├── assembly/
    │   ├── five_dof_arm_complete_assembly.step # Master 50+ part assembly STEP
    │   └── freecad_5dof.FCStd                  # FreeCAD native project
    ├── parts/                         # Structural 3D printed components
    │   ├── *.step                     # High-precision solid models
    │   └── *.stl                      # Slice-ready 3D printing meshes
    ├── components/
    │   └── *.step                     # COTS STEP files (servos, bearings, electronics)
    ├── fasteners/
    │   └── *.step                     # ISO/DIN fasteners (M3, M4, M8 screws, nuts)
    ├── scripts/
    │   └── generate_final_3d_model.py # CadQuery automated generation scripts
    └── manufacturing/
        └── MANUFACTURING_GUIDE.md     # Slicing parameters, filament selection, perimeters
```

## Quick Start Guide

### 1. Build and Run ROS 2 Visualization
From `/home/jeremiah/ros2_ws`:
```bash
colcon build --packages-select astari_selah_description
source install/setup.bash
ros2 launch astari_selah_description display.launch.py
```

### 2. Connect Live Hardware (ESP32)
```bash
ros2 launch astari_selah_description hardware.launch.py serial_port:=/dev/ttyUSB0
```

### 3. Flash ESP32 Firmware
```bash
cd src/astari_selah/firmware
pio run --target upload --upload-port /dev/ttyUSB0
```
