import base64
import os
import string
import random
import winsound
from numpy.random import choice
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_pw1():
    st = ['s','t','e','f','a','n','o']
    i = 0
    list = [st[i], random.choice(string.ascii_uppercase), random.choice(string.digits)]
    pwd = b""
    for _ in range(9):
        if len(list) == 3:
            probabilities = [0.5, 0.25, 0.25]
        elif len(list) == 2:
            probabilities = [0.6, 0.4]
        else:
            probabilities = [1]
        char = choice(list, p=probabilities)
        if char.isdigit():
            del list[len(list)-1]
        elif char.islower():
            i += 1
            if i < 7:
                list[0] = st[i]
            else:
                del list[0]
        else:
            if not list[len(list) - 1].isupper():
                del list[len(list) - 2]
            else:
                del list[len(list) - 1]
        pwd += bytes(char, 'utf-8')
    return pwd

cyphertext = b'gAAAAABgoqMJ17XcgGFW347sJ9q1cXjzd1Cl74v42sZVhmbGGer1_l1NFfZSM-FRCVpCaZ9' \
             b'-JYjy5Ut0Ycy4E1GHyUxCSEgROSw2HFsJjX43qZgk2AyMG1Vzfxx8V212x3WWwszfCV1rR2KWHvUyorQB' \
             b'-0asgI3NLcrZiLVjJSQHg2qOqqKNUyv-TQsR-EIo-GgI4FOnA1kyFymTQv2Vcjxq4zAtUO3' \
             b'-nssuxuVC_n27xefX4eRd_GrnonCvRL_0b_3KYt-pQp4iT_hcbvuEnuM--Ue-F_BjYg== '
salt = b'\xd4\x1f\xceg\xe9\xafW\xad\xb7+Y\xc3\xd9t\xe1\xc6'
print('salt = ', salt)

i = 1
while i == 1:
    passwd = generate_pw1()
    print('password:  ', passwd)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwd))
    f = Fernet(key)
    try:
        print(f.decrypt(cyphertext))
        i = 0
    except:
        pass
print('This is the password: ', passwd)
print('This is the cleartext: ', f.decrypt(cyphertext))
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)


