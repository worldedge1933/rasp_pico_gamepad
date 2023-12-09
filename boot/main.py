from machine import Pin, SoftSPI
import st7789py as st7789
import vga1_16x16
import gc
from draw import draw

def main(LCD: st7789.ST7789, key_up_: Pin, key_down_: Pin, key_left_: Pin, key_right_: Pin, key_A_: Pin, key_B_: Pin, key_X_: Pin, key_Y_: Pin) -> None:
    pen = draw(LCD)
    while True:
        LCD.text(vga1_16x16, "games:", 10, 30, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "1.snake", 10, 60, color=st7789.WHITE, background=st7789.BLACK)
        pen.arrow(240 - 30 - 10, 75, 30, 'r')
        pen.arrow(240 - 30 - 10, 135, 30, 'l')
        LCD.text(vga1_16x16, "choose", 134, 202, color=st7789.WHITE, background=st7789.BLACK)
        while True:
            if key_Y_.value() == 0:
                import snake
                snake.main(LCD, key_up_, key_down_, key_left_, key_right_, key_A_, key_B_, key_X_, key_Y_)
                del snake
                gc.collect()
                break


if __name__ == "__main__":
    tft = st7789.ST7789(
        SoftSPI(baudrate=30000000, polarity=1, sck=Pin(10), mosi=Pin(11), miso=Pin(16)),
        240,
        240,
        reset=Pin(12, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(13, Pin.OUT),
        rotation=1)

    key_up = Pin(2, Pin.IN, Pin.PULL_UP)
    key_down = Pin(18, Pin.IN, Pin.PULL_UP)
    key_left = Pin(16, Pin.IN, Pin.PULL_UP)
    key_right = Pin(20, Pin.IN, Pin.PULL_UP)
    key_A = Pin(15, Pin.IN, Pin.PULL_UP)
    key_B = Pin(17, Pin.IN, Pin.PULL_UP)
    key_X = Pin(19, Pin.IN, Pin.PULL_UP)
    key_Y = Pin(21, Pin.IN, Pin.PULL_UP)

    main(tft, key_up, key_down, key_left, key_right, key_A, key_B, key_X, key_Y)