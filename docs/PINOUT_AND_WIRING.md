# Electronics, Pinouts & Power Distribution

All heavy electrical components are situated inside the stationary base platform to minimize the arm's moving mass and lower the center of gravity.

## 1. Power Distribution Network
- **Primary Source**: 11.1V (3S) LiPo Battery (XT60 connector).
- **Servo Power Rail (High Current)**:
  - XL4016 Buck Converter: Steps down 11.1V -> **6.8V – 7.2V** (supports up to 8A continuous for RDS5160 & MG996R servos).
  - High-capacity buffer: 1000 µF capacitor across the servo rail to prevent brownouts during simultaneous multi-joint acceleration.
- **Logic Power Rail (Low Noise)**:
  - LM2596 Buck Converter: Steps down 11.1V -> **5.0V** (powers ESP32 NodeMCU microcontrollers and PCA9685 logic VCC).
  - Buffer: 470 µF capacitor.

## 2. Microcontroller Pinout (Base ESP32 NodeMCU)

| ESP32 Pin | Function | Connected Peripheral | Signal Description |
| :--- | :--- | :--- | :--- |
| **GPIO 21** | I2C SDA | PCA9685 SDA | Serial Data line (4.7kΩ pull-up to 3.3V) |
| **GPIO 22** | I2C SCL | PCA9685 SCL | Serial Clock line (4.7kΩ pull-up to 3.3V) |
| **GPIO 34** | ADC1_CH6 | FSR 402 Pressure Sensor | Analog voltage (0 – 3.3V) from voltage divider |
| **GPIO 2** | Digital Out | Onboard LED | 1Hz Heartbeat indicator |
| **VIN** | Power In | LM2596 VOUT (+5.0V) | Logic supply |
| **GND** | Ground | Common Ground | Common return rail |

## 3. PCA9685 Channel Assignments

| PCA9685 Channel | Controlled Actuator | Target Joint | PWM Frequency / Pulse |
| :--- | :--- | :--- | :--- |
| **Channel 0** | DSSERVO RDS5160 | Joint 1 (Base Yaw) | 50 Hz, 500 – 2500 µs |
| **Channel 1** | DSSERVO RDS5160 | Joint 2 (Shoulder Pitch) | 50 Hz, 500 – 2500 µs |
| **Channel 2** | TowerPro MG996R | Joint 3 (Elbow Pitch) | 50 Hz, 500 – 2500 µs |
| **Channel 3** | TowerPro MG996R | Joint 4 (Wrist Pitch) | 50 Hz, 500 – 2500 µs |
| **Channel 4** | TowerPro MG996R | Joint 5 (Gripper) | 50 Hz, 500 – 2500 µs |

## 4. FSR 402 Tactile Sensor Conditioning Circuit
The FSR 402 changes resistance from >1 MΩ (no contact) down to <1 kΩ (heavy pressure). It is conditioned using a voltage divider:
```
+3.3V (ESP32)
   |
   +-- [ FSR 402 Sensor ] --+
                            |
                            +----> GPIO 34 (Analog Input)
                            |
                        [ 10 kΩ Resistor ]
                            |
                           GND
```
- At rest: Vout ≈ 0.0V (ADC ≈ 0).
- At contact: Vout rises toward 3.0V (ADC rises toward 3700).
