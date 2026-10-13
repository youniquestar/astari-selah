# System Architecture & Middleware Division

The 5-DOF industrial manipulator utilizes a hybrid architecture dividing real-time hardware execution and high-level robotics computing:

```
+-------------------------------------------------------------------------------+
|                       HOST WORKSTATION (ROS 2 Humble)                        |
|                                                                               |
|  +--------------------+         +-------------------+         +------------+  |
|  |    RViz2 / MoveIt  | <-----> |   robot_state_    | <------ |   joint_   |  |
|  |   (Visualization)  | /tf     |     publisher     |         |   states   |  |
|  +--------------------+         +-------------------+         +-----+------+  |
|                                                                     ^         |
|                                                                     |         |
|                          +-----------------------------+            |         |
|                          |    esp32_bridge.py Node     | -----------+         |
|                          |  - Parses Serial @ 50 Hz    |                      |
|                          |  - deg -> rad conversion    |                      |
|                          |  - Publishes /joint_states  |                      |
|                          |  - Publishes /fsr_pressure  |                      |
|                          +--------------+--------------+                      |
+-----------------------------------------|-------------------------------------+
                                          | USB-Serial @ 115200 Baud
                                          | Format: "J1:deg,J2:deg,...,FSR:val"
+-----------------------------------------v-------------------------------------+
|                     MICROCONTROLLER (ESP32 - Bare-Metal C++)                 |
|                                                                               |
|  +----------------------+      +----------------------+      +-------------+  |
|  |   Telemetry Manager  | <--> |   Kinematics Engine  | ---> |   PCA9685   |  |
|  | - 50Hz Hardware Loop |      | - D-H Parameters     |      | PWM Driver  |  |
|  | - Packet Serializer  |      | - Analytical FK & IK |      | (50Hz I2C)  |  |
|  +----------------------+      +----------------------+      +------+------+  |
|             ^                                                       |         |
|             | Analog Reading                                        | PWM     |
|             | (GPIO 34)                                             v         |
|  +----------+-----------+                                      +----+------+  |
|  |   FSR 402 Pressure   |                                      | 5x Servos |  |
|  |  (EMA Filtered Force)|                                      | RDS5160 & |  |
|  +----------------------+                                      |  MG996R   |  |
|                                                                +-----------+  |
+-------------------------------------------------------------------------------+
```

## Subsystem Responsibilities

### 1. ESP32 Base Microcontroller (Firmware)
- Deterministic 50Hz hardware loop (20ms interval).
- PCA9685 I2C generation for 5 servos.
- Soft-start / velocity-limited trajectory ramping to prevent high inrush current and gear train wear.
- Real-time analog polling and EMA filtering of the FSR 402 tactile sensor.
- Onboard D-H forward/inverse kinematics engine for low-latency standalone control.

### 2. ROS 2 Serial Bridge (`esp32_bridge.py`)
- Communicates over `/dev/ttyUSB0` at 115200 baud.
- Converts angles between microcontroller degrees and ROS standard radians.
- Broadcasts standard `sensor_msgs/msg/JointState` on `/joint_states`.
- Broadcasts tactile feedback on `/fsr_pressure`.
- Listens for commanded trajectories on `/target_joint_states` and streams them to the ESP32.

### 3. ROS 2 Visualization & Modeling (`astari_selah_description`)
- Provides `astari_selah.urdf.xacro` with exact joint offsets and realistic physical materials.
- Integrates with `robot_state_publisher` and RViz2 for 3D state visualization.
