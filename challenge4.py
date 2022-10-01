#!/usr/bin/python
import binascii
import shutil
import math
from termcolor import colored, cprint
import os


size = 0
blocksize = 1024
file = "\\\\.\\D:"


def read_file(in_file, start_cluster, file_size, filename):
    # prints current position
    pos = in_file.tell()
    print(start_cluster)
    in_file.seek(0, 0)
    in_file.seek(start_cluster, 0)
    #print(in_file.readline().hex())
    data = in_file.read(file_size).hex()
    print(data)
    #in_file.seek(-start_cluster, 1)
    fp = open(filename, "wb")
    fp.write(bytes.fromhex(data))
    fp.close()



def search_file(in_file, filename, ext):
    filename = "./" + filename + "." + ext
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
        print("value address: " + str(low_word_int + 134 * 1024))

        print("low_word: " + str(low_word_int)+"  hex: "+str(low_word) + "  file size: " + str(file_size) +
                  "  start cluster: " + str(low_word_int) + "  end cluster: " + str(math.ceil(cluster_end)))
        read_file(in_file, (low_word_int + 134) * 1024, file_size, filename)
    else:
        in_file.read(4)
        low_word1 = in_file.read(1).hex()
        low_word2 = in_file.read(1).hex()
        low_word = low_word2 + low_word1
        low_word_int = int(low_word, 16)
        if low_word_int != 0:
            return -1

        s1 = in_file.read(1).hex()
        s2 = in_file.read(1).hex()
        s3 = in_file.read(1).hex()
        s4 = in_file.read(1).hex()

        file_size = int(s4 + s3 + s2 + s1, 16)
        cluster_end = file_size / blocksize
        print(" high_word: " + str(high_word_int) + " hex: " + str(high_word) + "  file size: " + str(file_size) +
                "  start cluster: " + str(high_word_int) + "  end cluster: " + str(math.ceil(cluster_end)))
        read_file(in_file, (high_word_int + 134) * 1024, file_size, filename)


def analyzer(filename):
    sector = size / 32
    with open(filename, 'rb') as in_file:
        while sector > 0:
            name = ""
            aux = in_file.read(1).hex()
            if int(aux, 16) == int("E5", 16):
                name = in_file.read(7).hex()
                aux += name
                ext_hex = in_file.read(3).hex()
                try:
                    file_name = bytes.fromhex(name).decode('utf-8')
                except Exception:
                    in_file.read(21)
                    sector -= 1
                    continue
                try:
                    ext = bytes.fromhex(ext_hex).decode('utf-8')
                except Exception:
                    in_file.read(21)
                    sector -= 1
                    continue
                if not file_name.isalnum() and not ext.isalnum():
                    in_file.read(21)
                    sector -= 1
                    continue
                file_name = file_name.replace(bytes.fromhex('00').decode('utf-8'), "")
                text = colored("Name deleted file: " + file_name + "    extension format: " + ext, 'green',
                                attrs=['reverse', 'blink'])
                print(text)
                in_file.read(9)
                pos = in_file.tell() + 12
                search_file(in_file, file_name, ext)
                in_file.seek(0, 0)
                in_file.read(pos)
            else:
                in_file.read(15)
                sector -= 1
        in_file.close()


usage = shutil.disk_usage("D:\\")
size = usage[0]
print("Spazio totale del disco: " + str(usage[0]) + " bytes")
analyzer(file)
