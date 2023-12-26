import st7789py as st7789
from machine import SPI, Pin
from draw import draw
import time

            
class Array:
    def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y 
    def __add__(self, other):
        if (type(other) == list) and len(other) == 2:
            return Array(self.x + other[0], self.y + other[1])
        if isinstance(self, Array) == True:
            return Array(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        if (type(other) == list) and len(other) == 2:
            return Array(self.x - other[0], self.y - other[1])
        if isinstance(self, Array) == True:
            return Array(self.x - other.x, self.y - other.y)
        
    def __repr__(self) -> str:
        return f'{[self.x,self.y]}'
    
        
class Tetris:
    def __init__(self, LCD: st7789.ST7789):
        self.LCD = LCD
#        self.map = [[1,1,1,1,1,1,1,1,1,1,1,1]]
#        line = [1,0,0,0,0,0,0,0,0,0,0,1]
#        self.map += [line[:] for _ in range(20)]
#        self.map += [[1,1,1,1,1,1,1,1,1,1,1,1]]
        self.maps = [0]*20
        self.maps += [int('1111111111',2)]
        self.pen = draw(LCD)
    
    def show(self):
        self.LCD.fill(st7789.BLACK)
        self.LCD.fill_rect(5,5,121,231,st7789.WHITE)
        self.LCD.fill_rect(10,10,111,221,st7789.BLACK)
        self.pen.arrow(240 - 30 - 18, 75, 30, 'r')
        self.pen.arrow(240 - 30 - 18, 135, 30, 'l')
    def show_tet(self):
        _y = 11
        j = 0
        for j in range(20):
            _x = 11
            for i in range(10):
                if (self.maps[j] >> i) & 1 == 1:
                    self.LCD.fill_rect(_x, _y, 10, 10, st7789.WHITE)
                _x += 11
            _y += 11
    def block(self):
        self.blocks = []
        self.blocks += [Array(5,1),Array(6,1),Array(4,1),Array(5,0)]
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.WHITE)
            
    def down(self):
        for block in self.blocks:
            if (self.maps[block.y + 1] >> block.x) & 1 == 1:
                return False
        lastblocks = self.blocks[:]
        self.blocks = []
        for block in lastblocks:
            self.blocks += [block + Array(0,1)]
        for block in lastblocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.BLACK)
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.WHITE)      
        return True  
        
        
        
#                if self.map[j][i] == 1:
#                    self.LCD.fill_rect(i * 11, j * 11, 10, 10, st7789.WHITE)


                    
                
            
def main(LCD : st7789.ST7789, key_up_ : Pin, key_down_ : Pin, key_left_ : Pin, key_right_ : Pin, key_A_ : Pin, key_B_ : Pin, key_X_ : Pin, key_Y_ : Pin) -> None:
    tetris = Tetris(LCD)
    tetris.show()
    tetris.block()
    can_down = True
    while can_down:
        time.sleep(1)
        can_down = tetris.down()
    while True:
        if key_Y_.value() == 0:
            while True:
                if key_Y_.value() == 1:
                    break
            return
    
if __name__ == '__main__':
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

    key_up = Pin(2, Pin.IN, Pin.PULL_UP)
    key_down = Pin(18, Pin.IN, Pin.PULL_UP)
    key_left = Pin(16, Pin.IN, Pin.PULL_UP)
    key_right = Pin(20, Pin.IN, Pin.PULL_UP)
    key_A = Pin(15, Pin.IN, Pin.PULL_UP)
    key_B = Pin(17, Pin.IN, Pin.PULL_UP)
    key_X = Pin(19, Pin.IN, Pin.PULL_UP)
    key_Y = Pin(21, Pin.IN, Pin.PULL_UP)
    
    main(tft, key_up, key_down, key_left, key_right, key_A, key_B, key_X, key_Y)