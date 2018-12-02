# Helper file designed to be used throughout this PSET
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac

from pathlib import Path
import time

class Sorter:
    def __init__(self, data_type):
        self.data_type = data_type
        self.time = 0
    
    def clear_data(self):
        self.data = []

    def generate_data(self, count=1000, **kwargs):
        """ Generates random test data for sorting and
            stores the generated data
            
            Parameters
            ----------
            count: int
                The number of entries of the dataset
            
            kwargs: dict(str->any)
                Optional keyword arguments for random
            
        """
        self.clear_data()
        for _ in range(count):
            data_point = self.data_type() # generate one instance of test data
            data_point.random(**kwargs)
            self.data.append(data_point)
    
    def read_data(self, file_name):
        """ Loads the Sorter with data from a file under tests/
            
            Parameters
            ----------
            file_name: str
                The file name under tests/name.test

        """
        p = Path(file_name)
        if not p.exists():
            raise FileNotFoundError()

        self.clear_data()
        with open(p) as f:
            lines = f.readlines()
            for line in lines[1:]:
                datum = self.data_type()
                datum.parse(line)
                self.data.append(datum)
    
    def save_data(self, file_name):
        """ Saves the Data in the Sorter into a file under tests/name.test

            Parameters
            ----------
            file_name: str
                The name of the file
        
        """
        with open("tests/{}.test".format(file_name), "w") as f:
            f.write("{}\n".format(len(self.data)))
            for line in self.data:
                f.write(str(line)+"\n")
    
    def sort(self, method):
        """ Calls the sort method and records the sort time

            Parameters
            ----------
            method: function
                The method to be called
        """
        start_time = time.time()
        out = method()
        end_time = time.time()
        self.time = (end_time - start_time)*1000 # in ms
        return out

    def output(self, sorted_indices):
        """ Outputs generator of lines of the sorted data
            one line at a time

            Parameters
            ----------
            sorted_indices: List
                The indices of the sorted results
            
            Returns
            -------
            Generator(str)
        """
        if not isinstance(sorted_indices, list):
            sorted_indices = list(sorted_indices)
        num = 0
        while num < len(sorted_indices):
            yield str(self.data[sorted_indices[num]])
            num += 1
        yield str(self.time)
        
    def verify(self, sorted_indices):
        """ For the child classes to define """
        raise NotImplementedError()

class Data:
    def __init__(self):
        raise NotImplementedError()
    
    def random(self):
        raise NotImplementedError()
    
    def __str__(self):
        return self.__repr__()