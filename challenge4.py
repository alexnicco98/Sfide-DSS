import binascii
from binascii import unhexlify


def HexView(filename):
    with open(filename, 'rb') as in_file:
        while True:
            hexdata = in_file.read(16).hex()     # I like to read 16 bytes in then new line it.
            if hexdata == "00000000000000000000000000000000":                # breaks loop once no more binary data is read
                break
            #print("hexa: " + hexdata)
            print('Byte value: ', unhexlify(hexdata))


def prova(filename):
    with open(filename,'rb') as f:
        print("Disk Open")
        # Convert the binary data to upper case hex ascii code
        hexdata = binascii.hexlify(f.read(512))
        data = zip(hexdata[::2], hexdata[1::2])
        hexlist = ''.join( str(v) for v in data)
        print(hexdata)
        print(hexlist)


file = "\\\\.\\F:"
HexView(file)
#prova(file)