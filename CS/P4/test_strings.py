# P4 (not part of final result)
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# This is a file used to determine the BEST
# algorithm to alphabetically sort fixed-sized
# strings (length 1-40, we'll test them all)
# We want to figure out that for each length,
# what is the fastest algorithm for different
# sizes of data input

import random
import string
import time
from collections import defaultdict

def generate_data(str_len, str_no):
    return ["".join(random.choices(string.ascii_uppercase, k=str_len)) for _ in range(str_no)]

def sort_builtin(data):
    return sorted(data)

def sort_lsd_radix(data):
    n = len(data[0]) # length of strings
    for digit in range(n):
        l = defaultdict(list)
        for d in data:
            l[d[n-digit-1]].append(d)
        data = []
        for i in string.ascii_uppercase:
            data.extend(l[i])
    return data

class sort_msd:
    # Source describing algorithm: http://www.informit.com/articles/article.aspx?p=2180073&seqNum=3
    R = 26
    M = 15
    def __init__(self, data=[]):
        self.aux = []

    def sort_msd(self, data):
        self.data = data
        self.len = len(self.data[0])
        N = len(self.data)
        self.aux = [[] for _ in range(N)]
        self._sort(0, N-1, 0)
        return self.data

    def _sort_naive(self, lo, hi, d):
        # simple sorting for small arrays
        self.data[lo:hi+1] = sorted(self.data[lo:hi+1], key=lambda x:x[d])
    def _sort(self, lo, hi, d):
        if d >= self.len:
            return
        if (hi <= lo + sort_msd.M):
            self._sort_naive(lo, hi, d)
            return
        bins = [[] for _ in range(self.R)]
        for i in range(lo, hi+1):
            bins[ord(self.data[i-lo][d])-ord('A')].append(self.data[i])

        out = []
        for b in bins:
            out.extend(b)

        self.data[lo:hi+1] = out

        for i, b in enumerate(bins):
            self._sort(lo, lo+len(b)-1, d+1)
            lo = lo+len(b)

c = sort_msd()
methods = [sort_builtin, sort_lsd_radix, c.sort_msd]
for j in range(2, 7):
    for i in [1,2,5,10,20,40]:
        for _ in range(1):
            data = generate_data(i, 10**j)
            for method in methods:
                start = time.time()
                method(data)
                end = time.time()
                delta = end-start
                print("{}: {}ms for {} of len-{} strings".format(method.__name__, delta*1000, 10**j, i))