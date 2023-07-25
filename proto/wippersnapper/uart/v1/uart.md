
# uart.proto

This file details the WipperSnapper messaging API for interfacing with a UART bus.

## WipperSnapper Components

The following WipperSnapper components utilize `pwm.proto`:

* PMS* Air Quality Sensors
* Adafruit Universal GPS module using the MTK33x9 chipset


## Sequence Diagrams

### Attaching a UART Component to a device running WipperSnapper 

```mermaid
sequenceDiagram
autonumber

IO-->>WS Device: UARTDeviceAttachRequest
WS Device-->>WS Device Decoder: UARTDeviceAttachRequest
Note over WS Device, WS Device Decoder: Decodes UARTDeviceAttachRequest and finds UARTBusData, polling_interval and and device_id

WS Device Decoder-->>WS Device UART: UARTBusData
Note over WS Device Decoder, WS Device UART: Initializes UART bus using configuration within UARTBusData.

WS Device Decoder-->>WS Device UART: device_id and polling_interval
Note over WS Device Decoder, WS Device UART: Initializes UART device on bus and associates it with a driver and a polling period.
WS Device UART-->>WS Device: UARTDeviceAttachResponse
WS Device-->>IO: UARTDeviceAttachResponse
Note over WS Device, IO: Returns true if successful, False if not.
```




