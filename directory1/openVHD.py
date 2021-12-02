from pyvinil.vhd import VHD
from pyvinil import utils

def main ():
    vhd = VHD.open ("\\\\.\\F:")
    vhd.footer.disk_type = 3
    vhd.footer.uuid = utils.uuid_generate ()

    print('-' * 50)
    print("pointer:", vhd.vhd_pointer.value)

    print('-' * 50)
    print("DLL:", vhd.vinil_dll)

    print('-' * 50)
    print("Footer:", vhd.footer)
    print("disk_type:", vhd.footer.disk_type)
    print("real:", vhd.footer.disk_type.real)
    print("denominator:", vhd.footer.disk_type.denominator)
    print("imag:", vhd.footer.disk_type.imag)
    print("numerator:", vhd.footer.disk_type.numerator)
    print("bit_length:", vhd.footer.disk_type.bit_length())
    print("UUID:", get_string_Hex_nox (vhd.footer.uuid))
    print("COMMIT:", vhd.commit_structural_changes())

    '''print '-' * 50
    print "TELL:", vhd.tell ()

    print '-' * 50
    vhd_read = vhd.read (1)
    print "READ", vhd_read.title (), ":"
    print "TITLE:", vhd_read.title ()
    print "CAPITALIZE:", vhd_read.capitalize ()
    print "FORMAT:", vhd_read.format ()
    print "ISALNUM:", vhd_read.isalnum ()
    print "ISALPHA:", vhd_read.isalpha ()
    print "ISDIGIT:", vhd_read.isdigit ()
    print "ISLOWER:", vhd_read.islower ()
    print "ISSPACE:", vhd_read.isspace ()
    print "ISTITLE:", vhd_read.istitle ()
    print "ISUPPER:", vhd_read.isupper ()

    print '-' * 50
    print "TELL:", vhd.tell ()

    print '-' * 50
    vhd_read_2 = vhd.read (2)
    print("READ", vhd_read_2.title (), ":")
    print "TITLE:", vhd_read_2.title ()
    print "CAPITALIZE:", vhd_read_2.capitalize ()
    print "FORMAT:", vhd_read_2.format ()
    print "ISALNUM:", vhd_read_2.isalnum ()
    print "ISALPHA:", vhd_read_2.isalpha ()
    print "ISDIGIT:", vhd_read_2.isdigit ()
    print "ISLOWER:", vhd_read_2.islower ()
    print "ISSPACE:", vhd_read_2.isspace ()
    print "ISTITLE:", vhd_read_2.istitle ()
    print "ISUPPER:", vhd_read_2.isupper ()'''

# Convert a visible string to its corresponding hexadecimal representation
def get_string_Hex_nox (substr):
    byte_list = bytearray (substr)
    hexStr = ''
    for item in byte_list:
        tmp = hex (item) [2:]
        if len (tmp)% 2 == 1:
            tmp = '0' + tmp
        hexStr += tmp
    return hexStr

if __name__ == '__main__':
    main ()