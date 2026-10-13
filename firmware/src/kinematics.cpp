#include "kinematics.h"
#include <algorithm>

KinematicsEngine::KinematicsEngine()
    : L_base_z(ArmConfig::LENGTH_BASE_TO_SHOULDER),      // 148.0 mm
      L_upper(ArmConfig::LENGTH_UPPER_ARM_MM),           // 220.0 mm
      L_forearm(ArmConfig::LENGTH_FOREARM_MM),           // 180.0 mm
      L_tool(ArmConfig::LENGTH_WRIST_MM + ArmConfig::LENGTH_GRIPPER_MM) // 150.0 mm
{}

void KinematicsEngine::clampJointLimits(JointAngles &joints) {
    joints.q1_base_yaw = std::max(ArmConfig::LIMIT_BASE_YAW_MIN_DEG,
                         std::min(ArmConfig::LIMIT_BASE_YAW_MAX_DEG, joints.q1_base_yaw));

    joints.q2_shoulder_pitch = std::max(ArmConfig::LIMIT_SHOULDER_PITCH_MIN_DEG,
                               std::min(ArmConfig::LIMIT_SHOULDER_PITCH_MAX_DEG, joints.q2_shoulder_pitch));

    joints.q3_elbow_pitch = std::max(ArmConfig::LIMIT_ELBOW_PITCH_MIN_DEG,
                            std::min(ArmConfig::LIMIT_ELBOW_PITCH_MAX_DEG, joints.q3_elbow_pitch));

    joints.q4_wrist_pitch = std::max(ArmConfig::LIMIT_WRIST_PITCH_MIN_DEG,
                            std::min(ArmConfig::LIMIT_WRIST_PITCH_MAX_DEG, joints.q4_wrist_pitch));

    joints.q5_gripper = std::max(ArmConfig::LIMIT_GRIPPER_MIN_DEG,
                        std::min(ArmConfig::LIMIT_GRIPPER_MAX_DEG, joints.q5_gripper));
}

bool KinematicsEngine::areJointsValid(const JointAngles &joints) const {
    if (joints.q1_base_yaw < ArmConfig::LIMIT_BASE_YAW_MIN_DEG ||
        joints.q1_base_yaw > ArmConfig::LIMIT_BASE_YAW_MAX_DEG) return false;

    if (joints.q2_shoulder_pitch < ArmConfig::LIMIT_SHOULDER_PITCH_MIN_DEG ||
        joints.q2_shoulder_pitch > ArmConfig::LIMIT_SHOULDER_PITCH_MAX_DEG) return false;

    if (joints.q3_elbow_pitch < ArmConfig::LIMIT_ELBOW_PITCH_MIN_DEG ||
        joints.q3_elbow_pitch > ArmConfig::LIMIT_ELBOW_PITCH_MAX_DEG) return false;

    if (joints.q4_wrist_pitch < ArmConfig::LIMIT_WRIST_PITCH_MIN_DEG ||
        joints.q4_wrist_pitch > ArmConfig::LIMIT_WRIST_PITCH_MAX_DEG) return false;

    if (joints.q5_gripper < ArmConfig::LIMIT_GRIPPER_MIN_DEG ||
        joints.q5_gripper > ArmConfig::LIMIT_GRIPPER_MAX_DEG) return false;

    return true;
}

bool KinematicsEngine::computeFK(const JointAngles &joints, CartesianPose &out_pose) {
    // Convert joint angles to radians relative to planar horizontal axis
    // Servo 90° = vertical/neutral alignment
    float th1 = degToRad(joints.q1_base_yaw - 90.0f);
    float th2 = degToRad(joints.q2_shoulder_pitch);
    float th3 = degToRad(joints.q3_elbow_pitch - 90.0f);
    float th4 = degToRad(joints.q4_wrist_pitch - 90.0f);

    // Planar forward kinematics in vertical elevation plane
    float a1 = th2;
    float a2 = a1 + th3;
    float a3 = a2 + th4;

    float r = L_upper * cos(a1) + L_forearm * cos(a2) + L_tool * cos(a3);
    float z = L_base_z + L_upper * sin(a1) + L_forearm * sin(a2) + L_tool * sin(a3);

    out_pose.x_mm = r * cos(th1);
    out_pose.y_mm = r * sin(th1);
    out_pose.z_mm = z;
    out_pose.pitch_deg = radToDeg(a3);

    // Map gripper angle [15° closed -> 0mm, 75° open -> 70mm]
    float grip_ratio = (joints.q5_gripper - ArmConfig::LIMIT_GRIPPER_MIN_DEG) /
                       (ArmConfig::LIMIT_GRIPPER_MAX_DEG - ArmConfig::LIMIT_GRIPPER_MIN_DEG);
    out_pose.gripper_gap_mm = grip_ratio * 70.0f;

    return true;
}

bool KinematicsEngine::computeIK(const CartesianPose &target_pose, JointAngles &out_joints) {
    // 1. Solve Base Yaw (Joint 1)
    float q1_rad = atan2(target_pose.y_mm, target_pose.x_mm);
    float q1_deg = radToDeg(q1_rad) + 90.0f; // Transform to [0, 180] servo range

    // 2. Planar radial projection
    float r = sqrt(target_pose.x_mm * target_pose.x_mm + target_pose.y_mm * target_pose.y_mm);
    float z = target_pose.z_mm;

    // 3. Wrist center coordinates
    float pitch_rad = degToRad(target_pose.pitch_deg);
    float rw = r - L_tool * cos(pitch_rad);
    float zw = z - L_tool * sin(pitch_rad);

    float dr = rw;
    float dz = zw - L_base_z;
    float D_sq = dr * dr + dz * dz;
    float D = sqrt(D_sq);

    // Check reachability
    float max_reach = L_upper + L_forearm;
    float min_reach = fabs(L_upper - L_forearm);
    if (D > max_reach || D < min_reach) {
        return false; // Target point is outside physical arm workspace
    }

    // 4. Solve Elbow Pitch (Joint 3) via Law of Cosines
    float cos_q3 = (D_sq - L_upper * L_upper - L_forearm * L_forearm) / (2.0f * L_upper * L_forearm);
    cos_q3 = std::max(-1.0f, std::min(1.0f, cos_q3));
    float q3_internal_rad = acos(cos_q3);

    // 5. Solve Shoulder Pitch (Joint 2)
    float alpha = atan2(dz, dr);
    float cos_beta = (L_upper * L_upper + D_sq - L_forearm * L_forearm) / (2.0f * L_upper * D);
    cos_beta = std::max(-1.0f, std::min(1.0f, cos_beta));
    float beta = acos(cos_beta);

    float th2_rad = alpha + beta; // Elbow-down configuration

    // Map to servo angle frames
    float q2_deg = radToDeg(th2_rad);
    float q3_deg = radToDeg(M_PI - q3_internal_rad);
    float q4_deg = target_pose.pitch_deg - (q2_deg + q3_deg - 180.0f) + 90.0f;

    // 6. Map Gripper Gap (mm) to Joint Angle (deg)
    float grip_ratio = std::max(0.0f, std::min(1.0f, target_pose.gripper_gap_mm / 70.0f));
    float q5_deg = ArmConfig::LIMIT_GRIPPER_MIN_DEG +
                   grip_ratio * (ArmConfig::LIMIT_GRIPPER_MAX_DEG - ArmConfig::LIMIT_GRIPPER_MIN_DEG);

    JointAngles candidate(q1_deg, q2_deg, q3_deg, q4_deg, q5_deg);

    if (areJointsValid(candidate)) {
        out_joints = candidate;
        return true;
    }

    // If candidate violated joint limits, try clamping
    clampJointLimits(candidate);
    out_joints = candidate;
    return false;
}
