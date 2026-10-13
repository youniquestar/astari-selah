# 3D Printing & Fabrication Guide — 5-DOF Robotic Arm

## Recommended Materials & Slicing Specifications

| Part | Material | Infill Pattern / Density | Perimeters / Wall Count | Critical Printing Notes |
| :--- | :--- | :--- | :--- | :--- |
| **base_enclosure** | PETG | 35% Gyroid | 5 walls (2.0mm) | Print with solid 5.0mm bottom floor for rigidity and low CG. |
| **shoulder_yoke** | PETG | 45% Gyroid | 6 walls (2.4mm) | High torsional pivot. Ensure 608ZZ bearing pocket is calibrated (22.0mm ID). |
| **upper_arm** (Link 1) | PLA+ | 35% Gyroid | 5 walls (2.0mm) | 220mm length. Print horizontally with supports to maximize layer adhesion along bending axis. |
| **forearm** (Link 2) | PLA+ | 35% Gyroid | 4 walls (1.6mm) | 180mm length. Clear 20mm internal wiring channel. 20° angled shelf for ESP32-CAM. |
| **wrist** (Link 3) | PETG | 100% Solid | 5 walls (2.0mm) | High stress link at distal end. |
| **gripper_base** | PETG | 40% Gyroid | 4 walls (1.6mm) | Ensure M4 pivot hole and MG996R pocket have 0.3mm clearance. |
| **gripper_left_finger** | PETG | 100% Solid | Solid | Recessed pocket on inner face (1.0mm depth) for FSR 402 sensor. |
| **gripper_right_finger** | PETG | 100% Solid | Solid | Geared drive teeth. |

## Fastener & Hardware Requirements
- **M8 x 30mm Hex Bolt + M8 Hex Nut**: Shoulder counter-pivot through 608ZZ bearing.
- **M4 x 16mm SHCS**: Gripper jaw main hinge pivot.
- **M3 x 10mm / 16mm / 20mm SHCS**: Servo brackets, electronics standoffs, and link clamps.
- **M3 Hex Nuts & Flat Washers**: DIN 125 washers on all bearing faces.
- **608ZZ Ball Bearings (3x)**: Shoulder, Elbow, Wrist passive counter-pivots (8mm ID, 22mm OD, 7mm W).
- **6812ZZ Thin Section Ball Bearing (1x)**: Turntable base yaw support (60mm ID, 78mm OD, 10mm W).
