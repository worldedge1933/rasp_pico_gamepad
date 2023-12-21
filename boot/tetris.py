import st7789py as st7789
class _Array:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y 
            
class Array(_Array):
    def __add__(self, other: _Array | list):
        if (type(other) == list) and len(other) == 2:
            return Array(self.x + other[0], self.y + other[1])
        if isinstance(self, Array) == True:
            return Array(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other: _Array | list):
        if (type(other) == list) and len(other) == 2:
            return Array(self.x - other[0], self.y - other[1])
        if isinstance(self, _Array) == True:
            return Array(self.x - other.x, self.y - other.y)
        
    def __repr__(self) -> str:
        return f'{[self.x,self.y]}'
        
class Tretris:
    def __init__(self, LCD: st7789.ST7789):
        self.LCD = LCD
        self.map = [[1,1,1,1,1,1,1,1,1,1]]
        line = [1,0,0,0,0,0,0,0,0,1]
        self.map += [line[:] for _ in range(20)]
        self.map += [[1,1,1,1,1,1,1,1,1,1]]
    
        