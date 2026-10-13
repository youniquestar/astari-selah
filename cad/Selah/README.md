# Selah — Modular FreeCAD Mechanical Subsystem

This directory contains the professional, modular FreeCAD CAD rebuild of the **Astari Selah** 5-DOF articulated robotic manipulator.

## FreeCAD Document Hierarchy (`Selah_Master.FCStd`)

Within FreeCAD, all components and assemblies are organized under the root folder/group **`Selah`**:

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
│   ├── Servo_RDS5160_Shoulder          # 60 kg·cm digital actuator model
│   ├── Servo_MG996R_Elbow              # 11 kg·cm metal gear actuator model
│   └── FSR402_Tactile_Sensor           # Interlink force-sensing resistor model
└── 08_Bearings_And_Fasteners/
    ├── Bearing_6812ZZ_Base             # 60x78x10mm thin-section turntable bearing
    └── Bearing_608ZZ_Pivot             # 8x22x7mm radial counter-pivot bearing
```

## Modular Directory Organization

```
cad/Selah/
├── assembly/
│   ├── Selah_Master.FCStd              # Master native FreeCAD document with complete Selah hierarchy
│   └── Selah_Assembly.step             # Master ISO-10303 STEP solid of entire manipulator
├── parts/                              # Individual modular parts (each with dedicated .FCStd project)
│   ├── Base_Enclosure.FCStd / .step / .stl
│   ├── Shoulder_Yoke.FCStd / .step / .stl
│   ├── Upper_Arm.FCStd / .step / .stl
│   ├── Forearm.FCStd / .step / .stl
│   ├── Wrist.FCStd / .step / .stl
│   ├── Gripper_Base.FCStd / .step / .stl
│   ├── Gripper_Left_Finger.FCStd / .step / .stl
│   └── Gripper_Right_Finger.FCStd / .step / .stl
├── components/                         # COTS hardware STEP solids
│   ├── Servo_RDS5160_Shoulder.step
│   ├── Servo_MG996R_Elbow.step
│   ├── Bearing_6812ZZ_Base.step
│   ├── Bearing_608ZZ_Pivot.step
│   └── FSR402_Tactile_Sensor.step
└── scripts/
    └── build_selah_cad.py              # Automated FreeCAD headless rebuild script
```

## Rebuilding the CAD Models Headless
To programmatically regenerate all `.FCStd` files, STEP solids, and STL meshes:
```bash
freecadcmd cad/Selah/scripts/build_selah_cad.py
```
