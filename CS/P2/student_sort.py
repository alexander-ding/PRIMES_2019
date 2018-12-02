# Problem 2
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Where the actual Sorter is defined

import random
import string
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

class StudentSort(Sorter):
    def __init__(self, data=[]):
        self.data = data
        super().__init__(StudentData)
    

    def sort_builtin(self):
        """ Sort the data by outputting a list of
            indices that order the array
            Use the builtin sort function
            
            Returns
            -------
            List(int)
        """
        # first by graduation, then by GPA (inverted)
        return [i[0] for i in sorted(enumerate(self.data), key=lambda x:(x[1].graduation, -x[1].GPA))] 

    def sort_counting(self):
        """ Sort the data by using counting sort
            Each bin is a GPA between 0.00 (bin 0) and 4.00 (bin 401)
            For each graduation year, there are 401 of these
            
            Returns
            -------
            List(int)
        """
        def _index(year, GPA):
            """ Helper function to access the right bin

                Parameters
                ----------
                year: int
                    The year of the student (2018-2022)
                GPA: float
                    The GPA of the student (0.00 to 4.00)

                Returns
                -------
                int
            """
            return (year - 2018)*401+round((4.00-GPA)*100) # GPA in decreasing order
        l = [[] for _ in range(5*401)] # initialize empty bins for every possible (year, GPA)
        for i, d in enumerate(self.data):
            l[_index(d.graduation, d.GPA)].append(i)
        return chain(*l)

    def sort_twopass(self):
        """ Sort the data by first doing the O(n) sorting and then
            the O(nlogn) sorting, since this minimizes the time usage
            
            Returns
            -------
            List(int)
        """
        # counting sort the years
        l = [[] for _ in range(5)] # initialize empty bins for each year
        for i, d in enumerate(self.data):
            l[d.graduation-2018].append(i)
        for i in range(5):
            l[i].sort(key=lambda x: self.data[x].GPA, reverse=True)
        
        return chain(*l)
    
    def sort_combined(self):
        """ Sort the data by first analyzing data 
            size and choosing the right method

            THIS IS THE FINAL SUBMITTED METHOD
            
            Returns
            -------
            List(int)
        """
        if len(self.data) < 1000:
            return self.sort_builtin()
        elif len(self.data) < 1000000:
            return self.sort_twopass()
        else:
            return self.sort_counting()


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
        for index, i in enumerate(sorted_index[1:]):
            if self.data[i].graduation < self.data[last_i].graduation: 
                # graduation year only increases
                return False
            else:
                # in case it's the same year
                # assert that this is the very next instance of the smaller
                # GPA found
                for j in sorted_index[index+1:]:
                    if self.data[j].graduation == self.data[i].graduation:
                        if self.data[j].GPA > self.data[i].GPA:
                            return False
                        elif self.data[j].GPA == self.data[i].GPA and j < i:
                            return False    
            last_i = i
        
        return True