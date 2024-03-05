
# checkin.proto

This file details connecting a new or existing hardware to the Adafruit IO MQTT broker.

## WipperSnapper Components

  

The following WipperSnapper components utilize `servo.proto`:
* [Generic Servo](https://github.com/adafruit/Wippersnapper_Components/tree/main/components/servo/servo)
  

## Sequence Diagrams

  

### Create: Servo

```mermaid
sequenceDiagram
autonumber
IO-->>Device: ServoAttachRequest
Note over IO, Device: Contains:<br> `servo_pin` from form<br>`servo_freq` of 50Hz<br> `min_pulse_width` from form <br> `max_pulse_width` from form

Device->>IO: ServoAttachResponse
Note over IO, Device: Contains: Success code and servo's pin
```

### Write: Servo

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