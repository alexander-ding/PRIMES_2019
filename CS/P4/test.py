# P4
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Run me under the folder of this particular problem
# Provides test functions

from string_sort import StringData, StringSort
from pathlib import Path
from collections import defaultdict

def generate_testing_data():
    """ Generate testing data of various lengths
    """
    print("Generating test data")
    c = StringSort()
    for i in range(0,10):
        c.generate_data(10)
        c.save_data("0{}".format(i))
    
    for i in range(10,20):
        c.generate_data(100)
        c.save_data(i)
    
    for i in range(20,30):
        c.generate_data(1000)
        c.save_data(i)

    for i in range(30,40):
        c.generate_data(10000)
        c.save_data(i)
    
    for i in range(40,50):
        c.generate_data(100000)
        c.save_data(i)
    
    for i in range(50,60):
        c.generate_data(1000000)
        c.save_data(i) 

    for i in range(60,70):
        c.generate_data(10000000)
        c.save_data(i)
    print("Generation successful!")

def test_all(test_methods=[], verify=False, files=None):
    """ Tests all the test files in the tests/ directory 
        Returns the logged time for each test
        and method used

        Parameters
        ----------
        test_methods: List
            List of name of method names to be called
        
        verify: bool
            Whether the code should verify the result of the sorting
        
        files: Union(List(Union(Str, int))), None)
            The files to test. If None, then test all
        
        Returns
        -------
        Dict()
    """
    c = StringSort()
    if files is None:
        p = Path("tests")
        names = list(p.glob("*.test"))
    else:
        names = [Path("tests/{}.test".format(f)) for f in files]
    names = sorted(names)
    logs = [["size", "name"]+test_methods] # header
    for name in names:
        c.read_data(name) # reading could take a long time
        print("Testing {}".format(str(name.name)))
        log = [len(c.data), name.name]
        for method_name in test_methods:
            method = getattr(c, method_name)
            out = c.sort(method)
            print("{}: {}ms for {} lines of input, avg: {}".format(method_name, c.time, len(c.data), c.time/len(c.data)))
            log.append(c.time)
            if verify:
                if not isinstance(out, list):
                    out = list(out)
                if not c.verify(out):
                    print("ERROR: sorting fails at {}".format(name.name))
                    exit(1)
                else:
                    print("Checks out")
        logs.append(log)
    
    return logs

def write_logs(out, logs):
    import csv
    with open(out, "w") as f:
        w = csv.writer(f, "excel")
        for log in logs:
            w.writerow(log)

# READ MEEEEEEE!!!!!
def test_output():
    """ Runs all the tests and prints outputs into files in output/
        THIS IS THE FUNCTION YOU SHOULD RUN
    """
    c = StringSort()
    method = c.sort_combined # this is our method of choice/final submission method
    p = Path("tests")
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

generate_testing_data() # this generates testing data. Takes a long time

# logs = test_all(["sort_builtin", "sort_bins", "sort_combined"], True, [str(i).zfill(2) for i in range(61)]) # test different methods for the fastest
# write_logs("logs/time.csv", logs) # log the times of each method tested

test_output() # put files in directory tests and run this to test