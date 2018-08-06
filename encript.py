import os, random, struct, hashlib
from Crypto.Cipher import AES


def encrypt_file(key, root, in_filename, chunksize=64*1024):
    out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(root + '\\' + in_filename)

    with open(root + '\\' + in_filename, 'rb') as infile:
        with open(root + '\\' + out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, root, in_filename, chunksize=24*1024):
    out_filename = os.path.splitext(in_filename)[0]

    with open(root + '\\' + in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(root + '\\' + out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def encryption(key, encrypt_path, is_encrypt):
    if (os.path.isdir(encrypt_path)): 
        for root, dirs, files in os.walk(encrypt_path): 
            for file in files:
                if (is_encrypt == 'y'):  
                    if (file[-4:] != '.enc'): 
                        encrypt_file(key, root, file)  
                        os.remove(root + '\\' + file)
                else:  
                    if (file[-4:] == '.enc'):  
                        decrypt_file(key, root, file)  
                        os.remove(root + '\\' + file) 

    else: 
        root, file = os.path.split(encrypt_path)
        if (is_encrypt == 'y'): 
            if (file[-4:] != '.enc'):  
                encrypt_file(key, root, file)  
                os.remove(root + '\\' + file) 
        else:  
            if (file[-4:] == '.enc'): 
                decrypt_file(key, root, file) 
                os.remove(root + '\\' + file) 