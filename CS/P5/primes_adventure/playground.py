# P5 (not part of submission)
# This is where I test some more random things out

from primality import is_prime_miller, is_prime_naive, is_prime_aks

large_prime = 32416187567
large_composite = 200 * 32416188227	

# print(is_prime_aks(large_prime)) # yep this takes forever
import timeit

print(timeit.timeit("is_prime_miller(large_composite, 1)", number=10, globals=locals()))
# print(timeit.timeit("is_prime_aks(large_composite)", number=10, globals=locals()))
print(timeit.timeit("is_prime_naive(large_composite)", number=10,globals=locals()))