# %%
import plistlib
import debug_log
from pprint import pprint as pp
from PIL import Image
import ipywidgets as widgets

#import PIL import Image

fileName = "./test.plist"
pl = dict()
with open(fileName, 'rb') as fp:
    pl = plistlib.load(fp)
    
    print(type(pl))
    
    #pp(pl)
    #print(pl['frames'])
    for fxbox in pl.values():
        print(type(fxbox))
        for framinof in fxbox.items():
            #pp(fxbox)
            #print(type(framinof))
            #framinof.
            debug_log.console_write(framinof, color='blue')
            
    
widgets.IntSlider()
    

# %%
# load and show an animated gif file using module pyglet
# download module pyglet from: http://www.pyglet.org/download.html
# the animated dinosaur-07.gif file is in the public domain
# download from http://www.gifanimations.com
# tested with Python2.5 and pyglet1.1a2  by  vegaseat   22apr2008

import pyglet

# pick an animated gif file you have in the working directory
ag_file = "skull.gif"
animation = pyglet.resource.animation(ag_file)
sprite = pyglet.sprite.Sprite(animation)

# create a window and set it to the image size
win = pyglet.window.Window(width=sprite.width, height=sprite.height)

# set window background color = r, g, b, alpha
# each value goes from 0.0 to 1.0
green = 0, 1, 0, 1
pyglet.gl.glClearColor(*green)

@win.event
def on_draw():
    win.clear()
    sprite.draw()

pyglet.app.run()

# %%
from PIL import Image
 
# 이미지 열기
im = Image.open('python.png')
 
# 이미지 크기 출력
print(im.size)
 
# 이미지 JPG로 저장
im.save('python.jpg')

# %%
from PIL import Image
 
im = Image.open('python.png')
 
# Thumbnail 이미지 생성
size = (64, 64)
im.thumbnail(size)  
 
im.save('python-thumb.jpg')

# %%
from PIL import Image
im = Image.open('python.png')
cropImage = im.crop((100, 100, 150, 150))
cropImage.save('python-crop.jpg')

# %%
from PIL import Image
im = Image.open('python.png')
 
# 크기를 600x600 으로
img2 = im.resize((600, 600))
img2.save('python-600.jpg')
 
# 90도 회전
img3 = im.rotate(90)
img3.save('python-rotate.jpg')

# %%
from PIL import Image, ImageFilter
 
im = Image.open('python.png')
blurImage = im.filter(ImageFilter.BLUR)
 
blurImage.save('python-blur.png')

# %%
import plistlib
import debug_log
from pprint import pprint as pp


fileName = "./test.plist"
pl = dict()
with open(fileName, 'rb') as fp:
    pl = plistlib.load(fp)
    
    print(type(pl))
    
    #pp(pl)
    #print(pl['frames'])
    # for fxbox in pl.values():
    #     print(type(fxbox))
    #     for framinof in fxbox.values():
    #         #pp(fxbox)
    #         #print(type(framinof))
    #         #framinof.
    #         debug_log.console_write(framinof, color='blue')
            
    # for key, val in pl.items():
    #     pp("key = {key}, value={value}".format(key=key,value=val))
    
    
    # for i in pl : 
    #     pp(pl[i].values())
    #     pp("key = {key}, value={value}".format(pl[i].keys(),pl[i].values()))
for key, val in pl['metadata'].items():
    #print(item)
    #debug_log.console_write(item, color='blue')
    #debug_log.console_write(item['frame'], color='red')
    #debug_log.console_write(property, color='red')
    pp("key = {key}, value={value}".format(key=key,value=val))
    
for item in pl['frames'].values():
    #print(item)
    debug_log.console_write(item, color='blue')
    #debug_log.console_write(item['frame'], color='red')
    for key, val in item.items() : 
        #debug_log.console_write(property, color='red')
        pp("key = {key}, value={value}".format(key=key,value=val))
        
        
# for val in pl.values():
#     pp(val)
    
# for key, val in pl.items():
#     pp("key = {key}, value={value}".format(key=key,value=val))
#     pl.
    
    
# for i in pl : 
#     pp(pl[i].values())
#     pp("key = {key}, value={value}".format(pl[i].keys(),pl[i].values()))
    


