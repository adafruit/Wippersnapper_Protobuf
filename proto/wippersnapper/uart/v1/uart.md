
# uart.proto

This file details the WipperSnapper messaging API for interfacing with a UART bus.

## WipperSnapper Components

The following WipperSnapper components utilize `pwm.proto`:

* PMS* Air Quality Sensors
* Adafruit Universal GPS module using the MTK33x9 chipset


## Sequence Diagrams

### UART Bus Initialization 

```mermaid
sequenceDiagram
autonumber

IO-->>Device: UARTInitRequest

Device->>IO: UARTInitResponse
Note over IO, Device: Returns true if successful, False if not.
```

### Attaching a device to the UART bus

```mermaid
sequenceDiagram
autonumber

IO-->>Device: UARTDeviceAttachRequest

Device->>IO: UARTDeviceAttachResponse
```



