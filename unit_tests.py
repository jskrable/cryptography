#!/usr/bin/env python3
# coding: utf-8
"""
title: unit_tests.py
date: 2019-11-19
author: jskrable
description: unit testing for ciphers.py and crypt_helpers.py
"""

import math
import random
import unittest
import argparse
import ciphers
import crypt_helpers as cp

global SIZE
# SIZE = 100

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


class TestBreakers(unittest.TestCase):


    def test_BabyStepGiantStep(self):
        for i in range(SIZE):
            m = cp.prime_search(8, True)
            b = cp.primitive_root_search(m)
            a = cp.blum_blum_shub(6)
            result = cp.baby_step_giant_step(a, b, m)
            answer = cp.fast_exp(b, result, m)
            self.assertEqual(a, answer)


    def test_PollardsRho(self):
        for i in range(SIZE):
            p = cp.prime_search(5, True)
            q = cp.prime_search(5, True)
            n = p * q
            factor = cp.pollards_rho(n)
            self.assertEqual(True, factor in [p,q])            


class TestCiphers(unittest.TestCase):


    def test_RSA(self):
        for i in range(SIZE):
            r = ciphers.RSA(7)
            message = cp.blum_blum_shub(6)
            self.assertEqual(message, r.decrypt(r.encrypt(message)))
            self.assertEqual(message, r.crack(r.encrypt(message)))


    def test_ElGamal(self):
        for i in range(SIZE):
            g = ciphers.ElGamal()
            message = cp.blum_blum_shub(6)
            c1, c2 = g.encrypt(message)
            decrypted = g.decrypt(c1, c2)
            cracked = g.crack(c1, c2)
            self.assertEqual(message, decrypted)
            self.assertEqual(message, cracked)


def arg_parser():
    """
    function to parse arguments sent to terminal. descriptions below.
    call [script] -h to show help.
    """
    parser = argparse.ArgumentParser(
        description='unit testing for ciphers.py and crypt_helpers.py')
    parser.add_argument('-s', '--size', default=50, type=int, nargs='?',
                        help='the number of test loops to run for each suite, default 50')
    parser.add_argument('-a', '--all', default=True, type=bool, nargs='?',
                        help='runs all test suites, default True')
    parser.add_argument('-b', '--breakers', default=False, type=bool, nargs='?',
                        help='runs just the breaker suite, default False')
    parser.add_argument('-c', '--ciphers', default=False, type=bool, nargs='?',
                        help='runs just the cipher suite, including RSA and ElGamal, default False')
    parser.add_argument('-u', '--utilities', default=False, type=bool, nargs='?',
                        help='runs just the cryptographic helper function suite, default False')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = arg_parser()
    SIZE = args.size
    tests = []
    if args.breakers:
        tests = unittest.TestLoader().loadTestsFromTestCase(TestBreakers)
        print('\nCipher-breaking tests selected')
    elif args.ciphers:
        tests = unittest.TestLoader().loadTestsFromTestCase(TestCiphers)
        print('\nEnd-to-end cipher tests selected')
    elif args.utilities:
        tests = unittest.TestLoader().loadTestsFromTestCase(TestCryptHelpers)
        print('\nCryptographic utility function tests selected')
    else:
        ch_suite = unittest.TestLoader().loadTestsFromTestCase(TestCryptHelpers)
        c_suite = unittest.TestLoader().loadTestsFromTestCase(TestCiphers)
        b_suite = unittest.TestLoader().loadTestsFromTestCase(TestBreakers)
        tests = unittest.TestSuite([ch_suite, c_suite, b_suite])
        print('\nAll test suites selected')

    print('Starting unit tests...')
    print('\n----------------------------------------------------------------------\n')
    unittest.TextTestRunner(verbosity=2).run(tests)