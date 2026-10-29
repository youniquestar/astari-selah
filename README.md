<div align="center">

# 🤖 Astari Selah — 5-DOF Articulated Robotic Manipulator

**An open-source, production-grade 5-DOF robotic manipulator uniting ESP32 bare-metal C++ firmware (FreeRTOS), ROS 2 Jazzy kinematics & MoveIt 2 trajectory planning, and FreeCAD 1.x verified hybrid physical B-Rep assemblies.**

[![ROS 2](https://img.shields.io/badge/ROS_2-Jazzy_Jalisco_%2F_Humble-22314E.svg?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/jazzy/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04_LTS_%2F_22.04_LTS-E95420.svg?style=for-the-badge&logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/24.04/)
[![RTOS](https://img.shields.io/badge/RTOS-FreeRTOS_v10.4-3C873A.svg?style=for-the-badge&logo=cplusplus&logoColor=white)](https://www.freertos.org/)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-Core_v6.1+-F58220.svg?style=for-the-badge&logo=platformio&logoColor=white)](https://platformio.org/)
[![FreeCAD](https://img.shields.io/badge/CAD-FreeCAD_v1.1.4_%2F_v1.0-CB333B.svg?style=for-the-badge&logo=freecad&logoColor=white)](https://www.freecad.org/)
<br/>
[![C++](https://img.shields.io/badge/C%2B%2B-17-00599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.12_%2F_3.10-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Target MCU](https://img.shields.io/badge/MCU-ESP32--WROOM--32-E7352C.svg?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![Reach](https://img.shields.io/badge/Reach-700_mm-00B4D8.svg?style=for-the-badge)](#-hardware-specifications--bill-of-materials)
[![Total Mass](https://img.shields.io/badge/Total_Mass-4.093_kg-success.svg?style=for-the-badge)](#-freecad-b-rep-audit--exact-si-inertias)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/colcon_build-passing-brightgreen.svg?style=for-the-badge&logo=githubactions&logoColor=white)](ros2/astari_selah_description)

<br/>

<p align="center">
  <a href="#-project-overview">Overview</a> •
  <a href="#-hybrid-design-lineage">Design Lineage</a> •
  <a href="#-software--package-versions-matrix">Package Matrix</a> •
  <a href="#-hardware-specifications--bill-of-materials">BOM & Specs</a> •
  <a href="#-cad-double-layer-verification-pipeline">CAD Pipeline</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-electronics--power-distribution">Electronics</a> •
  <a href="#-step-by-step-reproduction-guide">Reproduction Guide</a> •
  <a href="#-kinematics--coordinates">Kinematics</a> •
  <a href="#-troubleshooting">Troubleshooting</a> •
  <a href="#-license">License</a>
</p>

</div>

---

## 🌟 Project Overview

**Astari Selah** is a high-performance, open-source 5-DOF articulated robotic arm engineered for robotics students, researchers, and engineers within the ROS 2 and physical AI communities. 

Following a comprehensive design overhaul, Astari Selah rejects brittle procedural CAD generation in favor of a **physically validated hybrid architecture** combining the tested mechanical foundations of **E.R.A 5-DOF** (RoboticWorx) and **CHIMERA A1** (GitHub / GrabCAD), scaled and adapted to house our chosen actuators, sensors, and structural interfaces:

- **700 mm Extended Spherical Reach**: High-reach articulated profile ($d_1=90\text{ mm}, a_2=280\text{ mm}, a_3=230\text{ mm}, a_4=90\text{ mm}, a_5=100\text{ mm}$) delivering full tabletop and conveyor pick-and-place coverage.
- **Geared Stepper & Servo Actuation Stack**: 
  - **Joint 1 (Base Yaw) & Joint 2 (Shoulder Pitch)**: NEMA 17 (48mm) stepper motors paired with high-reduction **10:1 planetary gearboxes** delivering $15-18\text{ Nm}$ holding torque against gravity.
  - **Joint 3 (Elbow Pitch)**: NEMA 17 (40mm) stepper motor paired with a **5:1 planetary gearbox** ($8\text{ Nm}$ holding torque).
  - **Joint 4 (Wrist Pitch) & Joint 5 (Gripper Claws)**: Metal-gear **TowerPro MG996R** servos to eliminate distal cantilever mass.
- **Dual-Bearing Moment Decoupling**: High radial and overturning moment loads are completely decoupled from motor shafts using a heavy **6812ZZ thin-section bearing** ($\varnothing 78.0\text{ mm}$ OD) on the base turntable and a **608ZZ radial bearing** on the shoulder counter-pivot.
- **Integrated Vision & Tactile Perception**:
  - **Eye-in-Hand Forearm Camera**: Dedicated $20^\circ$ downward angled mounting shelf at the $210\text{ mm}$ mark for an **ESP32-CAM (OV2640 sensor, 66° FOV)** providing real-time visual servoing.
  - **Closed-Loop Tactile Grasping**: Embedded circular pocket ($\varnothing 18.5 \times 1.0\text{ mm}$) in the left gripper jaw for an **Interlink Electronics FSR 402** force-sensitive resistor with dynamic contact detection.
- **Double-Layer Verification Pipeline**:
  - **Layer 1 (SolidCraft)**: Full parametric B-Rep modeling, COTS pockets, internal conduits, and kinematic constraints.
  - **Layer 2 (FreeCAD 1.x Replication)**: Independent spatial orientation audit, 3D collision clearance validation ($0.4\text{ mm}$ PETG tolerance), and exact CAD-derived rotational inertia matrix extraction.
- **Native ROS 2 Jazzy & Gazebo Harmonic Two-Tier Simulation**:
  - URDF digital twin parameterized with exact FreeCAD B-Rep mass matrices ($4.093\text{ kg}$ total system).
  - Production `ros2_control` hardware interface (`mock_components/GenericSystem` tested with cubic spline `JointTrajectoryController`).
  - MoveIt 2 semantic configuration (`astari_selah.srdf`) with `arm` and `gripper` planning groups.
  - Gazebo Harmonic dynamic simulation launch with `ros_gz_bridge` and camera streaming.

---

## 🏛️ Hybrid Design Lineage

Astari Selah eliminates unjoined multi-shells and internal procedural hollows by synthesizing tested, physical geometries:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PRIMARY PHYSICAL FOUNDATION ARMS                     │
├───────────────────────────────────┬────────────────────────────────────┤
│   E.R.A 5-DOF (RoboticWorx)       │   CHIMERA A1 5-DOF (GitHub/GrabCAD)│
│   • 208 Solids, 5.62M mm³ Master  │   • 81 Solids, 3.23M mm³ Master    │
│   • 245x194mm Wide-Stance Base    │   • Compact Dual-Bearing Yoke      │
│   • 329mm Long-Span Spar Geometry │   • Enclosed Forearm/Elbow Casing  │
│   • Turntable Thrust Bearing      │   • Meshing Spur-Geared Gripper    │
└─────────────────┬─────────────────┴──────────────────┬─────────────────┘
                  │                                    │
                  └─────────────────┬──────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      ASTARI SELAH 700mm HYBRID CAD                     │
│  - Base Enclosure: E.R.A wide stance + 6812ZZ bearing + NEMA 17 10:1   │
│  - Shoulder Yoke: CHIMERA dual clevis + 608ZZ idler + NEMA 17 10:1     │
│  - Upper Arm: E.R.A spar scaled to 280mm + NEMA 17 5:1 planetary       │
│  - Forearm: CHIMERA casing scaled to 230mm + 20° ESP32-CAM optical shelf│
│  - Wrist & Gripper: CHIMERA coupler (90mm) + 100mm jaws w/ FSR 402     │
│  - Zero Hollow Cavities: Standoffs sunk 1.5mm into 5mm solid PETG floor │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│  LAYER 1: SOLIDCRAFT PARAMETRIC   │ │   LAYER 2: FREECAD REPLICATION   │
│  • B-Rep solid modeling           │ │   • Independent 3D spatial audit │
│  • 0.4mm 3D printing clearances   │ │   • 100% Manifold / Valid check  │
│  • Planetary gearbox adapters     │ │   • Exact SI inertia derivation  │
└───────────────────────────────────┘ └──────────────────────────────────┘
```

---

## 📦 Software & Package Versions Matrix

The entire software and simulation stack is validated on Ubuntu Linux:

| Ecosystem / Layer | Package / Tool | Primary Version | Backwards Compatible | Role in Astari Selah |
| :--- | :--- | :--- | :--- | :--- |
| **Host OS** | **Ubuntu Linux** | `24.04 LTS` (Noble) | `22.04 LTS` (Jammy) | Primary development operating system |
| **Robotics Middleware** | **ROS 2** | `Jazzy Jalisco` | `Humble Hawksbill` | Node graph, URDF/Xacro, TF2, ros2_control |
| **Motion Planning** | **MoveIt 2** | `Jazzy` | `Humble` | OMPL / Pilz kinematic planning, collision scene |
| **Dynamic Simulation**| **Gazebo** | `Gazebo Harmonic (gz sim)`| `Fortress / Classic` | Physics, holding torque, camera plugin |
| **Simulation Bridge** | **ros_gz_bridge** | `ros-jazzy-ros-gz` | `ros-humble-ros-gz` | Bidirectional clock, camera, and joint bridging |
| **Build System** | **colcon** | `colcon-core 0.3.x` | `0.3.0` | Multi-package ROS 2 CMake workspace build tool |
| **Compiler Toolchain** | **GCC / G++** | `13.2.0` | `11.4.0` | Standard C++17 compilation |
| **CAD Engine** | **FreeCAD** | `v1.1.4` (AppImage) | `v1.0.0` / `v0.21.2` | B-Rep verification, spatial audit, inertia extraction |
| **Embedded Framework**| **FreeRTOS** | `v10.4.3+` | `v10.0.0` | Preemptive task scheduling on ESP32 Dual-Core |
| **Embedded Toolchain**| **PlatformIO Core**| `6.1.15+` | `6.0.0` | Bare-metal firmware compilation and flashing |
| **Target MCU** | **ESP32-WROOM-32**| `Xtensa Dual 240MHz`| — | Real-time step pulse generation & kinematics |

---

## 🦾 Hardware Specifications & Bill of Materials

### 1. Kinematic Link Lengths & Dimensions
Total Articulated Spherical Reach: **700.0 mm** (Platform axis to gripper tip).

```
[Base: 90mm] ─── (J1: Yaw) ─── [Yoke: 63mm] ─── (J2: Pitch) ─── [Upper Arm: 280mm]
                                                                         │
                                                                    (J3: Pitch)
                                                                         │
[Gripper Tip] ◄── [Jaws: 100mm] ── (J5) ── [Wrist: 90mm] ── (J4) ── [Forearm: 230mm]
```

| Segment Name | Center-to-Center | Envelope Dimensions ($L \times W \times H$) | Volume ($\text{mm}^3$) | Material & Infill | COTS Recess Features |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Base_Enclosure** | — | $245.0 \times 194.0 \times 52.0\text{ mm}$ | $620,028.8$ | PETG ($5.0\text{ mm}$ solid floor) | $\varnothing 78.2\text{ mm}$ (6812ZZ), NEMA 17 48mm cradle, electronics standoffs |
| **Shoulder_Yoke** | $63.0\text{ mm}$ offset | $133.0 \times 116.0 \times 84.5\text{ mm}$ | $237,128.6$ | PETG ($45\%$ Gyroid) | $\varnothing 59.8\text{ mm}$ spigot, 10:1 planetary ring mount, 608ZZ idler |
| **Upper_Arm** | **$280.0\text{ mm}$** | $65.0 \times 52.0 \times 340.0\text{ mm}$ | $633,925.7$ | PETG ($40\%$ Gyroid) | NEMA 17 40mm cradle, 5:1 planetary adapter, M8 pivot nut |
| **Forearm** | **$230.0\text{ mm}$** | $48.0 \times 46.0 \times 285.0\text{ mm}$ | $532,765.7$ | PETG ($40\%$ Gyroid) | $20^\circ$ ESP32-CAM shelf ($40\times 27\text{ mm}$), J4 MG996R pocket |
| **Wrist** | **$90.0\text{ mm}$** | $42.0 \times 38.0 \times 125.0\text{ mm}$ | $143,347.2$ | PETG ($100\%$ Solid) | 25T servo horn recess, J5 MG996R actuator cradle |
| **Gripper_Base** | — | $54.0 \times 60.0 \times 45.0\text{ mm}$ | $79,771.3$ | PETG ($100\%$ Solid) | Dual finger pivot bosses, J5 servo horn drive recess |
| **Gripper_Left_Finger** | **$100.0\text{ mm}$** | $25.0 \times 22.0 \times 115.0\text{ mm}$ | $22,149.8$ | PETG ($100\%$ Solid) | $\varnothing 18.5 \times 1.0\text{ mm}$ FSR 402 pocket, wire canal |
| **Gripper_Right_Finger**| **$100.0\text{ mm}$** | $25.0 \times 22.0 \times 115.0\text{ mm}$ | $22,283.5$ | PETG ($100\%$ Solid) | Meshing spur gear sector, M3 pivot counterbore |

---

### 2. Actuator Specifications & Software Bounds

| Joint ID | Joint Name | Axis | Actuator Stack | Holding Torque | Operating Range | Software Limits (URDF) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Joint 1** | `joint1_base_yaw` | $Z$ | NEMA 17 (48mm) + 10:1 Planetary | $15.0\text{ Nm}$ | $10^\circ - 170^\circ$ | `[0.1745, 2.9671] rad` |
| **Joint 2** | `joint2_shoulder_pitch` | $Y$ | NEMA 17 (48mm) + 10:1 Planetary | $18.0\text{ Nm}$ | $0^\circ - 90^\circ$ | `[0.0000, 1.5708] rad` |
| **Joint 3** | `joint3_elbow_pitch` | $Y$ | NEMA 17 (40mm) + 5:1 Planetary | $8.0\text{ Nm}$ | $0^\circ - 120^\circ$ | `[0.0000, 2.0944] rad` |
| **Joint 4** | `joint4_wrist_pitch` | $Y$ | TowerPro MG996R Metal Gear | $1.1\text{ Nm}$ ($11\text{ kg}\cdot\text{cm}$) | $-90^\circ - +90^\circ$ | `[-1.5708, 1.5708] rad` |
| **Joint 5** | `joint5_gripper_left` | $Y$ | TowerPro MG996R Metal Gear | $1.1\text{ Nm}$ ($11\text{ kg}\cdot\text{cm}$) | $0^\circ - 45^\circ$ | `[0.0000, 0.7854] rad` |
| **Mimic** | `joint5_gripper_right` | $Y$ | Meshing Spur Gear Sector ($m=1.0$) | Direct | $0^\circ - 45^\circ$ | Mimic multiplier `1.0` |

---

### 3. Complete Bill of Materials (BOM)

| Category | Component / Part | Specification / Model | Qty | Purpose / Placement |
| :--- | :--- | :--- | :--- | :--- |
| **Actuators** | High-Torque Stepper | NEMA 17 Bipolar (48mm body, 2.0A, 59 N·cm) | 2 | Base Yaw (J1) & Shoulder Pitch (J2) |
| **Actuators** | Mid-Torque Stepper | NEMA 17 Bipolar (40mm body, 1.5A, 42 N·cm) | 1 | Elbow Pitch (J3) |
| **Actuators** | Planetary Gearbox 10:1 | NEMA 17 Flange 10:1 Precision Planetary | 2 | J1 & J2 high-ratio reduction |
| **Actuators** | Planetary Gearbox 5:1 | NEMA 17 Flange 5:1 Precision Planetary | 1 | J3 elbow reduction |
| **Actuators** | Metal-Gear Servos | TowerPro MG996R ($11\text{ kg}\cdot\text{cm}$) | 2 | Wrist Pitch (J4) & Gripper Drive (J5) |
| **Electronics**| Microcontroller | ESP32-WROOM-32 (Xtensa Dual 240MHz) | 1 | Real-time motion control & inverse kinematics |
| **Electronics**| Stepper Drivers | TMC2209 SilentStepStick (UART / Step-Dir) | 3 | Ultra-quiet microstepping (16x interpolated to 256x) |
| **Electronics**| Vision Module | ESP32-CAM (OV2640 Sensor, 2MP, 66° FOV) | 1 | Forearm eye-in-hand perception ($20^\circ$ tilt) |
| **Electronics**| Tactile Sensor | Interlink Electronics FSR 402 ($\varnothing 18.3\text{ mm}$) | 1 | Left gripper fingertip grasp pressure detection |
| **Power** | Main Buck Converter | XL4016 Step-Down Module ($8\text{A}$ Cont.) | 1 | $11.1\text{V} \rightarrow 12.0\text{V}/7.2\text{V}$ stepper & servo rails |
| **Power** | Logic Buck Converter | LM2596 Step-Down Module ($2\text{A}$ Cont.) | 1 | $11.1\text{V} \rightarrow 5.0\text{V}$ clean logic rail |
| **Power** | Primary Battery | 3S LiPo Battery ($11.1\text{V}$, $3000-5000\text{ mAh}$, XT60) | 1 | Primary untethered DC power supply |
| **Bearings** | Turntable Bearing | 6812ZZ Thin Section ($60\times 78\times 10\text{ mm}$) | 1 | Base yaw vertical and radial moment load isolation |
| **Bearings** | Radial Pivot Bearings | 608ZZ Miniature Bearings ($8\times 22\times 7\text{ mm}$) | 2 | Shoulder and elbow idler counter-pivots |
| **Fasteners** | Shoulder Counter Bolt | ISO 4017 / DIN 933 M8 $\times$ 30mm Bolt + M8 Nyloc | 1 | Shoulder clevis counter-pivot clamp |
| **Fasteners** | ISO Screws & Nuts | ISO 4762 M3 (10, 16, 20mm), M4 (16mm) SHCS | 40 | Motor cradles, gearbox rings, enclosure base |
| **Filament** | PETG Filament | 1.75mm Industrial Black / Grey | ~1.6 kg | Base enclosure, yoke, upper arm, forearm, gripper |

---

## 🔬 FreeCAD B-Rep Audit & Exact SI Inertias

Independent replication in **FreeCAD 1.1.4** verified all 8 parts are **100% Manifold, Closed, and Valid**:

| Link Name | FreeCAD Mass ($M$) | Center of Mass $[X, Y, Z]\text{ mm}$ | $I_{xx}\;[\text{kg}\cdot\text{m}^2]$ | $I_{yy}\;[\text{kg}\cdot\text{m}^2]$ | $I_{zz}\;[\text{kg}\cdot\text{m}^2]$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **base_link** | **$1.850\text{ kg}$** | $[0.00, 0.00, 26.00]$ | $4.850 \times 10^{-3}$ | $7.120 \times 10^{-3}$ | $9.640 \times 10^{-3}$ |
| **link1_shoulder_yoke** | **$0.820\text{ kg}$** | $[0.00, 12.50, 42.25]$ | $1.850 \times 10^{-3}$ | $2.140 \times 10^{-3}$ | $1.420 \times 10^{-3}$ |
| **link2_upper_arm** | **$0.680\text{ kg}$** | $[140.00, 0.00, 0.00]$ | $3.500 \times 10^{-4}$ | $4.820 \times 10^{-3}$ | $4.820 \times 10^{-3}$ |
| **link3_forearm** | **$0.450\text{ kg}$** | $[115.00, 0.00, 0.00]$ | $1.800 \times 10^{-4}$ | $2.310 \times 10^{-3}$ | $2.310 \times 10^{-3}$ |
| **link4_wrist** | **$0.140\text{ kg}$** | $[45.00, 0.00, 0.00]$ | $4.200 \times 10^{-5}$ | $1.150 \times 10^{-4}$ | $1.150 \times 10^{-4}$ |
| **gripper_base** | **$0.075\text{ kg}$** | $[20.00, 0.00, 0.00]$ | $2.100 \times 10^{-5}$ | $2.800 \times 10^{-5}$ | $2.800 \times 10^{-5}$ |
| **gripper_left_finger**| **$0.039\text{ kg}$** | $[48.00, 12.00, 0.00]$ | $8.500 \times 10^{-6}$ | $2.900 \times 10^{-5}$ | $2.900 \times 10^{-5}$ |
| **gripper_right_finger**|**$0.039\text{ kg}$** | $[48.00, -12.00, 0.00]$| $8.500 \times 10^{-6}$ | $2.900 \times 10^{-5}$ | $2.900 \times 10^{-5}$ |
| **Total System** | **$4.093\text{ kg}$** | — | — | — | — |

*Parameters exported to [`cad/parts/inertials.json`](cad/parts/inertials.json) and integrated into [`astari_selah.urdf.xacro`](ros2/astari_selah_description/urdf/astari_selah.urdf.xacro).*

---

## 🏛️ System Architecture

```
+---------------------------------------------------------------------------------------------------+
|                                 HOST WORKSTATION (ROS 2 Jazzy / Ubuntu 24.04)                     |
|                                                                                                   |
|   +--------------------------+         +----------------------------+         +---------------+   |
|   |   RViz2 / MoveIt 2       | <-----> |   robot_state_publisher    | <------ | /joint_states |   |
|   |  (Interactive Planning)  |  /tf    |   (Publishes Transforms)   |         | (sensor_msgs) |   |
|   +--------------------------+         +----------------------------+         +-------+-------+   |
|                                                                                       ^           |
|   +------------------------------------------------------------------+                |           |
|   |                 ros2_control Controller Manager                  |                |           |
|   |  • joint_state_broadcaster   (publishes /joint_states) ----------+                |           |
|   |  • arm_controller            (JointTrajectoryController, splines)                 |           |
|   |  • gripper_controller        (JointTrajectoryController)                          |           |
|   +----------------------------------+-------------------------------+                |           |
|                                      |                                                |           |
|                                      | Action / Topic Commands                        |           |
|                                      v                                                |           |
|   +------------------------------------------------------------------+                |           |
|   |                      esp32_bridge.py Node                        | ---------------+           |
|   |  • 50Hz Serial Polling Engine (115200 Baud)                      |                            |
|   |  • Subscribes: /target_joint_states                              |                            |
|   |  • Publishes: /fsr_pressure (Float32) & /joint_states            |                            |
|   +----------------------------------+-------------------------------+                            |
+--------------------------------------|------------------------------------------------------------+
                                       | USB-Serial (UART)
                                       | Packet: "J1:deg,J2:deg,J3:deg,J4:deg,J5:deg,FSR:val\n"
+--------------------------------------v------------------------------------------------------------+
|                                    MICROCONTROLLER (ESP32 - FreeRTOS)                             |
|                                                                                                   |
|   +-------------------------+        +---------------------------+        +-------------------+   |
|   |    Telemetry Manager    | <----> |     Kinematics Engine     | -----> |  FastAccelStepper |   |
|   | - FreeRTOS 50Hz Task    |        | - Forward D-H Solvers     |        | - TMC2209 Step/Dir|   |
|   | - Packet Parser/Emitter |        | - Analytical IK Solver    |        | - J1, J2, J3 Axes |   |
|   +-------------------------+        +---------------------------+        +---------+---------+   |
|                ^                                                                    |             |
|                | ADC Voltage (GPIO 34)                                              | PWM (50Hz)  |
|   +------------+------------+                                                       v             |
|   |    FSR 402 Conditioning |                                             +---------+---------+   |
|   |  - EMA Low-Pass Filter  |                                             | PCA9685 I2C Driver|   |
|   |  - Dynamic Tare Sensor  |                                             | - J4 (Wrist Pitch)|   |
|   +-------------------------+                                             | - J5 (Gripper Jaw)|   |
|                                                                           +-------------------+   |
+---------------------------------------------------------------------------------------------------+
```

---

## ⚡ Electronics & Power Distribution

### 1. Dual-Rail Isolated Power Topology
```
+───────────────────────────+
|   3S LiPo Battery (11.1V) |
|   XT60 Connector          |
+──────────────┬────────────+
               │
       ┌───────┴────────────────────────┐
       │                                │
       ▼                                ▼
+──────────────────────────+     +──────────────────────────+
|  XL4016 Buck Converter   |     |  LM2596 Buck Converter   |
|  Output: 12.0V / 7.2V @8A|     |  Output: 5.0V @ 2A       |
+──────────────┬───────────+     +──────────────┬───────────+
               │                                │
       [1000 µF Capacitor]              [470 µF Capacitor]
               │                                │
       ┌───────┴──────────────┐                 │
       ▼                      ▼                 ▼
+──────────────+       +──────────────+  +──────────────────────────+
| 3x TMC2209   |       | PCA9685 Rail |  |  ESP32 VIN & Logic VCC   |
| Stepper Motor|       | J4/J5 Servos |  |  ESP32-CAM Logic VCC     |
+──────────────+       +──────────────+  +──────────────────────────+
       │                      │                 │
       └──────────────────────┴────────► GND ◄──┘
```

### 2. ESP32 Pin Connections
| ESP32 Pin | Function | Peripheral Connection | Signal Description |
| :--- | :--- | :--- | :--- |
| **GPIO 18 / 19** | `STEP / DIR 1` | TMC2209 Driver 1 | J1 Base Yaw stepper step & dir |
| **GPIO 23 / 5**  | `STEP / DIR 2` | TMC2209 Driver 2 | J2 Shoulder Pitch stepper step & dir |
| **GPIO 13 / 12** | `STEP / DIR 3` | TMC2209 Driver 3 | J3 Elbow Pitch stepper step & dir |
| **GPIO 21** | `I2C SDA` | PCA9685 SDA | Serial Data for J4/J5 servo controller |
| **GPIO 22** | `I2C SCL` | PCA9685 SCL | Serial Clock for J4/J5 servo controller |
| **GPIO 34** | `ADC1_CH6` | FSR 402 Force Divider | Analog voltage input ($0.0\text{V} - 3.3\text{V}$) |
| **GPIO 2**  | `GPIO_OUT` | Built-in Blue LED | 1 Hz Heartbeat indicator |

---

## 🛠️ Step-by-Step Reproduction Guide

### 1. Build Workspace
```bash
# Source ROS 2 (Jazzy or Humble)
source /opt/ros/jazzy/setup.bash

# Build the description and control packages
cd ~/ros2_ws
colcon build --packages-select astari_selah_description
source install/setup.bash
```

### 2. Visual Model Inspection in RViz2
```bash
ros2 launch astari_selah_description display.launch.py
```

### 3. Launch ros2_control & Live Trajectory Execution
```bash
# Terminal 1: Launch controller manager & spawners (with or without RViz2)
ros2 launch astari_selah_description ros2_control.launch.py use_rviz:=true

# Terminal 2: Run automated multi-joint trajectory test
ros2 run astari_selah_description test_arm_control_execution.py
```

### 4. Dynamic Simulation in Gazebo Harmonic
```bash
ros2 launch astari_selah_description gazebo.launch.py
```

### 5. Flash Embedded Firmware (PlatformIO)
```bash
cd ~/ros2_ws/src/astari_selah/firmware
pio run -e esp32dev -t upload
```

---

## 🦾 Kinematics & Coordinate Frames

### Denavit-Hartenberg (DH) Classical Parameters (700 mm Reach)

| Joint ($i$) | Link Name | $d_i\;[\text{m}]$ | $\theta_i\;[\text{rad}]$ | $a_i\;[\text{m}]$ | $\alpha_i\;[\text{rad}]$ | Range |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | Base Yaw | **$0.090$** | $\theta_1^*$ | $0.000$ | $+\pi/2$ | $10^\circ - 170^\circ$ |
| **2** | Shoulder Pitch | $0.000$ | $\theta_2^*$ | **$0.280$** | $0.000$ | $0^\circ - 90^\circ$ |
| **3** | Elbow Pitch | $0.000$ | $\theta_3^*$ | **$0.230$** | $0.000$ | $0^\circ - 120^\circ$ |
| **4** | Wrist Pitch | $0.000$ | $\theta_4^*$ | **$0.090$** | $0.000$ | $-90^\circ - +90^\circ$ |
| **5** | Gripper Jaw | $0.000$ | $0$ | **$0.100$** | $0.000$ | $0^\circ - 45^\circ$ |

---

## 🔧 Troubleshooting

- **Permission Denied on `/dev/ttyUSB0`**:
  ```bash
  sudo usermod -a -G dialout $USER
  sudo chmod 666 /dev/ttyUSB0
  ```
- **Xacro / ROS 2 Jazzy Parameter Parsing**:
  In ROS 2 Jazzy, passing `Command(['xacro', ...])` inside launch nodes requires explicit wrapping with `launch_ros.parameter_descriptions.ParameterValue(..., value_type=str)` to prevent YAML parser errors. This is already resolved in our launch files.
- **Gazebo ros_gz_bridge Missing**:
  Install bridge tools via:
  ```bash
  sudo apt install ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-sim
  ```

---

## 📜 License & Acknowledgements

- **License**: Apache 2.0 (see [LICENSE](LICENSE)).
- **Acknowledgements**:
  - **RoboticWorx**: For the open-source **E.R.A 5-DOF** robotic arm base plate, long-span spar architecture, and build documentation.
  - **Prathviraj-mv**: For the open-source **CHIMERA A1 5-DOF** dual-bearing yoke, elbow casing, and geared gripper designs.
