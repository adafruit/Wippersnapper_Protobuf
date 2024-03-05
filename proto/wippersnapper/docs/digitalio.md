
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

### Remove a Digital Pin

```mermaid
sequenceDiagram
autonumber

IO->>Device: ServoWriteRequest
Note over IO, Device: Position is sent from Adafruit IO as a pulse width<br> between 500uS and 2500uS. <br> The client application must convert pulse width to duty cycle<br>with fixed freq of 50Hz prior to writing to the servo pin.
```

  

### Update: Servo

```mermaid
sequenceDiagram
autonumber

IO->>Device: ServoDetachRequest
Note over IO, Device: Deinits servo object, releases gpio pin
IO-->>Device: ServoAttachRequest
Note over IO, Device: Contains:<br> `servo_pin` from form<br>`servo_freq` of 50Hz<br> `min_pulse_width` from form <br> `max_pulse_width` from form
Device->>IO: ServoAttachResponse
Note over IO, Device: Contains: Success code and servo's pin
```

  

### Delete: Servo

```mermaid
sequenceDiagram
autonumber
IO->>Device: ServoDetachRequest
Note over IO, Device: Contains:<br> `servo_pin` from DB.
```

  

### Sync: Servo

```mermaid
sequenceDiagram
autonumber
IO-->>Device: ServoAttachRequest
Note over IO, Device: Contains:<br> `servo_pin` from form<br>`servo_freq` of 50Hz<br> `min_pulse_width` from form <br> `max_pulse_width` from form

Device->>IO: ServoAttachResponse
Note over IO, Device: Contains: Success code and servo's pin
```