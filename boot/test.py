from machine import Pin, SPI
import st7789py as st7789
import framebuf
import time


if __name__ == "__main__":
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
    tft.fill(st7789.BLUE)
    # FrameBuffer needs 2 bytes for every RGB565 pixel
    with open('snake_icon.565','rb') as f:
        fbuf = framebuf.FrameBuffer(bytearray(f.read()), 100, 100, framebuf.RGB565)

    tft.blit_buffer(fbuf,30,30,100,100)

 