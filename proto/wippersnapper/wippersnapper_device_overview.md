# WipperSnapper Happy Path: Complete Device Flow

This document demonstrates the complete "happy path" flow for a WipperSnapper device, from initial check-in through adding one of each component type. This serves as a comprehensive overview of how all the WipperSnapper protocol buffers work together.

## Overview

WipperSnapper enables IoT devices to connect to Adafruit IO and control various hardware components through MQTT messaging. The flow consists of:

1. **Device Registration** - Device checks in and registers with Adafruit IO
2. **Hardware Configuration** - IO configures the device's hardware capabilities
3. **Component Lifecycle** - Adding, using, updating, and removing components
4. **Data Flow** - Sensors send data to IO, outputs receive commands from IO

---

## 1. Device Registration & Check-In

The device must first register with Adafruit IO and establish its identity and capabilities.

```mermaid
sequenceDiagram
autonumber
participant Device as WipperSnapper Device
participant IO as Adafruit IO Broker
participant Boards as Boards Repository

Device->>IO: CreateDescriptionRequest
Note over Device,IO: Contains: machine_name, MAC address,<br/>firmware version
IO->>Boards: Check if hardware definition exists
Boards->>IO: Hardware JSON definition
IO->>Device: CreateDescriptionResponse (RESPONSE_OK)
Note over IO,Device: Contains: total_gpio_pins, total_analog_pins,<br/>total_i2c_ports, reference_voltage

Device->>Device: Configure Hardware Classes
Note over Device: - Digital IO Class: total_gpio_pins<br/>- Analog IO Class: total_analog_pins, reference_voltage<br/>- I2C Class: total_i2c_ports

Device->>IO: RegistrationComplete
Note over Device,IO: Device is ready to accept commands
```

**Key Messages:**
- `CreateDescriptionRequest` - Device identifies itself (machine_name, MAC, version)
- `CreateDescriptionResponse` - IO returns hardware capabilities
- `RegistrationComplete` - Device confirms it's ready

---

## 2. Adding Components: One of Each Type

Once registered, the device can have various components attached. Let's walk through adding one of each component type.

### 2.1 Digital GPIO Pin (Input)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant GPIO as Digital IO Class

IO->>Device: ConfigurePinRequest
Note over IO,Device: pin_name: "D13"<br/>gpio_direction: D_INPUT<br/>sample_mode: SM_TIMER<br/>period: 1.0 (seconds)

Device->>GPIO: Configure Pin
GPIO->>Device: Pin Configured

loop Every 1 second
    GPIO->>Device: Read Pin Value
    Device->>IO: PinEvent
    Note over Device,IO: pin_name: "D13"<br/>value: true/false
end
```

**Messages Used:** `ConfigurePinRequest`, `PinEvent`

---

### 2.2 I2C Sensor (BME280 - Temperature & Humidity)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant I2C as I2C Class
participant Sensor as BME280 Sensor

Note over IO,Device: Step 1: I2C Scan (if needed)
IO->>Device: I2CBusScanRequest
Note over IO,Device: i2c_port_number: 0<br/>Contains I2CBusInitRequest
Device->>I2C: Initialize Bus & Scan
I2C->>Device: Addresses Found
Device->>IO: I2CBusScanResponse
Note over Device,IO: addresses_found: [0x77]<br/>bus_response: BUS_RESPONSE_SUCCESS

Note over IO,Device: Step 2: Initialize Sensor
IO->>Device: I2CDeviceInitRequest
Note over IO,Device: i2c_device_address: 0x77<br/>i2c_device_name: "bme280"<br/>i2c_device_properties: [<br/>  {SENSOR_TYPE_AMBIENT_TEMPERATURE, 5000ms},<br/>  {SENSOR_TYPE_RELATIVE_HUMIDITY, 5000ms}<br/>]

Device->>I2C: Initialize BME280
I2C->>Sensor: Configure Sensor
Sensor->>I2C: Init Success
I2C->>Device: Device Ready

Device->>IO: I2CDeviceInitResponse
Note over Device,IO: i2c_device_address: 0x77<br/>bus_response: BUS_RESPONSE_SUCCESS

Note over Device,Sensor: Step 3: Periodic Data Reporting
loop Every 5 seconds
    Sensor->>I2C: Read Temperature & Humidity
    I2C->>Device: Sensor Data
    Device->>IO: I2CDeviceEvent
    Note over Device,IO: sensor_address: 0x77<br/>sensor_event: [<br/>  {SENSOR_TYPE_AMBIENT_TEMPERATURE, 23.5},<br/>  {SENSOR_TYPE_RELATIVE_HUMIDITY, 45.2}<br/>]
end
```

**Messages Used:** `I2CBusScanRequest`, `I2CBusScanResponse`, `I2CDeviceInitRequest`, `I2CDeviceInitResponse`, `I2CDeviceEvent`

---

### 2.3 E-Paper Display (UC8179 - 5.83" E-Ink)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant Display as Display Controller
participant Driver as UC8179 Driver

Note over IO,Device: Step 1: Add Display
IO->>Device: DisplayAddOrReplace
Note over IO,Device: type: DISPLAY_TYPE_EPD<br/>driver: DISPLAY_DRIVER_EPD_UC8179<br/>name: "eink-display"<br/>spi_epd: {bus: 0, pin_dc: "D10", pin_rst: "D9",<br/>         pin_cs: "D8", pin_busy: "D11"}<br/>config_epd: {mode: EPD_MODE_MONO,<br/>            width: 648, height: 480, text_size: 2}

Device->>Display: Create Display
Display->>Driver: Initialize UC8179
Driver->>Display: Init Success
Display->>Device: Display Ready

Device->>IO: DisplayAddedOrReplaced
Note over Device,IO: name: "eink-display"<br/>did_add: true

Note over IO,Device: Step 2: Write to Display
IO->>Device: DisplayWrite
Note over IO,Device: name: "eink-display"<br/>message: "Temperature: 23.5°C"

Device->>Display: Write Text
Display->>Driver: Render Text
Driver->>Display: Display Updated
```

**Messages Used:** `DisplayAddOrReplace`, `DisplayAddedOrReplaced`, `DisplayWrite`

---

### 2.4 PWM Output (Dimmable LED)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant PWM as PWM Class

Note over IO,Device: Step 1: Attach PWM
IO->>Device: PWMAttachRequest
Note over IO,Device: pin: "D6"<br/>frequency: 5000 (Hz)<br/>resolution: 12 (bits)

Device->>PWM: Attach PWM to Pin
PWM->>Device: PWM Attached

Device->>IO: PWMAttachResponse
Note over Device,IO: pin: "D6"<br/>did_attach: true

Note over IO,Device: Step 2: Control Brightness
loop User adjusts slider
    IO->>Device: PWMWriteDutyCycleRequest
    Note over IO,Device: pin: "D6"<br/>duty_cycle: 128 (0-255)
    Device->>PWM: Set Duty Cycle
    PWM->>Device: LED Brightness Updated
end
```

**Messages Used:** `PWMAttachRequest`, `PWMAttachResponse`, `PWMWriteDutyCycleRequest`

---

### 2.5 Servo Motor

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant Servo as Servo Class

Note over IO,Device: Step 1: Attach Servo
IO->>Device: ServoAttachRequest
Note over IO,Device: servo_pin: "D5"<br/>servo_freq: 50 (Hz)<br/>min_pulse_width: 500 (µs)<br/>max_pulse_width: 2500 (µs)

Device->>Servo: Attach Servo
Servo->>Device: Servo Ready

Device->>IO: ServoAttachResponse
Note over Device,IO: servo_pin: "D5"<br/>Success

Note over IO,Device: Step 2: Control Position
loop User adjusts position
    IO->>Device: ServoWriteRequest
    Note over IO,Device: servo_pin: "D5"<br/>pulse_width: 1500 (µs)
    Device->>Servo: Set Position
    Servo->>Device: Servo Moved
end
```

**Messages Used:** `ServoAttachRequest`, `ServoAttachResponse`, `ServoWriteRequest`

---

### 2.6 NeoPixel LED Strip

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant Pixels as Pixels Class

Note over IO,Device: Step 1: Create Pixel Strip
IO->>Device: PixelsCreateRequest
Note over IO,Device: pixels_type: PIXELS_TYPE_NEOPIXEL<br/>pixels_num: 10<br/>pixels_ordering: RGB<br/>pixels_brightness: 50<br/>pixels_pin_neopixel: "D4"

Device->>Pixels: Create NeoPixel Strip
Pixels->>Device: Strip Created

Device->>IO: PixelsCreateResponse
Note over Device,IO: is_success: true

Note over IO,Device: Step 2: Set Color
loop User changes color
    IO->>Device: PixelsWriteRequest
    Note over IO,Device: pixels_type: PIXELS_TYPE_NEOPIXEL<br/>pixels_pin_data: "D4"<br/>pixels_color: 0xFF5500 (Orange)
    Device->>Pixels: Set All Pixels
    Pixels->>Device: Colors Updated
end
```

**Messages Used:** `PixelsCreateRequest`, `PixelsCreateResponse`, `PixelsWriteRequest`

---

### 2.7 DS18B20 Temperature Sensor (OneWire)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant DS18 as DS18x20 Class
participant Sensor as DS18B20 Sensor

Note over IO,Device: Step 1: Initialize OneWire Bus & Sensor
IO->>Device: Ds18x20InitRequest
Note over IO,Device: pin: "D7"<br/>period: 2000 (ms)

Device->>DS18: Initialize OneWire Bus
DS18->>Sensor: Configure DS18B20
Sensor->>DS18: Ready
DS18->>Device: Sensor Ready

Device->>IO: Ds18x20InitResponse
Note over Device,IO: pin: "D7"<br/>is_success: true

Note over Device,Sensor: Step 2: Periodic Temperature Reading
loop Every 2 seconds
    Sensor->>DS18: Read Temperature
    DS18->>Device: Temperature Data
    Device->>IO: Ds18x20DeviceEvent
    Note over Device,IO: pin: "D7"<br/>sensor_event: {<br/>  SENSOR_TYPE_AMBIENT_TEMPERATURE,<br/>  22.3<br/>}
end
```

**Messages Used:** `Ds18x20InitRequest`, `Ds18x20InitResponse`, `Ds18x20DeviceEvent`

---

### 2.8 UART Device (GPS Module)

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant UART as UART Class
participant GPS as GPS Module

Note over IO,Device: Step 1: Attach UART Device
IO->>Device: UARTDeviceAttachRequest
Note over IO,Device: device_id: "gps"<br/>uart_bus: {baud: 9600, tx: "D1", rx: "D2"}<br/>polling_interval: 1000 (ms)

Device->>UART: Initialize UART Bus
UART->>GPS: Configure GPS Module
GPS->>UART: GPS Ready
UART->>Device: Device Ready

Device->>IO: UARTDeviceAttachResponse
Note over Device,IO: device_id: "gps"<br/>is_success: true

Note over Device,GPS: Step 2: Periodic GPS Data
loop Every 1 second
    GPS->>UART: Read NMEA Sentences
    UART->>Device: Parse GPS Data
    Device->>IO: UARTDeviceEvent
    Note over Device,IO: device_id: "gps"<br/>sensor_event: [<br/>  {latitude, 40.7128},<br/>  {longitude, -74.0060},<br/>  {altitude, 10.5}<br/>]
end
```

**Messages Used:** `UARTDeviceAttachRequest`, `UARTDeviceAttachResponse`, `UARTDeviceEvent`

---

## 3. Complete System Overview

Here's how all these components work together on a single device:

```mermaid
graph TB
    subgraph "Adafruit IO Broker"
        IO[MQTT Broker]
        UI[Web UI Dashboard]
    end

    subgraph "WipperSnapper Device"
        Device[Device Core]
        GPIO[Digital IO]
        I2C[I2C Bus]
        Display[Display Controller]
        PWM[PWM Controller]
        Servo[Servo Controller]
        Pixels[Pixels Controller]
        DS18[DS18x20 Controller]
        UART[UART Controller]
    end

    subgraph "Physical Hardware"
        Pin[GPIO Pin D13]
        BME[BME280 Sensor]
        EPD[E-Paper Display]
        LED[Dimmable LED]
        Motor[Servo Motor]
        Strip[NeoPixel Strip]
        Temp[DS18B20 Sensor]
        GPS[GPS Module]
    end

    UI -->|User Commands| IO
    IO <-->|MQTT Messages| Device

    Device <--> GPIO
    Device <--> I2C
    Device <--> Display
    Device <--> PWM
    Device <--> Servo
    Device <--> Pixels
    Device <--> DS18
    Device <--> UART

    GPIO <--> Pin
    I2C <--> BME
    Display <--> EPD
    PWM <--> LED
    Servo <--> Motor
    Pixels <--> Strip
    DS18 <--> Temp
    UART <--> GPS

    style IO fill:#e1f5ff
    style Device fill:#fff4e6
    style UI fill:#e1f5ff
```

---

## 4. Data Flow Summary

### Input Components (Send Data to IO)
| Component | Message Type | Frequency | Data Type |
|-----------|-------------|-----------|-----------|
| Digital GPIO (Input) | `PinEvent` | Periodic (timer) or Event-driven | Boolean (HIGH/LOW) |
| I2C Sensors | `I2CDeviceEvent` | Periodic (configurable) | Multiple sensor values |
| DS18B20 | `Ds18x20DeviceEvent` | Periodic (configurable) | Temperature |
| UART GPS | `UARTDeviceEvent` | Periodic (configurable) | Location data |

### Output Components (Receive Commands from IO)
| Component | Message Type | Trigger | Action |
|-----------|-------------|---------|--------|
| Digital GPIO (Output) | `ConfigurePinRequest` | User toggle | Set pin HIGH/LOW |
| Display | `DisplayWrite` | User input | Render text/image |
| PWM LED | `PWMWriteDutyCycleRequest` | User slider | Adjust brightness |
| Servo | `ServoWriteRequest` | User control | Move to position |
| NeoPixels | `PixelsWriteRequest` | User color picker | Set LED colors |

---

## 5. Component Lifecycle

All components follow a similar lifecycle pattern:

```mermaid
stateDiagram-v2
    [*] --> NotConfigured
    NotConfigured --> Initializing: CreateRequest / AttachRequest
    Initializing --> Active: CreateResponse(success) / AttachResponse(success)
    Initializing --> Error: CreateResponse(fail) / AttachResponse(fail)
    Active --> Operating: Read/Write Operations
    Operating --> Active: Continue Operations
    Active --> Updating: UpdateRequest
    Updating --> Active: UpdateResponse
    Active --> Removing: DeleteRequest / DetachRequest
    Removing --> [*]: DeleteResponse / DetachResponse
    Error --> [*]: User Intervention Required
```

**Lifecycle Operations:**
- **Create/Attach** - Initialize the component with configuration
- **Operate** - Read data (inputs) or write commands (outputs)
- **Update** - Modify configuration (often requires detach/reattach)
- **Delete/Detach** - Remove the component and free resources

---

## 6. Error Handling

### Common Error Responses

**I2C Bus Errors:**
- `BUS_RESPONSE_ERROR_PULLUPS` - Missing pull-up resistors on SDA/SCL
- `BUS_RESPONSE_ERROR_WIRING` - Connection issue, check wiring
- `BUS_RESPONSE_UNSUPPORTED_SENSOR` - Firmware needs update
- `BUS_RESPONSE_DEVICE_INIT_FAIL` - Sensor not responding at address

**General Pattern:**
1. Device returns error response with status code
2. IO displays error to user
3. User corrects hardware/configuration issue
4. User retries operation

---

## 7. MQTT Topic Structure

All WipperSnapper communication uses structured MQTT topics:

**Broker → Device (Commands):**
```
/:username/wprsnpr/:clientId/signals/device/:component
```

**Device → Broker (Responses/Data):**
```
/:username/wprsnpr/:clientId/signals/broker/:component
```

**Component Types:**
- `status` - Device registration and check-in
- `pin` - Digital GPIO operations
- `i2c` - I2C device operations
- `display` - Display operations
- `pwm` - PWM operations
- `servo` - Servo operations
- `pixels` - NeoPixel/DotStar operations
- `ds18x20` - DS18x20 temperature sensor operations
- `uart` - UART device operations

---

## 8. Best Practices

### Device Setup
1. Always complete device registration before adding components
2. Perform I2C scan before adding I2C devices
3. Initialize buses (I2C, UART, OneWire) before devices
4. Verify hardware connections match proto configuration

### Component Configuration
1. Use appropriate polling periods (don't over-poll sensors)
2. Set reasonable PWM frequencies for target hardware
3. Configure display text_size based on display resolution
4. Use proper pixel ordering for NeoPixel types

### Error Recovery
1. Check bus response codes after all I2C operations
2. Implement retry logic with backoff for transient errors
3. Log detailed error information for debugging
4. Validate hardware configuration before firmware updates

---

## Next Steps

- For detailed API documentation, see individual component `.proto` files
- For component-specific workflows, see individual `.md` files:
  - [i2c.md](i2c/v1/i2c.md) - I2C sensors and devices
  - [display.md](display/v1/display.md) - Display controllers
  - [pwm.md](pwm/v1/pwm.md) - PWM outputs
  - [servo.md](servo/v1/servo.md) - Servo motors
  - [pixels.md](pixels/v1/pixels.md) - NeoPixels and DotStars
  - [ds18x20.md](ds18x20/v1/ds18x20.md) - DS18B20 temperature sensors
  - [uart.md](uart/v1/uart.md) - UART devices (GPS, air quality sensors)
- For hardware definitions, see [WipperSnapper_Boards](https://github.com/adafruit/Wippersnapper_Boards)
- For component definitions, see [WipperSnapper_Components](https://github.com/adafruit/Wippersnapper_Components)
