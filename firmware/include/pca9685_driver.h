#pragma once

#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>
#include "arm_config.h"
#include "kinematics.h"

/**
 * ============================================================================
 * PCA9685 16-CHANNEL I2C PWM SERVO DRIVER INTERFACE WITH TRAJECTORY SMOOTHING
 * ============================================================================
 */

class PCA9685Driver {
public:
    PCA9685Driver();

    /**
     * Initializes Wire I2C communication and sets PCA9685 PWM frequency to 50Hz.
     */
    bool begin(uint8_t sda_pin = ArmConfig::PIN_I2C_SDA,
               uint8_t scl_pin = ArmConfig::PIN_I2C_SCL,
               uint8_t i2c_addr = ArmConfig::PCA9685_I2C_ADDR);

    /**
     * Directly writes target angles to all servos without interpolation.
     */
    void writeJointAnglesImmediate(const JointAngles &angles);

    /**
     * Sets target angles for smooth ramped interpolation.
     */
    void setTargetAngles(const JointAngles &target);

    /**
     * Call cyclically (e.g., at 50Hz) to advance interpolated motion smoothly.
     * Prevents current surges and violent mechanical jerk.
     */
    void update(float dt_seconds);

    /**
     * Get currently commanded/interpolated joint positions.
     */
    const JointAngles& getCurrentAngles() const { return current_angles_; }

    /**
     * Convert angle in degrees [0, 180] to 12-bit PCA9685 pulse count [0, 4095].
     */
    uint16_t angleToTicks(float angle_deg);

private:
    Adafruit_PWMServoDriver pwm_driver_;
    JointAngles current_angles_;
    JointAngles target_angles_;
    bool is_initialized_;

    void writeChannelPulse(uint8_t channel, uint16_t pulse_ticks);
    float stepToward(float current, float target, float max_step);
};
