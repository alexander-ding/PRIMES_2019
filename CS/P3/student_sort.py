# Problem 3
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Where the actual Sorter is defined

import random
import string
import math
from itertools import chain
from common import Sorter, Data

def generate_name():
    """ Generates a random name

        Returns
        -------
        str
    """
    pool = string.ascii_letters + "-' " # pool of letters to choose from
    name_len = random.randint(1,30)
    return "".join(random.choices(pool, k=name_len))

class StudentData(Data):
    IDs = []
    index = 0
    def __init__(self, id=0, first="", last="", GPA=0.0, graduation=0):
        self.id = id
        self.first=first
        self.last=last
        self.GPA=GPA
        self.graduation=graduation
    
    def __repr__(self):
        return "{id:09d} {last}, {first} {GPA} {grad}".format(id=self.id, last=self.last, first=self.first, GPA=self.GPA, grad=self.graduation)

    @classmethod
    def reset(self, size):
        """ Resets the ordering from which student ID is drawn

            Parameters
            ----------
            size: int
                The number of data entries to expect for random
                generation
        """
        StudentData.IDs = random.sample(range(0, 1000000000), size)
        StudentData.index = 0

    def random(self):
        """ Populates self with a random data set
            Since only ID matters, the other fields would be
            foo-like values
        """
        ID = StudentData.IDs[StudentData.index]
        StudentData.index += 1
        self.__init__(ID, "A c", "B d", 0.1, 2018)

    def parse(self, s):
        """ Parses one line of string into an instance of StudentData
            
            Parameters
            ----------
            s: str
                The line of input
            
        """
        id_last, rest = s.split(", ")
        rest = rest.split(" ")
        year = int(rest[-1])
        GPA = float(rest[-2])
        first = " ".join(rest[:-2])

        rest = id_last.split(" ")
        id = int(rest[0])
        last = " ".join(rest[1:])
        return self.__init__(id, first, last, GPA, year)

class StudentSort(Sorter):
    def __init__(self, data=[]):
        self.data = data
        super().__init__(StudentData)
    
    def generate_data(self, count=1000):
        """ Generates random test data for sorting and
            stores the generated data
            Wrapper for the Super()'s generate_data
            
            Parameters
            ----------
            count: int
                The number of entries of the dataset
            
        """
        StudentData.reset(count)
        super().generate_data(count)

    def sort_builtin(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Use the builtin sort function

            THIS IS THE FINAL SUBMITTED METHOD
            
            Returns
            -------
            List(int)
        """
        # by id
        return [i[0] for i in sorted(enumerate(self.data), key=lambda x:x[1].id)] 

    def sort_radix_1(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Split the len(9) index into digits
            to perform radix sort
        """
        output = range(len(self.data))

        # each loop of this is a counting sort
        for digit in range(10):
            l = [[] for _ in range(10)] # initialize empty bins for each year
            for i in output:
                l[ self.data[i].id//(10**digit) % 10 ].append(i)
            output = list(chain(*l))
            
        return output

    def sort_radix_3(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Split the len(9) index into groups of 3 digits (1000 numbers)
            to perform radix sort
        """
        n = len(self.data)
        group_size = 3

        def _get_group_id(n, i):
            """ Returns the specific group of three numbers of the id, starting
                from the rightmost
                For example, _get_group_id(1020,0) returns the rightmost group of 3,
                which is 020, and _get_group_id(1020,1) returns the middle group of 3,
                which, after filling in some 0's, is 001. 

                Parameters
                ----------
                n: int
                    The number to be split into groups
                i: int
                    Which group to be returned, with 0 as the rightmost group
                
                Returns
                -------
                int
            """
            return (n // (10**(group_size*i))) % (10**group_size)

        output = list(range(n))

        # each loop of this is a counting sort
        for group_number in range(group_size):
            count = [0] * (10**group_size)
            # count occurences of each possible group
            for i in range(0, n):
                count[_get_group_id(self.data[output[i]].id, group_number)] += 1

            # add up to get actual index
            for i in range(1, 10**group_size):
                count[i] += count[i-1]

            new_output = [0]*n
            for i in range(n-1,-1,-1): # [0,n-1] enuemrated backwards
                id = _get_group_id(self.data[output[i]].id, group_number)
                new_output[count[id]-1] = output[i]
                count[id] -= 1
            output = new_output
            
        return output
    
    def sort_merge(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Use a standard mergesort that compares based on the id

            Returns
            -------
            List(int)
        """
        def merge_sort(l):
            """ Standard mergesort on a list of integers

                Parameters
                ----------
                l: List(int)
            """
            # Source: algorithm description https://www.geeksforgeeks.org/merge-sort/
            if len(l) > 1:
                mid = len(l)//2
                left = l[:mid]
                right = l[mid:]

                merge_sort(left)
                merge_sort(right)

                i_l = 0
                i_r = 0
                j = 0
                while i_l < len(left) and i_r < len(right):
                    if self.data[left[i_l]].id < self.data[right[i_r]].id:
                        l[j] = left[i_l]
                        i_l += 1
                    else:
                        l[j] = right[i_r]
                        i_r += 1
                    j += 1
                
                while i_l < len(left):
                    l[j] = left[i_l]
                    i_l += 1
                    j += 1
                
                while i_r < len(right):
                    l[j] = right[i_r]
                    i_r += 1
                    j += 1
        output = list(range(len(self.data)))
        merge_sort(output)
        return output
        
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
        last_id = -1
        for i in sorted_index:
            if self.data[i].id <= last_id:
                return False
            last_id = self.data[i].id
        return True