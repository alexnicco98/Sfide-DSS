#!/usr/bin/python
import binascii
import shutil
import math
import os
from pathlib import Path

size = 0
blocksize = 1024
file = "\\\\.\\D:"


def read_file(in_file, start_cluster, file_size):
    #print(start_cluster)
    in_file.seek(start_cluster, os.SEEK_SET)
    # prints current position
    print(in_file.tell())

    print(in_file.readline().decode("utf-8"))

    print(str(in_file.read(32).hex()))



def search_file(in_file):
    #in_file.read(32)
    aux = in_file.read(1).hex()
    if int(aux, 16) == int("E5", 16):
        '''name = in_file.read(7).hex()
        print(bytes.fromhex(name).decode('utf-8'))'''
        in_file.read(19)
        high_word1 = in_file.read(1).hex()
        high_word2 = in_file.read(1).hex()
        high_word = high_word2 + high_word1
        high_word_int = int(high_word, 16)
        if high_word_int == 0:
            in_file.read(4)
            low_word1 = in_file.read(1).hex()
            low_word2 = in_file.read(1).hex()
            low_word = low_word2 + low_word1
            low_word_int = int(low_word, 16)
            s1 = in_file.read(1).hex()
            s2 = in_file.read(1).hex()
            s3 = in_file.read(1).hex()
            s4 = in_file.read(1).hex()

            file_size = int(s4 + s3 + s2 + s1, 16)
            cluster_end = file_size / blocksize

            print("low_word: " + str(low_word_int)+"  hex: "+str(low_word) + "  file size: " + str(file_size) +
                  "  start cluster: " + str(low_word_int) + "  end cluster: " + str(math.ceil(cluster_end)))
            pos = in_file.tell()
            read_file(in_file, low_word_int, file_size)
            in_file.seek(pos, os.SEEK_SET)
        else:
            in_file.read(6)
            s1 = in_file.read(1).hex()
            s2 = in_file.read(1).hex()
            s3 = in_file.read(1).hex()
            s4 = in_file.read(1).hex()

            file_size = int(s4 + s3 + s2 + s1, 16)
            cluster_end = file_size / blocksize
            #print("high_word: " + str(high_word_int) + " hex: " + str(high_word))
            print("high_word: " + str(high_word_int) + " hex: " + str(high_word) + "  file size: " + str(file_size) +
                  "  start cluster: " + str(high_word_int) + "  end cluster: " + str(math.ceil(cluster_end)))
            pos = in_file.tell()
            read_file(in_file, high_word_int, file_size)
            in_file.seek(pos, os.SEEK_SET)
    else:
        #print("ramo else")
        in_file.read(31)
        search_file(in_file)


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
                            in_file.read(21)
                            #print("not ascii")
                            break
                        file_name = file_name.replace(bytes.fromhex('00').decode('utf-8'), "")
                        print("Name deleted file: " + file_name + "    extension format: " + ext)
                        in_file.read(21)
                        search_file(in_file)
                    finally:
                        #in_file.read(21)
                        #search_file(in_file)
                        break
                    #print("Name deleted file: " +  bytes.fromhex(name).decode('latin-1'))
                    print("trovato")
                    #break
                else:
                    in_file.read(31)
                    space = 0
                hexdata = hexdata + aux + " "
                space -= 1
            #print("hexa: " + hexdata)
            #print(hexdata) # unhexlify(hexdata)
            sector -= 1


'''def prova(filename):
    with open(filename,'rb') as f:
        print("Disk Open")
        block = f.read(512)
        print(block.hex())
        # Convert the binary data to upper case hex ascii code
        hexdata = binascii.hexlify(f.read(512))
        data = zip(hexdata[::2], hexdata[1::2])
        #hexlist = ''.join( str(v) for v in data)
        for i in range(len(hexdata)//2):
            print(codecs.decode(hexdata[i*2:i*2+2], "hex").decode('utf-8'), end="")
        print(hexdata)
        #print(hexlist)


def prova2(filename):
    data = Path(filename).read_bytes()
    print(data)
    i = int.from_bytes(data[:4], byteorder='little', signed=False)
    print(i)'''



usage = shutil.disk_usage("D:\\")
size = usage[0]
print("Spazio totale del disco: " + str(usage[0]) + " bytes")
#file = "C:/Users/anicc/Desktop/Sfide-DSS/prova.txt"
HexView(file)
#prova(file)