# Problem 1
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Where the actual Sorter is defined

import random
import string

from common import Sorter, Data

def generate_name():
    """ Generates a random name

        Returns
        -------
        str
    """
    pool = string.ascii_letters + "-' " # pool of letters to choose from
    name_len = random.randint(1,30)
    name = ""
    for _ in range(name_len):
        name = name + pool[random.randint(0, len(pool)-1)]
    return name

class StudentData(Data):
    def __init__(self, first="", last="", GPA=0.0, graduation=0):
        self.first=first
        self.last=last
        self.GPA=GPA
        self.graduation=graduation
    
    def __repr__(self):
        return "{}, {} {} {}".format(self.last, self.first, self.GPA, self.graduation)

    def random(self, random_range=5):
        """ Populates self with a random data set

            Parameters
            ----------
            random_range: int
                The range of graduation dates
        """
        assert 1 <= random_range <= 5
        self.__init__(generate_name(), generate_name(), random.randint(0,400)/100, random.randint(2018,2018+random_range-1))

    def parse(self, s):
        """ Parses one line of string into an instance of StudentData
            
            Parameters
            ----------
            s: str
                The line of input
            
        """
        last, rest = s.split(", ")
        rest = rest.split(" ")
        year = int(rest[-1])
        GPA = float(rest[-2])
        first = " ".join(rest[:-2])
        return self.__init__(first, last, GPA, year)

class CountingSort(Sorter):
    def __init__(self, data=[]):
        self.data = data
        super().__init__(StudentData)
    
    
    def sort_naive(self):
        """ Sort the data by outputting a list of
            indices that order the array
            This is the version I think is most orthodox 
            (basically copying the reference book)
            
            Returns
            -------
            List(int)
        """
        k = 5
        B = [0] * len(self.data)
        C = [0] * k # five graduation years to count no. of points of that length
        for j in range(0, len(self.data)):
            C[self.data[j].graduation-2018] += 1
        for i in range(1,k):
            C[i] = C[i] + C[i-1]
        for j in range(len(self.data), 0, -1):
            j = j-1 # just to be 0-based
            Aj = self.data[j].graduation-2018
            B[C[Aj]-1] = j
            C[Aj] = C[Aj] - 1

        return B


    def sort_counting(self):
        """ Sort the data by outputting a list of
            indices that order the array

            THIS IS THE FINAL SUBMITTED METHOD
            
            Returns
            -------
            List(int)
        """
        year_to_ids = {}
        for i in range(2018, 2023):
            year_to_ids[i] = []
        for i, d in enumerate(self.data):
            year_to_ids[d.graduation].append(i)

        accumulated = []
        for i in range(2018, 2023):
            accumulated += year_to_ids[i]
        return accumulated
    
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
            if self.data[i].graduation < self.data[last_i].graduation: 
                # graduation year only increases
                return False
            elif self.data[i].graduation == self.data[last_i].graduation:
                # in case it's the same year
                # assert that this is the very next instance of the same
                # graduation year found
                for j in range(last_i+1, len(self.data)):
                    if self.data[j].graduation == self.data[i].graduation:
                        if self.data[j] == self.data[i]:
                            break
                        else:
                            return False
            else: 
                # verify that it's the first instance of the next graduation year
                for j in range(0, len(self.data)):
                    if self.data[j].graduation == self.data[i].graduation:
                        if self.data[j] == self.data[i]:
                            break
                        else:
                            return False
            last_i = i
        
        return True