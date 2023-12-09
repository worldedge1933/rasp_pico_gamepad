'''
显示坐标是240*240，游戏坐标是60*60，每个游戏坐标对应一个4x4的像素矩阵
'''


import random
import time
import machine
from machine import Pin, SoftSPI
import st7789py as st7789
import vga1_16x16 


def set_4_4_pix(LCD : st7789.ST7789, coor : list, color : int) -> None:
    '''
    给定一个游戏坐标，把以这个坐标对应的4*4显示方格设置为黑色
    '''
    for i in range(0, 4):
        for j in range(0, 4):
            LCD.pixel(coor[0]*4 + i, coor[1]*4 + j, color)
            
def get_next_move(dir : int, snake) -> list:
    '''
    获取蛇前进方向的下一个游戏坐标
    '''
    if dir == 1:
        return [snake[0][0] + 0, snake[0][1] - 1]
    elif dir == -1:
        return [snake[0][0] + 0, snake[0][1] + 1]
    elif dir == 2:
        return [snake[0][0] - 1, snake[0][1] + 0]
    elif dir == -2:
        return [snake[0][0] + 1, snake[0][1] - 0]

def move_a_step(LCD: st7789.ST7789, next_coor, snake, eat_apple=False):
    '''
    实现蛇身向前走一步的显示
    修改蛇身记录
    '''
    snake.insert(0, next_coor)
    set_4_4_pix(LCD, snake[0], st7789.BLACK)
    if eat_apple == False:
        set_4_4_pix(LCD, snake[-1], st7789.WHITE)
        snake.pop()
    return snake
    
def create_an_apple(LCD, game_map):
    '''
    在空白处生成一个苹果，显示，并返回苹果游戏坐标
    '''
    apple_coor = [30, 30]
    while True:
        apple_coor[0] = random.randint(1, 58)
        apple_coor[1] = random.randint(1, 58)
        if game_map[apple_coor[0]][apple_coor[1]] == 0:
            break
    set_4_4_pix(LCD, apple_coor, st7789.RED)
    return apple_coor

# 方向，上下左右分别是1，-1，2，-2，不能设置为当前方向的反方向，根据按键操作通过外部中断获取方向 
# 这里和82行是用外部中断方法检测按键输入
def up_interrupt(key):
    global direct_state
    direct_state = 1 if direct_tem != -1 else direct_state
#    print(direct_state)
def down_interrupt(key):
    global direct_state
    direct_state = -1 if direct_tem != 1 else direct_state
#    print(direct_state)
def left_interrupt(key):
    global direct_state
    direct_state = 2 if direct_tem != -2 else direct_state
#    print(direct_state)
def right_interrupt(key):
    global direct_state
    direct_state = -2 if direct_tem != 2 else direct_state
#    print(direct_state)


def main(LCD : st7789.ST7789, key_up_ : Pin, key_down_ : Pin, key_left_ : Pin, key_right_ : Pin, key_A_ : Pin, key_B_ : Pin, key_X_ : Pin, key_Y_ : Pin) -> None:

    key_up_.irq(up_interrupt, Pin.IRQ_FALLING)        
    key_down_.irq(down_interrupt, Pin.IRQ_FALLING)
    key_left_.irq(left_interrupt, Pin.IRQ_FALLING)
    key_right_.irq(right_interrupt, Pin.IRQ_FALLING)
    # 游戏循环

    while True:
        # 方向，上下左右分别是1，-1，2，-2，不能设置为当前方向的反方向，根据按键操作通过外部中断获取方向
        global direct_state, direct_tem
        direct_state = -2
        direct_tem = -2

        # 记录蛇身的游戏坐标，按蛇头到蛇尾方向排列坐标
        global snake
        snake = [[x, 30] for x in range(20, 10, -1)]

        # 游戏地图，用于记录地图蛇身以及苹果的游戏坐标
        global game_map
        game_map =[[0 for i in range(0, 60)] for j in range (0, 60)]
        # 主运行
        LCD.fill(st7789.BLACK)
        LCD.text(vga1_16x16, "choose", 4, 30, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "speed", 4, 60, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "1", 220, 22, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "2", 220, 82, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "3", 220, 142, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "4", 220, 202, color=st7789.WHITE, background=st7789.BLACK)
        rest_time = 0.3
        while True:
            if key_A_.value() == 0:
                rest_time = 0.3
                level = 1
                break
            if key_B_.value() == 0:
                rest_time = 0.15
                level = 2
                break
            if key_X_.value() == 0:
                rest_time = 0.05
                level = 3
                break
            if key_Y_.value() == 0:
                rest_time = 0.01
                level = 4
                break
        LCD.fill(st7789.WHITE)
        for ls in snake:
            game_map[ls[0]][ls[1]] = 1
            set_4_4_pix(LCD, ls, st7789.BLACK)
#        print(7)
        apple_coor_tem = create_an_apple(LCD, game_map)
#        print(6)
        game_map[apple_coor_tem[0]][apple_coor_tem[1]] = -1
#        print(4)
        
        while True:
#            print(5)
            direct_tem = direct_state
            next_coor_tem = get_next_move(direct_tem, snake)
#            print(3)
            if (next_coor_tem[0] >= 60 or next_coor_tem[0] < 0) or (next_coor_tem[1] >= 60 or next_coor_tem[1] < 0):
                break
            elif game_map[next_coor_tem[0]][next_coor_tem[1]] == 1:
                break
            elif game_map[next_coor_tem[0]][next_coor_tem[1]] == -1:
                game_map[next_coor_tem[0]][next_coor_tem[1]] = 1
                snake = move_a_step(LCD, next_coor_tem, snake, eat_apple=True)
                apple_coor_tem = create_an_apple(LCD, game_map)
                game_map[apple_coor_tem[0]][apple_coor_tem[1]] = -1
                time.sleep(rest_time)
            else:
                game_map[next_coor_tem[0]][next_coor_tem[1]] = 1
                game_map[snake[-1][0]][snake[-1][1]] = 0
                snake = move_a_step(LCD, next_coor_tem, snake)
                time.sleep(rest_time)
        score = len(snake) - 10
        LCD.fill(st7789.BLACK)
        LCD.text(vga1_16x16, "your score :{0}".format(score), 4, 30, color=st7789.WHITE, background=st7789.BLACK)
        with open(f'snake{level}.csv', "r") as f:
            data = f.readlines()
            best_score = int(data[0])
        LCD.text(vga1_16x16, "best score :{0}".format(best_score), 4, 90, color=st7789.WHITE, background=st7789.BLACK)
        if score > best_score:
            with open(f'snake{level}.csv', 'w') as f:
                f.write(str(score))
        LCD.text(vga1_16x16, "new game", 102, 142, color=st7789.WHITE, background=st7789.BLACK)
        LCD.text(vga1_16x16, "exit", 166, 202, color=st7789.WHITE, background=st7789.BLACK)
#        print(1)
        while True:
            if key_X_.value() == 0:
                break
            elif key_Y_.value() == 0:
#                print(2)
                LCD.fill(st7789.BLACK)
                return



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

    snake_state = main(tft, key_up, key_down, key_left, key_right, key_A, key_B, key_X, key_Y)
    print(snake_state)

