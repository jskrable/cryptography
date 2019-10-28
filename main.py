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


# WRITE TESTS FOR RSA
class TestRSA(unittest.TestCase):

    def test(self):

        messages = [x for x in [random.randint(10000, 100000) 
                    for x in range(1000) if prime_check(x)] if prime_check(x)]
        mods = [random.randint(10000, 100000) for x in range(len(messages))]
        Es = [random.randint(10000, 100000) for x in range(len(messages))]

        [self.assertEqual(
            message, 
            (rsa_decrypt(
                rsa_encrypt(message, mods[i], Es[i]), mods[i], Es[i])))
            for i, message in enumerate(messages)]


class TestFastExponentiation(unittest.TestCase):

    def test(self):

        Xs = [random.randint(1, 10000) for x in range(300000)]
        Es = [random.randint(1, 300) for x in range(300000)]
        Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(
            fast_exp(x, Es[i], Ms[i]),
            ((x ** Es[i]) % Ms[i])) for i, x in enumerate(Xs)]


class TestBabyStepGiantStep(unittest.TestCase):

    def test(self):

        Mods = [x for x in [random.randint(1, 10000) for x in range(1000)] if prime_check(x)]
        Bs = [random.randint(1, 10000) for x in range(len(Mods))]
        As = [random.randint(1, 10000) for x in range(len(Mods))]
        # Ms = [random.randint(1, 1000) for x in range(300000)]

        [self.assertEqual(
            (Bs[i] ** baby_step_giant_step(Bs[i], As[i], Mods[i])[0] % Mods[i]),
            (As[i] % Mods[i])) for i in range(len(Bs))]


def primitive_root_search(m):
    
    if not prime_check(m):
        return -1

    phi_m = phi(m)

    for r in range(2, phi_m):
        flag = False
        for f in eff_prime_factors(phi_m):
            if fast_exp(r, (phi_m // f), m) == 1:
                flag = True
                break
        if not flag:
            return r

    return -1


# Algorithm for solving discrete log problem given a log base and mod
# mod must be prime for this to work???????
def baby_step_giant_step(b, a, mod):

    if not prime_check(mod):
        return -1

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
# ensure m > n
def gcd(m, n):
    # clean implementation
    if m == 0:
        return n
    else:
        return gcd(n % m, m)
    # printout implementation
    # if m == 0:
    #     return n
    # else:
    #     # print(f'gcd({m},{n%m}) = {m//(n%m)} * {n%m} + {m - (m//(n%m))*(n%m)}')
    #     print(f'{m} = {m//(n%m)} * {n%m} + {m - (m//(n%m))*(n%m)}')
    #     if m - (m//(n%m))*(n%m) == 1:
    #         return 1
    #     else:
    #         return gcd(n % m, m)


# Extended Euclidean algorithm. Returns a pair of integers such that xm + yn
# returns the smallest possible positive integer
def ext_gcd(m, n):
    # clean implementation
    if m == 0:
        return n, 0, 1
    else:
        div, x, y = ext_gcd(n % m, m)
        return div, y - n // m * x, x
    # TODO write a printout implementation for this??


def phi(n):
    return len([x for x in range(1, n) if gcd(x, n) == 1])


# A function to print all prime factors of
# a given number n
def eff_prime_factors(n):

    factors = set()

    while n % 2 == 0:
        factors.add(2),
        n = n // 2

    for i in range(3, int(n**0.5)+1, 2):
        while n % i == 0:
            factors.add(i),
            n = n // i

    if n > 2:
        factors.add(n)

    return factors


def prime_check(n, d=2):

    while d < int(n**0.5)+1:
        if n % d == 0:
            return False
            n = n / d
        d += 1

    return True


# Non-efficient algorithm to find prime factors of n
def non_eff_prime_factors(n, d=2):

    while d < int(n**0.5):
        if n % d == 0:
            n = n / d
        d += 1

    non_eff_prime_factors(n, d)

    print(int(n))


def el_gamal(p, m):

    if not prime_check(p):
        return -1

    # Alice
    g = primitive_root_search(p)
    x = random.randint(1,p-1)
    h = fast_exp(g, x, p)

    # Bob
    r = random.randint(1,p-1)
    c1 = fast_exp(g, r, p)
    c2 = (fast_exp(h, r, p) * m) % p

    # Alice
    s = fast_exp(c1, x, p)
    decrypted = (fast_exp(s, p-2, p) * c2) % p

    return m, decrypted


def diffie_hellman():

    return -1


def rsa_encrypt(message, mod, e):
    return fast_exp(message, e, mod)


def rsa_decrypt(message, mod, e):
    d = phi(mod) + ext_gcd(phi(mod), e)[-1]
    return fast_exp(message, d, mod)


if __name__ == '__main__':
    unittest.main()
