# pixels.proto

This file details the WipperSnapper messaging API for interfacing with a strand of addressable RGB(W) pixels (Adafruit NeoPixel/WS2812b, DotStar/APA102).

## WipperSnapper Components

The following component definitions reference `pixels.proto`:
* [Adafruit_DotStar](https://github.com/adafruit/Wippersnapper_Components/pull/44)
* [Adafruit_NeoPixels](https://github.com/adafruit/Wippersnapper_Components/pull/44)

## Architecture Overview

The v2 Pixels API uses message envelopes:

- **B2D (BrokerToDevice)** - Commands from Adafruit IO to device
  - `add` - Add a strand of addressable pixels
  - `remove` - Remove a strand and release resources
  - `write` - Write a color to a strand

- **D2B (DeviceToBroker)** - Responses from device to Adafruit IO
  - `added` - Confirmation of strand initialization

## Enums

### Type
| Value | Description |
|-------|-------------|
| `T_UNSPECIFIED` | Unspecified (error) |
| `T_NEOPIXEL` | NeoPixel strand |
| `T_DOTSTAR` | DotStar strand |

### Order (Color Ordering)
| Value | Description |
|-------|-------------|
| `O_GRB` | Green, Red, Blue (NeoPixel default) |
| `O_GRBW` | Green, Red, Blue, White |
| `O_RGB` | Red, Green, Blue |
| `O_RGBW` | Red, Green, Blue, White |
| `O_BRG` | Blue, Red, Green (DotStar default) |
| `O_RBG` | Red, Blue, Green |
| `O_GBR` | Green, Blue, Red |
| `O_BGR` | Blue, Green, Red |

## Message Details

### Add

- **type** - Pixel type (`T_NEOPIXEL` or `T_DOTSTAR`)
- **num** - Number of pixels in the strand
- **ordering** - Color ordering (e.g., `O_GRB`)
- **brightness** - Strand brightness (0-255)
- **pin_data** - Data pin for NeoPixel or DotStar
- **pin_dotstar_clock** - Clock pin (DotStar only)
- **write** - Optional initial write (used during check-in)

### Write

- **pin_data** - Data pin of the strand
- **color** - 32-bit color value (MSB: white for RGBW or ignored for RGB, then red, green, blue LSB)

### Added (response)

- **is_success** - True if strand initialized successfully
- **pin_data** - Data pin of the responding strand

## Sequence Diagrams

### Create: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_NEOPIXEL<br/>num: 8<br/>ordering: O_GRB<br/>brightness: 128<br/>pin_data: "D5"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"
```

### Write: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { write }
Note over IO, Device: pin_data: "D5"<br/>color: 0x00FF0000 (red)
```

### Update: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { remove }
Note over IO, Device: pin_data: "D5"

IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_NEOPIXEL<br/>num: 16<br/>ordering: O_GRB<br/>brightness: 64<br/>pin_data: "D5"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"
```

### Delete: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { remove }
Note over IO, Device: pin_data: "D5"
```

### Sync: NeoPixel
```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_NEOPIXEL<br/>num: 8<br/>ordering: O_GRB<br/>brightness: 128<br/>pin_data: "D5"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"

IO->>Device: ws.pixels.B2D { write }
Note over IO, Device: pin_data: "D5"<br/>color: 0x0000FF00 (green, from feed's last_value)
```


### Create: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_DOTSTAR<br/>num: 12<br/>ordering: O_BRG<br/>brightness: 128<br/>pin_data: "D5"<br/>pin_dotstar_clock: "D6"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"
```

### Write: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { write }
Note over IO, Device: pin_data: "D5"<br/>color: 0x0000FF00 (green)
```

### Update: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { remove }
Note over IO, Device: pin_data: "D5"

IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_DOTSTAR<br/>num: 24<br/>ordering: O_BRG<br/>brightness: 64<br/>pin_data: "D5"<br/>pin_dotstar_clock: "D6"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"
```

### Delete: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { remove }
Note over IO, Device: pin_data: "D5"
```

### Sync: DotStar
```mermaid
sequenceDiagram
autonumber
IO->>Device: ws.pixels.B2D { add }
Note over IO, Device: type: T_DOTSTAR<br/>num: 12<br/>ordering: O_BRG<br/>brightness: 128<br/>pin_data: "D5"<br/>pin_dotstar_clock: "D6"

Device->>IO: ws.pixels.D2B { added }
Note over Device,IO: is_success: true<br/>pin_data: "D5"

IO->>Device: ws.pixels.B2D { write }
Note over IO, Device: pin_data: "D5"<br/>color: 0x00FF0000 (red, from feed's last_value)
```
