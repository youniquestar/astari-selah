#include <Arduino.h>
#include "arm_config.h"
#include "kinematics.h"
#include "pca9685_driver.h"
#include "fsr_sensor.h"
#include "telemetry.h"

/**
 * ============================================================================
 * 5-DOF INDUSTRIAL ROBOTIC ARM - MAIN ESP32 BARE-METAL FIRMWARE
 * ============================================================================
 */

// Hardware and algorithm modules
KinematicsEngine kinematics;
PCA9685Driver    servo_driver;
FSRSensor        fsr(ArmConfig::PIN_FSR_ANALOG);
TelemetryManager telemetry;

// Timing control for 50Hz loop
uint32_t last_loop_time_us = 0;
uint32_t last_heartbeat_ms = 0;
bool     led_state = false;

void setup() {
    // 1. Initialize Status LED
    pinMode(ArmConfig::PIN_STATUS_LED, OUTPUT);
    digitalWrite(ArmConfig::PIN_STATUS_LED, HIGH);

    // 2. Initialize USB-Serial Telemetry (115200 baud)
    telemetry.begin(ArmConfig::SERIAL_BAUD_RATE);
    delay(200);
    Serial.println("\n[SYSTEM] Astari Selah: 5-DOF Robotic Arm ESP32 Firmware Initializing...");

    // 3. Initialize Analog Pressure Sensor
    fsr.begin();
    Serial.println("[SYSTEM] FSR 402 Pressure Sensor configured on GPIO 34.");

    // 4. Initialize PCA9685 16-channel PWM Driver
    if (!servo_driver.begin(ArmConfig::PIN_I2C_SDA, ArmConfig::PIN_I2C_SCL)) {
        Serial.println("[ERROR] Failed to initialize PCA9685 via I2C!");
    } else {
        Serial.println("[SYSTEM] PCA9685 PWM Driver active at 50Hz.");
    }

    // 5. Establish Home Pose
    JointAngles home_pose;
    servo_driver.writeJointAnglesImmediate(home_pose);
    Serial.println("[SYSTEM] Manipulator armed at HOME configuration.");
    Serial.printf("[SYSTEM] 50Hz Telemetry active (Period: %d ms).\n", ArmConfig::TELEMETRY_PERIOD_MS);

    last_loop_time_us = micros();
}

void loop() {
    uint32_t current_time_us = micros();
    uint32_t elapsed_us = current_time_us - last_loop_time_us;

    // Fixed 50Hz Loop (20,000 microseconds)
    if (elapsed_us >= (ArmConfig::TELEMETRY_PERIOD_MS * 1000)) {
        float dt = elapsed_us / 1000000.0f;
        last_loop_time_us = current_time_us;

        // 1. Poll incoming commands from ROS 2
        IncomingCommand cmd;
        if (telemetry.checkIncomingCommand(cmd)) {
            if (cmd.type == CommandType::SET_ANGLES) {
                kinematics.clampJointLimits(cmd.target_joints);
                servo_driver.setTargetAngles(cmd.target_joints);
            }
            else if (cmd.type == CommandType::SET_CARTESIAN) {
                JointAngles solved_joints;
                if (kinematics.computeIK(cmd.target_pose, solved_joints)) {
                    servo_driver.setTargetAngles(solved_joints);
                } else {
                    Serial.println("ERR:IK_OUT_OF_REACH");
                }
            }
            else if (cmd.type == CommandType::HOME_ARM) {
                JointAngles home;
                servo_driver.setTargetAngles(home);
            }
        }

        // 2. Poll pressure sensor on claw
        fsr.update();

        // 3. Advance smooth servo trajectory interpolation
        servo_driver.update(dt);

        // 4. Stream 50Hz telemetry back to ROS 2 host
        const JointAngles &current = servo_driver.getCurrentAngles();
        telemetry.streamTelemetry(current, fsr.getFilteredValue());

        // 5. 1Hz Heartbeat LED toggle
        uint32_t now_ms = millis();
        if (now_ms - last_heartbeat_ms >= 500) {
            last_heartbeat_ms = now_ms;
            led_state = !led_state;
            digitalWrite(ArmConfig::PIN_STATUS_LED, led_state ? HIGH : LOW);
        }
    }

    // Yield to FreeRTOS scheduler
    yield();
}
