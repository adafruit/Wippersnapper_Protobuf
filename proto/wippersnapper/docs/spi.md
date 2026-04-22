# spi.proto

Reusable SPI bus and device pin configuration, shared across WipperSnapper component types.

## DeviceConfig

Identifies an SPI device by bus number and pin assignments for the four standard SPI signals plus chip select.

```protobuf
message DeviceConfig {
  int32 bus       = 1;  // SPI bus number (0, 1, ...)
  string pin_mosi = 2;  // MOSI pin
  string pin_sck  = 3;  // SCK pin
  string pin_miso = 4;  // MISO pin (leave empty if device is write-only)
  string pin_cs   = 5;  // Chip Select pin
}
```

### Field Details

| Field | Description |
|-------|-------------|
| **bus** | SPI peripheral index. `0` selects the default/first SPI bus. |
| **pin_mosi** | Master Out Slave In. Required for all SPI devices. |
| **pin_sck** | Serial Clock. Required for all SPI devices. |
| **pin_miso** | Master In Slave Out. Optional — omit for write-only devices (displays, DACs). |
| **pin_cs** | Chip Select (active low). Each device on a shared bus needs its own CS pin. |

### Hardware SPI vs Software SPI

When `pin_mosi` and `pin_sck` match the board's default SPI bus pins, the firmware uses hardware SPI (fast DMA transfers). Non-default pins fall back to software bit-bang SPI (slower).

## Usage by Other Protos

`DeviceConfig` is imported by component protos that communicate over SPI. Each component adds its own peripheral-specific pins on top.

### Displays (display.proto)

Display SPI configs extend `DeviceConfig` with Data/Command and Reset pins:

```protobuf
import "spi.proto";

message TftSpiConfig {
  ws.spi.DeviceConfig spi = 1;  // SPI bus + standard pins
  string pin_dc  = 2;           // Data/Command pin
  string pin_rst = 3;           // Reset pin
}

message EpdSpiConfig {
  ws.spi.DeviceConfig spi = 1;  // SPI bus + standard pins
  string pin_dc       = 2;      // Data/Command pin
  string pin_rst      = 3;      // Reset pin
  string pin_sram_cs  = 4;      // SRAM Chip Select (optional)
  string pin_busy     = 5;      // Busy signal pin
}
```

See [display.md](display.md) for full display API documentation.

## Related Documentation

- [display.md](display.md) — Display API (SPI TFT and EPD displays)
- [i2c.md](i2c.md) — I2C interface (analogous shared bus config)
