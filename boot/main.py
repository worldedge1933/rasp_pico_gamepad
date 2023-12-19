from machine import Pin, SPI
import st7789py as st7789
import vga1_16x16
import gc
from draw import draw
import snake
import framebuf

class Main_menu:
    def __init__(self, LCD: st7789.ST7789) -> None:
        self.LCD = LCD
        self.pen = draw(LCD)
        self.games_name = ['snake', 'tetris']
        self.game_icon = [['snake_icon.565',100,100], ['tetris_icon.565',100,100]]
        self.games = [snake, snake]
        self.current_game = 0
    def next_game(self):
        length = len(self.games_name[self.current_game]) * 16
        self.LCD.fill_rect(10, 60, len(self.games_name[self.current_game]) * 16, 16, st7789.BLACK)
        if self.current_game == len(self.games_name) - 1:
            self.current_game = 0
        else:
            self.current_game += 1
        with open(self.game_icon[self.current_game][0],'rb') as f:
            self.LCD.blit_buffer(framebuf.FrameBuffer(bytearray(f.read()), self.game_icon[self.current_game][2], self.game_icon[self.current_game][1], framebuf.RGB565),10,80,self.game_icon[self.current_game][1],self.game_icon[self.current_game][2])
        self.LCD.fill_rect(10, 60, length, 16, st7789.BLACK)
        self.LCD.text(vga1_16x16, f"{self.games_name[self.current_game]}", 10, 60, color=st7789.WHITE, background=st7789.BLACK)
        gc.collect()
    def previous_game(self):
        length = len(self.games_name[self.current_game]) * 16
        if self.current_game == 0:
            self.current_game = len(self.games_name) - 1
        else:
            self.current_game -= 1
        with open(self.game_icon[self.current_game][0],'rb') as f:
            self.LCD.blit_buffer(framebuf.FrameBuffer(bytearray(f.read()), self.game_icon[self.current_game][2], self.game_icon[self.current_game][1], framebuf.RGB565),10,80,self.game_icon[self.current_game][1],self.game_icon[self.current_game][2])
        self.LCD.fill_rect(10, 60, length, 16, st7789.BLACK)
        self.LCD.text(vga1_16x16, f"{self.games_name[self.current_game]}", 10, 60, color=st7789.WHITE, background=st7789.BLACK)
        gc.collect()
    def show(self) -> None:
        self.LCD.fill(st7789.BLACK)
        with open('snake_icon.565','rb') as f:
            self.LCD.blit_buffer(framebuf.FrameBuffer(bytearray(f.read()), 100, 100, framebuf.RGB565),10,80,100,100)
        with open('check_icon.565','rb') as f:
            self.LCD.blit_buffer(framebuf.FrameBuffer(bytearray(f.read()), 48, 48, framebuf.RGB565),186,186,48,48)
#        game_icon = self.pen.drawcsv('snake_icon.csv',100,100,reverse=True,mode='r')
#        check_icon = self.pen.drawcsv('check_icon.csv',48,48,reverse=True,mode='r')
#        self.LCD.blit_buffer(game_icon, 10, 80, 100, 100)
#        self.LCD.blit_buffer(check_icon, 186, 186, 48, 48)
        self.LCD.text(vga1_16x16, "game:", 10, 30, color=st7789.WHITE, background=st7789.BLACK)
        self.LCD.text(vga1_16x16, f"{self.games_name[self.current_game]}", 10, 60, color=st7789.WHITE, background=st7789.BLACK)
        self.pen.arrow(240 - 30 - 18, 75, 30, 'r')
        self.pen.arrow(240 - 30 - 18, 135, 30, 'l')
        gc.collect()
#        self.LCD.text(vga1_16x16, "choose", 134, 202, color=st7789.WHITE, background=st7789.BLACK)



    


def main(LCD: st7789.ST7789, key_up_: Pin, key_down_: Pin, key_left_: Pin, key_right_: Pin, key_A_: Pin, key_B_: Pin, key_X_: Pin, key_Y_: Pin) -> None:
    while True:
        main_menu = Main_menu(LCD)
        main_menu.show()
        while True:
            if key_B_.value() == 0:
                while True:
                    if key_B_.value() == 1:
                        main_menu.next_game()
                        break
            if key_X_.value() == 0:
                while True:
                    if key_X_.value() == 1:
                        main_menu.previous_game()
                        break
            if key_Y_.value() == 0:
                while True:
                    if key_Y_.value() == 1:
                        gc.collect()
                        main_menu.games[main_menu.current_game].main(LCD, key_up_, key_down_, key_left_, key_right_, key_A_, key_B_, key_X_, key_Y_)
                        gc.collect()
                        break
                break


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

    key_up = Pin(2, Pin.IN, Pin.PULL_UP)
    key_down = Pin(18, Pin.IN, Pin.PULL_UP)
    key_left = Pin(16, Pin.IN, Pin.PULL_UP)
    key_right = Pin(20, Pin.IN, Pin.PULL_UP)
    key_A = Pin(15, Pin.IN, Pin.PULL_UP)
    key_B = Pin(17, Pin.IN, Pin.PULL_UP)
    key_X = Pin(19, Pin.IN, Pin.PULL_UP)
    key_Y = Pin(21, Pin.IN, Pin.PULL_UP)
    
    gc.enable()
    
    main(tft, key_up, key_down, key_left, key_right, key_A, key_B, key_X, key_Y)