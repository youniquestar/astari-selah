#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
import time

class ArmTester(Node):
    def __init__(self):
        super().__init__('arm_tester')
        self.arm_pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        self.gripper_pub = self.create_publisher(
            JointTrajectory,
            '/gripper_controller/joint_trajectory',
            10
        )
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_cb,
            10
        )
        self.latest_joint_state = None
        self.get_logger().info("ArmTester initialized.")

    def joint_state_cb(self, msg):
        self.latest_joint_state = msg

    def send_arm_trajectory(self):
        msg = JointTrajectory()
        msg.joint_names = [
            'joint1_base_yaw',
            'joint2_shoulder_pitch',
            'joint3_elbow_pitch',
            'joint4_wrist_pitch'
        ]
        point = JointTrajectoryPoint()
        # Move to home position: J1=90 deg (1.5708), J2=45 deg (0.7854), J3=60 deg (1.0472), J4=0 deg
        point.positions = [1.5708, 0.7854, 1.0472, 0.0]
        point.velocities = [0.0, 0.0, 0.0, 0.0]
        point.time_from_start.sec = 2
        msg.points.append(point)

        self.arm_pub.publish(msg)
        self.get_logger().info(f"Published arm trajectory to target: {point.positions}")

    def send_gripper_command(self, open_rad=0.5):
        msg = JointTrajectory()
        msg.joint_names = ['joint5_gripper_left']
        point = JointTrajectoryPoint()
        point.positions = [open_rad]
        point.time_from_start.sec = 1
        msg.points.append(point)

        self.gripper_pub.publish(msg)
        self.get_logger().info(f"Published gripper trajectory to target: {point.positions}")

def main():
    rclpy.init()
    node = ArmTester()

    # Wait for subscribers to connect
    start = time.time()
    while time.time() - start < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)
        if node.arm_pub.get_subscription_count() > 0 and node.gripper_pub.get_subscription_count() > 0:
            break

    node.get_logger().info(f"Arm pub connected: {node.arm_pub.get_subscription_count()} subs")
    node.get_logger().info(f"Gripper pub connected: {node.gripper_pub.get_subscription_count()} subs")

    # Send trajectories
    node.send_arm_trajectory()
    node.send_gripper_command(0.4)

    # Spin to monitor response
    start = time.time()
    while time.time() - start < 3.0:
        rclpy.spin_once(node, timeout_sec=0.1)

    if node.latest_joint_state:
        node.get_logger().info(f"Latest joint states:\n  Names: {list(node.latest_joint_state.name)}\n  Positions: {[round(p, 4) for p in node.latest_joint_state.position]}")
    else:
        node.get_logger().warn("No joint states received.")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
