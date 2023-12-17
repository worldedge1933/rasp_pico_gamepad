from PIL import Image
import csv

def png2csv(filename: str):
    image = Image.open(filename)
    pixels = [[1 if image.getpixel((i,j))[3] == 0 else 0 for i in range(image.width)] for j in range(image.height)]
#    for row in pixels:
#        print(row)
    with open(f'{filename[:-4]}.csv',mode="w",encoding='utf-8',newline='') as file:
        write = csv.writer(file)
        for row in pixels:
            write.writerow(row)        
#    with open('check_icon.csv',mode="r") as file:
#        for line in file.readline():
#            data = line.rstrip().split(',')
        
        
#        list_of_integers = list(map(int, line.split(',')))
#        print(type(list_of_integers))
        
def RGBA2RGB(png:str):

    # 打开图像
    img = Image.open(png)

    # 检查图像模式
    if img.mode == 'RGBA':
        # 创建一个白色背景图片（同样大小）
        bg = Image.new('RGB', img.size, (255,255,255))

        # 合并背景和图片
        bg.paste(img, (0,0), img)
        
        # 保存为新的文件
        bg.save(f'{png[:-4]}jpg', quality=95)  # JPEG支持 RGB，quality参数控制输出质量

    else:
        print("The image is not RGBA.")

RGBA2RGB('check_icon.png')
