
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
WS Device-->>WS Device Decoder: Decode UARTDeviceAttachRequest
WS Device Decoder-->>WS Device UART: Configure UART bus with UARTBusData and attach device per device_id and polling_interval
WS Device UART-->>WS Device: Create UARTDeviceAttachResponse
WS Device-->>IO: UARTDeviceAttachResponse
Note over WS Device, IO: Returns true if successful, False if not.
```




