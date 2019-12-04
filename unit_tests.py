#!/usr/bin/env python3
# coding: utf-8
"""
title: unit_tests.py
date: 2019-11-19
author: jskrable
description: classwork for CS789: Cryptography
"""

import unittest
import random
import math
import ciphers
import crypt_helpers as cp

global SIZE
SIZE = 10

class TestCryptHelpers(unittest.TestCase):
    """
    Unit tests for the functions in crypt_helpers.py.

    TODO:
    - write for primitive root search
    - write for extended euclidean
    - write for efficient prime factors


    """
    def test_Euclidean(self):
        with open('./primes.txt') as f:
            data = f.read()
            primes = [int(x) for x in data[1:-1].split(',')]

        p_len = len(primes)
        for p in primes:
            for q in primes:
                if p != q:
                    self.assertEqual(1, cp.gcd(p,q))


    # def test_PrimeSearch(self):
    #     for i in range(SIZE):
    #         # switch = True if random.random() >= 0.5 else False
    #         order = random.randint(1,3)
    #         p = cp.prime_search(order, True)
    #         self.assertEqual(True, cp.miller_rabin(p))


    def test_FastExponentiation(self):

        Xs = [random.randint(1, 10000) for x in range(SIZE)]
        Es = [random.randint(1, 300) for x in range(SIZE)]
        Ms = [random.randint(1, 1000) for x in range(SIZE)]

        [self.assertEqual(
            cp.fast_exp(x, Es[i], Ms[i]),
            ((x ** Es[i]) % Ms[i])) for i, x in enumerate(Xs)]


    def test_MillerRabin(self):
        with open('./primes.txt') as f:
            data = f.read()
            primes = [int(x) for x in data[1:-1].split(',')]

        for i, p in enumerate(primes):
            self.assertEqual(True, cp.miller_rabin(p))


    def test_BlumBlumShub(self):
        for i in range(SIZE):
            s = random.randint(1,25)
            n = len(str(cp.blum_blum_shub(s)))
            self.assertEqual(s,n)


    # def test_NaorReingold(self):
    #     for i in range(SIZE):
    #         s = random.randint(1,25)
    #         n = len(str(cp.naor_reingold(s)))
    #         self.assertEqual(s,n)



    def test_BabyStepGiantStep(self):
        for i in range(SIZE):
            m = cp.prime_search(8, True)
            b = cp.primitive_root_search(m)
            a = cp.blum_blum_shub(6)
            result = cp.baby_step_giant_step(a, b, m)
            answer = cp.fast_exp(b, result, m)
            self.assertEqual(a, answer)



class TestCiphers(unittest.TestCase):

    def test_RSA(self):
        for i in range(SIZE):
            r = ciphers.RSA()
            message = cp.blum_blum_shub(6)
            self.assertEqual(message, r.decrypt(r.encrypt(message)))
            # self.assertEqual(message, r.crack(r.encrypt(message)))



    def test_ElGamal(self):
        for i in range(SIZE):
            g = ciphers.ElGamal()
            message = cp.blum_blum_shub(6)
            c1, c2 = g.encrypt(message)
            decrypted = g.decrypt(c1, c2)
            cracked = g.crack(c1, c2)
            self.assertEqual(message, decrypted)
            self.assertEqual(message, cracked)



# class TestBabyStepGiantStep(unittest.TestCase):

#     def test(self):

#         with open('./primes.txt') as f:
#             data = f.read()
#             primes = [int(x) for x in data[1:-1].split(',')]

#         Mods = primes
#         Bs = [random.randint(1, 10000) for x in range(len(Mods))]
#         As = [random.randint(1, 10000) for x in range(len(Mods))]
#         # Ms = [random.randint(1, 1000) for x in range(300000)]

#         [self.assertEqual(
#             (Bs[i] ** cp.baby_step_giant_step(Bs[i], As[i], Mods[i])[0] % Mods[i]),
#             (As[i] % Mods[i])) for i in range(len(Bs))]


if __name__ == '__main__':

    unittest.main()
