#pragma once

#include <cmath>
#include "arm_config.h"

/**
 * ============================================================================
 * 5-DOF MANIPULATOR FORWARD & INVERSE KINEMATICS ENGINE (D-H ANALYTICAL SOLVER)
 * ============================================================================
 */

struct JointAngles {
    float q1_base_yaw;       // Degrees [10, 170]
    float q2_shoulder_pitch; // Degrees [45, 145]
    float q3_elbow_pitch;    // Degrees [30, 160]
    float q4_wrist_pitch;    // Degrees [20, 160]
    float q5_gripper;        // Degrees [15, 75]

    JointAngles()
        : q1_base_yaw(ArmConfig::HOME_BASE_YAW_DEG),
          q2_shoulder_pitch(ArmConfig::HOME_SHOULDER_PITCH_DEG),
          q3_elbow_pitch(ArmConfig::HOME_ELBOW_PITCH_DEG),
          q4_wrist_pitch(ArmConfig::HOME_WRIST_PITCH_DEG),
          q5_gripper(ArmConfig::HOME_GRIPPER_DEG) {}

    JointAngles(float j1, float j2, float j3, float j4, float j5)
        : q1_base_yaw(j1), q2_shoulder_pitch(j2),
          q3_elbow_pitch(j3), q4_wrist_pitch(j4), q5_gripper(j5) {}
};

struct CartesianPose {
    float x_mm;             // Millimeters in robot base frame
    float y_mm;
    float z_mm;
    float pitch_deg;        // Tool orientation pitch relative to horizontal
    float gripper_gap_mm;   // Jaw opening width [0, 70 mm]

    CartesianPose() : x_mm(250.0f), y_mm(0.0f), z_mm(150.0f), pitch_deg(0.0f), gripper_gap_mm(35.0f) {}
    CartesianPose(float x, float y, float z, float p, float g)
        : x_mm(x), y_mm(y), z_mm(z), pitch_deg(p), gripper_gap_mm(g) {}
};

class KinematicsEngine {
public:
    KinematicsEngine();

    /**
     * Compute Forward Kinematics (FK)
     * Maps joint angles -> End-effector tip Cartesian coordinates (X, Y, Z, Pitch)
     */
    bool computeFK(const JointAngles &joints, CartesianPose &out_pose);

    /**
     * Compute Inverse Kinematics (IK)
     * Maps desired end-effector pose -> Joint angles
     * Returns true if a valid kinematic solution within software limits was found.
     */
    bool computeIK(const CartesianPose &target_pose, JointAngles &out_joints);

    /**
     * Enforces physical joint limits, preventing servo and linkage collisions.
     */
    void clampJointLimits(JointAngles &joints);

    /**
     * Checks if joint angles are within valid safe boundaries.
     */
    bool areJointsValid(const JointAngles &joints) const;

    /**
     * Convert degrees to radians and vice-versa
     */
    static inline float degToRad(float deg) { return deg * (M_PI / 180.0f); }
    static inline float radToDeg(float rad) { return rad * (180.0f / M_PI); }

private:
    float L_base_z;   // 148.0 mm (Base + Yoke height to shoulder axis)
    float L_upper;    // 220.0 mm (Link 1)
    float L_forearm;  // 180.0 mm (Link 2)
    float L_tool;     // 150.0 mm (Wrist 60mm + Gripper 90mm)
};
