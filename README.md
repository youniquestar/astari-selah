<div align="center">

# 🤖 Astari Selah — 5-DOF Articulated Robotic Manipulator

**An open-source, production-grade 5-DOF robotic manipulator uniting ESP32 bare-metal C++ firmware (FreeRTOS), ROS 2 Humble kinematics, and modular FreeCAD parametric solid assemblies.**

[![ROS 2](https://img.shields.io/badge/ROS_2-Humble_Hawksbill-22314E.svg?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420.svg?style=for-the-badge&logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![RTOS](https://img.shields.io/badge/RTOS-FreeRTOS_v10.4-3C873A.svg?style=for-the-badge&logo=cplusplus&logoColor=white)](https://www.freertos.org/)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-Core_v6.1+-F58220.svg?style=for-the-badge&logo=platformio&logoColor=white)](https://platformio.org/)
[![FreeCAD](https://img.shields.io/badge/CAD-FreeCAD_v1.0_%2F_v0.21-CB333B.svg?style=for-the-badge&logo=freecad&logoColor=white)](https://www.freecad.org/)
<br/>
[![C++](https://img.shields.io/badge/C%2B%2B-17-00599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.10.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Target MCU](https://img.shields.io/badge/MCU-ESP32--WROOM--32-E7352C.svg?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![Reach](https://img.shields.io/badge/Reach-550_mm-00B4D8.svg?style=for-the-badge)](docs/HARDWARE_SPECS.md)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/colcon_build-passing-brightgreen.svg?style=for-the-badge&logo=githubactions&logoColor=white)](ros2/astari_selah_description)

<br/>

<p align="center">
  <a href="#-project-overview">Overview</a> •
  <a href="#-software--package-versions-matrix">Package Matrix</a> •
  <a href="#-hardware-specifications--bill-of-materials">BOM & Specs</a> •
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

**Astari Selah** is a high-performance, open-source 5-DOF robotic arm engineered for robotics students, researchers, and hobbyists within the global ROS community. Built from the ground up for modularity and reproducibility, it combines:

- **550 mm Articulated Reach**: Kinematically verified arm profile (Base Turntable $\rightarrow$ Shoulder $\rightarrow$ Upper Arm $\rightarrow$ Forearm $\rightarrow$ Wrist $\rightarrow$ End-Effector Jaw).
- **High-Torque Joint Actuation**: Dual 60 kg·cm DSSERVO RDS5160 core servos on high-load axes (Base Yaw, Shoulder Pitch) paired with triple metal-gear TowerPro MG996R servos on distal links.
- **Radial Moment Isolation**: 6812ZZ thin-section bearing (60 mm ID) on base turntable and 608ZZ counter-pivots to isolate bending moments from servo gear trains.
- **Deterministic 50 Hz Hardware Loop**: FreeRTOS-scheduled ESP32 bare-metal C++ firmware generating 12-bit PCA9685 I2C PWM signals with S-curve soft-start ramping.
- **Closed-Loop Tactile Sensing**: Interlink FSR 402 force-sensitive resistor with onboard Exponential Moving Average (EMA) filtering for grasp detection.
- **Dual-Rail Isolated Power Distribution**: High-power XL4016 (8A, 6.8V–7.2V) for servo transients and low-noise LM2596 (2A, 5.0V) for logic.
- **Native ROS 2 Humble Integration**: Xacro-parameterized URDF model, RViz2 visualizers with interactive GUI joint sliders, and asynchronous 50Hz serial bridge.
- **100% Modular Native FreeCAD Models**: Complete master assembly ([Selah_Master.FCStd](cad/assembly/Selah_Master.FCStd)) structured under the root `Selah` folder hierarchy with 8 modular sub-assemblies, individual `.FCStd` projects for every part in [`cad/parts/`](cad/parts/), STEP solids, and slice-ready STL meshes.

---

## 📦 Software & Package Versions Matrix

The entire stack has been rigorously tested and validated on the following environment:

| Ecosystem / Layer | Package / Tool | Recommended Version | Minimum Version | Role in Astari Selah | Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Operating System** | **Ubuntu Linux** | `22.04.5 LTS` (Jammy) | `22.04 LTS` | Host development OS | [ubuntu.com](https://releases.ubuntu.com/22.04/) |
| **Robotics Middleware** | **ROS 2** | `Humble Hawksbill` | `Humble` | Communication middleware, URDF, TF2, RViz2 | [docs.ros.org](https://docs.ros.org/en/humble/) |
| **Build System (ROS)** | **colcon** | `colcon-core 0.3.x` | `0.3.0` | Multi-package ROS 2 CMake workspace build tool | [colcon.readthedocs.io](https://colcon.readthedocs.io/) |
| **Build System (C++)** | **CMake** | `3.22.1+` | `3.20.0` | Ament CMake configuration for description package | [cmake.org](https://cmake.org/) |
| **Compiler Toolchain** | **GCC / G++** | `11.4.0` | `10.0` | Standard C++17 compilation | [gcc.gnu.org](https://gcc.gnu.org/) |
| **Embedded Framework** | **FreeRTOS** | `v10.4.3+` | `v10.0.0` | Deterministic task scheduling on ESP32 Dual-Core | [freertos.org](https://www.freertos.org/) |
| **Embedded Toolchain** | **PlatformIO Core** | `6.1.15+` | `6.0.0` | Bare-metal firmware compilation and flashing | [platformio.org](https://platformio.org/) |
| **MCU Platform** | **espressif32** | `v6.5.0` | `v5.0.0` | PlatformIO Espressif 32 development platform | [docs.platformio.org](https://docs.platformio.org/en/latest/platforms/espressif32.html) |
| **Embedded Core** | **Arduino-ESP32** | `v2.0.14+` | `v2.0.0` | Espressif Arduino core built on ESP-IDF v4.4 | [github.com/espressif](https://github.com/espressif/arduino-esp32) |
| **Embedded Library** | **Adafruit PWM Driver** | `^3.0.2` | `3.0.0` | PCA9685 16-channel 12-bit I2C servo controller | [github.com/adafruit](https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library) |
| **CAD Tool** | **FreeCAD** | `v1.0.0` / `v0.21.2` | `0.20.0` | Native 3D parametric CAD modeling and assembly | [freecad.org](https://www.freecad.org/) |
| **Scripting / Logic** | **Python** | `3.10.12` | `3.10.0` | Hardware bridge node, kinematics verification | [python.org](https://www.python.org/) |
| **Serial Library** | **pySerial** | `3.5+` | `3.4` | Low-latency serial packet transport (115200 baud) | [pyserial.readthedocs.io](https://pyserial.readthedocs.io/) |

---

## 🦾 Hardware Specifications & Bill of Materials

### 1. Kinematic Link Lengths & Dimensions
Total Articulated Reach: **550.0 mm** (Platform axis to gripper tip).

```
[Base: 85mm] ─── (J1: Yaw) ─── [Yoke: 63mm] ─── (J2: Pitch) ─── [Upper Arm: 220mm]
                                                                        │
                                                                   (J3: Pitch)
                                                                        │
[Gripper Tip] ◄── [Jaws: 90mm] ── (J5) ── [Wrist: 60mm] ── (J4) ── [Forearm: 180mm]
```

| Segment | Length (Center-to-Center) | Profile / Cross-Section | Mass (Est.) | Fabrication Material |
| :--- | :--- | :--- | :--- | :--- |
| **Base Enclosure** | $H = 85.0\text{ mm}$ | $\varnothing 180\text{ mm}$ D-Profile | $1200\text{ g}$ (w/ electronics) | PETG ($5.0\text{ mm}$ reinforced floor) |
| **Shoulder Yoke** | $H = 63.0\text{ mm}$ (offset) | Dual-pivot clevis | $350\text{ g}$ | PETG ($45\%$ Gyroid Infill) |
| **Link 1: Upper Arm** | **$220.0\text{ mm}$** | $55\text{ mm} \times 45\text{ mm}$ Box Beam | $280\text{ g}$ | PLA+ ($35\%$ Gyroid Infill) |
| **Link 2: Forearm** | **$180.0\text{ mm}$** | $\varnothing 42\text{ mm}$ OD Tubular ($20\text{ mm}$ conduit) | $220\text{ g}$ | PLA+ ($35\%$ Gyroid Infill) |
| **Link 3: Wrist** | **$60.0\text{ mm}$** | $40\text{ mm} \times 35\text{ mm}$ | $120\text{ g}$ | PETG ($100\%$ Solid) |
| **End-Effector (Gripper)** | **$90.0\text{ mm}$** (closed) | Dual-opposed spur gear jaws | $140\text{ g}$ | PETG ($100\%$ Solid) |

### 2. Actuator Specifications & Software Bounds

| Joint ID | Joint Name | Axis | Actuator | Stall Torque | Operating Range | Software Limits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Joint 1** | `joint1_base_yaw` | $Z$ | DSSERVO RDS5160 | $60\text{ kg}\cdot\text{cm}$ ($7.2\text{V}$) | $0^\circ - 180^\circ$ | **$10^\circ - 170^\circ$** |
| **Joint 2** | `joint2_shoulder_pitch` | $Y$ | DSSERVO RDS5160 | $60\text{ kg}\cdot\text{cm}$ ($7.2\text{V}$) | $0^\circ - 180^\circ$ | **$45^\circ - 145^\circ$** |
| **Joint 3** | `joint3_elbow_pitch` | $Y$ | TowerPro MG996R | $11\text{ kg}\cdot\text{cm}$ ($6.8\text{V}$) | $0^\circ - 180^\circ$ | **$30^\circ - 160^\circ$** *(Anti-singularity)* |
| **Joint 4** | `joint4_wrist_pitch` | $Y$ | TowerPro MG996R | $11\text{ kg}\cdot\text{cm}$ ($6.8\text{V}$) | $0^\circ - 180^\circ$ | **$20^\circ - 160^\circ$** |
| **Joint 5** | `joint5_gripper_left` | $Y$ | TowerPro MG996R | $11\text{ kg}\cdot\text{cm}$ ($6.8\text{V}$) | $0^\circ - 180^\circ$ | **$15^\circ - 75^\circ$** |

### 3. Complete Bill of Materials (BOM)

| Category | Component / Part | Specification / Model | Qty | Purpose / Placement |
| :--- | :--- | :--- | :--- | :--- |
| **Electronics** | Microcontroller | ESP32-WROOM-32 (30-pin NodeMCU) | 1 | Real-time loop, kinematics, serial telemetry |
| **Electronics** | PWM Controller | PCA9685 16-Channel 12-Bit I2C Driver | 1 | 50Hz servo PWM signal generation |
| **Electronics** | Tactile Sensor | Interlink Electronics FSR 402 | 1 | Gripper tip contact pressure sensing |
| **Actuators** | High-Torque Servo | DSSERVO RDS5160 ($60\text{ kg}\cdot\text{cm}$) | 2 | Base Yaw (J1) & Shoulder Pitch (J2) |
| **Actuators** | Standard Servo | TowerPro MG996R Metal Gear ($11\text{ kg}\cdot\text{cm}$) | 3 | Elbow Pitch (J3), Wrist (J4), Gripper (J5) |
| **Power** | Servo Buck Converter | XL4016 Step-Down Module ($8\text{A}$ Cont.) | 1 | $11.1\text{V} \rightarrow 6.8\text{V}-7.2\text{V}$ high-current rail |
| **Power** | Logic Buck Converter | LM2596 Step-Down Module ($2\text{A}$ Cont.) | 1 | $11.1\text{V} \rightarrow 5.0\text{V}$ clean logic rail |
| **Power** | Battery Supply | 3S LiPo Battery ($11.1\text{V}$, $2200-5000\text{ mAh}$, XT60) | 1 | Primary DC power source |
| **Power** | Buffer Capacitors | $1000\,\mu\text{F}$ ($16\text{V}$) + $470\,\mu\text{F}$ ($16\text{V}$) | 1+1 | Inrush absorption on servo & logic rails |
| **Bearings** | Turntable Bearing | 6812ZZ Deep Groove Thin Section ($60\times 78\times 10\text{ mm}$) | 1 | Base yaw vertical and radial moment load |
| **Bearings** | Pivot Bearings | 608ZZ Miniature Radial Bearings ($8\times 22\times 7\text{ mm}$) | 3 | Shoulder, Elbow, Wrist passive counter-pivots |
| **Fasteners** | Counter-Pivot Bolt | ISO 4017 / DIN 933 M8 $\times$ 30mm Bolt + M8 Nut | 1 | Shoulder clevis counter-pivot clamp |
| **Fasteners** | Gripper Pivot Bolt | ISO 4762 M4 $\times$ 16mm SHCS + M4 Nyloc Nut | 1 | Gripper jaw dual-gear main hinge |
| **Fasteners** | Structural Screws | ISO 4762 M3 $\times$ 10mm, 16mm, 20mm SHCS | 30 | Servo brackets, enclosure base, clamp collars |
| **Filament** | PETG Filament | 1.75mm (Black / Industrial Grey) | ~1.2 kg | Base enclosure, shoulder yoke, wrist, gripper |
| **Filament** | PLA+ Filament | 1.75mm (Orange / High Rigidity) | ~0.6 kg | Upper arm beam, forearm cylinder |

---

## 🏛️ System Architecture

Astari Selah divides tasks strictly between real-time low-level embedded hardware and high-level robotics middleware:

```
+---------------------------------------------------------------------------------------------------+
|                                 HOST WORKSTATION (ROS 2 Humble)                                   |
|                                                                                                   |
|   +--------------------------+         +----------------------------+         +---------------+   |
|   |      RViz2 / MoveIt      | <-----> |   robot_state_publisher    | <------ | /joint_states |   |
|   |  (3D State & Kinematics) |  /tf    |   (Publishes Transforms)   |         | (sensor_msgs) |   |
|   +--------------------------+         +----------------------------+         +-------+-------+   |
|                                                                                       ^           |
|                                                                                       |           |
|                                        +----------------------------------+           |           |
|                                        |       esp32_bridge.py Node       | ----------+           |
|                                        |   - 50Hz Serial Polling Engine   |                       |
|                                        |   - rad <-> deg Transformation   |                       |
|                                        |   - Publishes /joint_states      |                       |
|                                        |   - Publishes /fsr_pressure      |                       |
|                                        |   - Listens /target_joint_states |                       |
|                                        +-----------------+----------------+                       |
+----------------------------------------------------------|----------------------------------------+
                                                           | USB-Serial @ 115200 Baud (UART)
                                                           | Packet: "J1:deg,J2:deg,...,FSR:val\n"
+----------------------------------------------------------v----------------------------------------+
|                                    MICROCONTROLLER (ESP32 - FreeRTOS)                             |
|                                                                                                   |
|   +-------------------------+        +---------------------------+        +-------------------+   |
|   |    Telemetry Manager    | <----> |     Kinematics Engine     | -----> |  PCA9685 Driver   |   |
|   | - FreeRTOS 50Hz Task    |        | - Forward D-H Solvers     |        | - 12-Bit PWM      |   |
|   | - Packet Parser/Emitter |        | - Analytical IK Solver    |        | - S-Curve Ramping |   |
|   +-------------------------+        +---------------------------+        +---------+---------+   |
|                ^                                                                    |             |
|                | ADC Voltage (GPIO 34)                                              | 50Hz PWM    |
|   +------------+------------+                                                       v             |
|   |    FSR 402 Conditioning |                                             +---------+---------+   |
|   |  - EMA Low-Pass Filter  |                                             |   5x High-Torque  |   |
|   |  - Dynamic Tare Sensor  |                                             |   Robotic Servos  |   |
|   +-------------------------+                                             +-------------------+   |
+---------------------------------------------------------------------------------------------------+
```

---

## ⚡ Electronics & Power Distribution

### 1. Dual-Rail Isolated Power Topology
Servos draw instantaneous peak currents exceeding 6A during synchronized acceleration. Power rails are physically isolated to prevent microcontroller brownout resets.

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
|  Output: 6.8V - 7.2V @ 8A|     |  Output: 5.0V @ 2A       |
+──────────────┬───────────+     +──────────────┬───────────+
               │                                │
       [1000 µF Capacitor]              [470 µF Capacitor]
               │                                │
               ▼                                ▼
+──────────────────────────+     +──────────────────────────+
|  PCA9685 Servo V+ Rail   |     |  ESP32 VIN & Logic VCC   |
|  Powers 5x Servos        |     |  PCA9685 Logic VCC       |
+──────────────────────────+     +──────────────────────────+
               │                                │
               └─────────► Common GND ◄─────────┘
```

### 2. ESP32 Pin Connections & PCA9685 Channel Map

| ESP32 Pin | Function | Peripheral Connection | Signal Description |
| :--- | :--- | :--- | :--- |
| **GPIO 21** | `I2C SDA` | PCA9685 SDA | Serial Data (Internal pull-up enabled) |
| **GPIO 22** | `I2C SCL` | PCA9685 SCL | Serial Clock (Internal pull-up enabled) |
| **GPIO 34** | `ADC1_CH6` | FSR 402 Force Divider | Analog voltage input ($0.0\text{V} - 3.3\text{V}$) |
| **GPIO 2** | `GPIO_OUT` | Built-in Blue LED | 1 Hz Heartbeat indicator |
| **VIN** | `POWER_IN` | LM2596 VOUT (+5.0V) | Regulated logic power supply |
| **GND** | `GROUND` | Common Ground Bus | Star-ground configuration |

| PCA9685 Output | Target Joint | Servo Model | Min Pulse | Center Pulse | Max Pulse |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Channel 0** | Joint 1 (Base Yaw) | DSSERVO RDS5160 | $500\,\mu\text{s}$ | $1500\,\mu\text{s}$ | $2500\,\mu\text{s}$ |
| **Channel 1** | Joint 2 (Shoulder Pitch) | DSSERVO RDS5160 | $500\,\mu\text{s}$ | $1500\,\mu\text{s}$ | $2500\,\mu\text{s}$ |
| **Channel 2** | Joint 3 (Elbow Pitch) | TowerPro MG996R | $500\,\mu\text{s}$ | $1500\,\mu\text{s}$ | $2500\,\mu\text{s}$ |
| **Channel 3** | Joint 4 (Wrist Pitch) | TowerPro MG996R | $500\,\mu\text{s}$ | $1500\,\mu\text{s}$ | $2500\,\mu\text{s}$ |
| **Channel 4** | Joint 5 (Gripper Jaw) | TowerPro MG996R | $500\,\mu\text{s}$ | $1500\,\mu\text{s}$ | $2500\,\mu\text{s}$ |

### 3. FSR 402 Tactile Conditioning Circuit
The force sensor is wired in a voltage divider configuration directly on the left gripper tip:
```
+3.3V (ESP32)
   │
   ├─── [ FSR 402 Sensor ] ───┐
                              ├───► GPIO 34 (Analog In, ADC1_CH6)
   ┌─── [ 10 kΩ Resistor ] ───┘
   │
  GND
```

---

## 🛠️ Step-by-Step Reproduction Guide

Follow these exact steps to replicate Astari Selah on your system.

### Phase 1: Environment & Toolchain Prerequisites

Ensure you are running **Ubuntu 22.04 LTS**. Install standard system utilities and ROS 2 Humble Desktop:

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install core compilation tools and Python packages
sudo apt install -y build-essential cmake git python3-pip \
                    python3-colcon-common-extensions python3-rosdep \
                    python3-vcstool

# 3. Install Python serial communication library
pip install pyserial

# 4. Install PlatformIO Core for embedded compilation
pip install platformio

# 5. Configure serial port permissions (CRITICAL: prevents permission errors on /dev/ttyUSB0)
sudo usermod -a -G dialout $USER
sudo wget https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules -O /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

> [!NOTE]
> Log out and log back in (or reboot) after adding your user to the `dialout` group for group permissions to take effect.

---

### Phase 2: Clone Workspace & Build ROS 2 Package

```bash
# 1. Create a clean ROS 2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 2. Clone Astari Selah repository
git clone https://github.com/youniquestar/astari-selah.git

# 3. Return to workspace root and resolve any dependencies
cd ~/ros2_ws
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# 4. Build the Astari Selah description package
colcon build --packages-select astari_selah_description

# 5. Source the overlay environment
source install/setup.bash
```

To automatically load the workspace in every new terminal, add it to your `~/.bashrc`:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

---

### Phase 3: 3D Printing & Mechanical Assembly

All slice-ready STL files are located in [`cad/parts/`](cad/parts/).

#### Slicing Settings Table
| Part Name | Recommended Filament | Infill % & Pattern | Wall Count / Perimeters | Layer Height | Support |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `base_enclosure.stl` | **PETG** | 35% Gyroid | 5 walls ($2.0\text{ mm}$) | $0.20\text{ mm}$ | Touching buildplate |
| `shoulder_yoke.stl` | **PETG** | 45% Gyroid | 6 walls ($2.4\text{ mm}$) | $0.20\text{ mm}$ | Yes (Clevis overhang) |
| `upper_arm.stl` | **PLA+** | 35% Gyroid | 5 walls ($2.0\text{ mm}$) | $0.20\text{ mm}$ | Horizontal orientation |
| `forearm.stl` | **PLA+** | 35% Gyroid | 4 walls ($1.6\text{ mm}$) | $0.20\text{ mm}$ | Support internal cavity |
| `wrist.stl` | **PETG** | 100% Solid | 5 walls ($2.0\text{ mm}$) | $0.16\text{ mm}$ | None |
| `gripper_base.stl` | **PETG** | 40% Gyroid | 4 walls ($1.6\text{ mm}$) | $0.20\text{ mm}$ | None |
| `gripper_left_finger.stl` | **PETG** | 100% Solid | Solid | $0.16\text{ mm}$ | Recessed sensor pocket |
| `gripper_right_finger.stl`| **PETG** | 100% Solid | Solid | $0.16\text{ mm}$ | Gear teeth facing up |

#### Mechanical Assembly Sequence
1. **Turntable Base**: Press-fit the **6812ZZ** ball bearing into the base enclosure upper recess. Fasten the RDS5160 base servo using M3 screws.
2. **Shoulder Clevis**: Mount the shoulder yoke to the base servo horn. Insert the **608ZZ** counter-pivot bearing on the opposite arm of the clevis and clamp using the M8 $\times$ 30mm bolt.
3. **Upper Arm & Forearm**: Press 608ZZ bearings into the counter-flanges of Link 1 and Link 2. Bolt the servo horns with M3 hardware. Ensure internal wiring channels are clear.
4. **End-Effector Jaw**: Affix the FSR 402 sensor into the recessed inner pad of the left finger using thin 3M adhesive. Mesh the jaw gears and pivot on the M4 $\times$ 16mm hinge bolt.

---

### Phase 4: Flash ESP32 Bare-Metal Firmware

Connect the ESP32 to your computer using a Micro-USB data cable.

```bash
# 1. Navigate to the firmware directory
cd ~/ros2_ws/src/astari_selah/firmware

# 2. Build the embedded C++ project
pio run

# 3. Flash to ESP32 (automatically detects /dev/ttyUSB0)
pio run --target upload --upload-port /dev/ttyUSB0

# 4. Open serial monitor to verify 50Hz telemetry output
pio device monitor -b 115200
```

**Expected Serial Output Stream:**
```text
[INIT] Astari Selah Firmware Initialized @ 50Hz
[PCA9685] Frequency set to 50Hz (prescale: 121)
[FSR] Tare established at ADC offset: 24
J1:90.0,J2:90.0,J3:90.0,J4:90.0,J5:45.0,FSR:0.00
J1:90.0,J2:90.0,J3:90.0,J4:90.0,J5:45.0,FSR:0.00
```
*(Press `Ctrl + C` or `Ctrl + ]` to exit the monitor).*

---

### Phase 5: Launch RViz2 Kinematic Visualization

Test the URDF kinematic chain and coordinate transforms in RViz2:

```bash
# Launch interactive visualization with joint sliders GUI
ros2 launch astari_selah_description display.launch.py use_gui:=true
```

- Move the GUI sliders to observe real-time forward kinematic movements.
- Inspect coordinate frames (`base_link`, `link_1`, `link_2`, `link_3`, `gripper_link`, `fsr_contact_frame`).

---

### Phase 6: Live Hardware Bringup & Telemetry Streaming

Power on your 11.1V LiPo battery rail, then start the hardware bridge:

```bash
# Launch hardware bridge connected to ESP32
ros2 launch astari_selah_description hardware.launch.py serial_port:=/dev/ttyUSB0
```

Open a second terminal to inspect live sensor topics:

```bash
# 1. Echo live joint states (radians)
ros2 topic echo /joint_states

# 2. Echo tactile force feedback (pressure scale)
ros2 topic echo /fsr_pressure

# 3. Command the arm to move to target joint angles
ros2 topic pub --once /target_joint_states sensor_msgs/msg/JointState \
  "{name: ['joint1_base_yaw', 'joint2_shoulder_pitch', 'joint3_elbow_pitch', 'joint4_wrist_pitch', 'joint5_gripper_left'], \
    position: [1.57, 1.20, 1.80, 1.57, 0.50]}"
```

---

## 📐 Kinematics & Coordinate Frames

### Denavit-Hartenberg (D-H) Parameter Table
The analytical kinematic model conforms to standard proximal D-H convention:

| Frame ($i$) | Link Name | Joint Angle ($\theta_i$) | Link Twist ($\alpha_{i-1}$) | Link Length ($a_{i-1}$) | Joint Offset ($d_i$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0 $\rightarrow$ 1** | Base to Shoulder | $\theta_1^*$ (Base Yaw) | $0^\circ$ | $0\text{ mm}$ | $d_1 = 85.0\text{ mm}$ |
| **1 $\rightarrow$ 2** | Shoulder to Elbow | $\theta_2^*$ (Shoulder Pitch) | $+90^\circ$ | $a_1 = 63.0\text{ mm}$ | $0\text{ mm}$ |
| **2 $\rightarrow$ 3** | Elbow to Wrist | $\theta_3^*$ (Elbow Pitch) | $0^\circ$ | $a_2 = 220.0\text{ mm}$ | $0\text{ mm}$ |
| **3 $\rightarrow$ 4** | Wrist to Flange | $\theta_4^*$ (Wrist Pitch) | $0^\circ$ | $a_3 = 180.0\text{ mm}$ | $0\text{ mm}$ |
| **4 $\rightarrow$ 5** | Flange to Tool Tip | $\theta_5^*$ (End-Effector) | $0^\circ$ | $a_4 = 150.0\text{ mm}$ | $0\text{ mm}$ |

$$\text{Maximum Articulated Reach} = a_1 + a_2 + a_3 + a_4 = 63 + 220 + 180 + 150 = \mathbf{613\text{ mm}} \quad (\text{Horizontal Linear Line})$$
$$\text{Nominal Operating Reach} = 220 + 180 + 60 + 90 = \mathbf{550\text{ mm}}$$

---

## 🔧 Troubleshooting

<details>
<summary><b>1. Serial Port Permission Denied (<code>/dev/ttyUSB0: Permission denied</code>)</b></summary>

**Cause**: Your Linux user account lacks read/write rights to the dialout serial device group.  
**Resolution**:
```bash
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB0
```
Log out and log back in for changes to apply.
</details>

<details>
<summary><b>2. ESP32 Resets or Reboots When Multiple Servos Move Simultaneously</b></summary>

**Cause**: Severe voltage sag on the 5V logic line caused by servo inrush current.  
**Resolution**:
- Confirm the **XL4016** buck converter is supplying the servos (adjusted to $6.8\text{V}-7.2\text{V}$) and NOT the ESP32.
- Confirm the **$1000\,\mu\text{F}$ capacitor** is soldered directly across the PCA9685 high-current screw terminal terminals.
- Ensure the LM2596 converter for the ESP32 logic rail has an independent ground trace.
</details>

<details>
<summary><b>3. PCA9685 I2C Communication Error (<code>PCA9685 not detected</code>)</b></summary>

**Cause**: Missing pull-up resistors or loose I2C wiring on GPIO 21 / GPIO 22.  
**Resolution**:
- Run `sudo apt install i2c-tools` and inspect I2C addresses on ESP32 boot.
- Verify default address is `0x40`.
- Keep I2C wires shorter than $15\text{ cm}$ to prevent signal distortion.
</details>

<details>
<summary><b>4. Colcon Build Indexes Non-ROS Python or C++ Folders</b></summary>

**Cause**: `colcon` recursively searches directories and tries to compile firmware or CAD files.  
**Resolution**:
Verify that empty `COLCON_IGNORE` marker files exist in `cad/`, `docs/`, and `firmware/`:
```bash
touch ~/ros2_ws/src/astari_selah/cad/COLCON_IGNORE
touch ~/ros2_ws/src/astari_selah/firmware/COLCON_IGNORE
```
</details>

---

## 🗺️ Project Roadmap

- [x] High-precision FreeCAD 3D parametric solids with STEP and STL exports.
- [x] Bare-metal C++ firmware with deterministic 50Hz FreeRTOS task loop.
- [x] Dynamic S-curve trajectory ramping on 12-bit PCA9685 channels.
- [x] Kinematic Xacro/URDF model with accurate joint offsets.
- [x] Asynchronous Python hardware serial bridge for ROS 2 Humble.
- [ ] MoveIt 2 motion planning pipeline and trajectory execution interface (`astari_selah_moveit_config`).
- [ ] Physics simulation in Gazebo Harmonic with `ros2_control` hardware abstraction.
- [ ] Vision-guided pick-and-place with ESP32-CAM and OpenCV AprilTag detection.

---

## 🤝 Contributing

Contributions from the global robotics and open-source community are warmly welcome!

1. **Fork the Repository**: Click the `Fork` button at the top right of this page.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-awesome-feature
   ```
3. **Commit Your Changes**: Follow Conventional Commits:
   ```bash
   git commit -m "feat(ros2): add custom trajectory controller interface"
   ```
4. **Push to Your Branch**:
   ```bash
   git push origin feat/your-awesome-feature
   ```
5. **Open a Pull Request**: Submit your PR with a description of the improvements and verification tests.

---

## 📄 License & Attribution

This project is licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for complete details.

```
Copyright 2026 Jeremiah Alao (youniquestar)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

---

<div align="center">
  <b>Developed with passion for open robotics by <a href="https://github.com/youniquestar">Jeremiah Alao</a>.</b><br/>
  <i>Star ⭐ the repository if you found this project helpful!</i>
</div>
