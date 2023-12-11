from machine import Pin, SPI
import st7789py as st7789

tft = st7789.ST7789(
        SPI(1,100000_000,polarity=1, phase=1,sck=Pin(10),mosi=Pin(11),miso=None),
        240,
        240,
        reset=Pin(12, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=1
    )

