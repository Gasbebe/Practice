from threading import Thread
from threading import Event as tEvent
import plistlib
import re
import time
from tkinter import *
from PIL import ImageTk, Image

fileName = "./test.plist"
pl = dict()
event = tEvent()


sourceImg = any
imageList = []

#number_rex = re.compile('[0-9]+\w')
with open(fileName, 'rb') as fp:
    pl = plistlib.load(fp)
    
    print(type(pl))
    
for key, val in pl['metadata'].items():
    print("key = {key}, value={value}".format(key=key,value=val))
    if(key == "textureFileName") :
        sourceImg = Image.open(val)
        
for key1, val1 in pl['frames'].items():
    print("key = {key}, value={value}".format(key=key1,value=val1))
    print(val1['frame'])
    p1 = re.findall('[0-9]+', val1['frame']) 
    
    print(val1['offset'])
    print(val1['rotated'])
    print(val1['sourceColorRect'])
    print(val1['sourceSize'])
    p2 = re.findall('[0-9]+', val1['sourceSize']) 
    print(p1[0])
    area = (int(p1[0]),int(p1[1]), int(p1[0]) + int(p2[0]), int(p1[1]) + int(p2[1]))
    imageList.append(sourceImg.crop(area))
        
root = Tk()
root.title("Image Viewer")
 
canvas = Canvas(root, width = 500, height = 500, background= "black")  
canvas.pack()
 
count = 0
threadFlag = False
def button_pressed():
    print("hello")
    if event.is_set() is False :
        event.set()
    else :
        event.clear()
        t = Thread(target=animation)
        t.start()
    
def animation():
    while(True):
        global count
        img = ImageTk.PhotoImage(imageList[count])
        count = (count + 1)% len(imageList)
        canvas.create_image(350, 200, anchor=NE, image=img)
        canvas.image = img
        time.sleep(0.05)
        if event.is_set() :
            return
    
button = Button(
    master=root,
    text="클릭하세요",
    bg="white",
    fg="blue",
    width=80,
    height=2,
    command=button_pressed,
)

button.pack()


root.mainloop()
#t.join()
