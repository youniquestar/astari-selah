# 3D Mechanical CAD Subsystem — Astari Selah

This directory contains the physical CAD assemblies, structural components, standard fasteners, COTS electronics STEP models, and automated build scripts for the **Astari Selah** 5-DOF robotic manipulator.

## Directory Structure

All 3D models and mechanical assets are located directly within their respective functional directories under `cad/`:

```
cad/
├── assembly/
│   ├── Selah_Master.FCStd              # Master native FreeCAD document with complete group hierarchy
│   └── Selah_Assembly.step             # Master ISO-10303 STEP solid of entire manipulator
├── parts/                              # Modular 3D printed components (each with .FCStd, .step, and .stl)
│   ├── Base_Enclosure.FCStd / .step / .stl
│   ├── Shoulder_Yoke.FCStd / .step / .stl
│   ├── Upper_Arm.FCStd / .step / .stl
│   ├── Forearm.FCStd / .step / .stl
│   ├── Wrist.FCStd / .step / .stl
│   ├── Gripper_Base.FCStd / .step / .stl
│   ├── Gripper_Left_Finger.FCStd / .step / .stl
│   └── Gripper_Right_Finger.FCStd / .step / .stl
├── components/                         # COTS hardware STEP solids
│   ├── servo_rds5160_60kg.step         # 60 kg·cm high-torque digital actuator
│   ├── servo_mg996r.step               # 11 kg·cm metal-gear actuator
│   ├── bearing_6812zz_turntable.step   # 60x78x10mm thin-section turntable bearing
│   ├── bearing_608zz_counter_pivot.step# 8x22x7mm radial counter-pivot bearing
│   └── sensor_fsr402_tactile.step      # Force-sensing resistor tactile sensor
├── fasteners/                          # Standard ISO/DIN fasteners
│   ├── bolt_m8x30_hex.step             # ISO 4017 M8x30mm hex head pivot bolt
│   ├── nut_m8_nyloc.step               # ISO 7040 M8 nylon-insert locking nut
│   ├── screw_m3x16_shcs.step           # ISO 4762 M3x16mm socket head cap screw
│   └── screw_m4x16_shcs.step           # ISO 4762 M4x16mm socket head cap screw
├── scripts/                            # Parametric CAD generation scripts
│   ├── build_cad.py                    # Master B-Rep & FreeCAD rebuild script
│   └── generate_cots_library.py        # COTS hardware & fastener library generator
├── manufacturing/
│   └── MANUFACTURING_GUIDE.md          # 3D printing tolerances, infill, and slicer guide
├── COLCON_IGNORE                       # Excludes CAD directory from ROS 2 workspace builds
└── README.md
```

## FreeCAD Document Hierarchy (`Selah_Master.FCStd`)

Within FreeCAD, the master document is organized into functional groups:

```
Selah/  (Root App::DocumentObjectGroup)
├── 01_Base_Assembly/
│   └── Base_Enclosure                  # D-Profile 180mm base with cooling louvers & standoffs
├── 02_Shoulder_Assembly/
│   └── Shoulder_Yoke                   # Dual-pivot clevis with RDS5160 & 608ZZ pocket
├── 03_Upper_Arm_Assembly/
│   └── Upper_Arm                       # Link 1 (220mm) tapered truss beam with lightening windows
├── 04_Forearm_Assembly/
│   └── Forearm                         # Link 2 (180mm) with 22mm conduit & 20° camera shelf
├── 05_Wrist_Assembly/
│   └── Wrist                           # Link 3 (60mm) servo housing & 4-bolt circular flange
├── 06_Gripper_Assembly/
│   ├── Gripper_Base                    # End-effector chassis with gear shield
│   ├── Gripper_Left_Finger             # Articulated jaw with recessed FSR 402 tactile pocket
│   └── Gripper_Right_Finger            # Counter-rotating geared jaw
├── 07_Actuators_And_Electronics/
│   ├── servo_rds5160_60kg
│   ├── servo_mg996r
│   └── sensor_fsr402_tactile
└── 08_Bearings_And_Fasteners/
    ├── bearing_6812zz_turntable
    └── bearing_608zz_counter_pivot
```

## Rebuilding the CAD Models

To regenerate all STEP solids, slice-ready STLs, and native FreeCAD documents:

```bash
# 1. Regenerate COTS hardware & fasteners
python3 cad/scripts/generate_cots_library.py

# 2. Rebuild all 8 structural parts and master FreeCAD assembly
python3 cad/scripts/build_cad.py
```
