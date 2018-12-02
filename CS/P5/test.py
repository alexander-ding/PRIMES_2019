from prime_sort import PrimesData, PrimesSort
from pathlib import Path
from collections import defaultdict

def generate_testing_data():
    """ Generate testing data of various lengths
    """
    print("Generating test data")
    c = PrimesSort()
    for i in range(0,10):
        c.generate_data(10000)
        c.save_data("0{}".format(i))
    
    for i in range(10,20):
        c.generate_data(10000, large_prime=True)
        c.save_data(i)
    
    for i in range(20,30):
        c.generate_data(10000, complex_composite=True)
        c.save_data(i)

    for i in range(30,40):
        c.generate_data(10000, large_prime=True, complex_composite=True)
        c.save_data(i)
    
    for i in range(40,50):
        c.generate_data(100000, large_prime=True)
        c.save_data(i)
    
    for i in range(50,60):
        c.generate_data(100000, complex_composite=True)
        c.save_data(i) 

    for i in range(60,70):
        c.generate_data(100000, large_prime=True, complex_composite=True)
        c.save_data(i)
    
    for i in range(70,80):
        c.generate_data(1000000, large_prime=True)
        c.save_data(i)
    
    for i in range(80,90):
        c.generate_data(1000000, complex_composite=True)
        c.save_data(i) 

    for i in range(90,100):
        c.generate_data(1000000, large_prime=True, complex_composite=True)
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
            Whether the result of sorting is verified
        
        files: Union(List(Union(Str, int))), None)
            The files to test. If None, then test all
        
        Returns
        -------
        Dict()
    """
    c = PrimesSort()
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

def test_all_preprocess(test_methods=[], verify=False, files=None):
    """ Tests preprocess functions on files
        Returns the logged time for each test
        and method used

        Parameters
        ----------
        test_methods: List
            List of name of method names to be called
        
        verify: bool
            Whether the result is verified
        
        files: Union(List(Union(Str, int))), None)
            The files to test. If None, then test all
        
        Returns
        -------
        Dict()
    """
    c = PrimesSort()
    if files is None:
        p = Path("tests")
        names = list(p.glob("*.test"))
    else:
        names = [Path("tests/{}.test".format(f)) for f in files]
    names = sorted(names)
    logs = [["size", "name"]+test_methods] # header

    import time
    for name in names:
        c.read_data(name) # reading could take a long time
        print("Testing {}".format(str(name.name)))
        log = [len(c.data), name.name]
        for method_name in test_methods:
            start = time.time()
            for d in c.data:
                method = getattr(d, method_name)
                method()
                if verify:
                    if not d.verify():
                        print("ERROR: {} fails at {}".format(method_name, name.name))
                        exit(1)
            end = time.time()
            delta = (end-start)*1000
            print("{}: {}ms for {} lines of input, avg: {}".format(method_name, delta, len(c.data), delta/len(c.data)))
            log.append(delta)
            if verify:
                print("Checks out")

        logs.append(log)
    
    return logs

# READ MEEEEEEE!!!!!
def test_output():
    """ Runs all the tests and prints outputs into files in output/
        THIS IS THE FUNCTION YOU SHOULD RUN
    """
    c = PrimesSort()
    method = c.sort_counting # this is our method of choice/final submission method
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

generate_testing_data() # this is very memory heavy
# tests = range(30,60)
# log_preprocess = test_all_preprocess(["preprocess_pure_miller", "preprocess_split"], verify=False, files=[str(i).zfill(2) for i in tests])
# log_sort = test_all(["sort_builtin", "sort_counting"], verify=True, files=[str(i).zfill(2) for i in tests])
# print(log_preprocess)
# print(log_sort)
test_output()