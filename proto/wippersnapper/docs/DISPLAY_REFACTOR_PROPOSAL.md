# Display Proto Refactor: Unifying I2C Output Devices

## Problem

Currently in v2, I2C-connected displays (LED backpacks, character LCDs, OLEDs) are separated in `i2c_output.proto` while SPI-connected displays are in `display.proto`. This creates an inconsistent API where the same logical device type (a display) is configured differently depending on its physical interface.

## Solution: Unified Display Proto

Following the GPS pattern (where GPS can be I2C or UART), all displays should be in `display.proto` regardless of interface type (I2C, SPI, parallel, etc.).

---

## Proposed Changes to display.proto

### 1. Expand DisplayType Enum

```protobuf
enum DisplayType {
  DISPLAY_TYPE_UNSPECIFIED = 0;
  DISPLAY_TYPE_EPD         = 1;  // E-Paper Display
  DISPLAY_TYPE_TFT         = 2;  // TFT Color Display
  DISPLAY_TYPE_OLED        = 3;  // OLED Monochrome/Color (NEW)
  DISPLAY_TYPE_LED_BACKPACK = 4; // 7-Seg/Alphanumeric LED (NEW)
  DISPLAY_TYPE_CHAR_LCD    = 5;  // Character LCD (NEW)
}
```

### 2. Expand DisplayDriver Enum

```protobuf
enum DisplayDriver {
  DISPLAY_DRIVER_UNSPECIFIED = 0;

  // EPD Drivers
  DISPLAY_DRIVER_EPD_SSD1680 = 1;
  DISPLAY_DRIVER_EPD_ILI0373 = 2;
  DISPLAY_DRIVER_EPD_UC8253  = 4;
  DISPLAY_DRIVER_EPD_UC8179  = 5;
  DISPLAY_DRIVER_EPD_UC8151  = 6;
  DISPLAY_DRIVER_EPD_SSD1683 = 7;

  // TFT Drivers
  DISPLAY_DRIVER_TFT_ST7789  = 3;

  // OLED Drivers (NEW)
  DISPLAY_DRIVER_OLED_SSD1306 = 10;
  DISPLAY_DRIVER_OLED_SH1106  = 11;
  DISPLAY_DRIVER_OLED_SSD1327 = 12;

  // LED Backpack Drivers (NEW)
  DISPLAY_DRIVER_LED_HT16K33  = 20;  // Adafruit LED backpacks

  // Character LCD Drivers (NEW)
  DISPLAY_DRIVER_LCD_HD44780  = 30;  // Standard character LCD via I2C backpack
}
```

### 3. Add I2C Display Config Messages

Import from i2c_output.proto or define inline:

```protobuf
/**
 * OledConfig for OLED displays (I2C or SPI)
 */
message OledConfig {
  int32 width           = 1;  // Width in pixels
  int32 height          = 2;  // Height in pixels
  int32 text_size       = 3;  // Text scale factor (1 = 6x8px, 2 = 12x16px)
  bool invert           = 4;  // Invert display colors
  int32 contrast        = 5;  // Contrast level (0-255)
}

/**
 * LedBackpackConfig for 7-segment and alphanumeric LED displays
 */
message LedBackpackConfig {
  int32 brightness      = 1;  // Brightness (0-15)
  LedBackpackAlignment alignment = 2;  // Text alignment
  int32 digits          = 3;  // Number of digits (4, 8, etc.)
}

enum LedBackpackAlignment {
  LBA_UNSPECIFIED = 0;
  LBA_LEFT        = 1;
  LBA_RIGHT       = 2;
  LBA_CENTER      = 3;
}

/**
 * CharLcdConfig for character LCD displays
 */
message CharLcdConfig {
  int32 rows            = 1;  // Number of rows (2, 4, etc.)
  int32 columns         = 2;  // Number of columns (16, 20, etc.)
  bool enable_backlight = 3;  // Backlight on/off
}

/**
 * I2cDisplayConfig for I2C-connected displays
 * This is separate from I2cBusConfig as it includes display-specific I2C params
 */
message I2cDisplayConfig {
  uint32 device_address = 1;  // 7-bit I2C address (e.g., 0x3C for SSD1306)
  string bus_sda        = 2;  // Optional alternate SDA pin
  string bus_scl        = 3;  // Optional alternate SCL pin
}
```

### 4. Update DisplayAddOrReplace Message

```protobuf
message DisplayAddOrReplace {
  DisplayType type     = 1;
  DisplayDriver driver = 2;
  string name          = 3 [(nanopb).max_size = 64];

  // Interface configuration (how display is physically connected)
  oneof interface_type {
    EpdSpiConfig spi_epd          = 4;
    TftSpiConfig spi_tft          = 5;
    I2cDisplayConfig i2c          = 6;  // For OLED, LED backpack, char LCD over I2C
    TtlRgb666PinConfig ttl_rgb666 = 7;
    I8080PinConfig i8080          = 8;
    DsiPinConfig dsi              = 9;
  }

  // Display-specific configuration (what the display can do)
  oneof config {
    EPDConfig config_epd              = 10;
    TftConfig config_tft              = 11;
    TtlRgb666Config config_ttl_rgb666 = 12;
    I8080Config config_i8080          = 13;
    DsiConfig config_dsi              = 14;
    OledConfig config_oled            = 15;  // NEW
    LedBackpackConfig config_led      = 16;  // NEW
    CharLcdConfig config_char_lcd     = 17;  // NEW
  }
}
```

### 5. Update DisplayWrite for I2C Displays

DisplayWrite already supports text messages, which works for all I2C displays:

```protobuf
message DisplayWrite {
  string name = 1 [(nanopb).max_size = 64];
  oneof content {
    string message               = 2 [(nanopb).max_size = 1024];  // Works for LED, LCD, OLED
    string url                   = 3 [(nanopb).max_size = 10240]; // For graphical displays
    string base64image           = 4 [(nanopb).max_size = 102400];
    BinaryImageType binary_image = 5;
  }

  // Display-specific write options (optional)
  bool clear_first  = 6;  // Clear display before writing
  int32 cursor_x    = 7;  // Cursor position X (for char LCD)
  int32 cursor_y    = 8;  // Cursor position Y (for char LCD)
}
```

---

## Usage Examples

### Example 1: SSD1306 OLED over I2C

```protobuf
DisplayAddOrReplace {
  type: DISPLAY_TYPE_OLED,
  driver: DISPLAY_DRIVER_OLED_SSD1306,
  name: "status-display",

  i2c: {
    device_address: 0x3C
  },

  config_oled: {
    width: 128,
    height: 64,
    text_size: 1,
    contrast: 127
  }
}
```

### Example 2: 7-Segment LED Backpack over I2C

```protobuf
DisplayAddOrReplace {
  type: DISPLAY_TYPE_LED_BACKPACK,
  driver: DISPLAY_DRIVER_LED_HT16K33,
  name: "clock-display",

  i2c: {
    device_address: 0x70
  },

  config_led: {
    brightness: 8,
    alignment: LBA_RIGHT,
    digits: 4
  }
}
```

### Example 3: Character LCD over I2C

```protobuf
DisplayAddOrReplace {
  type: DISPLAY_TYPE_CHAR_LCD,
  driver: DISPLAY_DRIVER_LCD_HD44780,
  name: "info-display",

  i2c: {
    device_address: 0x27
  },

  config_char_lcd: {
    rows: 2,
    columns: 16,
    enable_backlight: true
  }
}
```

### Example 4: Writing to any display

```protobuf
// Works for LED backpack, char LCD, OLED, etc.
DisplayWrite {
  name: "clock-display",
  message: "12:34"
}

DisplayWrite {
  name: "info-display",
  message: "Temp: 23.5C\nHumidity: 45%",
  cursor_x: 0,
  cursor_y: 0,
  clear_first: true
}
```

---

## Benefits of Unified Approach

### 1. Consistent API

```
// ALL displays use the same pattern:
DisplayAddOrReplace → DisplayAddedOrReplaced
DisplayWrite → (no response)
DisplayRemove → DisplayRemoved
```

No special handling for "I2C displays" vs "SPI displays" at the API level.

### 2. Interface Independence

```
type: DISPLAY_TYPE_OLED
interface: I2C (address 0x3C)

OR

type: DISPLAY_TYPE_OLED
interface: SPI (bus 0, pins...)
```

Same display type, different interface - handled naturally.

### 3. Follows GPS Pattern

```
GPS via I2C:
  i2c.DeviceAddOrReplace {
    is_gps: true,
    gps_config: {...}
  }

GPS via UART:
  uart.Add {
    is_gps: true,
    gps_config: {...}
  }
```

```
Display via I2C:
  DisplayAddOrReplace {
    type: DISPLAY_TYPE_OLED,
    i2c: {...},
    config_oled: {...}
  }

Display via SPI:
  DisplayAddOrReplace {
    type: DISPLAY_TYPE_OLED,
    spi: {...},
    config_oled: {...}
  }
```

### 4. Cleaner Component Registration

```protobuf
// At check-in, all displays look the same:
component_adds: [
  {display: {
    type: DISPLAY_TYPE_OLED,
    i2c: {device_address: 0x3C},
    ...
  }},
  {display: {
    type: DISPLAY_TYPE_EPD,
    spi_epd: {...},
    ...
  }}
]
```

No need for separate `i2c_output` component type.

---

## Migration Path

### Phase 1: Add new types to display.proto
- Add OLED, LED_BACKPACK, CHAR_LCD to DisplayType
- Add drivers to DisplayDriver
- Add config messages
- Add I2cDisplayConfig

### Phase 2: Update i2c.proto
- Remove or deprecate i2c_output references
- Point to display.proto for display devices

### Phase 3: Update firmware
- Implement new display types in display controller
- Migrate I2C display handling from I2C controller to display controller

### Phase 4: Update docs
- Update display.md to show all display types
- Add examples for I2C-connected displays
- Update HAPPY_PATH.md to show unified display registration

---

## Implementation Notes

### I2cDisplayConfig vs I2cBusConfig

`I2cDisplayConfig` is display-specific and includes just the essentials:
- device_address (required)
- bus_sda/bus_scl (optional, for alternate buses)

This is simpler than the full I2C bus config which includes multiplexers, alternate buses, etc.

### DisplayDriver Naming

Follow convention:
- `DISPLAY_DRIVER_[TYPE]_[CHIP]`
- EPD_SSD1680, TFT_ST7789, OLED_SSD1306, LED_HT16K33, LCD_HD44780

### Text-Only vs Graphical Displays

The API handles both:
- **Text-only** (LED, char LCD): Use `message` field in DisplayWrite
- **Graphical** (OLED, EPD, TFT): Can use `message`, `url`, `base64image`, or `binary_image`

### Backlight Control

For char LCDs, backlight can be:
1. Set at init time: `enable_backlight` in config
2. Toggled at write time: Add optional `backlight` field to DisplayWrite

---

## Questions to Resolve

1. **Should I2C displays have their own B2D/D2B envelopes?**
   - No - all displays use top-level Display messages
   - Display controller routes to appropriate driver based on interface_type

2. **How to handle display-specific write features?**
   - Add optional fields to DisplayWrite (cursor_x, cursor_y, etc.)
   - Use driver-specific interpretation (e.g., HT16K33 ignores cursor)

3. **Should SSD1306 be OLED-specific or general?**
   - SSD1306 can drive both OLED and LCD panels
   - Keep as DISPLAY_DRIVER_OLED_SSD1306 for now
   - Can add DISPLAY_DRIVER_LCD_SSD1306 if needed

---

## Summary

This refactor creates a clean, consistent display API where:
- ✅ All displays use same messages (DisplayAddOrReplace, DisplayWrite, DisplayRemove)
- ✅ Interface type (I2C, SPI, parallel) is just a configuration detail
- ✅ Display capabilities (resolution, features) are separate from interface
- ✅ Follows established GPS pattern for multi-interface devices
- ✅ Simplifies component registration at check-in
- ✅ Enables future expansion (DSI, MIPI, etc.) without API changes
