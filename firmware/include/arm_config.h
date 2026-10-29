#pragma once

#ifdef ARDUINO
#include <Arduino.h>
#else
#include <cstdint>
#endif

/**
 * ============================================================================
 * ASTARI SELAH: 70 CM HYBRID STEPPER-SERVO ROBOTIC ARM - EMBEDDED CONFIGURATION
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

// Stepper Step/Dir/Enable Pin Definitions (TMC2209 / TB6600 Drivers)
constexpr uint8_t PIN_STEPPER_ENABLE   = 32; // Shared Active-Low Driver Enable
constexpr uint8_t PIN_J1_STEP          = 25; // Base Yaw Stepper Step
constexpr uint8_t PIN_J1_DIR           = 26; // Base Yaw Stepper Dir
constexpr uint8_t PIN_J2_STEP          = 27; // Shoulder Pitch Stepper Step
constexpr uint8_t PIN_J2_DIR           = 14; // Shoulder Pitch Stepper Dir
constexpr uint8_t PIN_J3_STEP          = 12; // Elbow Pitch Stepper Step
constexpr uint8_t PIN_J3_DIR           = 13; // Elbow Pitch Stepper Dir

// Stepper Microstep Calibration (1.8° steppers @ 16 microsteps = 3200 steps/rev)
// Joint 1: 10:1 Planetary Gearbox -> 32,000 steps / 360° = 88.889 steps/deg
constexpr float STEPS_PER_DEG_J1       = 88.8889f;
// Joint 2: 10:1 Planetary Gearbox -> 32,000 steps / 360° = 88.889 steps/deg
constexpr float STEPS_PER_DEG_J2       = 88.8889f;
// Joint 3: 5:1 Planetary Gearbox  -> 16,000 steps / 360° = 44.444 steps/deg
constexpr float STEPS_PER_DEG_J3       = 44.4444f;

// ----------------------------------------------------------------------------
// 3. I2C PCA9685 PWM DRIVER CONFIGURATION (For Distal J4 & J5 Servos)
// ----------------------------------------------------------------------------
constexpr uint8_t  PCA9685_I2C_ADDR    = 0x40;
constexpr float    PWM_FREQUENCY_HZ    = 50.0f; // 20ms period
constexpr uint32_t PCA9685_RESOLUTION  = 4096;  // 12-bit PWM

constexpr uint16_t SERVO_MIN_PULSE_US  = 500;   // 0 degrees (~102 counts at 50Hz)
constexpr uint16_t SERVO_MAX_PULSE_US  = 2500;  // 180 degrees (~512 counts at 50Hz)

constexpr uint8_t CH_WRIST_PITCH       = 0; // TowerPro MG996R (J4)
constexpr uint8_t CH_GRIPPER           = 1; // TowerPro MG996R (J5)

// ----------------------------------------------------------------------------
// 4. KINEMATIC DIMENSIONS & REACH (in millimeters)
// Total Articulated Reach = 280 + 230 + 90 + 100 = 700.0 mm
// ----------------------------------------------------------------------------
constexpr float LENGTH_BASE_HEIGHT_MM  = 90.0f;  // Base enclosure platform (d1)
constexpr float LENGTH_SHOULDER_YOKE_MM= 70.0f;  // Yoke axis offset above platform
constexpr float LENGTH_BASE_TO_SHOULDER= 160.0f; // Global Z height of shoulder pivot
constexpr float LENGTH_UPPER_ARM_MM    = 280.0f; // Link 1: Upper Arm axis-to-axis (a2)
constexpr float LENGTH_FOREARM_MM      = 230.0f; // Link 2: Forearm axis-to-axis (a3)
constexpr float LENGTH_WRIST_MM        = 90.0f;  // Link 3: Wrist axis-to-axis (a4)
constexpr float LENGTH_GRIPPER_MM      = 100.0f; // Link 4: End-effector closed jaw tip (a5)

constexpr float MAX_WORKSPACE_RADIUS_MM= 700.0f;
constexpr float MIN_WORKSPACE_RADIUS_MM= 120.0f;

// ----------------------------------------------------------------------------
// 5. JOINT SOFTWARE BOUNDARIES & CALIBRATED TRAVEL LIMITS (in Degrees)
// ----------------------------------------------------------------------------
constexpr float LIMIT_MIN_BASE_YAW     = 10.0f;
constexpr float LIMIT_MAX_BASE_YAW     = 170.0f;
constexpr float HOME_BASE_YAW_DEG      = 90.0f;

constexpr float LIMIT_MIN_SHOULDER     = 0.0f;   // Horizontal forward
constexpr float LIMIT_MAX_SHOULDER     = 90.0f;  // Vertical upright
constexpr float HOME_SHOULDER_PITCH_DEG= 90.0f;

constexpr float LIMIT_MIN_ELBOW        = 0.0f;   // Straight extension
constexpr float LIMIT_MAX_ELBOW        = 120.0f; // Bent
constexpr float HOME_ELBOW_PITCH_DEG   = 45.0f;

constexpr float LIMIT_MIN_WRIST        = -90.0f;
constexpr float LIMIT_MAX_WRIST        = 90.0f;
constexpr float HOME_WRIST_PITCH_DEG   = 0.0f;

constexpr float LIMIT_MIN_GRIPPER      = 0.0f;   // Closed (0 mm gap)
constexpr float LIMIT_MAX_GRIPPER      = 45.0f;  // Fully Open (80 mm gap)
constexpr float HOME_GRIPPER_DEG       = 0.0f;

// ----------------------------------------------------------------------------
// 6. FSR 402 FORCE SENSING RESISTOR CALIBRATION
// ----------------------------------------------------------------------------
constexpr uint16_t FSR_ADC_NO_LOAD     = 50;
constexpr uint16_t FSR_ADC_MAX_LOAD    = 4095;
constexpr float    FSR_MAX_FORCE_NEWTONS= 20.0f;

} // namespace ArmConfig
