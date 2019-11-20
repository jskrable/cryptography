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
import crypt_helpers as crypt


class testMillerRabin(unittest.TestCase):

    def test(self):
        with open('./primes.txt') as f:
            data = f.read()
            primes = [int(x) for x in data[1:-1].split(',')]

        [self.assertEqual(
            True,
            crypt.miller_rabin(n, 20)) for n in primes]

# WRITE TESTS FOR RSA
class TestRSA(unittest.TestCase):

    def test(self):

        messages = [x for x in [random.randint(10000, 100000) 
                    for x in range(1000) if prime_check(x)] if prime_check(x)]
        mods = [random.randint(10000, 100000) for x in range(len(messages))]
        Es = [random.randint(10000, 100000) for x in range(len(messages))]

        [self.assertEqual(
            message, 
            (crypt.rsa_decrypt(
                crypt.rsa_encrypt(message, mods[i], Es[i]), mods[i], Es[i])))
            for i, message in enumerate(messages)]


class TestFastExponentiation(unittest.TestCase):

    def test(self):

        Xs = [random.randint(1, 10000) for x in range(300000)]
        Es = [random.randint(1, 300) for x in range(300000)]
        Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(
            crypt.fast_exp(x, Es[i], Ms[i]),
            ((x ** Es[i]) % Ms[i])) for i, x in enumerate(Xs)]


class TestBabyStepGiantStep(unittest.TestCase):

    def test(self):

        Mods = [x for x in [random.randint(1, 10000) for x in range(1000)] if prime_check(x)]
        Bs = [random.randint(1, 10000) for x in range(len(Mods))]
        As = [random.randint(1, 10000) for x in range(len(Mods))]
        # Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(
            (Bs[i] ** crypt.baby_step_giant_step(Bs[i], As[i], Mods[i])[0] % Mods[i]),
            (As[i] % Mods[i])) for i in range(len(Bs))]


if __name__ == '__main__':
    unittest.main()
