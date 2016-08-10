
class Intelligence:

    Memory = {
            #"self":"[mutate (self)][query (approval)][remember (self) (approval)][self]",
            #"self":"[print [memory]]",
            #"self":"[print [value (memory)]]",
            #"self":"[print (dictionary (a))]",
            #"self":"[print [value (dictionary (b))]]",
            #"self":"[print [value [test]]]",

            #"self":"[print [run [value [test]]]]",
            #"self":"[print [run [value (memory)]]]]",
            #"self":"[print [value [run [value (memory)]]]]",
            #"self":"[print [value [memory]]]",
            "self":"[print [value [run [value [test]]]]]",
            #"self":"[print [value (print)]]",
            

            "mutate":"",
            "query":"",
            "remember":"",
            "recall":"",
            #"memory":"[python \"self.CacheStore(self.entity.Memory, -2)\"]",
            "memory":"[return (print)]",
            #"print":"[python \"print(self.CacheRetrieve(0))\"]",
            "print":"[python \"print(self.CacheRetrieve(0, -1))\"]",

            "value":"[python \"self.CacheStore(eval(self.CacheRetrieve(0, -1)), -2)\"]",
            "argument":"[python \"self.CacheStore(self.CacheRetrieve(0, -3), -2)\"]",
            "return":"[python \"self.CacheStore(self.CacheRetrieve(0, -1), -3)\"]",
            "set":"[python \"exec(self.CacheRetrieve(0, -1) + \" = \" + self.CacheRetrieve(1, -1))\"]",
            "run":"[python \"self.RunConceptExecute(self.CacheRetrieve(0, -1))\"]",



            "approval":"0",
            "dictionary":{
                "a":"hello world!!!!",
                "b":"I'M ANOTHER THING!!"
                },

            "test":"[return (memory)]"
            }


    # 2: [print "THING"] //thing is arg level 2
    # 3: [python etc etc, needs to get level above it


# issue:
#
# need to be able to EXECUTE concepts 
# need to be able to GET THE CONTENT of concepts 
# need to be able to GET THE REFERENCE to concepts

# [] can execute executable concepts
# () gets the content of concepts
# {} gets a reference to concepts (self.entity.Memory["KEY"])


# questions:
# [] for nonexecutable concepts? Same as ()?



# instead:
# () gets a reference to concepts, and {} gets a literal to it in the very rare
# instances it's necessary?

# NOTE: if you have a QUOTED REFERENCE TO SOMETHING, you can get the VALUE of
# that something with 
# eval(referenceString)
#
# you can SET the value of that REFERENCE by using 
# exec(referenceString + " = [VALUE]")



# (self) stores "self.entity.Memory["self"]" in the cache


# [set (recall) (memory)]

# (recall)
#   () tell platform to store "self.entity.Memory["recall"]" in cache 0
#
# (memory)
#   () tell platform to store "self.entity.Memory["memory"]" in cache 1
#
# [set]
#   [python "exec(


    def TestReferences(self):
        x = { "thing":13 }
        print(x) # {'thing':13}
        print(str(x["thing"])) # 13
        reference = "x[\"thing\"]"
        print(reference) # 'x["thing"]'
        print(eval(reference)) # 13
        exec(reference + " = 14")
        print(eval(reference)) # 14
        
