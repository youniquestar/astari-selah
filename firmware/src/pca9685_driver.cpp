#include "pca9685_driver.h"
#include <Wire.h>

PCA9685Driver::PCA9685Driver()
    : pwm_driver_(ArmConfig::PCA9685_I2C_ADDR),
      is_initialized_(false)
{}

bool PCA9685Driver::begin(uint8_t sda_pin, uint8_t scl_pin, uint8_t i2c_addr) {
    Wire.begin(sda_pin, scl_pin);
    pwm_driver_ = Adafruit_PWMServoDriver(i2c_addr, Wire);
    pwm_driver_.begin();
    pwm_driver_.setPWMFreq(ArmConfig::PWM_FREQUENCY_HZ);

    delay(10);
    is_initialized_ = true;

    // Command servos to initial home positions
    writeJointAnglesImmediate(current_angles_);
    return true;
}

uint16_t PCA9685Driver::angleToTicks(float angle_deg) {
    // Clamp angle to safe physical sweep [0, 180]
    float clamped_deg = std::max(0.0f, std::min(180.0f, angle_deg));

    // Linear interpolation from microseconds to 12-bit PCA9685 ticks
    // Period = 1,000,000 us / 50 Hz = 20,000 us
    // Ticks = (pulse_us / 20000.0) * 4096
    float pulse_us = ArmConfig::SERVO_MIN_PULSE_US +
                     (clamped_deg / 180.0f) * (ArmConfig::SERVO_MAX_PULSE_US - ArmConfig::SERVO_MIN_PULSE_US);

    float ticks = (pulse_us / 20000.0f) * 4096.0f;
    return static_cast<uint16_t>(ticks);
}

void PCA9685Driver::writeChannelPulse(uint8_t channel, uint16_t pulse_ticks) {
    if (!is_initialized_) return;
    pwm_driver_.setPWM(channel, 0, pulse_ticks);
}

void PCA9685Driver::writeJointAnglesImmediate(const JointAngles &angles) {
    current_angles_ = angles;
    target_angles_  = angles;

    writeChannelPulse(ArmConfig::CH_BASE_YAW,       angleToTicks(angles.q1_base_yaw));
    writeChannelPulse(ArmConfig::CH_SHOULDER_PITCH, angleToTicks(angles.q2_shoulder_pitch));
    writeChannelPulse(ArmConfig::CH_ELBOW_PITCH,    angleToTicks(angles.q3_elbow_pitch));
    writeChannelPulse(ArmConfig::CH_WRIST_PITCH,    angleToTicks(angles.q4_wrist_pitch));
    writeChannelPulse(ArmConfig::CH_GRIPPER,        angleToTicks(angles.q5_gripper));
}

void PCA9685Driver::setTargetAngles(const JointAngles &target) {
    target_angles_ = target;
}

float PCA9685Driver::stepToward(float current, float target, float max_step) {
    float diff = target - current;
    if (fabs(diff) <= max_step) {
        return target;
    }
    return current + ((diff > 0.0f) ? max_step : -max_step);
}

void PCA9685Driver::update(float dt_seconds) {
    if (!is_initialized_) return;

    // Compute maximum allowable angular change for this step
    float max_delta = ArmConfig::MAX_SERVO_VELOCITY_DPS * dt_seconds;

    current_angles_.q1_base_yaw = stepToward(current_angles_.q1_base_yaw, target_angles_.q1_base_yaw, max_delta);
    current_angles_.q2_shoulder_pitch = stepToward(current_angles_.q2_shoulder_pitch, target_angles_.q2_shoulder_pitch, max_delta);
    current_angles_.q3_elbow_pitch = stepToward(current_angles_.q3_elbow_pitch, target_angles_.q3_elbow_pitch, max_delta);
    current_angles_.q4_wrist_pitch = stepToward(current_angles_.q4_wrist_pitch, target_angles_.q4_wrist_pitch, max_delta);
    current_angles_.q5_gripper = stepToward(current_angles_.q5_gripper, target_angles_.q5_gripper, max_delta);

    // Write updated pulse commands to hardware
    writeChannelPulse(ArmConfig::CH_BASE_YAW,       angleToTicks(current_angles_.q1_base_yaw));
    writeChannelPulse(ArmConfig::CH_SHOULDER_PITCH, angleToTicks(current_angles_.q2_shoulder_pitch));
    writeChannelPulse(ArmConfig::CH_ELBOW_PITCH,    angleToTicks(current_angles_.q3_elbow_pitch));
    writeChannelPulse(ArmConfig::CH_WRIST_PITCH,    angleToTicks(current_angles_.q4_wrist_pitch));
    writeChannelPulse(ArmConfig::CH_GRIPPER,        angleToTicks(current_angles_.q5_gripper));
}
