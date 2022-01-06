#!/usr/bin/python
import binascii
import shutil
from pathlib import Path

size = 0
blocksize = 1024


def HexView(filename):
    sector = size / blocksize #blocksize / 32
    with open(filename, 'rb') as in_file:
        while sector > 0:
            space = 32
            hexdata = ""
            name = ""
            while space > 0:
                aux = in_file.read(1).hex()
                #print("Name deleted file: " +  bytes.fromhex("209C593904E021B7").decode('latin-1'))
                if int(aux, 16) == int("E5", 16) and space == 32:
                    name = in_file.read(7).hex()
                    space -= 6
                    aux += name
                    #print("name: " + bytes.fromhex(name).decode('ascii'))
                    ext_hex = in_file.read(3).hex()
                    try:
                        file_name = bytes.fromhex(name).decode('utf-8')
                        ext = bytes.fromhex(ext_hex).decode('utf-8')
                        if not file_name.isalnum() and not ext.isalnum():
                            #print("not ascii")
                            break
                        file_name = file_name.replace(bytes.fromhex('00').decode('utf-8'), "")
                        print("Name deleted file: " + file_name + "    extension format: " + ext)
                        #print("trovato")
                    finally:
                        in_file.read(21)
                        break
                    #print("Name deleted file: " +  bytes.fromhex(name).decode('latin-1'))
                    print("trovato")
                    break
                else:
                    in_file.read(31)
                    space = 0
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
usage = shutil.disk_usage("D:\\")
size = usage[0]
print("Spazio totale del disco: " + str(usage[0]) + " bytes")
#file = "C:/Users/anicc/Desktop/Sfide-DSS/prova.txt"
HexView(file)
#prova(file)