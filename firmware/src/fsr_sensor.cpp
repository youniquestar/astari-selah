#include "fsr_sensor.h"

FSRSensor::FSRSensor(uint8_t pin)
    : pin_(pin),
      raw_value_(0),
      filtered_value_(0.0f),
      alpha_(ArmConfig::FSR_FILTER_ALPHA)
{}

void FSRSensor::begin() {
    pinMode(pin_, INPUT);
    // ESP32 ADC: 12-bit resolution, 0 to 3.3V range
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);

    // Initial warm-up reading
    raw_value_ = analogRead(pin_);
    filtered_value_ = static_cast<float>(raw_value_);
}

void FSRSensor::update() {
    raw_value_ = analogRead(pin_);
    // Exponential Moving Average filter: y[k] = alpha * x[k] + (1 - alpha) * y[k-1]
    filtered_value_ = (alpha_ * static_cast<float>(raw_value_)) + ((1.0f - alpha_) * filtered_value_);
}

bool FSRSensor::isObjectDetected() const {
    return filtered_value_ > ArmConfig::FSR_TOUCH_THRESHOLD_RAW;
}

float FSRSensor::getEstimatedGrams() const {
    if (!isObjectDetected()) return 0.0f;

    // Piecewise empirical calibration for FSR 402 with 10k pull-down resistor:
    // Voltage Vout = (Vcc * R_pulldown) / (R_fsr + R_pulldown)
    // Approximate transfer function mapping ADC counts to Grams:
    float normalized = (filtered_value_ - ArmConfig::FSR_TOUCH_THRESHOLD_RAW) /
                       (ArmConfig::ADC_MAX_VALUE - ArmConfig::FSR_TOUCH_THRESHOLD_RAW);

    if (normalized < 0.0f) normalized = 0.0f;

    // Non-linear power model fitting FSR log-log force curve:
    float grams = 1000.0f * pow(normalized, 1.4f);
    return grams;
}
