#!/usr/bin/env python3
# coding: utf-8
"""
title: main.py
date: 2019-09-15
author: jskrable
description: classwork for CS789: Cryptography
"""


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


# A function to print all prime factors of  
# a given number n 
def eff_prime_factors(n): 
      
    # Print the number of two's that divide n 
    while n % 2 == 0: 
        print(2), 
        n = n / 2
          
    # n must be odd at this point 
    # so a skip of 2 ( i = i + 2) can be used 
    for i in range(3,int(n**0.5)+1,2): 
          
        # while i divides n , print i ad divide n 
        while n % i== 0: 
            print(i), 
            n = n / i 
              
    # Condition if n is a prime 
    # number greater than 2 
    if n > 2: 
        print(int(n))


# Non-efficient algorithm to find prime factors of n
def non_eff_prime_factors(n, d=2):

	

	while d < int(n**0.5):
		if n % d == 0:
			print(d)
			n = n / d
		d += 1

	non_eff_prime_factors(n, d)

	print(int(n))


