#pragma once

#include <Arduino.h>
#include "kinematics.h"

/**
 * ============================================================================
 * TELEMETRY & SERIAL PROTOCOL MANAGER (50Hz STREAMING FOR ROS 2 SERIAL BRIDGE)
 * ============================================================================
 */

enum class CommandType {
    NONE,
    SET_ANGLES,
    SET_CARTESIAN,
    HOME_ARM,
    PING
};

struct IncomingCommand {
    CommandType type;
    JointAngles target_joints;
    CartesianPose target_pose;

    IncomingCommand() : type(CommandType::NONE) {}
};

class TelemetryManager {
public:
    TelemetryManager();

    /**
     * Initializes hardware serial port at 115200 baud
     */
    void begin(uint32_t baud = ArmConfig::SERIAL_BAUD_RATE);

    /**
     * Streams joint states and FSR sensor data formatted for ROS 2:
     * Format: "J1:<deg>,J2:<deg>,J3:<deg>,J4:<deg>,J5:<deg>,FSR:<adc>\n"
     */
    void streamTelemetry(const JointAngles &joints, float fsr_val);

    /**
     * Non-blocking parser checking for incoming commands from host ROS 2 bridge
     */
    bool checkIncomingCommand(IncomingCommand &cmd);

private:
    String rx_buffer_;
    bool parseLine(const String &line, IncomingCommand &cmd);
};
