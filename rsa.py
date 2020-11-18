from __future__ import unicode_literals
from math import sqrt
import random
from random import randint as rand
from random import getrandbits
import sympy
import time
import binascii

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None  
    else:
        return x % m

def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(1, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
    return True


def generate_prime(bitlength):
    a = '1'+'0'*(bitlength-1)
    b = '1'*bitlength
    p = sympy.randprime(int(a, 2), int(b, 2))
    return p


def generate_keypair(keysize):
    p = generate_prime(keysize)
    q = generate_prime(keysize)
    n = p * q
    phi = (p-1)*(q-1)//gcd(p-1, q-1)
    e = sympy.randprime(1,phi)
    d = mod_inverse(e,phi)
    if e != d:
        return ((e, n), (d, n))  


def encrypt(plain_text, package):
    e, n = package
    if plain_text > n:
        print('Message is too large for key to handle')
    msg_ciphertext = pow(plain_text, e, n)
    return msg_ciphertext


def decrypt(msg_ciphertext, package):
    d, n = package
    msg_plaintext = pow(msg_ciphertext, d, n)
    return binascii.unhexlify(hex(msg_plaintext)[2:]).decode()

