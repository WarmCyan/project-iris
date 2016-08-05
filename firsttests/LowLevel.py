import sys

debug = False

def WritePythonFile(filename, contents):
    if debug:
        print("LL> Writing python file '" + filename + ".py'...")

    outfile = open(filename + ".py", 'w')
    outfile.write(contents)
    outfile.close()

    if debug:
        print("LL> Complete!") 

def ExecutePythonFile(name):
    #erase module from system
    if name in sys.modules:
        if debug:
            print("LL> Removing module '" + name + "'...")
        del sys.modules[name]

    #import it
    if debug:
        print("LL> Importing module '" + name + "'...")
    __import__(name)
