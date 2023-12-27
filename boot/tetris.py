import st7789py as st7789
from machine import SPI, Pin
from draw import draw
import time
import vga1_16x16
import random
import gc
            
class Array:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y 
    def rotation(self):
        return Array(self.y, self.x * (-1))
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
        self.maps = [int('100000000001',2)]*20
        self.maps += [int('111111111111',2)]
        self.pen = draw(LCD)
        self.score = 0
        self.blocks = []
        self.block_number = random.randint(0,4)
        self.color_number = random.randint(0,5)
        self.color = 0
    
    def show(self):
        self.LCD.fill(st7789.BLACK)
        self.LCD.fill_rect(5,5,121,231,0x79ef)
        self.LCD.fill_rect(10,10,111,221,st7789.BLACK)
        for i in range(21):
            self.LCD.hline(10, 11 * i + 10, 111, 0x79ef)
        for i in range(11):
            self.LCD.vline(i * 11 + 10, 10, 221, 0x79ef)
        self.LCD.text(vga1_16x16, str(self.score), 140, 20, 0x79ef)
        self.LCD.text(vga1_16x16, 'O', 240 - 30 - 18, 15, 0x79ef)
        self.pen.arrow(240 - 30 - 18, 75, 30, 'r', color=0x79ef)
        self.pen.arrow(240 - 30 - 18, 135, 30, 'l', color=0x79ef)
        self.pen.arrow(240 - 30 - 18, 195, 30, 'd', color=0x79ef)

    def show_tet(self):
        self.LCD.fill_rect(10,10,111,221,st7789.BLACK)
        for i in range(21):
            self.LCD.hline(10, 11 * i + 10, 111, 0x79ef)
        for i in range(11):
            self.LCD.vline(i * 11 + 10, 10, 221, 0x79ef)
        _y = 11
        for j in range(20):
            _x = 11
            for i in range(10):
                if (self.maps[j] >> (i+1)) & 1 == 1:
                    self.LCD.fill_rect(_x, _y, 10, 10, self.color)
                _x += 11
            _y += 11

    def block(self):
        blocks = [[Array(5,1),Array(6,1),Array(4,1),Array(5,0)],
                  [Array(5,1),Array(6,1),Array(6,0),Array(5,0)],
                  [Array(5,1),Array(6,0),Array(4,1),Array(5,0)],
                  [Array(5,1),Array(6,1),Array(4,1),Array(6,0)],
                  [Array(5,2),Array(5,0),Array(5,1),Array(5,3)]]
        colors = [0x9d37, 0xe679, 0xbdb4, 0xbe56, 0xe46f, st7789.MAGENTA]
        self.blocks = []
        self.blocks += blocks[self.block_number]
        for block in self.blocks:
            if (self.maps[block.y] >> (block.x + 1)) & 1 == 1:
                return False
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, colors[self.color_number])
        self.color = colors[self.color_number]
        self.block_number = random.randint(0,4)
        self.color_number = random.randint(0,5)
        self.LCD.fill_rect(140, 75, 50, 50, st7789.BLACK)
        for block in blocks[self.block_number]:
            self.LCD.fill_rect(block.x * 11 + 100, block.y * 11 + 80, 10, 10, colors[self.color_number])

        return True
    
    def rotation(self):
        time.sleep(0.1)
        blocks_new = []
        for block in self.blocks:
            dif = block - self.blocks[0]
            block_new = dif.rotation() + self.blocks[0]
            blocks_new.append(block_new)
            if (self.maps[block_new.y] >> (block_new.x + 1)) & 1 == 1:
                return
        lastblocks = self.blocks[:]
        self.blocks = blocks_new
        for block in lastblocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.BLACK)
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, self.color)      
        return
            
    def down(self):
        for block in self.blocks:
            if (self.maps[block.y + 1] >> (block.x + 1)) & 1 == 1:
                for block in self.blocks:
                    self.maps[block.y] = self.maps[block.y] | (1 << (block.x + 1))
                return False
        lastblocks = self.blocks[:]
        self.blocks = []
        for block in lastblocks:
            self.blocks += [block + Array(0,1)]
        for block in lastblocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.BLACK)
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, self.color)      
        return True  
    
    def right(self):
        time.sleep(0.1)
        for block in self.blocks:
            if (self.maps[block.y] >> (block.x+2)) & 1 == 1:
                return
        lastblocks = self.blocks[:]
        self.blocks = []
        for block in lastblocks:
            self.blocks += [block + Array(1,0)]
        for block in lastblocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.BLACK)
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, self.color)      
        return
    
    def left(self):
        time.sleep(0.1)
        for block in self.blocks:
            if (self.maps[block.y] >> (block.x)) & 1 == 1:
                return
        lastblocks = self.blocks[:]
        self.blocks = []
        for block in lastblocks:
            self.blocks += [block + Array(-1,0)]
        for block in lastblocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, st7789.BLACK)
        for block in self.blocks:
            self.LCD.fill_rect(block.x * 11 + 11, block.y * 11 + 11, 10, 10, self.color)      
        return
    
    def line_clear(self):
        lines = []
        for i in range(20):
            if self.maps[i] == 4095:
                lines.insert(0,i)
        leng = len(lines)
        if leng != 0:
            time.sleep(0.5)
        for line in lines:
            self.maps.pop(line)
            for i in range(10):
                self.LCD.fill_rect(11*i + 11, line * 11 + 11, 10, 10, st7789.BLACK)
        for _ in lines:
            self.maps.insert(0,int('100000000001',2))
        if leng != 0:
            self.score += (leng ** 2 + leng) // 2
            self.LCD.text(vga1_16x16, str(self.score), 140, 20, 0x79ef)
            time.sleep(0.5)
            self.show_tet()

    def end(self):
        self.LCD.fill(st7789.BLACK)
        self.LCD.text(vga1_16x16, "your score :".format(self.score), 4, 30, color=0x79ef, background=st7789.BLACK)
        self.LCD.text(vga1_16x16, "{0}".format(self.score), 4, 60, color=0x79ef, background=st7789.BLACK)
        with open(f'tetris_score.csv', "r") as f:
            data = f.readlines()
            best_score = int(data[0])
        self.LCD.text(vga1_16x16, "best score :".format(best_score), 4, 90, color=0x79ef, background=st7789.BLACK)
        self.LCD.text(vga1_16x16, "{0}".format(best_score), 4, 120, color=0x79ef, background=st7789.BLACK)
        if self.score > best_score:
            with open(f'tetris_score.csv', 'w') as f:
                f.write(str(self.score))
        self.LCD.text(vga1_16x16, "new game", 102, 142, color=0x79ef, background=st7789.BLACK)
        self.LCD.text(vga1_16x16, "exit", 166, 202, color=0x79ef, background=st7789.BLACK)
        while True:
            if self.key_X_.value() == 0:
                while True:
                    if self.key_X_.value() == 1:
                        gc.collect()
                        return True
            if self.key_Y_.value() == 0:
#                print(2)
                while True:
                    if self.key_Y_.value() == 1:
                        gc.collect
                        self.LCD.fill(st7789.BLACK)
                        return False





        
        
    

        
        
        
#                if self.map[j][i] == 1:
#                    self.LCD.fill_rect(i * 11, j * 11, 10, 10, st7789.WHITE)


                    
                
            
def main(LCD : st7789.ST7789, key_up_ : Pin, key_down_ : Pin, key_left_ : Pin, key_right_ : Pin, key_A_ : Pin, key_B_ : Pin, key_X_ : Pin, key_Y_ : Pin) -> None:
    def quick_down(p):
        global rest_time 
        rest_time = 0
    tetris = Tetris(LCD)
    tetris.key_X_ = key_X_
    tetris.key_Y_ = key_Y_
    def irq_A(p):
        key_B_.irq(handler=None)
        key_X_.irq(handler=None)
        tetris.rotation()
        key_B_.irq(irq_B,Pin.IRQ_FALLING)
        key_X_.irq(irq_X,Pin.IRQ_FALLING)

    def irq_B(p):
        key_X_.irq(handler=None)
        key_A_.irq(handler=None)
        tetris.right()
        key_X_.irq(irq_X,Pin.IRQ_FALLING)
        key_A_.irq(irq_A,Pin.IRQ_FALLING)

    def irq_X(p):
        key_B_.irq(handler=None)
        key_A_.irq(handler=None)
        tetris.left()
        key_B_.irq(irq_B,Pin.IRQ_FALLING)
        key_A_.irq(irq_A,Pin.IRQ_FALLING)


    key_Y_.irq(quick_down,Pin.IRQ_FALLING)

    can_game = True

    while can_game:
        tetris.show()
        while True:
            can_down = True
            can_block = tetris.block()
            global rest_time
            rest_time = 1
            key_B_.irq(irq_B,Pin.IRQ_FALLING)
            key_X_.irq(irq_X,Pin.IRQ_FALLING)
            key_A_.irq(irq_A,Pin.IRQ_FALLING)
            if can_block:
                while can_down:
                    time.sleep(rest_time)
                    key_B_.irq(handler=None)
                    key_X_.irq(handler=None)
                    key_A_.irq(handler=None)
                    can_down = tetris.down()
                    key_B_.irq(irq_B,Pin.IRQ_FALLING)
                    key_X_.irq(irq_X,Pin.IRQ_FALLING)
                    key_A_.irq(irq_A,Pin.IRQ_FALLING)
                key_B_.irq(handler=None)
                key_X_.irq(handler=None)
                key_A_.irq(handler=None)
                tetris.line_clear()
            else:
                key_B_.irq(handler=None)
                key_X_.irq(handler=None)
                key_A_.irq(handler=None)
                time.sleep(1)
                can_game = tetris.end()
                break
        tetris.__init__(LCD)
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