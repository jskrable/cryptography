#!/usr/bin/env python3
# coding: utf-8
"""
title: crypt_helpers.py
date: 2019-09-15
author: jskrable
description: cryptographic helper functions
"""

import os
import random
import math
import hashlib
import numpy as np
from bitstring import BitArray


def get_primes():
    """
    reads file of primes numbers and returns a list.
    use for testing.
    """
    with open('./primes.txt') as f:
            data = f.read()
            primes = [int(x) for x in data[1:-1].split(',')]
    return primes


def os_random(order, m=math.inf, n=0):
    """
    returns a random int between n and m using the operating
    system's true random function
    """
    return int.from_bytes(os.urandom(order), byteorder='little')


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


def prime_search(order=5, true_random=False, safe=False):
    """
    Searches for and returns a prime number. Uses the 
    operating system's true random functions.
    """
    p = 0
    while not miller_rabin(p):
        if true_random:
            p = blum_blum_shub(order)
        else:
            p = os_random(order)
    if safe:
        p = 2 * p + 1
    return p


def naor_reingold(size=10):
    """
    cryptographically secure pseudo-random number generator
    """
    n = os_random(1)
    p = prime_search()
    q = prime_search()
    N = p * q
    a = [(os_random(2), os_random(2)) for i in range(n)]

    b = os_random(3)
    while gcd(N,b) != 1:
        b = os_random
    g = b ** 2 % N

    r = '{0:b}'.format(os_random(600))[:2*n]
    r = np.array(list(r), dtype=int)

    # using the generally agreed upon bit to digit ratio
    limit = math.floor(size * math.log(10, 2))
    bits = ''
    for i in range(n):
        x = [0 if os_random(1) >= 128 else 1 for i in range(n)]
        e = np.sum(np.array([t[x[i]] for i, t in enumerate(a)]))
        b_int = fast_exp(g,e,N)
        b_bin = '{0:b}'.format(b_int).zfill(2*n)
        bit = str(np.dot(r, np.array(list(b_bin), dtype=int)) % 2)
        bits += bit
        if len(bits) >= limit:
            break

    # ensure digits match the size argument
    b = BitArray(bin=bits).uint
    digits = len(str(b))
    if digits < size:
        diff = size - digits
        b = int(''.join(['1'for i in range(diff)]) + str(b))
    elif digits > size:
        b = int(str(b)[:size])
    return b


def blum_blum_shub(size=10):
    """
    cryptographically secure pseudo-random number generator
    size is the number of digits in the generated integer
    """
    p = 0
    q = 0
    while p % 4 != 3:
        p = prime_search()
    while q % 4 != 3:
        q = prime_search()
    n = p * q
    seed = os_random(5) % n
    # using the generally agreed upon bit to digit ratio
    limit = math.floor(size * math.log(10, 2))
    Si = seed
    bits = ''
    for i in range(n-1):
        if len(bits) >= limit:
            break
        if gcd(n,i) == 1:
            Sj = fast_exp(Si, 2, n)
            bits += str(Sj % 2)
            Si = Sj 

    # ensure digits match the size argument
    b = BitArray(bin=bits).uint
    digits = len(str(b))
    if digits < size:
        diff = size - digits
        b = int(''.join(['1'for i in range(diff)]) + str(b))
    elif digits > size:
        b = int(str(b)[:size])
    return b


def miller_rabin(n, k=30, safe=False):
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

    # add safe in here


    return True


def baby_step_giant_step(a, b, mod):
    """
    solves discrete log problem given an answer a, log base b, and
    modular group mod.
    """
    n = phi(mod)
    m = math.ceil((n**0.5) % mod)
    # baby step, more efficient to store in dict
    j = {fast_exp(b, j, mod) : j for j in range(m)}
    # fermat's little theorem, c = (b**-1)**m = b**(phi(mod)-1)**m
    c = fast_exp(fast_exp(b, (n - 1), mod), m, mod)
    # giant step, similar to j, but break and return if a match is found
    for i in range(m):
        y = (a * fast_exp(c, i, mod)) % mod
        if y in j:
            return (i * m) + j[y] % n
    # failure if no overlap found
    return None


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
    if m == 0:
        return n, 0, 1
    else:
        div, x, y = ext_gcd(n % m, m)
        return div, y - n // m * x, x


def phi(n):
    """
    Helper function to find the size of the group
    """
    if miller_rabin(n):
        return n-1
    else:
        return len([x for x in range(1, n) if gcd(x, n) == 1])


def eff_prime_factors(n):
    """
    function to find a set of all prime factors for any 
    given n. takes in an integer, returns a set.
    """
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


def pollards_rho(n, x=2, limit=5):
    """
    hitting recursion limit, refactor to 2 loops?
    prime init is helping...
    """
    if miller_rabin(n, 30):
        raise Exception('n is prime you fool.')

    c = 1
    g = 1
    count = 1
    f = lambda x: x**2 + c % n
    while (g == 1):
        # tortoise
        x = f(x)
        # hare
        y = f(f(x))
        g = gcd(abs(x-y), n)
        count += 1
        if (g == n) or (count >= limit):
            x = random.randint(2, n-2)
            c = random.randint(2, n-1)
            y = x
            count = 1
    return g


# def str_to_int(message):
#     """
#     """
#     return int(message.encode().hex(), 16)


# def int_to_str(message):
#     return bytearray.fromhex(hex(message)[2:])