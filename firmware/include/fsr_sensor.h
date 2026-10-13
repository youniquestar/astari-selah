#pragma once

#include <Arduino.h>
#include "arm_config.h"

/**
 * ============================================================================
 * FSR 402 FORCE SENSING RESISTOR - PRESSURE SENSING & FILTERING
 * ============================================================================
 */

class FSRSensor {
public:
    explicit FSRSensor(uint8_t pin = ArmConfig::PIN_FSR_ANALOG);

    /**
     * Initialize ADC configuration (12-bit, 11dB attenuation for 0-3.3V range)
     */
    void begin();

    /**
     * Poll sensor reading and update filtered value
     */
    void update();

    /**
     * Returns raw 12-bit ADC count [0, 4095]
     */
    uint16_t getRawValue() const { return raw_value_; }

    /**
     * Returns smoothed ADC reading (Exponential Moving Average)
     */
    float getFilteredValue() const { return filtered_value_; }

    /**
     * Returns estimated contact force in Grams (calibrated curve)
     */
    float getEstimatedGrams() const;

    /**
     * Returns true if contact pressure exceeds touch threshold
     */
    bool isObjectDetected() const;

private:
    uint8_t pin_;
    uint16_t raw_value_;
    float filtered_value_;
    float alpha_;
};
