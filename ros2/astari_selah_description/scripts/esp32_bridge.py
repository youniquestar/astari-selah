#!/usr/bin/env python3
"""
================================================================================
5-DOF ROBOTIC ARM — ROS 2 HARDWARE BRIDGE NODE (ESP32 <-> ROS 2)
================================================================================
Interfaces the ESP32 bare-metal microcontroller with the ROS 2 ecosystem.
- Reads 50Hz telemetry packets: J1:<deg>,J2:<deg>,J3:<deg>,J4:<deg>,J5:<deg>,FSR:<val>
- Converts degrees to radians
- Publishes sensor_msgs/msg/JointState to /joint_states
- Publishes std_msgs/msg/Float32 to /fsr_pressure
- Subscribes to /target_joint_states and commands the ESP32 over serial
================================================================================
"""

import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32, Header

try:
    import serial
except ImportError:
    serial = None


class ESP32BridgeNode(Node):
    def __init__(self):
        super().__init__('esp32_bridge')

        # Declare parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baud', 115200)
        self.declare_parameter('simulation_fallback', True)

        self.port_name = self.get_parameter('port').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud').get_parameter_value().integer_value
        self.simulation_fallback = self.get_parameter('simulation_fallback').get_parameter_value().bool_value

        # Joint name mapping matching URDF definition
        self.joint_names = [
            'joint1_base_yaw',
            'joint2_shoulder_pitch',
            'joint3_elbow_pitch',
            'joint4_wrist_pitch',
            'joint5_gripper_left',
        ]

        # Publishers
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.fsr_pub = self.create_publisher(Float32, '/fsr_pressure', 10)

        # Subscriber for target joint commands
        self.sub_target = self.create_subscription(
            JointState,
            '/target_joint_states',
            self.target_joint_callback,
            10
        )

        self.serial_conn = None
        self.sim_time = 0.0
        self.connect_serial()

        # 50 Hz timer loop (20 ms interval)
        self.timer = self.create_timer(0.02, self.timer_callback)
        self.get_logger().info(f'ESP32 Bridge initialized on port {self.port_name} at {self.baud_rate} baud.')

    def connect_serial(self):
        if serial is None:
            self.get_logger().warn('pyserial not installed! Running in simulation mode.')
            return

        try:
            self.serial_conn = serial.Serial(
                port=self.port_name,
                baudrate=self.baud_rate,
                timeout=0.05
            )
            self.get_logger().info(f'Successfully connected to ESP32 on {self.port_name}')
        except Exception as e:
            if self.simulation_fallback:
                self.get_logger().warn(
                    f'Could not open {self.port_name} ({e}). Fallback to simulation telemetry loop.'
                )
                self.serial_conn = None
            else:
                self.get_logger().error(f'Failed to open serial port: {e}')

    def target_joint_callback(self, msg: JointState):
        """Send target joint commands from ROS 2 to the ESP32 microcontroller."""
        if not self.serial_conn or not self.serial_conn.is_open:
            return

        # Find angles in radians, convert to degrees
        joint_dict = dict(zip(msg.name, msg.position))
        j1 = math.degrees(joint_dict.get('joint1_base_yaw', 1.5708))
        j2 = math.degrees(joint_dict.get('joint2_shoulder_pitch', 1.5708))
        j3 = math.degrees(joint_dict.get('joint3_elbow_pitch', 1.5708))
        j4 = math.degrees(joint_dict.get('joint4_wrist_pitch', 1.5708))
        j5 = math.degrees(joint_dict.get('joint5_gripper_left', 0.7854))

        cmd_str = f'CMD:ANGLES,{j1:.2f},{j2:.2f},{j3:.2f},{j4:.2f},{j5:.2f}\n'
        try:
            self.serial_conn.write(cmd_str.encode('ascii'))
        except Exception as e:
            self.get_logger().error(f'Error writing to serial: {e}')

    def timer_callback(self):
        now = self.get_clock().now()

        # Mode A: Hardware Serial Connection
        if self.serial_conn and self.serial_conn.is_open:
            try:
                while self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith('J1:'):
                        self.parse_and_publish_line(line, now)
            except Exception as e:
                self.get_logger().error(f'Serial communication error: {e}')
                self.serial_conn = None
            return

        # Mode B: Simulation Fallback Telemetry (if hardware not plugged in)
        if self.simulation_fallback:
            self.sim_time += 0.02
            # Generate gentle sinusoidal motions around neutral home positions
            q1 = math.radians(90.0 + 20.0 * math.sin(self.sim_time * 0.5))
            q2 = math.radians(90.0 + 15.0 * math.cos(self.sim_time * 0.7))
            q3 = math.radians(90.0 + 20.0 * math.sin(self.sim_time * 0.6))
            q4 = math.radians(90.0 + 15.0 * math.cos(self.sim_time * 0.8))
            q5 = math.radians(45.0 + 15.0 * math.sin(self.sim_time * 1.0))
            fsr_val = max(0.0, 300.0 + 200.0 * math.sin(self.sim_time))

            js_msg = JointState()
            js_msg.header = Header(stamp=now.to_msg(), frame_id='base_link')
            js_msg.name = self.joint_names
            js_msg.position = [q1, q2, q3, q4, q5]
            self.joint_pub.publish(js_msg)

            fsr_msg = Float32(data=float(fsr_val))
            self.fsr_pub.publish(fsr_msg)

    def parse_and_publish_line(self, line: str, timestamp):
        """Parse 'J1:90.00,J2:45.00,J3:120.00,J4:90.00,J5:15.00,FSR:850.0'"""
        try:
            parts = line.split(',')
            data = {}
            for item in parts:
                k, v = item.split(':')
                data[k.strip()] = float(v.strip())

            # Convert angles to radians
            q1 = math.radians(data.get('J1', 90.0))
            q2 = math.radians(data.get('J2', 90.0))
            q3 = math.radians(data.get('J3', 90.0))
            q4 = math.radians(data.get('J4', 90.0))
            q5 = math.radians(data.get('J5', 45.0))
            fsr = data.get('FSR', 0.0)

            js_msg = JointState()
            js_msg.header = Header(stamp=timestamp.to_msg(), frame_id='base_link')
            js_msg.name = self.joint_names
            js_msg.position = [q1, q2, q3, q4, q5]
            self.joint_pub.publish(js_msg)

            fsr_msg = Float32(data=float(fsr))
            self.fsr_pub.publish(fsr_msg)

        except Exception as e:
            self.get_logger().debug(f'Malformed telemetry string: {line} ({e})')


def main(args=None):
    rclpy.init(args=args)
    node = ESP32BridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.serial_conn and node.serial_conn.is_open:
            node.serial_conn.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
