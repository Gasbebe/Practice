import plistlib
import re

fileName = "./f3_fx_entropicdecay.plist"
pl = dict()

#number_rex = re.compile('[0-9]+\w')
with open(fileName, 'rb') as fp:
    pl = plistlib.load(fp)
    
    print(type(pl))
    
for key, val in pl['metadata'].items():
    print("key = {key}, value={value}".format(key=key,value=val))
    
for key1, val1 in pl['frames'].items():
    print("key = {key}, value={value}".format(key=key1,value=val1))

    for key, val in val1.items() :
        print("key = {key}, value={value}".format(key=key,value=val))    
        print(type(val))
        if(type(val) ==  str) :
            #p = re.compile(r'^[0-9]+$')
            m = re.findall('[0-9]+', val) 
            if m:
                print('Match found: ', m)
            else:
                print('No match')
                #
                
                import glob
from tkinter import *
from tkinter import filedialog

def button_pressed():
    print(entry.get())
    entry.insert(index=END, string=", World!")
    # entry.delete(0, END)

def browse_button():
    filename = filedialog.askdirectory()
    #filedialog.
    #print(filename)
    entry.insert(index=END, string=filename)
    for file in glob.glob(filename + "\*", recursive=True):
        print(file)
    return filename

window = Tk()

entry = Entry(
    master=window, fg="black", bg="yellow", width=30, justify=CENTER, font=("Arial", 25)
)

button = Button(
    master=window,
    text="클릭하세요",
    bg="white",
    fg="blue",
    width=80,
    height=2,
    command=browse_button,
)


entry.pack()
button.pack()

window.mainloop()


# search all files inside a specific folder
# *.* means file name with any extension
dir_path = r'E:\demos\files_demos\account\**\*.*'
