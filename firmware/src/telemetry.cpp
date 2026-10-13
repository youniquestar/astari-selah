#include "telemetry.h"

TelemetryManager::TelemetryManager() {
    rx_buffer_.reserve(128);
}

void TelemetryManager::begin(uint32_t baud) {
    Serial.begin(baud);
    rx_buffer_ = "";
}

void TelemetryManager::streamTelemetry(const JointAngles &joints, float fsr_val) {
    // Exact format required by ROS 2 esp32_bridge.py node at 50Hz:
    // "J1:90.00,J2:45.00,J3:120.00,J4:90.00,J5:15.00,FSR:850.0\n"
    Serial.printf("J1:%.2f,J2:%.2f,J3:%.2f,J4:%.2f,J5:%.2f,FSR:%.1f\n",
                  joints.q1_base_yaw,
                  joints.q2_shoulder_pitch,
                  joints.q3_elbow_pitch,
                  joints.q4_wrist_pitch,
                  joints.q5_gripper,
                  fsr_val);
}

bool TelemetryManager::checkIncomingCommand(IncomingCommand &cmd) {
    while (Serial.available()) {
        char c = static_cast<char>(Serial.read());
        if (c == '\n' || c == '\r') {
            if (rx_buffer_.length() > 0) {
                bool success = parseLine(rx_buffer_, cmd);
                rx_buffer_ = "";
                if (success) return true;
            }
        } else {
            if (rx_buffer_.length() < 120) {
                rx_buffer_ += c;
            }
        }
    }
    return false;
}

bool TelemetryManager::parseLine(const String &line, IncomingCommand &cmd) {
    // 1. Home Command: "CMD:HOME"
    if (line.equalsIgnoreCase("CMD:HOME")) {
        cmd.type = CommandType::HOME_ARM;
        cmd.target_joints = JointAngles();
        return true;
    }

    // 2. Ping Command: "CMD:PING"
    if (line.equalsIgnoreCase("CMD:PING")) {
        cmd.type = CommandType::PING;
        Serial.println("ACK:PONG");
        return true;
    }

    // 3. Set Joint Angles: "CMD:ANGLES,<j1>,<j2>,<j3>,<j4>,<j5>"
    if (line.startsWith("CMD:ANGLES,")) {
        float j1, j2, j3, j4, j5;
        int parsed = sscanf(line.c_str(), "CMD:ANGLES,%f,%f,%f,%f,%f", &j1, &j2, &j3, &j4, &j5);
        if (parsed == 5) {
            cmd.type = CommandType::SET_ANGLES;
            cmd.target_joints = JointAngles(j1, j2, j3, j4, j5);
            return true;
        }
    }

    // 4. Set Cartesian IK: "CMD:IK,<x>,<y>,<z>,<pitch>,<grip_gap>"
    if (line.startsWith("CMD:IK,")) {
        float x, y, z, p, g;
        int parsed = sscanf(line.c_str(), "CMD:IK,%f,%f,%f,%f,%f", &x, &y, &z, &p, &g);
        if (parsed == 5) {
            cmd.type = CommandType::SET_CARTESIAN;
            cmd.target_pose = CartesianPose(x, y, z, p, g);
            return true;
        }
    }

    return false;
}
