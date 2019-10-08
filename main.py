#!/usr/bin/env python3
# coding: utf-8
"""
title: main.py
date: 2019-09-15
author: jskrable
description: classwork for CS789: Cryptography
"""

import unittest
import random
import math


class TestFastExponentiation(unittest.TestCase):

    def test(self):

        Xs = [random.randint(1, 10000) for x in range(300000)]
        Es = [random.randint(1, 300) for x in range(300000)]
        Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(fast_exp(x, Es[i], Ms[i]),
                          ((x ** Es[i]) % Ms[i])) for i, x in enumerate(Xs)]


class TestBabyStepGiantStep(unittest.TestCase):

    def test(self):

        Mods = [random.randint(1, 10000) for x in range(300000) if prime_check(x)]
        Bs = [random.randint(1, 10000) for x in range(len(Mods))]
        As = [random.randint(1, 10000) for x in range(len(Mods))]
        # Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(
            (b ** baby_step_giant_step(b, As[i], Mods[i])[0] % Mods[i]),
            (As[i] % Mods[i])) for i, b in enumerate(Bs)]


def primitive_root_search(m):
    rel_primes = {n for n in range(1, m) if gcd(n, m) == 1}
    return [g for g in range(1, m) if rel_primes == {(g**e % m) for e in range(1, m)}]


# Algorithm for solving discrete log problem given a log base and mod
# mod must be prime for this to work???????
def baby_step_giant_step(b, a, mod):
    n = phi(mod)
    m = math.ceil((n**0.5) % mod)

    # more efficient to store in dict
    # j = [(j, (b**j) % mod) for j in range(0,m)]
    j = {j: (b**j) % mod for j in range(0, m)}

    # c = (b**-1)**m = b**(phi(mod)-1)**m
    c = fast_exp(fast_exp(b, (n - 1), mod), m, mod)
    # print(c)

    i = {i: (a * (c ** i)) % mod for i in range(0, m)}
    # print(j)
    # print(i)
    shared = [(x, y) for x, vi in i.items() for y, vj in j.items() if vi == vj]
    # print(shared)
    l = [((i * m) + j) % n for i, j in shared]

    # check
    # print('GOOD') if b ** l[0] % mod == a
    # print(l)

    return l


def fast_exp(x, e, m, y=1):
    # print(f'x = {x}  e = {e} y = {y}')
    if e == 0:
        # print('DONE')
        return y
    elif (e % 2 == 0):
        x = (x**2) % m
        e //= 2
        # print('EVEN')
        return fast_exp(x, e, m, y)
    else:
        y = (y*x) % m
        e -= 1
        # print('ODD')
        return fast_exp(x, e, m, y)


# Euclidean algorithm for determining greatest common divisor
def gcd(m, n):
    if m == 0:
        return n
    else:
        return gcd(n % m, m)


# Extended Euclidean algorithm. Returns a pair of integers such that xm + yn
# returns the smallest possible positive integer
def ext_gcd(m, n):
    if m == 0:
        return n, 0, 1
    else:
        div, x, y = ext_gcd(n % m, m)
        return div, y - n // m * x, x


def phi(n):
    return len([x for x in range(1, n) if gcd(x, n) == 1])


# A function to print all prime factors of
# a given number n
def eff_prime_factors(n):

    # Print the number of two's that divide n
    while n % 2 == 0:
        print(2),
        n = n / 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(n**0.5)+1, 2):

        # while i divides n , print i ad divide n
        while n % i == 0:
            print(i),
            n = n / i

    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        print(int(n))


def prime_check(n, d=2):

    while d < int(n**0.5):
        if n % d == 0:
            return False
            n = n / d
        d += 1

    return True


# Non-efficient algorithm to find prime factors of n
def non_eff_prime_factors(n, d=2):

    while d < int(n**0.5):
        if n % d == 0:
            print(d)
            n = n / d
        d += 1

    non_eff_prime_factors(n, d)

    print(int(n))


if __name__ == '__main__':
    unittest.main()
