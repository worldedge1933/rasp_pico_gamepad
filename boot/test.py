import st7789py as st7789
colosrgb = [[153,164,188],
            [228,206,205],
            [190,181,164],
            [188,203,176],
            [227,140,122],
            [241,225,208]]
colors565 = []
for color in colosrgb:
    colors565.append(hex(st7789.color565(color)))

print(colors565)
print(hex(0b0111100111101111))