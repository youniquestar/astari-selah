# 5-DOF Robotic Arm Design Specifications

## 1. Actuator Envelope Constraints (The Foundation)
Because this is a hybrid actuator configuration, the CAD workspace must accommodate two entirely different motor frame sizes. Joint cutout brackets must be modeled around these hard boundaries:

### Heavy-Duty Category (Shoulder Pitch)
- **Actuator Model**: DSSERVO RDS5160 (60 kg·cm)
- **Physical Body Dimensions**: 60.0 mm (L) × 30.0 mm (W) × 48.0 mm (H)
- **Weight**: ~162 g per motor
- **CAD Tolerance Pocket**: Add **0.4 mm of clearance on all sides** of the mounting slot (**60.4 mm × 30.4 mm**).

### Mid-Duty Category (Base Yaw / Elbow Pitch)
- **Actuator Model**: DSSERVO RDS3235 (35 kg·cm)
- **Physical Body Dimensions**: 40.0 mm (L) × 20.0 mm (W) × 40.5 mm (H)
- **Weight**: ~60 g per motor
- **CAD Tolerance Pocket**: Add **0.4 mm of clearance on all sides** of the mounting slot (**40.4 mm × 20.4 mm**).

### Standard Category (Wrist Pitch/Roll, Gripper)
- **Actuator Model**: TowerPro MG996R (11 kg·cm)
- **Physical Body Dimensions**: 40.7 mm (L) × 19.7 mm (W) × 42.9 mm (H)
- **Weight**: ~55 g (allow ~65 g with metal horns and fasteners)
- **CAD Tolerance Pocket**: Add **0.3 mm of clearance on all sides** of the cutout brackets (**41.0 mm × 20.0 mm**).

---

## 2. Structural Link-by-Link Specifications
To achieve an exact **550 mm (55 cm)** total extended reach, link-to-link dimensions must be sketched precisely from the center of one joint's rotational axis to the next (center-to-center / axis-to-axis):

| Component / Link Segment | Axis-to-Axis (Center-to-Center) Length | Outer Diameter / Profile | Slicing & Manufacturing Rules |
| :--- | :--- | :--- | :--- |
| **Base Assembly** | Stationary (Height: 85 mm) | Diameter: 180 mm | PETG Filament. Print with a solid 5.0 mm bottom wall. Must house the heavy RDS5160 base servo and distribute tipping moment. |
| **Link 1: Upper Arm** | **220 mm** | Rectangular Profile: 55 mm W × 45 mm D | PLA+ Filament. 4.0 mm wall thickness with 35% Gyroid infill pattern for high rigidity. |
| **Link 2: Forearm** | **180 mm** | Cylindrical Profile: 42 mm OD | PLA+ Filament. 3.5 mm wall thickness. Integrated 20 mm internal hollow channel for routing servo & camera wires. |
| **Link 3: Wrist Assembly** | **60 mm** | Compact Bracket: 40 mm W × 35 mm H | PETG Filament. 4.0 mm solid walls. Houses MG996R wrist pitch servo. Limit tip-weight leverage. |
| **End Effector (Gripper)** | **90 mm** (Fully Closed) | Claw Length: 90 mm, Max Opening: 70 mm | PETG Filament. 100% solid infill on moving claw ears. Pocket on internal finger face recessed 1.0 mm for FSR 402 pressure sensor. |

**Total Reach Check**: 220 mm + 180 mm + 60 mm + 90 mm = **550 mm (55 cm)**.

---

## 3. Joint Geometry & Mechanical Constraints

### The Base & Shoulder Joint (High Torsional Load)
- **Yoke Configuration**: Cannot rely on motor axle spline alone to support the 220 mm upper arm link; must design a **dual-pivot yoke assembly**.
- **Bearing Support**: One side of the link connects to the RDS5160 metal horn. The exact opposite side must feature a molded pocket to press-fit a **608ZZ miniature ball bearing** (8 mm inner diameter, 22 mm outer diameter).
- **Fastener**: Run an **M8 screw** through this pivot to isolate bending forces from the servo casing.

### Forearm Camera Mount Pocket
- **Location**: Dedicated camera mounting shelf on distal end of Link 2 (Forearm) at exactly the **160 mm** mark (20 mm before wrist joint).
- **Angle & FOV**: Angled downward at a fixed **20° inclination** relative to link axis for ESP32-CAM to monitor gripper jaws during picking.
- **RF Isolation Clearance**: No M3 assembly screws, bearings, or servo bodies within **20 mm** of the ESP32-CAM's onboard gold PCB trace antenna.

---

## 4. Advanced Slicing Parameters for Fabrication
- **Gyroid Infill**: 30% to 40% density for Link 1 and Link 2 to distribute multi-axis torque.
- **Perimeter Wall Count**: 4 to 5 wall perimeters (0.4 mm nozzle size), creating a solid 2.0 mm structural outer shell.
