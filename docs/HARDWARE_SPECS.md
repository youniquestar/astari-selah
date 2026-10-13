# Manipulator Hardware & Kinematic Specifications

## 1. Kinematic Link Dimensions
Total Articulated Reach: **550 mm (55.0 cm)** from base platform to closed gripper tip.

| Segment | Length (Center-to-Center) | Cross-Section / Profile | Mass (Estimated) | Material |
| :--- | :--- | :--- | :--- | :--- |
| **Base Enclosure** | H = 85.0 mm | Dia = 180 mm D-profile | ~1200 g (incl. electronics) | PETG (5mm floor) |
| **Shoulder Yoke** | H = 63.0 mm (offset) | Dual-pivot clevis | ~350 g | PETG (45% Gyroid) |
| **Link 1: Upper Arm** | **220.0 mm** | 55 mm (W) x 45 mm (D) | ~280 g | PLA+ (35% Gyroid) |
| **Link 2: Forearm** | **180.0 mm** | Cylindrical 42 mm OD | ~220 g | PLA+ (35% Gyroid) |
| **Link 3: Wrist** | **60.0 mm** | 40 mm (W) x 35 mm (H) | ~120 g | PETG Solid |
| **Gripper (End-Effector)** | **90.0 mm** (closed) | Dual geared fingers (70mm opening) | ~140 g | PETG Solid |

*Reach Verification*: 220 mm + 180 mm + 60 mm + 90 mm = **550 mm**.

## 2. Actuator Specifications & Software Limits

| Joint ID | Joint Name | Axis | Actuator Model | Stall Torque | Operating Range | Software Limits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **J1** | `joint1_base_yaw` | Z | DSSERVO RDS5160 | 60 kg·cm | 0° – 180° | **10° to 170°** |
| **J2** | `joint2_shoulder_pitch` | Y | DSSERVO RDS5160 | 60 kg·cm | 0° – 180° | **45° to 145°** |
| **J3** | `joint3_elbow_pitch` | Y | TowerPro MG996R | 11 kg·cm | 0° – 180° | **30° to 160°** |
| **J4** | `joint4_wrist_pitch` | Y | TowerPro MG996R | 11 kg·cm | 0° – 180° | **20° to 160°** |
| **J5** | `joint5_gripper_left` | Y | TowerPro MG996R | 11 kg·cm | 0° – 180° | **15° to 75°** |

*Note on Elbow Limit*: Joint 3 is constrained between 30° and 160° to avoid the full 180° kinematic singularity where links 1 and 2 become perfectly collinear.

## 3. Bearings & Structural Support
- **Base Yaw Bearing**: 6812ZZ thin-section deep-groove ball bearing (60 mm ID, 78 mm OD, 10 mm W) taking vertical moment loads.
- **Shoulder Counter-Pivot**: 608ZZ miniature ball bearing (8 mm ID, 22 mm OD, 7 mm W) with M8 through-bolt isolating bending moments from the RDS5160 servo spline.
- **Elbow & Wrist Pivots**: 608ZZ bearings press-fitted into counter-flanges.
