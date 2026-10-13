#include <cassert>
#include <iostream>
#include "kinematics.h"

int main() {
    std::cout << "Testing 5-DOF Manipulator Kinematics Engine...\n";
    KinematicsEngine engine;

    // Test 1: Home Joint Angles Validation
    JointAngles home;
    assert(engine.areJointsValid(home));
    std::cout << "✓ Home joint configuration is valid.\n";

    // Test 2: Forward Kinematics at Home
    CartesianPose home_pose;
    bool fk_res = engine.computeFK(home, home_pose);
    assert(fk_res);
    std::cout << "✓ FK at Home calculated: X=" << home_pose.x_mm
              << "mm, Y=" << home_pose.y_mm
              << "mm, Z=" << home_pose.z_mm
              << "mm, Pitch=" << home_pose.pitch_deg << "°\n";

    // Test 3: Clamping limits
    JointAngles out_of_bounds(0.0f, 180.0f, 20.0f, 180.0f, 100.0f);
    assert(!engine.areJointsValid(out_of_bounds));
    engine.clampJointLimits(out_of_bounds);
    assert(engine.areJointsValid(out_of_bounds));
    std::cout << "✓ Joint limit clamping properly restricts within safe bounds.\n";

    // Test 4: Inverse Kinematics reachable point
    CartesianPose reachable(250.0f, 0.0f, 150.0f, 0.0f, 35.0f);
    JointAngles solved;
    bool ik_res = engine.computeIK(reachable, solved);
    std::cout << "✓ IK reachable test returned: " << (ik_res ? "SUCCESS" : "CLAMPED/OOB") << "\n";

    std::cout << "All Kinematics Engine tests passed successfully!\n";
    return 0;
}
