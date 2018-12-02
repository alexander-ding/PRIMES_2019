# P5 (not part of final solution -- just my problem solving process)
# This is where I define the best prime checkers for testing

# source https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

import random
def miller_test(d, n):
    a = random.randint(2,n-2)
    x = pow(a,d,n)

    if x==1 or x==(n-1):
        return True
    
    while d != (n-1):
        x = pow(x,2,n)
        d *= 2

        if x==1:
            return False
        if x==n-1:
            return True

    return False

def is_prime_miller(n, k=4):
    if n<=1 or n==4:
        return False
    if n<=3:
        return True
    
    d = n-1
    while (d%2)==0: # while even
        d = d//2
    for _ in range(k):
        if not miller_test(d,n):
            return False
    
    return True

import math

primes_known = []
# Source: https://www.geeksforgeeks.org/primality-test-set-1-introduction-and-school-method/
def is_prime_naive(n):
    if n<=1:
        return False
    if n==2 or n==3:
        return True
    
    if ((n%2)==0 or (n%3)==0):
        return False
    
    i = 5
    # step of 6
    for i in range(5,int(math.sqrt(n))+1, 6):
        if (n%i)==0 or (n%(i+2))==0:
            return False
    
    return True

# Source: https://rosettacode.org/wiki/AKS_test_for_primes#Python
def expand_x_1(n): 
# This version uses a generator and thus less computations
    c =1
    for i in range(n//2+1):
        c = c*(n-i)//(i+1)
        yield c
 
def is_prime_aks(p):
    if p==2:
        return True
 
    for i in expand_x_1(p):
        if i % p:
# we stop without computing all possible solutions
            return False
    return True
