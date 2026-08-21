# uart.proto

This file details the WipperSnapper messaging API for interfacing with a UART bus.

## WipperSnapper Components

The following WipperSnapper components utilize `uart.proto`:

* PMS* Air Quality Sensors
* Adafruit Universal GPS module using the MTK33x9 chipset
* Generic UART input/output devices
* Trinamic stepper motors / DYNAMIXEL servos

## Architecture Overview

The v2 UART API uses message envelopes:

- **B2D (BrokerToDevice)** - Commands from Adafruit IO to device
  - `add` - Configure a UART port and attach a device
  - `remove` - Detach a device and deinitialize the port
  - `write` - Write data (bytes or text) to a device

- **D2B (DeviceToBroker)** - Responses and data from device to Adafruit IO
  - `added` - Confirmation of device attachment
  - `written` - Confirmation of bytes written
  - `input_event` - Sensor data from a UART input device

## Enums

### DeviceType

| Value | Description |
|-------|-------------|
| `DT_UNSPECIFIED` | Unspecified device type |
| `DT_GENERIC_INPUT` | Generic UART input device |
| `DT_GENERIC_OUTPUT` | Generic UART output device |
| `DT_GPS` | GPS module |
| `DT_PM25AQI` | PM2.5 air quality sensor |
| `DT_TM22XX` | Trinamic stepper driver |

### PacketFormat

Serial data format (data bits, parity, stop bits). Common values:

| Value | Description |
|-------|-------------|
| `PF_8N1` | 8 data bits, no parity, 1 stop bit (most common) |
| `PF_8N2` | 8 data bits, no parity, 2 stop bits |
| `PF_8E1` | 8 data bits, even parity, 1 stop bit |
| `PF_8O1` | 8 data bits, odd parity, 1 stop bit |

(Also supports 5/6/7-bit variants with N/E/O parity and 1/2 stop bits.)

### GenericDeviceLineEnding

| Value | Description |
|-------|-------------|
| `GDLE_LF` | Newline (LF) |
| `GDLE_CRLF` | Carriage return + newline (CRLF) |
| `GDLE_TIMEOUT_100MS` | 100ms timeout between reads |
| `GDLE_TIMEOUT_1000MS` | 1s timeout between reads |

## Message Details

### Add

Contains two sub-messages:

**SerialConfig** (port configuration):
- **pin_rx** / **pin_tx** - RX and TX pins
- **device_name** - Device path (CPython only, e.g., `/dev/ttyUSB0`)
- **uart_nbr** - UART port number (0, 1, 2, etc.)
- **baud_rate** - Baud rate in bits per second
- **format** - Packet format (e.g., `PF_8N1`)
- **timeout** - Max milliseconds to wait for serial data (default 1000)
- **use_sw_serial** - Use software serial instead of hardware
- **sw_serial_invert** - Invert UART signal on RX/TX pins

**DeviceConfig** (device-specific):
- **device_type** - Type of device (`DT_GPS`, `DT_PM25AQI`, etc.)
- **device_id** - Unique identifier string
- **oneof config**: `GenericInputConfig`, `TrinamicDynamixelConfig`, or `PM25AQIConfig`

**Optional**: `write` field for initial write during check-in.

### Descriptor

Used in Remove, Write, Written, and InputEvent to identify the UART device:
- **uart_nbr** - UART port number
- **type** - Device type
- **device_id** - Device identifier

### Write

- **descriptor** - Identifies the target device
- **oneof payload**: `bytes_data` (raw bytes) or `text_data` (string)

### Written (response)

- **descriptor** - Identifies the device
- **bytes_written** - Number of bytes written

### InputEvent

- **descriptor** - Identifies the source device
- **events** - Sensor readings (`repeated ws.sensor.Event`)

## Sequence Diagrams

### Attaching a UART Component

```mermaid
sequenceDiagram
autonumber

IO->>Device: ws.uart.B2D { add }
Note over IO, Device: cfg_serial: {<br/>  pin_rx: "D0", pin_tx: "D1",<br/>  uart_nbr: 1, baud_rate: 9600,<br/>  format: PF_8N1<br/>}<br/>cfg_device: {<br/>  device_type: DT_PM25AQI,<br/>  device_id: "pm25-1",<br/>  pm25aqi: { period: 5000 }<br/>}

Device->>Device: Initialize UART port 1
Device->>Device: Attach PM2.5 driver

Device->>IO: ws.uart.D2B { added }
Note over Device, IO: descriptor: { uart_nbr: 1, type: DT_PM25AQI, device_id: "pm25-1" }<br/>success: true
```

### Sensor Data from a UART Input Device

```mermaid
sequenceDiagram
autonumber

loop Every period milliseconds
    Device->>IO: ws.uart.D2B { input_event }
    Note over Device, IO: descriptor: { uart_nbr: 1, device_id: "pm25-1" }<br/>events: [<br/>  {type: PM25_STD, value: 12.0},<br/>  {type: PM100_STD, value: 18.0}<br/>]
end
```

### Writing to a UART Output Device

```mermaid
sequenceDiagram
autonumber

IO->>Device: ws.uart.B2D { write }
Note over IO, Device: descriptor: { uart_nbr: 1, device_id: "stepper-1" }<br/>text_data: "G1 X10 Y20"

Device->>IO: ws.uart.D2B { written }
Note over Device, IO: descriptor: { uart_nbr: 1, device_id: "stepper-1" }<br/>bytes_written: 11
```

### Detaching a UART Component

```mermaid
sequenceDiagram
autonumber

IO->>Device: ws.uart.B2D { remove }
Note over IO, Device: descriptor: { uart_nbr: 1, device_id: "pm25-1" }

Device->>Device: Detach driver, deinitialize port
```
