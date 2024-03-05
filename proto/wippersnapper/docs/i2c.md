
# i2c.proto

This file details the API used by hardware running Adafruit WipperSnapper firmware for interfacing with the I2C bus and I2C sensors.

## WipperSnapper Component Definitions

The following JSON component definition type(s) reference `i2c.proto`:
* [i2c](https://github.com/adafruit/Wippersnapper_Components/tree/main/components/i2c)

## Sequence Diagrams

### I2C Scan

On Adafruit.io, an I2C scan can be initialized one of two ways:
1) User clicks "I2C Scan" button 
2) Users clicks an I2C component from the Component Picker

**Note:** The I2C scan always contains a I2CBusInitRequest message in case the bus was not previously initialized.

```mermaid
sequenceDiagram
autonumber

IO->>Device: I2CBusScanRequest<br>(contains I2CBusInitRequest)
Device->>App: I2CBusInitRequest
App->>Device: BusResponse
Device->>App: i2c_port_number
App->>I2C Class: Perform scan on<br>i2c_port_number 
I2C Class->>App: addresses_found
App->>Device: I2CBusScanResponse
Device->>IO: I2CBusScanResponse
```

### Create a new I2C device

**Note:** I2C devices may contain _multiple_ sensors (i.e: one device can contain a temperature and humidity sensor).  To work with multiple sensors, I2C commands typically contain a `I2CDeviceSensorProperties` sub-message, detailing the properties of the I2C device's sensor.

```mermaid
sequenceDiagram
autonumber

IO->>Device: I2CDeviceInitRequest<br>(contains I2CBusInitRequest)
Device->>App: I2CBusInitRequest
App->>Device: BusResponse
Device->>App: I2CDeviceInitRequest
App->>I2C Class: i2c_device_address, i2c_device_name,<br>i2c_device_properties
Note over App,I2C Class: At this point, the I2C sensor is configured <br>and ready to send data to Adafruit IO.
I2C Class->>App: I2CDeviceInitResponse
App->>Device: I2CDeviceInitResponse
Device->>IO: I2CDeviceInitResponse
```

### Update an existing I2C device

```mermaid
sequenceDiagram
autonumber

IO->>Device: I2CDeviceUpdateRequest
Device->>App: I2CDeviceUpdateRequest
App->>I2C Class: I2CDeviceUpdateRequest
Note over App,I2C Class: Update the properties of the "sub-sensors" <br> specified within i2c_device_properties array.
I2C Class->>App: I2CDeviceUpdateResponse
App->>Device: I2CDeviceUpdateResponse
Device->>IO: I2CDeviceUpdateResponse
```

### Sending data from an I2C component

The process of sending data from an I2C component involves a device sending a `I2CDeviceEvent` message to the broker. Since an i2c component may have more than one sub-component (i.e: a component may contain both a temperature sensor and a humidity sensor), the `sensor_event` is a repeated submessage array which contains the value and corresponding SI unit for all sub-sensors.

While the sequence diagram for this type of message looks simple, the process involves work on the MQTT broker to unpack and parse each `sensor_event` message:

```mermaid
sequenceDiagram
autonumber

Device->>IO: I2CDeviceEvent
```


### Delete an I2C device

The process of deleting an I2C device is straightforward and only requires the device's unique I2C address:

```mermaid
sequenceDiagram
autonumber

IO->>Device: I2CDeviceDeinitRequest
Device->>IO: I2CDeviceDeinitResponse
```


