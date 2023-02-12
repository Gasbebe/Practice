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