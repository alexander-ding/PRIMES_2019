# P1
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Run me under the folder of this particular problem
# Provides test functions

from counting_sort import CountingSort, StudentData
from pathlib import Path
import time

def generate_testing_data():
    """ Generate testing data of various lengths
    """
    print("Generating test data")
    c = CountingSort()
    for i in range(0,10):
        c.generate_data(10)
        c.save_data("0{}".format(i))
    
    for i in range(10,20):
        c.generate_data(10000)
        c.save_data(i)
    
    for i in range(20,30):
        c.generate_data(100000)
        c.save_data(i)
    
    for i in range(30,35):
        c.clear_data()
        for _ in range(100000):
            s = StudentData()
            s.random(random_range=1) # test for cases of only 1 year
            c.data.append(s)
        c.save_data(i)
    
    for i in range(35,40):
        c.clear_data()
        for _ in range(100000):
            s = StudentData()
            s.random(random_range=2) # test for cases of only 2 years
            c.data.append(s)
        c.save_data(i) 
    
    print("Generation successful!")
    
def test_all(test_naive=True):
    """ Tests all the test files in the tests/ directory 

        Parameters
        ----------
        test_naive: bool
            Whether or not to test the naive implementation described in the
            reference book
    """
    c = CountingSort()
    p = Path("tests")
    names = p.glob("*.test")
    names = sorted(names)
    for name in names:
        c.read_data(name) # reading could take a long time
        print("Testing {}".format(str(name.name)))
        out = c.sort(c.sort_counting)
        print("{}ms for {} lines of input, avg: {}".format(c.time, len(c.data), c.time/len(c.data)))
        if not c.verify(out):
            print("ERROR: sorting fails at {}".format(name.name))
            exit(1)

        if test_naive:
            out = c.sort(c.sort_naive)
            print("Naive: {}ms for {} lines of input, avg: {}".format(c.time, len(c.data), c.time/len(c.data)))
            if not c.verify(out):
                print("ERROR: sorting fails at {}".format(name.name))
                exit(1)

# READ MEEEEEEE!!!!!
def test_output():
    """ Runs all the tests and prints outputs into files in output/
        THIS IS THE FUNCTION YOU SHOULD RUN
    """
    c = CountingSort()
    method = c.sort_counting # this is our method of choice/final submission method
    p = Path("tests") # a path to all the tests
    names = p.glob("*.test")
    names = sorted(names)
    for name in names:
        print("Testing {}".format(name.name))
        c.read_data(name)
        out = c.sort(method)
        with open("output/{}.out".format(name.stem), "w") as f:
            for outline in c.output(out):
                f.write(outline)
                f.write("\n")

generate_testing_data() # this is very memory-heavy, since the generation process is very inefficient
# test_all(test_naive=True)
test_output()