# WipperSnapper v2 Happy Path: Complete Device Flow

This document demonstrates the complete "happy path" flow for a WipperSnapper v2 device, showcasing the new B2D/D2B envelope architecture. This serves as a comprehensive overview of how all the WipperSnapper protocol buffers work together in the v2 API.

## Key Changes in v2

### Message Envelope Architecture

**v2 introduces a cleaner message organization using envelopes:**

- **B2D (BrokerToDevice)** - All commands from Adafruit IO to device
- **D2B (DeviceToBroker)** - All responses and data from device to Adafruit IO

Each component (digitalio, analogio, i2c, etc.) has its own B2D and D2B envelope messages with specific payloads.

### Benefits of v2 Architecture

1. **Cleaner code organization** - Envelope pattern groups related messages
2. **Easier routing** - Top-level message type identifies component
3. **Better extensibility** - Adding new message types doesn't break existing code
4. **Type safety** - Stronger typing with oneof payloads

---

## Overview

The complete flow consists of:

1. **Device Registration** - Device checks in with Adafruit IO
2. **Component Addition** - Adding various hardware components
3. **Data Flow** - Sensors send data, outputs receive commands
4. **Component Management** - Updating and removing components

---

## 1. Complete Boot-to-Operation Example

### The Complete Flow: Device Boot → Component Registration → Operation

This example shows a device booting up, checking in with Adafruit IO, receiving its component configuration, and then operating normally. We'll follow an LED on D13 through its complete lifecycle.

```mermaid
sequenceDiagram
autonumber
participant Device as WipperSnapper Device
participant IO as Adafruit IO
participant Boards as Boards Repository
participant LED as LED on D13

Note over Device: POWER ON - Device Boots

Device->>Device: Initialize firmware
Device->>Device: Load persistent config (if any)

Note over Device,IO: PHASE 1: Check-In

Device->>IO: ws.checkin.D2B {<br/>  request: {<br/>    hardware_uid: "ESP32-C3-A1B2C3",<br/>    firmware_version: "2.0.0"<br/>  }<br/>}

IO->>Boards: Lookup "ESP32-C3"
Boards->>IO: Board definition found

IO->>IO: Load stored components<br/>for this device

IO->>Device: ws.checkin.B2D {<br/>  response: {<br/>    response: R_OK,<br/>    total_gpio_pins: 20,<br/>    total_analog_pins: 6,<br/>    reference_voltage: 3.3,<br/>    component_adds: [<br/>      {digitalio: {<br/>        pin_name: "D13",<br/>        gpio_direction: D_OUTPUT,<br/>        value: false<br/>      }},<br/>      {i2c: {<br/>        device_description: {device_address: 0x77},<br/>        device_name: "bme280",<br/>        device_period: 60.0,<br/>        device_sensor_types: [TEMPERATURE, HUMIDITY]<br/>      }}<br/>    ]<br/>  }<br/>}

Note over Device: PHASE 2: Component Initialization

Device->>Device: Configure GPIO controller<br/>(20 pins, 3.3V)
Device->>Device: Configure Analog controller<br/>(6 pins, 3.3V ref)

Note over Device: Process component_adds[0]: Digital Pin

Device->>LED: Configure D13 as OUTPUT
LED->>Device: Pin configured, initial value: LOW

Note over Device: Process component_adds[1]: I2C Sensor

Device->>Device: Initialize I2C bus
Device->>Device: Initialize BME280 at 0x77
Device->>Device: Start polling timer (60s)

Device->>IO: ws.checkin.D2B {<br/>  complete: {}<br/>}

Note over Device,IO: PHASE 3: Normal Operation Begins

Note over Device: User Action: Turn LED ON via Dashboard

IO->>Device: ws.digitalio.B2D {<br/>  write: {<br/>    pin_name: "D13",<br/>    value: true<br/>  }<br/>}

Device->>LED: Set pin HIGH
Note over LED: LED turns ON ✓

Note over Device: 60 seconds pass...

Device->>IO: ws.i2c.D2B {<br/>  device_event: {<br/>    device_description: {device_address: 0x77},<br/>    device_events: [<br/>      {type: TEMPERATURE, value: 23.5},<br/>      {type: HUMIDITY, value: 45.0}<br/>    ]<br/>  }<br/>}

Note over Device: User Action: Turn LED OFF (2nd Write)

IO->>Device: ws.digitalio.B2D {<br/>  write: {<br/>    pin_name: "D13",<br/>    value: false<br/>  }<br/>}

Device->>LED: Set pin LOW
Note over LED: LED turns OFF ✓

Note over Device,IO: System continues operating...
```

### Key Points in This Flow:

1. **Boot Phase**: Device initializes and loads any local persistent config
2. **Check-In Request**: Device identifies itself to IO with hardware_uid and firmware version
3. **Check-In Response**: IO returns board capabilities AND all configured components
4. **Component Initialization**: Device processes each component in `component_adds` array
5. **Complete Signal**: Device signals it's ready for normal operation
6. **First Write**: User triggers the first write operation (LED ON)
7. **Sensor Data**: I2C sensor sends periodic data
8. **Second Write**: User triggers second write operation (LED OFF)

---

## 2. Device Check-In Structure

### Check-In Request (D2B)

```protobuf
ws.checkin.D2B {
  request: {
    hardware_uid: "boardname-MACADDR",
    firmware_version: "2.0.0"
  }
}
```

### Check-In Response (B2D) with Components

```protobuf
ws.checkin.B2D {
  response: {
    response: R_OK,
    total_gpio_pins: 20,
    total_analog_pins: 6,
    reference_voltage: 3.3,

    // All pre-configured components sent here!
    component_adds: [
      {digitalio: {...}},
      {analogio: {...}},
      {i2c: {...}},
      // ... more components
    ]
  }
}
```

### Complete Signal (D2B)

```protobuf
ws.checkin.D2B {
  complete: {}
}
```

This signals the device has finished initialization and is ready for normal operation.

---

## 3. Component Registration Details

### ComponentAdd Message Structure

The `ComponentAdd` message is a union (oneof) that can contain any component type:

```protobuf
message ComponentAdd {
  oneof payload {
    ws.digitalio.Add digitalio    = 1;
    ws.analogio.Add analogio      = 2;
    ws.servo.Add servo            = 3;
    ws.pwm.Add pwm                = 4;
    ws.pixels.Add pixels          = 5;
    ws.ds18x20.Add ds18x20        = 6;
    ws.uart.Add uart              = 7;
    ws.i2c.DeviceAddOrReplace i2c = 8;
  }
}
```

### Example: Multiple Components at Check-In

```protobuf
component_adds: [
  // Digital Output: Status LED
  {
    digitalio: {
      pin_name: "D13",
      gpio_direction: D_OUTPUT,
      value: false
    }
  },

  // Digital Input: Button
  {
    digitalio: {
      pin_name: "D2",
      gpio_direction: D_INPUT_PULL_UP,
      sample_mode: SM_EVENT
    }
  },

  // Analog Input: Battery Monitor
  {
    analogio: {
      pin_name: "A1",
      period: 30.0,
      read_mode: SENSOR_TYPE_VOLTAGE
    }
  },

  // I2C Sensor: Temperature/Humidity
  {
    i2c: {
      device_description: {device_address: 0x77},
      device_name: "bme280",
      device_period: 60.0,
      device_sensor_types: [TEMPERATURE, HUMIDITY, PRESSURE],
      is_persistent: true
    }
  }
]
```

### Processing ComponentAdd Array

The device processes each `ComponentAdd` in sequence:

1. **Extract component type** from oneof
2. **Initialize hardware** for that component
3. **Configure parameters** from the Add message
4. **Store state** for persistent operation
5. **Continue to next** component

If any component fails to initialize, the device should log the error but continue processing remaining components.

---

## 4. Component Lifecycle with B2D/D2B Envelopes

All component interactions in v2 use the envelope pattern. Here's how it works:

```mermaid
graph LR
    IO[Adafruit IO] -->|B2D Envelope| Device[Device]
    Device -->|D2B Envelope| IO

    subgraph "B2D Commands"
    B1[Add Component]
    B2[Update Component]
    B3[Remove Component]
    B4[Write to Output]
    end

    subgraph "D2B Responses"
    D1[Component Added]
    D2[Component Updated]
    D3[Component Removed]
    D4[Sensor Data Event]
    end

    style IO fill:#e1f5ff
    style Device fill:#fff4e6
```

---

## 5. Adding Components During Runtime

After initial check-in, components can be added dynamically during operation:

### 5.1 Runtime Component Addition vs Check-In

**Difference:**
- **At Check-In**: Components sent in `component_adds` array during check-in response
- **At Runtime**: Components sent as individual B2D messages

### 5.2 Digital GPIO Input (Button) - Runtime Addition

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant GPIO as GPIO Controller

IO->>Device: ws.digitalio.B2D {<br/>  add: {<br/>    pin_name: "D2",<br/>    gpio_direction: D_INPUT_PULL_UP,<br/>    sample_mode: SM_EVENT<br/>  }<br/>}

Device->>GPIO: Configure pin D2 as input with pull-up
GPIO->>GPIO: Attach interrupt for state changes
GPIO->>Device: Pin configured

Note over Device: Button pressed/released
GPIO->>Device: State change detected

Device->>IO: ws.digitalio.D2B {<br/>  event: {<br/>    pin_name: "D2",<br/>    value: false<br/>  }<br/>}
```

### 5.3 Analog Input (Battery Monitor) - Runtime Addition

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant ADC as ADC Controller

IO->>Device: ws.analogio.B2D {<br/>  add: {<br/>    pin_name: "A1",<br/>    period: 10.0,<br/>    read_mode: SENSOR_TYPE_VOLTAGE<br/>  }<br/>}

Device->>ADC: Configure A1 for voltage reading
ADC->>Device: Pin configured, start polling

loop Every 10 seconds
    ADC->>ADC: Read analog value
    ADC->>Device: Voltage reading
    Device->>IO: ws.analogio.D2B {<br/>  event: {<br/>    pin_name: "A1",<br/>    value: 3.7V<br/>  }<br/>}
end
```

### 5.4 I2C Sensor (BME280 - Multi-Sensor) - Runtime Addition

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant I2C as I2C Controller
participant BME280 as BME280 Sensor

Note over IO: Step 1: Scan I2C Bus
IO->>Device: ws.i2c.B2D {<br/>  bus_scan: {<br/>    scan_default_bus: true<br/>  }<br/>}

Device->>I2C: Scan for devices
I2C->>Device: Found: [0x77]

Device->>IO: ws.i2c.D2B {<br/>  bus_scanned: {<br/>    bus_found_devices: [{device_address: 0x77}],<br/>    bus_status: BS_SUCCESS<br/>  }<br/>}

Note over IO: Step 2: Add Device
IO->>Device: ws.i2c.B2D {<br/>  device_add_replace: {<br/>    device_description: {device_address: 0x77},<br/>    device_name: "bme280",<br/>    device_period: 5.0,<br/>    device_sensor_types: [TEMPERATURE, HUMIDITY, PRESSURE]<br/>  }<br/>}

Device->>I2C: Initialize BME280
I2C->>BME280: Configure sensors
BME280->>I2C: Ready

Device->>IO: ws.i2c.D2B {<br/>  device_added_replaced: {<br/>    device_description: {device_address: 0x77},<br/>    bus_status: BS_SUCCESS,<br/>    device_status: DS_SUCCESS<br/>  }<br/>}

Note over Device: Step 3: Periodic Data
loop Every 5 seconds
    I2C->>BME280: Read all sensors
    BME280->>I2C: Temp: 23.5°C, Humidity: 45%, Pressure: 1013hPa
    Device->>IO: ws.i2c.D2B {<br/>  device_event: {<br/>    device_description: {device_address: 0x77},<br/>    device_events: [<br/>      {type: TEMPERATURE, value: 23.5},<br/>      {type: HUMIDITY, value: 45.0},<br/>      {type: PRESSURE, value: 1013.25}<br/>    ]<br/>  }<br/>}
end
```

### 5.5 E-Paper Display (UC8179) - Runtime Addition

```mermaid
sequenceDiagram
autonumber
participant IO as Adafruit IO
participant Device as WipperSnapper Device
participant Display as Display Controller
participant Driver as UC8179 Driver

IO->>Device: ws.display.DisplayAddOrReplace {<br/>  type: DISPLAY_TYPE_EPD,<br/>  driver: DISPLAY_DRIVER_EPD_UC8179,<br/>  name: "weather-display",<br/>  spi_epd: {<br/>    bus: 0, pin_dc: "D10", pin_rst: "D9",<br/>    pin_cs: "D8", pin_busy: "D11"<br/>  },<br/>  config_epd: {<br/>    mode: EPD_MODE_MONO,<br/>    width: 648, height: 480, text_size: 2<br/>  }<br/>}

Device->>Display: Initialize display
Display->>Driver: Load UC8179 driver
Driver->>Display: Driver ready

Device->>IO: ws.display.DisplayAddedOrReplaced {<br/>  name: "weather-display",<br/>  did_add: true<br/>}

Note over IO: Write to Display
IO->>Device: ws.display.DisplayWrite {<br/>  name: "weather-display",<br/>  message: "Temp: 23.5°C\\nHumidity: 45%"<br/>}

Device->>Display: Render text
Display->>Driver: Update display
Driver->>Display: Wait for busy pin
Display->>Device: Update complete
```

---

## 6. Complete System Architecture

Here's how all v2 components work together:

```mermaid
graph TB
    subgraph "Adafruit IO Broker"
        IO[MQTT Broker]
        UI[Web Dashboard]
    end

    subgraph "Message Envelopes"
        B2D[B2D Envelopes<br/>Commands to Device]
        D2B[D2B Envelopes<br/>Responses from Device]
    end

    subgraph "WipperSnapper Device"
        Device[Device Core<br/>Message Router]

        subgraph "Input Controllers"
            DigitalIn[Digital Input]
            AnalogIn[Analog Input]
            I2CSensor[I2C Sensors]
        end

        subgraph "Output Controllers"
            DigitalOut[Digital Output]
            Display[Display Controller]
            I2COut[I2C Outputs]
        end
    end

    subgraph "Physical Hardware"
        Button[Button on D2]
        Battery[Battery on A1]
        BME[BME280 @ 0x77]
        EPD[E-Paper Display]
        LED[LED on D13]
    end

    UI -->|User Commands| IO
    IO <-->|B2D/D2B| Device

    Device --> DigitalIn
    Device --> AnalogIn
    Device --> I2CSensor
    Device --> DigitalOut
    Device --> Display
    Device --> I2COut

    DigitalIn <--> Button
    AnalogIn <--> Battery
    I2CSensor <--> BME
    Display <--> EPD
    DigitalOut <--> LED

    style IO fill:#e1f5ff
    style Device fill:#fff4e6
    style UI fill:#e1f5ff
```

---

## 7. Message Envelope Structure

### Example: Digital IO Messages

**B2D (Commands to Device):**
```protobuf
message B2D {
  oneof payload {
    Add add       = 1;  // Add/configure pin
    Remove remove = 2;  // Remove pin
    Write write   = 3;  // Write to output pin
  }
}
```

**D2B (Responses from Device):**
```protobuf
message D2B {
  oneof payload {
    Event event = 1;  // Pin value changed
  }
}
```

### Message Flow Example

```
Adafruit IO                          Device
    |                                   |
    |  ws.digitalio.B2D                |
    |    add: {pin_name: "D2", ...}    |
    | --------------------------------> |
    |                                   |  Configure hardware
    |                                   |
    |  ws.digitalio.D2B                |
    |    event: {pin_name: "D2", ...}  |
    | <-------------------------------- |
    |                                   |
```

---

## 8. Component Summary Table

| Component | B2D Messages | D2B Messages | Direction |
|-----------|-------------|--------------|-----------|
| **digitalio** | add, remove, write | event | Input & Output |
| **analogio** | add, remove | event | Input only |
| **i2c** | bus_scan, device_add_replace, device_remove, device_output_write | bus_scanned, device_added_replaced, device_removed, device_event | Input & Output |
| **display** | DisplayAddOrReplace, DisplayRemove, DisplayWrite | DisplayAddedOrReplaced, DisplayRemoved | Output only |
| **pwm** | add, remove, write | - | Output only |
| **servo** | add, remove, write | - | Output only |
| **pixels** | add, remove, write | - | Output only |
| **ds18x20** | add, remove | event | Input only |
| **uart** | add, remove | event | Input only |

---

## 9. Data Flow Patterns

### Input Components (Sensors send data)

```mermaid
sequenceDiagram
    participant Sensor
    participant Device
    participant IO as Adafruit IO

    loop Periodic or Event-driven
        Sensor->>Device: Read sensor value
        Device->>Device: Package in D2B envelope
        Device->>IO: D2B{event: {...}}
    end
```

### Output Components (Commands from IO)

```mermaid
sequenceDiagram
    participant IO as Adafruit IO
    participant Device
    participant Output

    IO->>Device: B2D{write: {...}}
    Device->>Device: Extract from envelope
    Device->>Output: Apply command
    Output->>Device: Action complete
```

---

## 10. Error Handling

### Status Codes

Components return status codes in their responses:

**I2C Example:**
- `BS_SUCCESS` - Bus operation successful
- `BS_ERROR_PULLUPS` - Missing pull-up resistors
- `DS_SUCCESS` - Device operation successful
- `DS_NOT_FOUND` - Device not found at address

**Error Flow:**
```mermaid
sequenceDiagram
    IO->>Device: B2D{device_add_replace: {...}}
    Device->>Device: Attempt to initialize
    alt Success
        Device->>IO: D2B{device_added_replaced: {status: DS_SUCCESS}}
    else Failure
        Device->>IO: D2B{device_added_replaced: {status: DS_NOT_FOUND}}
        IO->>IO: Display error to user
    end
```

---

## 11. Component Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> NotConfigured
    NotConfigured --> Adding: B2D(add)
    Adding --> Active: D2B(added) success
    Adding --> Error: D2B(added) failure
    Active --> Operating: Normal operation
    Operating --> Active: Continue
    Active --> Updating: B2D(add) with new config
    Updating --> Active: D2B(added) success
    Active --> Removing: B2D(remove)
    Removing --> [*]: D2B(removed)
    Error --> [*]: User fixes issue
```

---

## 12. Best Practices for v2

### Message Routing
1. **Envelope pattern** - Always wrap messages in appropriate B2D/D2B envelope
2. **Type safety** - Use oneof payloads for compile-time type checking
3. **Component isolation** - Each component has its own envelope namespace

### Component Management
1. **Add before use** - Always add component before trying to use it
2. **Check responses** - Verify D2B responses for success/failure
3. **Cleanup** - Remove components when no longer needed
4. **Status codes** - Check and handle all status codes appropriately

### Performance
1. **Polling periods** - Choose appropriate periods for input components
2. **Event-driven** - Use event mode (SM_EVENT) for infrequent state changes
3. **Batch operations** - Group related component additions together

---

## 13. Migration from v1 to v2

### Key Differences

| Aspect | v1 | v2 |
|--------|----|----|
| **Message Organization** | Flat message structure | Envelope pattern (B2D/D2B) |
| **Component Namespacing** | Global proto namespace | Component-specific envelopes |
| **Display Support** | Limited | Extended (multiple interface types) |
| **I2C Flexibility** | Basic | Advanced (multiplexers, alt buses, GPS) |
| **Status Reporting** | Single status field | Separate Bus/Device status |

### Migration Example

**v1 I2C Add:**
```protobuf
I2CDeviceInitRequest {
  i2c_device_address: 0x77,
  i2c_device_name: "bme280",
  ...
}
```

**v2 I2C Add:**
```protobuf
ws.i2c.B2D {
  device_add_replace: {
    device_description: {device_address: 0x77},
    device_name: "bme280",
    ...
  }
}
```

---

## 14. Complete Example: Weather Station with Check-In

This example shows a weather station device booting up, receiving its configuration during check-in, and operating:

```mermaid
sequenceDiagram
    participant Device
    participant IO as Adafruit IO
    participant BME as BME280
    participant Display as E-Paper
    participant LED

    Note over Device: BOOT

    Device->>IO: checkin.D2B{request}
    IO->>Device: checkin.B2D{<br/>  response: {<br/>    component_adds: [BME280, E-Paper, LED]<br/>  }<br/>}

    Device->>BME: Initialize
    Device->>Display: Initialize
    Device->>LED: Initialize

    Device->>IO: checkin.D2B{complete}

    Note over Device,LED: NORMAL OPERATION

    loop Every 60 seconds
        BME->>Device: Read temp, humidity, pressure
        Device->>IO: i2c.D2B{device_event: {...}}
        IO->>Device: display.DisplayWrite{"Temp: 23°C"}
        Device->>Display: Update display
        IO->>Device: digitalio.B2D{write: LED blink}
        Device->>LED: Blink to show update
    end
```

---

## 15. Original Weather Station Example

Here's a complete example showing multiple components working together:

```mermaid
sequenceDiagram
    participant IO as Adafruit IO
    participant Device
    participant BME as BME280 (I2C)
    participant Display as E-Paper
    participant LED as Status LED

    Note over IO,LED: System Initialization
    IO->>Device: Add BME280 sensor
    IO->>Device: Add E-Paper display
    IO->>Device: Add Status LED

    Note over IO,LED: Normal Operation
    loop Every 60 seconds
        BME->>Device: Read temp, humidity, pressure
        Device->>IO: D2B{device_event: {...}}
        IO->>Device: B2D{DisplayWrite: "Temp: 23°C"}
        Device->>Display: Update display
        IO->>Device: B2D{digitalio.write: LED blink}
        Device->>LED: Blink to show update
    end
```

---

## Next Steps

- For component-specific details, see individual `.md` files:
  - [i2c.md](i2c.md) - I2C sensors and devices with v2 envelopes
  - [display.md](display.md) - Display controllers with multiple interface types
  - [digitalio.md](digitalio.md) - Digital GPIO with B2D/D2B
  - [analogio.md](analogio.md) - Analog input with B2D/D2B
  - [pwm.md](pwm.md), [servo.md](servo.md), [pixels.md](pixels.md), etc.

- For hardware definitions:
  - [WipperSnapper_Boards](https://github.com/adafruit/Wippersnapper_Boards)
  - [WipperSnapper_Components](https://github.com/adafruit/Wippersnapper_Components)

---

## Summary

The v2 WipperSnapper API brings:

 - ✅ **Cleaner architecture** with B2D/D2B envelopes
 - ✅ **Better organization** with component-specific namespaces
 - ✅ **Enhanced display support** for various interface types
 - ✅ **Improved I2C flexibility** with multiplexers and alternate buses
 - ✅ **Stronger typing** with protobuf oneof patterns
 - ✅ **Easier extensibility** for future features

The envelope pattern makes the codebase more maintainable while providing a clear, consistent interface for all WipperSnapper components.
