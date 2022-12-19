# pixels.proto

This file details the WipperSnapper messaging API for interfacing with a strand of addressable RGB(W) pixels (Adafruit NeoPixel/WS2812b, DotStar/APA102).

## WipperSnapper Components

The following component definitions reference `pixels.proto`:
* [Adafruit_DotStar](https://github.com/adafruit/Wippersnapper_Components/pull/44)
* [Adafruit_NeoPixels](https://github.com/adafruit/Wippersnapper_Components/pull/44)

## Sequence Diagrams

### Create: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` according to form <br>`pixels_pin_neopixel` according to form<br> `pixels_pin_dotstar_data` is unused<br>`pixels_pin_dotstar_clock` is unused
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
```

### Write: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsWriteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>pixels_pin_data according to DB<br>`pixels_pin_data` according to DB<br>`pixels_color` according to picker<br>
```

### Update: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsDeleteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>pixels_pin_data according to DB
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` of 0<br>`pixels_pin_neopixel` according to form<br> `pixels_pin_dotstar_data` is unused<br>`pixels_pin_dotstar_clock` is unused
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
```

### Delete: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsDeleteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_pin_data` according to DB
```

### Sync: NeoPixel
```mermaid
sequenceDiagram
autonumber
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` according to form <br>`pixels_pin_neopixel` according to form<br> `pixels_pin_dotstar_data` is unused<br>`pixels_pin_dotstar_clock` is unused
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
IO->>Device: PixelsWriteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_pin_data` according to DB<br>`pixels_color` according to feed's last_value<br>
```


### Create: DotStar

```mermaid
sequenceDiagram
autonumber
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` according to form <br>`pixels_pin_neopixel` unused<br> `pixels_pin_dotstar_data` according to form<br>`pixels_pin_dotstar_clock` according to form
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
```

### Write: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsWriteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>`pixels_pin_data` according to DB<br>`pixels_color` according to picker<br>
```

### Update: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsDeleteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>pixels_pin_data according to DB
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` of 0<br>`pixels_pin_neopixel` is unused<br> `pixels_pin_dotstar_data` according to form<br>`pixels_pin_dotstar_clock` according to form
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
```

### Delete: DotStar

```mermaid
sequenceDiagram
autonumber
IO->>Device: PixelsDeleteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>`pixels_pin_data` according to DB
```

### Sync: DotStar
```mermaid
sequenceDiagram
autonumber
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_DOTSTAR<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` according to form <br>`pixels_pin_neopixel` is unused<br> `pixels_pin_dotstar_data` according to form<br>`pixels_pin_dotstar_clock` according to form
Device->>IO: PixelsCreateResponse
Note over Device,IO: `is_success`, true if init'd OK
IO->>Device: PixelsWriteRequest
Note over IO, Device: Contains<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_pin_data` according to DB<br>`pixels_color` according to feed's last_value<br>
```
