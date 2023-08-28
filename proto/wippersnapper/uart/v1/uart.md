
# uart.proto

This file details the WipperSnapper messaging API for interfacing with a UART bus.

## WipperSnapper Components

The following WipperSnapper components utilize `uart.proto`:

* PMS* Air Quality Sensors
* Adafruit Universal GPS module using the MTK33x9 chipset


## Sequence Diagrams

### Attaching a UART Component to a device running WipperSnapper 

```mermaid
sequenceDiagram
autonumber

IO-->>WS Device: UARTDeviceAttachRequest

WS Device-->>WS Device Decoder: UARTDeviceAttachRequest

WS Device Decoder-->>WS Device UART: UARTBusData
Note over WS Device Decoder, WS Device UART: Initialize UART bus using configuration (UARTBusData).

WS Device Decoder-->>WS Device UART: device_id, polling_interval
Note over WS Device Decoder, WS Device UART: Initialize UART device on the UART bus and associate it with a driver and a polling period.

WS Device UART-->>WS Device: UARTDeviceAttachResponse

WS Device-->>IO: UARTDeviceAttachResponse
Note over WS Device, IO: Returns true if successful, False if not.
```




