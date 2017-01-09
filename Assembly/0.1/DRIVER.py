from test import IRIS

import time

instance = IRIS()

#print(str(instance.memory))



#instance.set("test/yeah", "thing")
#print(instance.get("test/yeah*"))

#instance.set("array0/0", "thing1")
#instance.set("array0/1", "thing2")

#print(instance.get("test/yeah"))
#print(instance.get("test/yeah*"))
#print(instance.get("array0/0*"))

#print(str(instance.memory))

def timeTests():

    assignment0 = time.clock()
    for i in range(0, testAmount):
        instance.set("test0", "hello there!")
    assignment0time = time.clock() - assignment0

    print("simple assignment = \t\t\t" + str(assignment0time))

    assignment1 = time.clock()
    for i in range(0, testAmount):
        instance.set("test1/yes", "thing")
    assignment1time = time.clock() - assignment1

    print("complex dictionary assignment = \t" + str(assignment1time))

    assignment2 = time.clock()
    for i in range(0, testAmount):
        instance.set("test2/0", "thing")
    assignment2time = time.clock() - assignment2

    print("complex array assignment = \t\t" + str(assignment2time))

    get0 = time.clock()
    for i in range(0, testAmount):
        instance.get("test0*")
    get0time = time.clock() - get0

    print("\nsimple get = \t\t\t\t" + str(get0time))

    get1 = time.clock()
    for i in range(0, testAmount):
        instance.get("test1/yes*")
    get1time = time.clock() - get1

    print("complex dictionary get = \t\t" + str(get1time))

    get2 = time.clock()
    for i in range(0, testAmount):
        instance.get("test2/0*")
    get2time = time.clock() - get2

    print("complex array get = \t\t\t" + str(get2time))

    control0set = time.clock()
    for i in range(0, testAmount):
        instance.memory["test0"] = "nope"
    control0settime = time.clock() - control0set

    print("\ncontrol set = \t\t\t\t" + str(control0settime))

    control1set = time.clock()
    for i in range(0, testAmount):
        instance.memory["test1"]["yes"] = "maybe"
    control1settime = time.clock() - control1set

    print("control complex set = \t\t\t" + str(control1settime))

    control0get = time.clock()
    for i in range(0, testAmount):
        instance.memory["test0"]
    control0gettime = time.clock() - control0get

    print("\ncontrol get = \t\t\t\t" + str(control0gettime))

    control1get = time.clock()
    for i in range(0, testAmount):
        instance.memory["test1"]["yes"]
    control1gettime = time.clock() - control1get

    print("control complex get = \t\t\t" + str(control1gettime))

# initial test instruction
instance.set("print", [["python", "# print\nprint(self.get(\"@/0*\"))"]])

instance.execute(["print", "hello"])
