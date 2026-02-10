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

### 2. Change DisplayDriver from Enum to String

**Rationale:** Using strings allows adding new drivers without protobuf changes. The driver name identifies the chip/controller IC.

```protobuf
message DisplayAddOrReplace {
  DisplayType type = 1;  // Enum: EPD, TFT, OLED, LED_BACKPACK, CHAR_LCD
  string driver    = 2;  // String: Driver chip name (e.g., "UC8179", "SSD1306")
  string panel     = 3;  // Optional: Panel identifier for driver (e.g., "5.83-648x480")
  string name      = 4;  // Display instance name
  // ... rest of message
}
```

**Known Driver Strings** (for reference - not enforced by proto):

```
// EPD (E-Paper Display) Drivers
"SSD1680"   // EPD controller for monochrome e-paper
"ILI0373"   // EPD controller (also known as SSD167)
"UC8253"    // EPD controller for 3.7" displays
"UC8179"    // EPD controller for 5.83" displays
"UC8151"    // EPD controller for flexible e-ink (also ILI0343)
"SSD1683"   // EPD controller for 4.2" grayscale displays

// TFT (Color LCD) Drivers
"ST7789"    // TFT LCD controller
"ILI9341"   // TFT LCD controller
"ST7735"    // TFT LCD controller

// OLED Drivers
"SSD1306"   // Monochrome OLED (128x64, 128x32)
"SH1106"    // Monochrome OLED (128x64)
"SSD1327"   // 4-bit grayscale OLED
"SSD1351"   // Color OLED

// LED Backpack Drivers
"HT16K33"   // Adafruit LED backpacks (7-segment, alphanumeric)

// Character LCD Drivers
"HD44780"   // Standard character LCD controller (via I2C backpack)
"PCF8574"   // I2C to parallel expander for LCD
```

### 3. Add Panel Identifier Field

For E-Paper displays especially, the same driver can support multiple panel sizes and configurations. The `panel` field identifies the specific panel:

```protobuf
string panel = 3;  // Optional panel identifier
```

**Example Panel Identifiers:**

```
// E-Paper Panels (driver: "UC8179")
"5.83-648x480-mono"     // 5.83" monochrome, 648x480 resolution
"5.65-600x448-7color"   // 5.65" 7-color ACeP display

// E-Paper Panels (driver: "SSD1683")
"4.2-300x400-gray4"     // 4.2" 4-level grayscale, 300x400

// Or use Adafruit product SKUs:
"adafruit-6397"         // Direct product reference
"adafruit-6381"

// OLED Panels (driver: "SSD1306")
"128x64"                // Standard 128x64 OLED
"128x32"                // Smaller 128x32 OLED
"64x48"                 // Tiny 64x48 OLED
```

**Benefits:**
- Same driver code, different panel configs
- Add new panels without proto changes
- Clear hardware specification
- Easier to look up datasheets

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
  DisplayType type = 1;  // Enum: DISPLAY_TYPE_EPD, DISPLAY_TYPE_TFT, etc.
  string driver    = 2;  // Driver chip: "UC8179", "SSD1306", "HT16K33", etc.
  string panel     = 3;  // Panel ID: "5.83-648x480-mono", "adafruit-6397", etc.
  string name      = 4 [(nanopb).max_size = 64];  // Instance name: "weather-display" // maybe should be feedname!

  // Interface configuration (how display is physically connected)
  oneof interface_type {
    EpdSpiConfig spi_epd          = 5;
    TftSpiConfig spi_tft          = 6;
    I2cDisplayConfig i2c          = 7;  // For OLED, LED backpack, char LCD over I2C
    TtlRgb666PinConfig ttl_rgb666 = 8;
    I8080PinConfig i8080          = 9;
    DsiPinConfig dsi              = 10;
  }

  // Display-specific configuration (what the display can do)
  oneof config {
    EPDConfig config_epd              = 11;
    TftConfig config_tft              = 12;
    TtlRgb666Config config_ttl_rgb666 = 13;
    I8080Config config_i8080          = 14;
    DsiConfig config_dsi              = 15;
    OledConfig config_oled            = 16;  // NEW
    LedBackpackConfig config_led      = 17;  // NEW
    CharLcdConfig config_char_lcd     = 18;  // NEW
  }
}
```

**Key Changes:**
- `driver` is now `string` (field 2) - no enum needed
- `panel` is new `string` (field 3) - identifies specific panel for driver
- Field numbers shifted to accommodate new fields

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
  driver: "SSD1306",
  panel: "128x64",
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
  driver: "HT16K33",
  panel: "4digit-7seg",      // 4-digit 7-segment display
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
  driver: "HD44780",
  panel: "16x2",             // 16 columns, 2 rows
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

### Example 4: UC8179 E-Paper with Different Panels

```protobuf
// 5.83" Monochrome E-Ink (Adafruit #6397)
DisplayAddOrReplace {
  type: DISPLAY_TYPE_EPD,
  driver: "UC8179",
  panel: "5.83-648x480-mono",  // Or "adafruit-6397"
  name: "large-eink",

  spi_epd: {
    bus: 0,
    pin_dc: "D10",
    pin_rst: "D9",
    pin_cs: "D8",
    pin_busy: "D11"
  },

  config_epd: {
    mode: EPD_MODE_MONO,
    width: 648,
    height: 480,
    text_size: 3
  }
}

// Same UC8179 driver, different panel size
DisplayAddOrReplace {
  type: DISPLAY_TYPE_EPD,
  driver: "UC8179",
  panel: "5.65-600x448-7color",  // 7-color ACeP display
  name: "color-eink",

  spi_epd: {
    bus: 0,
    pin_dc: "D10",
    pin_rst: "D9",
    pin_cs: "D8",
    pin_busy: "D11"
  },

  config_epd: {
    mode: EPD_MODE_GRAYSCALE4,  // 7-color treated as multi-level
    width: 600,
    height: 448,
    text_size: 2
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

## Additional Benefits of String-Based Driver/Panel

### Flexibility
- **No proto recompilation** - Add new drivers by updating firmware only
- **Rapid iteration** - Test new drivers without proto version bumps
- **Community drivers** - Third parties can add drivers via firmware mods

### E-Paper Specific Benefits
- **One driver, many panels** - UC8179 works with multiple panel sizes
- **Panel-specific tuning** - Different waveforms, refresh rates per panel
- **Product SKU mapping** - `panel: "adafruit-6397"` maps directly to products

### Firmware Implementation
```cpp
// Driver registry in firmware
DisplayDriver* createDriver(const char* driver_name, const char* panel_name) {
  if (strcmp(driver_name, "UC8179") == 0) {
    return new UC8179Driver(panel_name);
  }
  else if (strcmp(driver_name, "SSD1306") == 0) {
    return new SSD1306Driver(panel_name);
  }
  // ... etc
  return nullptr;  // Unknown driver
}

// UC8179 can load panel-specific configs
UC8179Driver::UC8179Driver(const char* panel) {
  if (strcmp(panel, "5.83-648x480-mono") == 0) {
    loadPanelConfig_583_mono();
  }
  else if (strcmp(panel, "5.65-600x448-7color") == 0) {
    loadPanelConfig_565_7color();
  }
  // ... etc
}
```

### Versioning Strategy
```
// Firmware version 2.1.0 supports:
"UC8179", "SSD1306", "HT16K33"

// Firmware version 2.2.0 adds:
"SSD1683", "SH1106", "ILI9341"

// Proto doesn't change!
// Only firmware update needed
```

---

## Summary

This refactor creates a clean, consistent display API where:
- ✅ All displays use same messages (DisplayAddOrReplace, DisplayWrite, DisplayRemove)
- ✅ Interface type (I2C, SPI, parallel) is just a configuration detail
- ✅ Display capabilities (resolution, features) are separate from interface
- ✅ Follows established GPS pattern for multi-interface devices
- ✅ Simplifies component registration at check-in
- ✅ Enables future expansion (DSI, MIPI, etc.) without API changes
- ✅ **String-based drivers** - Add new drivers without proto changes
- ✅ **Panel tracking** - Same driver supports multiple panel configurations
- ✅ **No enum limitations** - Firmware can support any driver/panel combination
