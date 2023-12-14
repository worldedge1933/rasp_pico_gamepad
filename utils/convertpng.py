from PIL import Image
import csv
image = Image.open('check_icon.png')
pixels = [[1 if image.getpixel((i,j))[3] == 0 else 0 for i in range(48)] for j in range(48)]
for row in pixels:
    print(row)
with open('check_icon.csv',mode="w",encoding='utf-8',newline='') as file:
    write = csv.writer(file)
    for row in pixels:
        write.writerow(row,)
        
with open('check_icon.csv',mode="r") as file:
    for line in file.readline():
        data = line.rstrip().split(',')
        
        
#        list_of_integers = list(map(int, line.split(',')))
#        print(type(list_of_integers))
        