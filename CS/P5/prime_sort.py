# Problem 5
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Where the actual Sorter is defined

import random
import string
import math
import random
from common import Sorter, Data
from itertools import chain

# Source: https://www.geeksforgeeks.org/primality-test-set-1-introduction-and-school-method/
def is_prime_naive(n):
    if n<=1:
        return False
    if n==2 or n==3:
        return True
    
    if ((n%2)==0 or (n%3)==0):
        return False
    
    # step of 6
    for i in range(5,int(math.sqrt(n))+1, 6):
        if (n%i)==0 or (n%(i+2))==0:
            return False
    
    return True

# use preloaded primes, for up to n = 3000000^2
def is_prime_naive_preloaded(n):
    if n <= 1:
        return False
    if n==2 or n==3:
        return True
    
    cutoff = int(math.sqrt(n))
    for p in PrimesData.small_primes:
        if p > cutoff:
            return True

        if (n % p) == 0:
            return False


# Source: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/ 

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

def is_prime_miller(n, k=1):
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

class PrimesData(Data):
    small_primes = [] # store primes up to 1000000-1
    composites = [] # store composites up to 1000000-1
    large_primes = [32416187567, 15487469
, 15489053, 49979233, 122949461, 141650611, 179426083, 295076767, 295078909] # manually store a few for test generation
    initialized = False
        
    def __init__(self, ints=None):
        if ints is None:
            self.ints = [0, 0, 0, 0, 0]
    
    def __repr__(self):
        return " ".join([str(i) for i in self.ints])

    @classmethod
    def initialize(cls):
        """ Initializes the set of small primes and composites
        """
        
        for i in range(1, 3000000):
            if is_prime_naive(i):
                cls.small_primes.append(i)
            else:
                cls.composites.append(i)
        print("Generate data initialized")
        cls.initialized = True

    def random(self, large_prime=False, complex_composite=False):
        """ Populates self with four composites and one prime

            Parameters
            ----------
            large_prime: bool
                Whether or not the prime is large
            
            complex_composite: bool
                Whether or not one product of large primes is
                included
        """
        if not PrimesData.initialized:
            PrimesData.initialize()
        
        # generate one prime as specified
        prime = random.choice(PrimesData.large_primes) if large_prime else random.choice(PrimesData.small_primes)

        # generate four composites
        composites = random.choices(PrimesData.composites, k=4)
        prime_index = random.randint(0,4)
        
        # in case of complex composite, replace one composite with
        # complex composite
        if complex_composite:
            complex_index = random.randint(0,3)
            composites[complex_index] = random.choice(PrimesData.large_primes) * random.choice(PrimesData.large_primes)
        
        composite_i = 0
        for i in range(5):
            if i == prime_index:
                self.ints[i] = prime
            else:
                self.ints[i] = composites[composite_i]
                composite_i += 1

    def parse(self, s):
        """ Parses one line of string into an instance of PrimesData
            
            Parameters
            ----------
            s: str
                The line of input
            
        """
        self.ints = [int(substr) for substr in s.split(" ")]

    @property
    def prime(self):
        return self.ints[self.prime_index]

    def preprocess_pure_miller(self):
        """ Implements the baseline algorithm described in the
            problem solution PDF. Utilize process of elimination
            and just the Miller-Rabin test
        """
        candidates = list(range(5)) # possible primes (indices)
        while len(candidates) > 1:
            for c in candidates[:]:
                if not is_prime_miller(self.ints[c]):
                    candidates.remove(c)
                    if len(candidates) == 1:
                        self.prime_index = candidates[0]
                        return

    def preprocess_naive_simul(self):
        """ The most basic naive algorithm, trying numbers out
            for all candidates simultaneously
        """
        candidates = list(range(5)) # indices of candidates left
        roots = [math.sqrt(x) for x in self.ints]
        # first elimination
        for i,n in enumerate(self.ints):
            if n<=1:
                candidates.remove(i)
            if n==2 or n==3:
                self.prime_index = i
                return
            if ((n%2)==0 or (n%3)==0):
                candidates.remove(i)

        if len(candidates) == 1:
            self.prime_index = candidates[0]
            return
        
        # steps of 5
        i = 5
        while len(candidates) > 1:
            for c in candidates[:]:
                if i > roots[c]:
                    self.prime_index = c
                    return
                if ((self.ints[c]%i)==0) or ((self.ints[c]%(i+2))==0):
                    candidates.remove(c)

                    # if this results in 1 candidate left
                    if len(candidates) == 1:
                        self.prime_index = candidates[0]
                        return
                        
            i += 6

        if len(candidates) == 1:
            self.prime_index = candidates[0]
            return
    
    def preprocess_split(self):
        """ Split the task between miller (for bigger numbers) and naive (for smaller numbers)
        """
        N = 10000000
        candidates = list(range(5)) # possible primes (indices)

        # if we get lucky
        for c in candidates[:]:
            if self.ints[c]<=1:
                candidates.remove(c)
            if self.ints[c]==2 or self.ints[c]==3:
                self.prime_index = c
                return
            if ((self.ints[c]%2)==0 or (self.ints[c]%3)==0):
                candidates.remove(c)

        if len(candidates) == 1:
            self.prime_index = candidates[0]
            return
        
        while len(candidates) > 1:
            # remaining candidates are all massive
            for c in candidates[:]:
                if self.ints[c] > N:
                    if not is_prime_miller(self.ints[c]):
                        candidates.remove(c)
                        # if this results in 1 candidate left
                        if len(candidates) == 1:
                            self.prime_index = candidates[0]
                            return
                else: 
                    if is_prime_naive_preloaded(self.ints[c]):
                        self.prime_index = c
                        return
                    else:
                        candidates.remove(c)
                        if len(candidates) == 1:
                            self.prime_index = candidates[0]
                            return

        if len(candidates) == 1:
            self.prime_index = candidates[0]
            return

    def preprocess(self):
        """ Define the preprocess of choice
            Just a utility for maintaining static code
        """
        self.preprocess_split()

    def verify(self):
        """ Checks whether the preprocess is correct
            This does not catch ALL the errors, but it should suffice
            as a sanity check
        """
        for _ in range(2):
            if not is_prime_miller(self.ints[self.prime_index]):
                return False
        return True


class PrimesSort(Sorter):
    def __init__(self, data=[]):
        self.data = data
        super().__init__(PrimesData)
    
    def sort_builtin(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Use the builtin sort function
            
            Returns
            -------
            List(int)
        """
        for d in self.data:
            d.preprocess()
        
        # sort first by position of prime, then by the prime's size
        # lastly by the sequence of integers
        return [i[0] for i in sorted(enumerate(self.data), key=lambda x:(x[1].prime_index, x[1].prime, x[1].ints))] 
    
    def sort_counting(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Split input into bins based on prime
            position. Then Timsort. 
            
            Returns
            -------
            List(int)
        """
        bins = [list() for _ in range(5)] # 5 empty lists
        for i in range(len(self.data)):
            self.data[i].preprocess()
            bins[self.data[i].prime_index].append(i)
        
        out = []
        for b in bins:
            out.extend(sorted(b, key=lambda x: (self.data[x].prime, self.data[x].ints)))
        
        return out

    def verify(self, sorted_index):
        """ Verifies that the output data is correct 
            
            Parameters
            ----------
            sorted_index: List()
                A list of sorted indices of the data
            
            Returns
            -------
            bool
        """ 
        if not isinstance(sorted_index, list):
            sorted_index = list(sorted_index)
        last_i = sorted_index[0]
        for i in sorted_index[1:]:
            last_prime_index = self.data[last_i].prime_index
            cur_prime_index = self.data[i].prime_index
            # prime_index must be non-decreasing
            if last_prime_index > cur_prime_index:
                return False
            elif last_prime_index == cur_prime_index:
                # if equal, then prime itself must be non-decreasing
                if self.data[last_i].ints[last_prime_index] > self.data[i].ints[cur_prime_index]:
                    return False
                elif self.data[last_i].ints[last_prime_index] == self.data[i].ints[cur_prime_index]:
                    # if equal, then the sequence of ints must be non-decreasing
                    if self.data[last_i].ints > self.data[i].ints:
                        return False
            last_i = i
        return True


PrimesData.initialize()