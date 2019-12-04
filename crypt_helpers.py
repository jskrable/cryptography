#!/usr/bin/env python3
# coding: utf-8
"""
title: crypt_helpers.py
date: 2019-09-15
author: jskrable
description: classwork for CS789: Cryptography
"""

import os
import random
import math
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


def prime_search(order=5, true_random=False):
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

    return p


def naor_reingold(size=100):
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

    bits = ''
    for i in range(n):
        x = [0 if os_random(1) >= 128 else 1 for i in range(n)]
        e = np.sum(np.array([t[x[i]] for i, t in enumerate(a)]))
        b_int = fast_exp(g,e,N)
        b_bin = '{0:b}'.format(b_int).zfill(2*n)
        bit = str(np.dot(r, np.array(list(b_bin), dtype=int)) % 2)
        bits += bit

    b = BitArray(bin=bits)
    return b.uint


def blum_blum_shub(size=100):
    """
    cryptographically secure pseudo-random number generator
    use os.urandom() or quantumrandom for setup??
    MAKE THIS SMALLER, YOU DON'T NEED SO BIG

    not very efficient, need to streamline.
    use bitstring classes? functions?
    
    # true random int
    int.from_bytes(os.urandom(5), byteorder='little')
    # convert to binary
    '{0:b}'.format(2)
    """
    p = 0
    q = 0
    while p % 4 != 3:
        p = prime_search()
    while q % 4 != 3:
        q = prime_search()
    n = p * q
    # check the seed to ensure it's 1 < seed < n
    seed = os_random(5) % n

    # [i for in range(n-1) if gcd(n,i) == 1]
    bits = ''
    # using the generally agreed upon bit to digit ratio
    limit = math.floor(size * math.log(10, 2))
    Si = seed
    for i in range(n-1):
        if len(bits) >= limit:
            break
        if gcd(n,i) == 1:
            Sj = fast_exp(Si, 2, n)
            bits += str(Sj % 2)
            Si = Sj 

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




def baby_step_giant_step(b, a, mod):
    """
    algorithm for solving discrete log problem given a log base b
    mod must be prime???????????
    """

    if not miller_rabin(mod, 30):
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


def exp(x, e, m, y=1):
    """
    Function allowing efficient exponentiation within a modular group.
    X is the number to raise
    E is the power to raise it to
    M is the modulus

    """
    if e == 0:
        return y
    elif (e % 2 == 0):
        x = (x**2) % m
        e //= 2
        return exp(x, e, m, y)
    else:
        y = (y*x) % m
        e -= 1
        return exp(x, e, m, y)



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
    if miller_rabin(n):
        return n-1
    else:
        return len([x for x in range(1, n) if gcd(x, n) == 1])


# A function to print all prime factors of
# a given number n
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


# def pollards_rho(n):

#     if miller_rabin(n, 30):
#         raise Exception('n is prime you fool.')

#     x = 2
#     y = x**2 -1 
#     g = gcd((x-y), n)

#     if g == 1:
#         # choose new x
#         break

#     elif 1 < g < n:
#         if miller_rabin(g, 30):
#             return g
#         else:
#             pollards_rho(g)

#     else:
#         x = x**2 + 1 % n
#         y = (y**2 + 1)**2 + 1 % n

