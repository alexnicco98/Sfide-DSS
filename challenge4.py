#!/usr/bin/python
import binascii
import codecs
import os
import struct
from binascii import unhexlify
from binascii import hexlify
from pathlib import Path

size = 2857750978
blocksize = 1024




def HexView(filename):
    sector = size / blocksize #blocksize / 32
    with open(filename, 'rb') as in_file:
        find = 0

        while sector > 0 and find == 0:
            space = 32
            hexdata = ""
            name = ""
            while space > 0:
                aux = in_file.read(1).hex()

                if int(aux, 16) == int("E5", 16):
                    name = in_file.read(1).hex()+" "+in_file.read(1).hex()+" "+in_file.read(1).hex()
                    #print("name: " + bytes.fromhex(name).decode('ascii'))
                    try:
                        print("Name deleted file: " +  bytes.fromhex(name).decode('utf-8'))
                        #print("trovato")
                    finally:
                        break
                    #print("Name deleted file: " +  bytes.fromhex(name).decode('latin-1'))
                    break
                    space -= 2
                    aux += name
                    print("trovato")
                    find = 1
                    break
                hexdata = hexdata + aux + " "
                space -= 1
            #print("hexa: " + hexdata)
            #print(hexdata) # unhexlify(hexdata)
            sector -= 1


def prova(filename):
    with open(filename,'rb') as f:
        print("Disk Open")
        block = f.read(512)
        print(block.hex())
        # Convert the binary data to upper case hex ascii code
        hexdata = binascii.hexlify(f.read(512))
        data = zip(hexdata[::2], hexdata[1::2])
        #hexlist = ''.join( str(v) for v in data)
        '''for i in range(len(hexdata)//2):
            print(codecs.decode(hexdata[i*2:i*2+2], "hex").decode('utf-8'), end="")'''
        print(hexdata)
        #print(hexlist)


def prova2(filename):
    data = Path(filename).read_bytes()
    print(data)
    i = int.from_bytes(data[:4], byteorder='little', signed=False)
    print(i)


file = "\\\\.\\D:"
#file = "C:/Users/anicc/Desktop/Sfide-DSS/prova.txt"
HexView(file)
#prova(file)