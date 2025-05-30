# signal.proto

This file details the `signal.proto` message used to communicate between WipperSnapper clients. 

## Message Format
The signal file contains two messages. Both messages contain `oneof` "payload" message, which is a union of all the possible messages that can be sent from a device to the broker (and visa-versa)

### Payload Message Naming Conventions

Message fields within `signal.proto` generally follow the naming convention:
* `_add`: Message contains a command payload for configuring and adding a component to a device.
  * `_added`: Message contains a response payload from an `_add` message 
* `_remove`: Message contains a payload for releasing a component's resources and "removing" it from the device.
  * `_removed`: Message contains a response payload from an `_remove` message
* `_write`: Message contains a payload for transmitting or "writing" data to a component connected to a device.
  * Within `pwm.proto`, there are multiple types of `_write` such as `_write_duty`, `_write_freq`, etc...
*  `_event`: Message is a payload containing sensor data and metadata. Data may be "packed", containing multiple sensor events.

Some message fields do not follow this naming convention because their API is more involved than the general fields above:
* `_scan`: Message contains a command payload for performing a scan of I2C components connected to a device
* `_response`: Message contains a response payload for an action not compatible with any of the above field names.


## Sequence Diagrams

### High-Level Operation

When a message is sent from a broker to a device, the `BrokerToDevice` message is utilized. When a message is sent from a device to a broker, the `DeviceToBroker` message is sent.

```mermaid
sequenceDiagram
autonumber

IO Broker->>Device Client: BrokerToDevice
Note over IO Broker,Device Client: /:username/wprsnpr/:clientId
Device Client->>App: BrokerToDevice
App->>(nanopb) Encoder/Decoder: BrokerToDevice
(nanopb) Encoder/Decoder->>Component Class: ServoAdd 
Component Class->>(nanopb) Encoder/Decoder: Result of ServoAdd, servo_added
(nanopb) Encoder/Decoder->>App: DeviceToBroker
App->>Device Client: DeviceToBroker
Device Client->>IO Broker: DeviceToBroker
Note over IO Broker,Device Client: /:username/wprsnpr/:clientId
```