# pixels.proto

This file details the WipperSnapper messaging API for interfacing with a strand of addressable RGB(W) pixels (Adafruit NeoPixel/WS2812b, DotStar/APA102). 


## Component Form Diagram

TODO

## Component Widget Diagram

TODO

## Sequence Diagrams 

### Create: NeoPixel

```mermaid
sequenceDiagram
autonumber
IO-->>Device: PixelsCreateRequest
Note over IO, Device: Contains:<br> `pixels_type` of PIXELS_TYPE_NEOPIXEL<br>`pixels_num` according to form<br>`pixels_ordering` according to form<br> `pixels_brightness` of 0<br>`pixels_pin_neopixel` according to form<br> `pixels_pin_dotstar_data` is unused<br>`pixels_pin_dotstar_clock` is unused

```

### Update: NeoPixel

### Delete: NeoPixel

### Sync: NeoPixel


### Create: DotStar

### Update: DotStar

### Delete: DotStar

### Sync: DotStar


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```