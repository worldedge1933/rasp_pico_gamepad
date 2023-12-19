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
        
def png2rgb565(filename: str):
    image = Image.open(filename)
    image2 = Image.new('RGB',image.size,(0,0,0))
#    pixels = [[1 if image.getpixel((i,j))[3] == 0 else 0 for i in range(image.width)] for j in range(image.height)]
    with open(f'{filename[:-4]}.565','wb') as file:
        for j in range(image.height):
            for i in range(image.width):
                if image.getpixel((i,j))[3] == 0:
                    file.write(b'\x00\x00')
                else:
                    file.write(b'\xFF\xFF')
if __name__ == "__main__":
    png2rgb565('tetris_icon.png')

