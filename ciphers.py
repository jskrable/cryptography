#!/usr/bin/env python3
# coding: utf-8
"""
title: ciphers.py
date: 2019-12-01
author: jskrable
description: cipher classes for RSA and El Gamal
"""

import math
import crypt_helpers as cp
from timeit import default_timer as timer

class RSA:

    def __init__(self, size=10, n=None, e=None):
        self.__p = cp.prime_search(size, True)
        self.__q = cp.prime_search(size, True)
        if not (cp.miller_rabin(self.__p) or cp.miller_rabin(self.q)):
            raise Exception('P or Q is not prime. Cannot safely encrypt. Please try again.')
            return -1
        self.__phi = ((self.__p - 1) * (self.__q - 1))
        if not n:
            self.n = self.__p * self.__q
        else:
            self.n = n
        if not e:
            e = cp.blum_blum_shub(size)
            while cp.gcd(self.__phi, e) != 1:
                e = cp.blum_blum_shub(size)
            self.e = e
        else: 
            self.e = e


    def encrypt(self, message, n=None, e=None):
        """
        function to encrypt a message, given a public key made up of
        a modulus and an exponent. raises the message to the exponent
        in modular group and returns the encrypted message.

        Can accept an external key as a tuple of (e, n), otherwise uses
        the key creted at initialization.
        """
        # if type(message) is str:
        #     message = cp.str_to_int(message)
        e = self.e if not e else e
        n = self.n if not n else n
        if message > n:
            raise Exception('Message larger than modular group. Cannot safely encrypt. Please provide larger size at class initialization.')
            return -1, -1
        return cp.fast_exp(message, self.e, self.n)


    def decrypt(self, message, decode=False):
        """
        function to decrypt a message encrypted using RSA, given a public
        key made up of a modulus and an exponent. calculates the decryption
        exponent using the extended euclidean algorithm and exponentiates 
        to solve the decryption.
        """
        d = self.__phi + cp.ext_gcd(self.__phi, self.e)[-1]
        decrypted = cp.fast_exp(message, d, self.n)
        # if decode:
        #     decrypted = cp.int_to_str(decrypted)
        return decrypted


    def crack(self, message, n=None, e=None):
        """
        function to crack RSA encryption using pollard's rho??
        get p and q by factoring n, calculate phi using that, get 
        d using that.
        """
        n = self.n if not n else n
        e = self.e if not e else e
        p = cp.pollards_rho(n)
        q = n // p
        phi = (p-1) * (q-1)
        d = phi + cp.ext_gcd(phi, e)[-1]
        return cp.fast_exp(message, d, n)


    def test(self, message):
        """ 
        Quick function to test the correctness of the cipher implementation
        """
        print('Modulus    : {}'.format(self.n))
        print('Exponent   : {}'.format(self.e))
        print('Message    : {}'.format(message))
        encrypted = self.encrypt(message)
        print('Encrypted  : {}'.format(encrypted))
        decrypted = self.decrypt(encrypted)
        print('Decrypted  : {}'.format(decrypted))
        t1 = timer()
        cracked = self.crack(encrypted)
        t2 = timer()
        print('Cracked    : {}'.format(cracked))
        print('Crack time : {} seconds'.format(t2-t1))


class ElGamal:

    def __init__(self, size=10, mod=None, base=None, key=None):
        self.mod = cp.prime_search(size, True) if not mod else mod
        # if not cp.miller_rabin(self.mod, 30):
        #     raise Exception('Modulus is not prime. Cannot safely encrypt.')
        #     return -1
        self.base = cp.primitive_root_search(self.mod) if not base else base
        self.__key_A = cp.blum_blum_shub(20) % self.mod
        self.key_pub = cp.fast_exp(self.base, self.__key_A, self.mod) if not key else key


    def encrypt(self, message, mod=None, base=None, key=None):
        """
        function to encrypt a message, given the mututally agreed modulus,
        the mutual base, and the public key transmitted by alice during cipher 
        initialization. returns another public key (Bob's), c1, and the encrypted
        message, c2.

        Accepts an external key. Requires mod, base, and key. If not provided, uses
        the mod, base, and key created at initialization.
        """
        # if type(message) is str:
        #     message = cp.str_to_int(message)
        mod = self.mod if not mod else mod
        base = self.base if not base else base
        key = self.key_pub if not key else key
        if message > mod:
            raise Exception('Message larger than modular group. Cannot safely encrypt. Please provide larger size at class initialization.')
            return -1, -1
        key_B = cp.blum_blum_shub(20) % mod
        c1 = cp.fast_exp(base, key_B, mod)
        c2 = (cp.fast_exp(key, key_B, mod) * message) % mod
        return c1, c2


    def decrypt(self, key, message, decode=False):
        """
        function to decrypt a message encrypted using el gamal, given the
        publically transmitted key from Bob, the encrypted message from Bob,
        and the previously known key_A that Alice chose during initialization.
        """
        s = cp.fast_exp(key, self.__key_A, self.mod)
        decrypted = (cp.fast_exp(s, self.mod-2, self.mod) * message) % self.mod
        # if decode:
        #     decrypted = cp.int_to_str(decrypted)
        return decrypted


    def crack(self, c1, c2, mod=None, base=None, key=None):
        """
        function to crack el gamal encryption using baby step giant step. takes in
        the following publically transmitted information:
        c1: the base taken to key_B power
        c2: the encrypted message
        key_pub: transmitted by Alice to begin the protocol
        base: transmitted by Alice to begin the protocol
        mod: the mutually agreed upon modular group, public knowledge

        uses baby step giant step to solve for Alice and Bob's keys, then decrypts
        the message using the same method as Alice.

        note key_A is derived here by solving a discrete log, not using the class's 
        private key_A attribute Alice saved earlier.
        """
        mod = self.mod if not mod else mod
        base = self.base if not base else base
        key = self.key_pub if not key else key
        # get Alice's private key by solving discrete log problem
        # runtime increases exponentially with larger keys
        key_A = cp.baby_step_giant_step(self.key_pub, self.base, self.mod)
        # solve for the decryption key with the cracked private key
        s = cp.fast_exp(c1, key_A, self.mod)
        # decrypt the message
        decrypted = (cp.fast_exp(s, self.mod-2, self.mod) * c2) % self.mod
        return decrypted


    def test(self, message):
        """ 
        Quick function to test the correctness of the cipher implementation
        """
        print('Modulus    : {}'.format(self.mod))
        print('Base       : {}'.format(self.base))
        print('Message    : {}'.format(message))
        c1, c2 = self.encrypt(message)
        print('Key        : {}'.format(c1))
        print('Encrypted  : {}'.format(c2))
        decrypted = self.decrypt(c1, c2)
        print('Decrypted  : {}'.format(decrypted))
        t1 = timer()
        cracked = self.crack(c1, c2)
        t2 = timer()
        print('Cracked    : {}'.format(cracked))
        print('Crack time : {} seconds'.format(t2-t1))