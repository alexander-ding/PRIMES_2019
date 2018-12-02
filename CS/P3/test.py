# P3
# Python 3.6, Fancy Text Editor (aka Visual Studio Code), Mac
# Run me under the folder of this particular problem
# Provides test functions

from student_sort import StudentSort, StudentData
from pathlib import Path

def generate_testing_data():
    """ Generate testing data of various lengths
    """
    print("Generating test data")
    c = StudentSort()
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
    
    for i in range(40,45):
        c.generate_data(100000)
        c.save_data(i)
    
    for i in range(45,50):
        c.generate_data(1000000)
        c.save_data(i) 

    for i in range(50,51):
        c.generate_data(10000000)
        c.save_data(i)
    print("Generation successful!")
    
def test_all(test_methods=[], verify=False):
    """ Tests all the test files in the tests/ directory 

        Parameters
        ----------
        test_methods: List
            List of name of method names to be called
        
        verify: bool
            Whether the code should verify the result of the sorting
    """
    c = StudentSort()
    p = Path("tests")
    names = p.glob("*.test")
    names = sorted(names)
    for name in names:
        c.read_data(name) # reading could take a long time
        print("Testing {}".format(str(name.name)))
        for method_name in test_methods:
            method = getattr(c, method_name)
            out = c.sort(method)
            print("{}: {}ms for {} lines of input, avg: {}".format(method_name, c.time, len(c.data), c.time/len(c.data)))
            if verify:
                if not isinstance(out, list):
                    out = list(out)
                if not c.verify(out):
                    print("ERROR: sorting fails at {}".format(name.name))
                    exit(1)
                else:
                    print("Checks out")

# READ MEEEEEEE!!!!!
def test_output():
    """ Runs all the tests and prints outputs into files in output/
        THIS IS THE FUNCTION YOU SHOULD RUN
    """
    c = StudentSort()
    method = c.sort_builtin # this is our method of choice/final submission method
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

generate_testing_data() # this is very memory-heavy, since the generation process is very inefficient
#test_all(["sort_merge", "sort_radix_1", "sort_radix_3", "sort_builtin"], verify=False)
test_output()