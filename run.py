import encript as enc
import os
import hashlib
from tkinter import filedialog
from tkinter import *

password = input('input password:')
password_byte = password.encode('utf-8') 
key = hashlib.sha256(password_byte).digest()    
   
is_encrypt = input('is it encryption? (y/n)? : ')

print('dir path Select')
root = Tk()
root.dirName=filedialog.askdirectory();
root.dirName.replace('/','//')

enc.encryption(key, root.dirName, is_encrypt)

print('finished')
