# 5-DOF Robotic Arm: ROS 2 Description Package (`five_dof_arm_description`)

ROS 2 Humble description package providing kinematic modeling, URDF/Xacro definitions, STL mesh visualizations, hardware serial bridge, and RViz2 launch workflows.

## Package Capabilities
- **Kinematic Model**: Complete `urdf/five_dof_arm.urdf.xacro` with exact joint offsets extracted from physical CAD (reach: 550mm).
- **Meshes**: Scaled visual and collision STLs converted directly from engineering STEP solids.
- **Hardware Bridge**: `scripts/esp32_bridge.py` communicating at 50Hz over USB-Serial (`/dev/ttyUSB0` at 115200 baud) with automatic fallback to simulated trajectories if hardware is unplugged.
- **Topics**:
  - `/joint_states` (`sensor_msgs/msg/JointState`) — Live joint angles (rad).
  - `/fsr_pressure` (`std_msgs/msg/Float32`) — Live analog touch force from left gripper finger.
  - `/target_joint_states` (`sensor_msgs/msg/JointState`) — Commanded joint angles streamed to ESP32.

## Quick Start Launch

### 1. Build Package
From the root of your ROS 2 workspace:
```bash
colcon build --packages-select five_dof_arm_description
source install/setup.bash
```

### 2. Launch Interactive RViz2 Visualization (with GUI Joint Sliders)
```bash
ros2 launch five_dof_arm_description display.launch.py use_gui:=true
```

### 3. Launch Live Hardware Mode (Connected to ESP32)
```bash
ros2 launch five_dof_arm_description hardware.launch.py serial_port:=/dev/ttyUSB0
```
