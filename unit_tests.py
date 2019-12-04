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
import sys
import ciphers
import crypt_helpers as cp



# Progress bar for cli
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


class testMillerRabin(unittest.TestCase):

    def test(self):
        print('\nStarting Miller-Rabin tests...')
        with open('./primes.txt') as f:
            data = f.read()
            primes = [int(x) for x in data[1:-1].split(',')]

        for i, p in enumerate(primes):
            progress(i+1, len(primes), 'of Miller-Rabin tests complete')
            self.assertEqual(True, cp.miller_rabin(p))


class TestBlumBlumShub(unittest.TestCase):

    def test(self):
        print('\nStarting Blum-Blum-Shub tests...')
        for i in range(SIZE):
            progress(i+1, SIZE, 'of Blum-Blum-Shub tests complete')
            s = random.randint(1,25)
            n = len(str(cp.blum_blum_shub(s)))
            self.assertEqual(s,n)


class TestRSA(unittest.TestCase):

    def test(self):
        print('\nStarting RSA tests...')
        for i in range(SIZE):
            progress(i+1, SIZE, 'of RSA tests complete')
            r = ciphers.RSA()
            message = 123456
            self.assertEqual(message, r.decrypt(r.encrypt(message)))



# class TestFastExponentiation(unittest.TestCase):

#     def test(self):

#         Xs = [random.randint(1, 10000) for x in range(300000)]
#         Es = [random.randint(1, 300) for x in range(300000)]
#         Ms = [random.randint(1, 1000) for x in range(300000)]

#         [self.assertEqual(
#             cp.fast_exp(x, Es[i], Ms[i]),
#             ((x ** Es[i]) % Ms[i])) for i, x in enumerate(Xs)]


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
    global SIZE
    SIZE = 100
    unittest.main()
