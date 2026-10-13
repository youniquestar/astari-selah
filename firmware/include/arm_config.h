#pragma once

#ifdef ARDUINO
#include <Arduino.h>
#else
#include <cstdint>
#endif

/**
 * ============================================================================
 * ASTARI SELAH: 5-DOF INDUSTRIAL ROBOTIC ARM - EMBEDDED CONFIGURATION
 * ============================================================================
 */

namespace ArmConfig {

// ----------------------------------------------------------------------------
// 1. SERIAL TELEMETRY & CONTROL PROTOCOL
// ----------------------------------------------------------------------------
constexpr uint32_t SERIAL_BAUD_RATE    = 115200;
constexpr uint32_t TELEMETRY_RATE_HZ   = 50;
constexpr uint32_t TELEMETRY_PERIOD_MS = 1000 / TELEMETRY_RATE_HZ; // 20 ms

// ----------------------------------------------------------------------------
// 2. HARDWARE PIN DEFINITIONS (ESP32 NodeMCU)
// ----------------------------------------------------------------------------
constexpr uint8_t PIN_I2C_SDA          = 21;
constexpr uint8_t PIN_I2C_SCL          = 22;
constexpr uint8_t PIN_FSR_ANALOG       = 34; // ADC1 Channel 6 (Input Only)
constexpr uint8_t PIN_STATUS_LED       = 2;  // Onboard blue LED

// ----------------------------------------------------------------------------
// 3. I2C PCA9685 PWM DRIVER CONFIGURATION
// ----------------------------------------------------------------------------
constexpr uint8_t  PCA9685_I2C_ADDR    = 0x40;
constexpr float    PWM_FREQUENCY_HZ    = 50.0f; // Standard analog/digital servo rate (20ms)
constexpr uint32_t PCA9685_RESOLUTION  = 4096;  // 12-bit PWM

// Calibrated microsecond pulse widths for RDS5160 & MG996R servos (0° to 180°)
constexpr uint16_t SERVO_MIN_PULSE_US  = 500;   // 0 degrees (~102 counts at 50Hz)
constexpr uint16_t SERVO_MAX_PULSE_US  = 2500;  // 180 degrees (~512 counts at 50Hz)

// Servo Channel Mapping on PCA9685 Breakout
constexpr uint8_t CH_BASE_YAW          = 0; // DSSERVO RDS5160
constexpr uint8_t CH_SHOULDER_PITCH    = 1; // DSSERVO RDS5160
constexpr uint8_t CH_ELBOW_PITCH       = 2; // TowerPro MG996R
constexpr uint8_t CH_WRIST_PITCH       = 3; // TowerPro MG996R
constexpr uint8_t CH_GRIPPER           = 4; // TowerPro MG996R

// ----------------------------------------------------------------------------
// 4. KINEMATIC DIMENSIONS & REACH (in millimeters)
// Total Extended Reach = 220 + 180 + 60 + 90 = 550.0 mm
// ----------------------------------------------------------------------------
constexpr float LENGTH_BASE_HEIGHT_MM  = 85.0f;  // Base enclosure platform
constexpr float LENGTH_SHOULDER_YOKE_MM= 63.0f;  // Yoke axis offset above platform
constexpr float LENGTH_BASE_TO_SHOULDER= 148.0f; // Global Z height of shoulder pivot
constexpr float LENGTH_UPPER_ARM_MM    = 220.0f; // Link 1 (Upper Arm axis-to-axis)
constexpr float LENGTH_FOREARM_MM      = 180.0f; // Link 2 (Forearm axis-to-axis)
constexpr float LENGTH_WRIST_MM        = 60.0f;  // Link 3 (Wrist axis-to-axis)
constexpr float LENGTH_GRIPPER_MM      = 90.0f;  // End-effector closed jaw tip
constexpr float MAX_ARTICULATED_REACH  = 550.0f; // 55 cm physical maximum

// ----------------------------------------------------------------------------
// 5. SOFTWARE ROTATIONAL LIMITS (in Degrees)
// ----------------------------------------------------------------------------
// Base Yaw: 10° to 170° (Default home: 90°)
constexpr float LIMIT_BASE_YAW_MIN_DEG       = 10.0f;
constexpr float LIMIT_BASE_YAW_MAX_DEG       = 170.0f;
constexpr float HOME_BASE_YAW_DEG            = 90.0f;

// Shoulder Pitch: 45° to 145° (Default home: 90°)
constexpr float LIMIT_SHOULDER_PITCH_MIN_DEG = 45.0f;
constexpr float LIMIT_SHOULDER_PITCH_MAX_DEG = 145.0f;
constexpr float HOME_SHOULDER_PITCH_DEG      = 90.0f;

// Elbow Pitch: 30° to 160° (Never 180° to avoid kinematic singularity)
constexpr float LIMIT_ELBOW_PITCH_MIN_DEG    = 30.0f;
constexpr float LIMIT_ELBOW_PITCH_MAX_DEG    = 160.0f;
constexpr float HOME_ELBOW_PITCH_DEG         = 90.0f;

// Wrist Pitch: 20° to 160° (Default home: 90°)
constexpr float LIMIT_WRIST_PITCH_MIN_DEG    = 20.0f;
constexpr float LIMIT_WRIST_PITCH_MAX_DEG    = 160.0f;
constexpr float HOME_WRIST_PITCH_DEG         = 90.0f;

// Gripper: 15° (closed, 0mm jaw gap) to 75° (fully open, 70mm jaw gap)
constexpr float LIMIT_GRIPPER_MIN_DEG        = 15.0f;
constexpr float LIMIT_GRIPPER_MAX_DEG        = 75.0f;
constexpr float HOME_GRIPPER_DEG             = 45.0f;

// Motion Profiling: Maximum angular speed (°/sec) to avoid mechanical shock
constexpr float MAX_SERVO_VELOCITY_DPS       = 120.0f; // Degrees per second

// ----------------------------------------------------------------------------
// 6. FSR 402 PRESSURE SENSOR CALIBRATION
// ----------------------------------------------------------------------------
constexpr uint32_t ADC_MAX_VALUE             = 4095;   // 12-bit ESP32 ADC
constexpr float    FSR_FILTER_ALPHA          = 0.25f;  // Exponential Moving Average weight
constexpr float    FSR_TOUCH_THRESHOLD_RAW   = 150.0f; // Noise floor threshold

} // namespace ArmConfig
