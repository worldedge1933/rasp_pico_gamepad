from machine import Pin, SPI
import time
import st7789py as st7789
class draw():
    def __init__(self, LCD: st7789.ST7789) -> None:
        self.LCD = LCD
        
    def arrow(self, x0: int, y0: int, size: int, direction: str, color=st7789.WHITE):
        '''
        Args:
            x0 (int): start point x coordinate
            y0 (int): start point y coordinate
            size (int): the size of the arrow
            direction (str): the direction of the arrow

                - 'u'-up
                - 'd'-down
                - 'l'-left
                - 'r'-right
        '''
        if direction == 'r':
            self.LCD.line(x0 + size - 1, y0 + (size // 2 + size % 2) - 1, x0, y0 , color)
            self.LCD.line(x0 + size - 1, y0 + (size // 2 + size % 2) - 1, x0, y0 + size - 1, color)  
        if direction == 'l':
            self.LCD.line(x0, y0 + (size // 2 + size % 2) - 1, x0 + size - 1, y0, color)
            self.LCD.line(x0, y0 + (size // 2 + size % 2) - 1, x0 + size - 1, y0 + size - 1, color)
        if direction == 'u':
            self.LCD.line(x0 + (size // 2 + size % 2) - 1, y0, x0, y0 + size -1, color)
            self.LCD.line(x0 + (size // 2 + size % 2) - 1, y0, x0 + size -1, y0 + size - 1, color)
        if direction == 'd':
            self.LCD.line(x0 + (size // 2 + size % 2) - 1, y0 + size -1, x0, y0, color)
            self.LCD.line(x0 + (size // 2 + size % 2) - 1, y0 + size -1, x0 + size - 1, y0, color)


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
    
    pen = draw(tft)
    tft.fill(st7789.BLACK)
    for str in ['u', 'd', 'l', 'r']:
        tft.fill_rect(30,30,30,30,st7789.BLACK)
        pen.arrow(30,30,30,str)
        time.sleep(0.5)
