#!/usr/bin/env python3
# coding: utf-8
"""
title: crypt_helpers.py
date: 2019-12-01
author: jskrable
description: cipher classes for RSA and El Gamal
"""

import math
import crypt_helpers as cp
from timeit import default_timer as timer

class RSA:

    def __init__(self, size=10):
        # make these strong primes???
        # use blum blum shub here!!!!
        self.__p = cp.prime_search(size, True)
        self.__q = cp.prime_search(size, True)
        if not (cp.miller_rabin(self.__p) or cp.miller_rabin(self.q)):
            raise Exception('P or Q is not prime. Cannot safely encrypt. Please try again.')
            return -1
        self.n = self.__p * self.__q
        self.__phi = ((self.__p - 1) * (self.__q - 1) )
        e = cp.blum_blum_shub(size)
        while cp.gcd(self.__phi, e) != 1:
            e = cp.blum_blum_shub(size)
        self.e = e


    def encrypt(self, message):
        """
        function to encrypt a message, given a public key made up of
        a modulus and an exponent. raises the message to the exponent
        in modular group and returns the encrypted message.
        """
        return cp.fast_exp(message, self.e, self.n)


    def decrypt(self, message):
        """
        function to decrypt a message encrypted using RSA, given a public
        key made up of a modulus and an exponent. calculates the decryption
        exponent using the extended euclidean algorithm and exponentiates 
        to solve the decryption.
        """
        # d = cp.phi(self.mod) + cp.ext_gcd(cp.phi(self.mod), self.e)[-1]
        d = self.__phi + cp.ext_gcd(self.__phi, self.e)[-1]
        return cp.fast_exp(message, d, self.n)


    def crack(self, message):
        """
        function to crack RSA encryption using pollard's rho??
        get p and 1 by factoring n, calculate phi using that, get 
        d using that.
        """

        def pollards_rho(n):

            if miller_rabin(n, 30):
                raise Exception('n is prime you fool.')

            x = 2
            y = x**2 -1 
            g = gcd((x-y), n)

            if g == 1:
                # choose new x
                None

            elif 1 < g < n:
                if miller_rabin(g, 30):
                    return g
                else:
                    pollards_rho(g)

            else:
                x = x**2 + 1 % n
                y = (y**2 + 1)**2 + 1 % n
        return -1


class ElGamal:

    def __init__(self, size=10):
        self.mod = cp.prime_search(size, True)
        if not cp.miller_rabin(self.mod, 30):
            raise Exception('Modulus is not prime. Cannot safely encrypt. Please provide a prime modulus at class initialization.')
            return -1
        self.base = cp.primitive_root_search(self.mod)
        self.__key_A = cp.blum_blum_shub(20) % self.mod
        self.key_pub = cp.fast_exp(self.base, self.__key_A, self.mod)


    def encrypt(self, message):
        """
        function to encrypt a message, given the mututally agreed modulus,
        the mutual base, and the public key transmitted by alice during cipher 
        initialization. returns another public key (Bob's), c1, and the encrypted
        message, c2.
        """
        if message > self.mod:
            raise Exception('Message larger than modular group. Cannot safely encrypt. Please provide larger modulus at class initialization.')
            return -1, -1
        key_B = cp.blum_blum_shub(20) % self.mod
        c1 = cp.fast_exp(self.base, key_B, self.mod)
        c2 = (cp.fast_exp(self.key_pub, key_B, self.mod) * message) % self.mod
        return c1, c2


    def decrypt(self, key, message):
        """
        function to decrypt a message encrypted using el gamal, given the
        publically transmitted key from Bob, the encrypted message from Bob,
        and the previously known key_A that Alice chose during initialization.
        """
        s = cp.fast_exp(key, self.__key_A, self.mod)
        decrypted = (cp.fast_exp(s, self.mod-2, self.mod) * message) % self.mod
        return decrypted


    def crack(self, c1, c2):
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

        def baby_step_giant_step(a, b, mod):
            """
            solves discrete log problem given an answer a, log base b, and
            modular group mod.
            """
            n = cp.phi(mod)
            m = math.ceil((n**0.5) % mod)
            # baby step, more efficient to store in dict
            j = {cp.fast_exp(b, j, mod) : j for j in range(m)}
            # fermat's little theorem, c = (b**-1)**m = b**(phi(mod)-1)**m
            c = cp.fast_exp(cp.fast_exp(b, (n - 1), mod), m, mod)
            # giant step, similar to j, but break and return if a match is found
            for i in range(m):
                y = (a * cp.fast_exp(c, i, mod)) % mod
                if y in j:
                    return (i * m) + j[y] % n
            # failure if no overlap found
            return None

        # get Alice's private key by solving discrete log problem
        # runtime increases exponentially with larger keys
        key_A = baby_step_giant_step(self.key_pub, self.base, self.mod)
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