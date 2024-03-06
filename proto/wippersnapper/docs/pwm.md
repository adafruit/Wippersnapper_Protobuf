
# pwm.proto

This file details the WipperSnapper messaging API for interfacing with PWM output components.

PWM components either have a fixed frequency with a variable duty cycle _or_ a variable frequency with a fixed duty cycle.

## WipperSnapper Components

The following WipperSnapper components utilize `pwm.proto`:

* Dimmable LED (Fixed Frequency, variable Duty Cycle)

* Piezo Buzzer (Variable Frequency, fixed Duty Cycle)


## Sequence Diagrams

### Create: Dimmable LED

```mermaid
sequenceDiagram
autonumber

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to form<br>`frequency` of 5000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.
```


### Write: Dimmable LED
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMWriteDutyCycle
Note over IO, Device: The duty_cycle (0->255) from the <br>IO slider widget is written to the `pin`.
```

### Update: Dimmable LED
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMRemove
Note over IO, Device: Detaches GPIO pin from a timer

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to form<br>`frequency` of 5000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.
```

### Delete: Dimmable LED
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMRemove
Note over IO, Device: Detaches GPIO pin from a timer
```

### Sync: Dimmable LED
```mermaid
sequenceDiagram
autonumber

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to DB<br>`frequency` of 5000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.

IO->>Device: PWMWriteDutyCycle
Note over IO, Device: duty_cycle (0->255) from IO feed's last_value.
```

### Create: Piezo Buzzer

```mermaid
sequenceDiagram
autonumber

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to form<br>`frequency` of 1000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.
```


### Write: Piezo Buzzer
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMWriteFrequency
Note over IO, Device: Any frequency > 0Hz to play a tone, 0Hz to turn off
```

### Update: Piezo Buzzer
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMRemove
Note over IO, Device: Detaches GPIO pin from a timer

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to form<br>`frequency` of 1000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.
```

### Delete: Piezo Buzzer
```mermaid
sequenceDiagram
autonumber
IO->>Device: PWMRemove
Note over IO, Device: Detaches GPIO pin from a timer
```

### Sync: Piezo Buzzer
```mermaid
sequenceDiagram
autonumber

IO-->>Device: PWMAdd
Note over IO, Device: Contains:<br> `pin` according to DB<br>`frequency` of 1000Hz<br> `resolution` of 12 bits

Device->>IO: PWMAdded
Note over IO, Device: Contains:<br> `pin` from <br>corresponding PWMAdd msg. <br>`did_attach` True if attached.

IO->>Device: PWMWriteFrequency
Note over IO, Device: frequency, in Hz, from IO feed's last_value.
```
