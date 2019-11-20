#!/usr/bin/env python3
# coding: utf-8
"""
title: crypt_helpers.py
date: 2019-09-15
author: jskrable
description: classwork for CS789: Cryptography
"""

import random
import math


def primitive_root_search(m):
    """
    searches for a primitive root

    """
    
    if not miller_rabin(m, 30):
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


def miller_rabin(n, k, safe=False):
    """
    probabilistic prime checker
    n: integer to check for primality
    k: number of tests to perform, translates to 1 - (0.25) ** k 
    probablity that n is prime
    safe: if true, performs a secondary check to ensure n is a safe
    prime

    """

    # catch easy primes
    if n == 2 or n == 3:
        return True

    # catch all even numbers
    if n % 2 == 0:
        return False

    # initialize r and m
    # n - 1 = 2**r * m
    r, m = 0, n - 1
    # continuously divide to get m and r
    while m % 2 == 0:
        r += 1
        m //= 2
    # outer loop, try k times
    for _ in range(k):
        a = random.randint(2, n - 1)
        b = fast_exp(a, m, n)
        if b == 1 or b == n - 1:
            continue
        for _ in range(r - 1):
            b = fast_exp(b, 2, n)
            if b == n - 1:
                break
        else:
            return False
    return True




def baby_step_giant_step(b, a, mod):
    """
    algorithm for solving discrete log problem given a log base b
    mod must be prime???????????
    """

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


def fast_exp(x, e, m, show=False, y=1):
    """
    Function allowing efficient exponentiation within a modular group.
    X is the number to raise
    E is the power to raise it to
    M is the modulus

    """
    if show:
        print(f'x = {x}  e = {e} y = {y}')
    if e == 0:
        # print('DONE')
        return y
    elif (e % 2 == 0):
        x = (x**2) % m
        e //= 2
        # print('EVEN')
        return fast_exp(x, e, m, show, y)
    else:
        y = (y*x) % m
        e -= 1
        # print('ODD')
        return fast_exp(x, e, m, show, y)



def gcd(m, n, show=False):
    """
    Euclidean algorithm for determining greatest common divisor
    ensure m > n to show clean work.
    set show to True to print out work
    """
    if m == 0:
        return n
    else:
        if show:
            print(f'{m} = {m//(n%m)} * {n%m} + {m - (m//(n%m))*(n%m)}')
            if m - (m//(n%m))*(n%m) == 1:
                return 1
            else:
                return gcd(n % m, m)
        return gcd(n % m, m)



def ext_gcd(m, n):
    """
    Extended Euclidean algorithm. Returns a pair of integers such that xm + yn
    returns the smallest possible positive integer
    """
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


