# P5 (not part of submission)
# This is where I test out the prime checkers systematically 
# for their runtime
# Here is a set of tests I would like to keep


from primality import is_prime_miller, is_prime_naive
import time
import random

# generate an answer key of primes and composites
primes = []
composites = []

for i in range(10000000,10500000):
    if is_prime_naive(i):
        primes.append(i)
    else:
        composites.append(i)

print("PRIMES found")

l = [("is_prime", "faster", "time")]

wrongs = 0

for i in primes+composites:
    start = time.time()
    is_prime = is_prime_naive(i)
    end = time.time()
    naive_time = end-start
    start = time.time()
    is_prime_maybe = is_prime_miller(i,1)
    end = time.time()
    miller_time = end-start
    if naive_time-miller_time > 0:
        l.append((is_prime, 'miller', naive_time, miller_time))
    else:
        l.append((is_prime, 'naive', naive_time, miller_time))
    
    if is_prime != is_prime_maybe:
        wrongs += 1
        print("Miller goes wrong at {}".format(i))

naive_count, miller_count = 0, 0
total_naive_faster = 0
total_naive_time, total_miller_time = 0, 0
for (is_prime, faster, naive_time, miller_time) in l[1:]:
    if faster == "miller":
        miller_count += 1  
    else:
        naive_count += 1
    total_miller_time += miller_time
    total_naive_time += naive_time
    total_naive_faster += (miller_time-naive_time)

print("Primes count:", len(primes), "Composites count:", len(composites))
print("Case count with naive faster:", naive_count, "Case count with miller faster:", miller_count)
print("Naive faster by:", total_naive_faster) # if neg, then miller is faster by
print("Naive total time:", total_naive_time, "Miller total time:", total_miller_time)
print("Miller gets wrong", wrongs)