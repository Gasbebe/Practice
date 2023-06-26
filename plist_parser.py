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






#============
import plistlib
import re
from dataclasses import dataclass

@dataclass
class Position:
    x : str = None
    y : str = None

class d_parse:
    def __init__(self) -> None:
        pass
    
    def load(self, path):
        with open(path, "rb") as fp:
            print("file path : {}", path)
            self.info = plistlib.load(fp)
    
    def get_frames(self):
        return self.info["frames"]
    
    def get_metadata(self):
        return self.info["metadata"]
    
    #{0,0}
    def get_position(self, pos_str : str):
        find_list = re.findall(r"\{[\d]+,\s*[\d]+\}", pos_str)
        pos_list = []
        for item in find_list :
            coordinates = item.strip("{}")
            pos = Position()
            pos.x, pos.y = coordinates.replace(" ", "").split(",")
            pos_list.append(pos)
            # []
        return pos_list
#=================
from d_parser import *
import os
import re

def main():
    # ss = re.findall(r"\{[\d]+,\s*[\d]+\}", "gleeee")
    parse = d_parse()
    parse.load(os.path.join(os.getcwd(), "resources", "fx", "f3_fx_circleofdessication.plist"))
    print(parse.get_frames())
    print(parse.get_metadata())
    
    for frame_info in parse.get_frames().values():
        test = frame_info["frame"]
        # pos_list = test.split(",") 
        # print(test)
        # print(parse.get_position(test))
        for item in parse.get_position(test):
            print("===================")
            print(item.x)
            print(item.y)
        
        # for pos in pos_list:
        #     # print(pos)
        #     print(parse.get_position(pos))
    print("Hello, World!")

if __name__ == "__main__":
    main()
