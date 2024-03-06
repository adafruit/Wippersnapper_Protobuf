
# digitalio.proto

  This file details the WipperSnapper messaging API for interfacing with digital I/O pins.

## WipperSnapper Components

The following WipperSnapper components utilize `servo.proto`:
* [pin](https://github.com/adafruit/Wippersnapper_Components/tree/main/components/pin)


## Sequence Diagrams

### Add a Digital Pin

```mermaid
sequenceDiagram
autonumber
IO->>Device: DeviceToBroker
Device->>App: DeviceToBroker
App->>Encoder/Decoder: DeviceToBroker
Encoder/Decoder->>Digital IO Class: DigitalIOAdd
```
