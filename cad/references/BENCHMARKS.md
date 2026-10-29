# 🦾 Robotics Reference Benchmarks & Mechanical Provenance

This directory stores the engineering benchmark studies and verified reference data used to guide the mechanical redesign and ROS 2 Jazzy kinematics of the **Astari Selah 5-DOF Manipulator**.

---

## 1. Benchmark Architectures Evaluated

### Benchmark A: SO-100 (The Robot Studio / Hugging Face LeRobot)
- **Kinematic Class**: 5-DOF + Parallel Gripper Articulated Manipulator.
- **Actuation Strategy**: Direct-drive bus servos with dual-ear clevises.
- **Reference Provenance**: Open-Source (Apache 2.0 / MIT) by Alexander Koch & Hugging Face.
- **Critical Mechanical Features Adopted**:
  - **Direct Horn Recessing**: The 25T round CNC aluminum disc horn ($\varnothing 20.0\text{ mm}$) is bolted directly into a precision recess in the link body using 4× M3 screws at $14.0\text{ mm}$ PCD, transferring shear torque across the screw shank circle rather than relying solely on the spline friction.
  - **Symmetric Geared Gripper**: Opposed involute/spur gear segments molded into jaw pivots to ensure synchronized, self-centering parallel grasping.
  - **Filleted Stress Relievers**: Generous interior fillet radii ($R \ge 2.5 - 3.0\text{ mm}$) along all link transitions to distribute bending stresses under horizontal payload cantilever.

### Benchmark B: Koch v1.1 Open-Source Arm
- **Kinematic Class**: 6-DOF Modular Arm.
- **Reference Provenance**: Open-Source Hardware (OSHWA).
- **Critical Mechanical Features Adopted**:
  - **Captive Nut Pockets**: Hex nut retention pockets ($5.5\text{ mm}$ AF for M3, $7.0\text{ mm}$ AF for M4) broached into link walls to permit one-handed maintenance with a single hex driver.
  - **Internal Wire Pass-Throughs**: Smooth, radiused conduits through the center of pivot axes to eliminate cable stretching and pinch hazards during full articulation.

### Benchmark C: WidowX 250 (Interbotix)
- **Kinematic Class**: 5-DOF Research Manipulator.
- **Reference Provenance**: Commercial / Open-Source ROS 2 Platform (Trossen Robotics).
- **Critical Mechanical Features Adopted**:
  - **Thin-Section Turntable Bearing**: Decoupling overturning moments from the base yaw actuator. The base yaw servo experiences pure rotational torque, while the radial and thrust loads from the 550 mm cantilever arm are completely carried by the 6812ZZ turntable bearing ($60\times 78\times 10\text{ mm}$).
  - **Orthogonal Clevis Alignment**: Precision shoulder yoke geometry maintaining perpendicularity between Joint 1 (Yaw) and Joint 2 (Pitch).

### Benchmark D: E.R.A 5-DOF Robotic Arm (RoboticWorx)
- **Kinematic Class**: 5-Axis Articulated Stepper Arm (1-meter vertical reach envelope).
- **Reference Provenance**: Open-Source Hardware / Hackster.io / MakerWorld by RoboticWorx.
- **Critical Mechanical Features Adopted**:
  - **Heavy Wide-Stance Base Plate**: $245 \times 194 \times 52\text{ mm}$ footprint eliminating overturning tip-hazards without needing bench clamps.
  - **Ribbed Upper Arm Spar**: $329\text{ mm}$ structural I-beam spar adapted to $280\text{ mm}$ center-to-center span with internal wire conduit.
  - **Thrust Bearing Turntable**: High-capacity circular turntable bearing isolating cantilever moment loads from the base stepper motor.

### Benchmark E: CHIMERA A1 5-DOF Robotic Arm (GitHub / GrabCAD)
- **Kinematic Class**: 5-DOF Manipulator with Planetary / Belt Reductions.
- **Reference Provenance**: Open-Source (`Prathviraj-mv/CHIMAERA-A1-----Open-source-5-DOF-Robotic-arm`).
- **Critical Mechanical Features Adopted**:
  - **Dual-Bearing Shoulder Yoke**: Dual-ear clevis supporting radial and axial loads across a 608ZZ counter-pivot.
  - **Forearm & Elbow Casing**: Enclosed structural housing adapted to $230\text{ mm}$ span with integrated $20^\circ$ optical shelf for ESP32-CAM.
  - **Geared Parallel Gripper**: Compact dual-finger jaw mechanism with meshing $m=1.0\text{ mm}$ spur gear sector and Interlink FSR 402 tactile pocket.

---

## 2. Astari Selah Hybrid Kinematic Ground Truth
- **Total Spherical Reach**: Exactly **$700.0\text{ mm}$** ($d_1=90\text{ mm}, a_2=280\text{ mm}, a_3=230\text{ mm}, a_4=90\text{ mm}, a_5=100\text{ mm}$).
- **Base Enclosure**: $245 \times 194 \times 52\text{ mm}$ footprint with $5.0\text{ mm}$ solid PETG floor, housing NEMA 17 (48mm), 10:1 planetary gearbox, and dual electronics.
- **Link 1 (Upper Arm)**: $280.0\text{ mm}$ center-to-center ($55 \times 45\text{ mm}$ box beam, NEMA 17 40mm + 5:1 planetary gearbox).
- **Link 2 (Forearm)**: $230.0\text{ mm}$ center-to-center with integrated $20^\circ$ downward angled ESP32-CAM optical shelf at $210\text{ mm}$.
- **Link 3 (Wrist)**: $90.0\text{ mm}$ center-to-center with MG996R servo cradle.
- **Gripper**: $100.0\text{ mm}$ reach, $80\text{ mm}$ stroke, with FSR 402 tactile sensing pocket.
- **Total Assembly Mass**: **$4.093\text{ kg}$** (B-Rep derived mass matrix with 40-45% Gyroid infill + COTS hardware).
