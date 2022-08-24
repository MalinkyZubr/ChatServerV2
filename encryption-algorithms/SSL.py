from threading import Thread, Lock
from Crypto.Cipher import AES
from Crypto import Random
import random
import hashlib
from base64 import b64encode, b64decode
import time
import dask
import numba
from numba import jit
import numpy as np
import json
import functools
from sympy.ntheory.factor_ import totient


@jit(nopython=True, parallel=True, nogil=True)
def get_factors(tt):
    factors = np.arange(1, tt)
    factors = factors[(tt%factors == 0)]
    return factors

class SSLSystem:
    def __init__(self):
        print('inited')

    def get_primes(self):
        with open(r'New-chat-server\encryption-algorithms\primes.json', 'r') as f:
            content = json.loads(f.read())
            index1 = random.randint(3000, 4000)
            index2 = index1 + 2
            prime1, prime2 = content[str(index1)], content[str(index2)]
            
            return prime1, prime2, prime1 * prime2

    def get_totient(self, primes_product):
        totient_n = totient(primes_product)
        return totient_n

    def generate_private_key(self, tn, e):
        for k in range(1,11):
            private_key = ((k * tn) + 1) / e
            if private_key == int(private_key):
                return private_key

    def create_keys(self):
        exponents = np.arange(3, 13, 2, dtype=int)
        p1, p2, n = self.get_primes()
        tn = self.get_totient(n)
        factors = get_factors(tn)

        for exponent in exponents:
            if exponent not in factors:
                e = exponent
                break

        public_key = {'n':int(n), 'e':int(e)}
        private_key = self.generate_private_key(tn, e)
        return private_key, public_key

    def decrypt_message(self, encrypted_message, public_key, private_key):
        return pow(int(encrypted_message), int(private_key), int(public_key['n']))

    def generate_message(self, public_key):
        message = random.randint(100000000, 999999999)
        encrypted_message = pow(int(message), int(public_key['e']), int(public_key['n']))
        return message, encrypted_message


