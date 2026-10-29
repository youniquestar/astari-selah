#include "kinematics.h"
#include <algorithm>

KinematicsEngine::KinematicsEngine()
    : L_base_z(ArmConfig::LENGTH_BASE_TO_SHOULDER),      // 160.0 mm
      L_upper(ArmConfig::LENGTH_UPPER_ARM_MM),           // 280.0 mm
      L_forearm(ArmConfig::LENGTH_FOREARM_MM),           // 230.0 mm
      L_tool(ArmConfig::LENGTH_WRIST_MM + ArmConfig::LENGTH_GRIPPER_MM) // 190.0 mm
{}

void KinematicsEngine::clampJointLimits(JointAngles &joints) {
    joints.q1_base_yaw = std::max(ArmConfig::LIMIT_MIN_BASE_YAW,
                         std::min(ArmConfig::LIMIT_MAX_BASE_YAW, joints.q1_base_yaw));

    joints.q2_shoulder_pitch = std::max(ArmConfig::LIMIT_MIN_SHOULDER,
                               std::min(ArmConfig::LIMIT_MAX_SHOULDER, joints.q2_shoulder_pitch));

    joints.q3_elbow_pitch = std::max(ArmConfig::LIMIT_MIN_ELBOW,
                            std::min(ArmConfig::LIMIT_MAX_ELBOW, joints.q3_elbow_pitch));

    joints.q4_wrist_pitch = std::max(ArmConfig::LIMIT_MIN_WRIST,
                            std::min(ArmConfig::LIMIT_MAX_WRIST, joints.q4_wrist_pitch));

    joints.q5_gripper = std::max(ArmConfig::LIMIT_MIN_GRIPPER,
                        std::min(ArmConfig::LIMIT_MAX_GRIPPER, joints.q5_gripper));
}

bool KinematicsEngine::areJointsValid(const JointAngles &joints) const {
    if (joints.q1_base_yaw < ArmConfig::LIMIT_MIN_BASE_YAW ||
        joints.q1_base_yaw > ArmConfig::LIMIT_MAX_BASE_YAW) return false;

    if (joints.q2_shoulder_pitch < ArmConfig::LIMIT_MIN_SHOULDER ||
        joints.q2_shoulder_pitch > ArmConfig::LIMIT_MAX_SHOULDER) return false;

    if (joints.q3_elbow_pitch < ArmConfig::LIMIT_MIN_ELBOW ||
        joints.q3_elbow_pitch > ArmConfig::LIMIT_MAX_ELBOW) return false;

    if (joints.q4_wrist_pitch < ArmConfig::LIMIT_MIN_WRIST ||
        joints.q4_wrist_pitch > ArmConfig::LIMIT_MAX_WRIST) return false;

    if (joints.q5_gripper < ArmConfig::LIMIT_MIN_GRIPPER ||
        joints.q5_gripper > ArmConfig::LIMIT_MAX_GRIPPER) return false;

    return true;
}

bool KinematicsEngine::computeFK(const JointAngles &joints, CartesianPose &out_pose) {
    float th1 = degToRad(joints.q1_base_yaw - 90.0f);
    float th2 = degToRad(joints.q2_shoulder_pitch);
    float th3 = degToRad(joints.q3_elbow_pitch - 90.0f);
    float th4 = degToRad(joints.q4_wrist_pitch);

    float a1 = th2;
    float a2 = a1 + th3;
    float a3 = a2 + th4;

    float r = L_upper * cosf(a1) + L_forearm * cosf(a2) + L_tool * cosf(a3);
    float z = L_base_z + L_upper * sinf(a1) + L_forearm * sinf(a2) + L_tool * sinf(a3);

    out_pose.x_mm = r * cosf(th1);
    out_pose.y_mm = r * sinf(th1);
    out_pose.z_mm = z;
    out_pose.pitch_deg = radToDeg(a3);
    out_pose.gripper_gap_mm = (joints.q5_gripper / ArmConfig::LIMIT_MAX_GRIPPER) * 80.0f;

    return true;
}

bool KinematicsEngine::computeIK(const CartesianPose &target_pose, JointAngles &out_joints) {
    float x = target_pose.x_mm;
    float y = target_pose.y_mm;
    float z = target_pose.z_mm;
    float pitch_rad = degToRad(target_pose.pitch_deg);

    // 1. Joint 1 Base Yaw
    float q1_deg = radToDeg(atan2f(y, x)) + 90.0f;

    // 2. Projected radial distance in horizontal plane
    float r = sqrtf(x * x + y * y);

    // Clamp workspace reach
    if (r > ArmConfig::MAX_WORKSPACE_RADIUS_MM || r < ArmConfig::MIN_WORKSPACE_RADIUS_MM) {
        return false;
    }

    // 3. Wrist Pivot location (subtract tool segment)
    float r_w = r - L_tool * cosf(pitch_rad);
    float z_w = z - L_base_z - L_tool * sinf(pitch_rad);

    float d_sq = r_w * r_w + z_w * z_w;
    float d = sqrtf(d_sq);

    // Reachable workspace check for 2-link planar arm
    if (d > (L_upper + L_forearm) || d < fabsf(L_upper - L_forearm)) {
        return false;
    }

    // 4. Joint 3 (Elbow) Law of Cosines
    float cos_q3 = (d_sq - L_upper * L_upper - L_forearm * L_forearm) / (2.0f * L_upper * L_forearm);
    cos_q3 = std::max(-1.0f, std::min(1.0f, cos_q3));
    float q3_rad = acosf(cos_q3); // Elbow up

    // 5. Joint 2 (Shoulder)
    float alpha = atan2f(z_w, r_w);
    float beta = atan2f(L_forearm * sinf(q3_rad), L_upper + L_forearm * cosf(q3_rad));
    float q2_rad = alpha + beta;

    // 6. Joint 4 (Wrist Pitch)
    float q4_rad = pitch_rad - (q2_rad - q3_rad);

    out_joints.q1_base_yaw = q1_deg;
    out_joints.q2_shoulder_pitch = radToDeg(q2_rad);
    out_joints.q3_elbow_pitch = radToDeg(q3_rad) + 90.0f;
    out_joints.q4_wrist_pitch = radToDeg(q4_rad);
    out_joints.q5_gripper = (target_pose.gripper_gap_mm / 80.0f) * ArmConfig::LIMIT_MAX_GRIPPER;

    clampJointLimits(out_joints);
    return areJointsValid(out_joints);
}
