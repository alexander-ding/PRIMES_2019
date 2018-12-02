# Problem 4
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Where the actual Sorter is defined

import random
import string
import math
from itertools import chain
from collections import Counter
from common import Sorter, Data

def generate_string():
    """ Generates a random string of random length 
        between 1 to 40 and upper characters

        Returns
        -------
        str
    """
    return "".join(random.choices(string.ascii_uppercase, k=random.randint(1,40)))

class StringData(Data):
    def __init__(self, s=""):
        self.s = s
    
    def __repr__(self):
        return self.s

    def random(self):
        """ Populates self with a random string
        """
        self.__init__(generate_string())

    def parse(self, s):
        """ Parses one line of string into an instance of StringData
            
            Parameters
            ----------
            s: str
                The line of input
            
        """
        # get rid of the \n
        return self.__init__(s[:-1])

    def preprocess(self):
        """ Preprocesses by computing most common 
            letter (the smallest one) and its 
            number of occurences
        """
        result = Counter(self.s)
        highest = 0
        current = ""
        for i in sorted(result.keys()):
            if result[i] > highest:
                highest = result[i]
                current = i
        self.count = highest
        self.char = ord(current) - ord("A")

class StringSort(Sorter):
    """ This StringSort sorts the data in the 
        following rule:

        1. First by the count of the most commonly
        occurring character (decreasing order)

        2. Then by the specific character of the
        most commonly occurring character. If
        there are multiple, pick the "smallest"
        (increasing order ("A" precedes "B"))

        3. Finally by the strings themselves
        (increasing order)
    """
    def __init__(self, data=[]):
        self.data = data
        super().__init__(StringData)

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
        # first by count (decreasing order)
        # then by character
        # finally by string itself
        return [i[0] for i in sorted(enumerate(self.data), key=lambda x:(-x[1].count, x[1].char, x[1].s))] 

    def sort_bins(self):
        """ Sort the data by outputting a list
            of indices that order the array

            Divides the input set into bins of strings
            sharing the same number of the same most 
            commonly occurring characters (i.e. each bin
            is indexed by the length and then the character)
            e.g., a bin can be that of strings that have 10 
            'n's, which is the most commonly occurring
            character of these strings. 

            Each bin is then treated as an individual string
            alphabetical sorting problem, where a palette of
            such algorithms is used. Note that for each bin,
            the string has fixed-length.

            Returns
            -------
            List(int) 
        """
        bins = [[] for _ in range(26*40)] # empty bins
        for i, d in enumerate(self.data):
            d.preprocess()
            bins[(40-d.count)*26+d.char].append(i)

        out = []
        for b in bins:
            out.extend(sorted(b, key=lambda x: self.data[x].s))
        
        return out

    def sort_combined(self):
        """ Sort the data by outputting a list
            of indices that order the array.
            Cutoff at 10000. If input size >
            cutoff, use sort_builtin. If not, 
            use sort_bins.

            THIS IS THE FINAL SUBMITTED METHOD

            Returns
            -------
            List(int)
        """
        if len(self.data) < 10000:
            return self.sort_builtin()
        else:
            return self.sort_bins()


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
            if self.data[i].count > self.data[last_i].count:
                return False
            elif self.data[i].count == self.data[last_i].count:
                if self.data[i].char < self.data[last_i].char:
                    return False
                elif self.data[i].char == self.data[last_i].char:
                    if self.data[i].s < self.data[last_i].s:
                        return False
            last_i = i
        return True