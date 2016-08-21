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
            #"self":"[print [value [run [value [test]]]]]",
            #"self":"[print [value (print)]]",
            
            #"self":"[set (THING) \"thing\"][print [value (THING)]]",
            #"self":"[print [value [runvalue (memory)]]]",
            #"self":"[print [runvalue (memory)]]]",
            #"self":"[set (THING (THING1)) \"yes\"][print [value (THING (THING1))]]",
            #"self":"[set (THING (THING1 (THING3))) (self)][print [value (THING (THING1 (THING3)))]]",
            
            #"self":"[print [concept (self)]]",
            #"self":"[print [runnable [concept (self)] [runnable [concept (mutate)]]]]",
            #"self":"[print [runnable [concept (mutate)] [referable [concept (self)]]]]",
            #"self":"[print [runnable \"YEAH\"]]", # TODO: THIS DOESN'T WORK. MAKE THIS WORK.

            #"self":"[print [run [runnable [concept (test)]]]]", # TODO: THIS DOESN'T WORK, (because of extra level), unsure if this SHOULD work or not # NOTE: made it work below, just have to make the runnable include a return concept
            #"self":"[print [run [value [run [value [run [runnable [concept (return)] [referable [concept (test)]]]]]]]]",
            #"self":"[print [run [value [run [value [run [runnable [concept (return)] [referable [concept (test)]]]]]]]]]",


            #"self":"[print [value [run [value [run [value [run [runnable [concept (return)] [referable [concept (test)]]]]]]]]]]", # FREAKING 11 LEVELS DEEP


            #"self":"[set (THING) [quotable [runnable [concept (mutate)] [referable [concept (self)]]]]][print [value (THING)]]", # NOTE: amazing meta powers ACTIVATE!!!!!!!!!!!!!!!
            #"self":"[print [quotable [concept (self)]]]",

            #"self":"[set (INPUT) [quotable [getinput]]][print [value (INPUT)]]",
            #"self":"[set (INPUT) [quotable [getinput]]][set [run [runnable [concept (return)] [referable [value (INPUT)]]]] [quotable [runnable [concept (print)] [referable [concept (Nathan)]]]]][print [value (Nathan)]]",

            #"self":"[print [value (runvalue)]]",
            #"self":"[print [runnable [concept (return)] [referable [concept (levelOne)] [referable [concept (levelTow)]]]]]",

            #"self":"[print [count [count [count [count [count]]]]]]",

            #"self":"[print [test2 \"hello world!\" \"Idk why you say hello, I say goodbye\"]]",

            #"self":"[set (THING1) (self)][set_quoted (THING2) (self)][print [value (THING1)]][print [value (THING2)]]",

            #"self":"[map_concept [concept (self)]][print [value (TEMP_ARG_0)]][print [value (CONCEPT_MAP)]]",
            #"self":"[print [value [run [runnable [concept (return) [referable [concept (self)]]]]]]]",
            #"self":"[print [value [get [referable [concept (self)]]]]]",
            "self":"[print [get [referable [concept (self)]]]]",
    

            
            # TODO: sincerely think about making current set "copy" and set_quoted the actual set? 
            # NOTE: ^ if you think about it, it makes more sense to just have a
            # set_quoted, because you can get the value of a differnet concept
            # if its needed, otherwise, just store string OF THE REFERENCE. Then
            # you get the best of both worlds! (but still like the copy idea)


            # mutate needs:
            #   1. List concepts
            #   2. Choose one randomly
            #   3. Get self string, 
            #   4. Get all base and first level concepts
            #   5. Randomly choose one to modify with the self string


            
            "mutate":"", # theoretically, this needs some kind of way to list all the available concepts.
            "query":"",
            "remember":"",
            "recall":"",

            # CORE CONCEPTS
            "value":"[python \"self.CacheStore(eval(self.CacheRetrieve(0, -1)), -2)\"]",
            "return":"[python \"self.CacheStore(self.CacheRetrieve(0, -1), -3)\"]",
            "set":"[python \"exec(self.CacheRetrieve(0, -1) + \" = \" + self.CacheRetrieve(1, -1))\"]",

            "set_quoted":"[python \"exec(self.CacheRetrieve(0, -1) + \" = '\" + self.CacheRetrieve(1, -1) + \"'\")\"]", # NOTE: this is because if something is passed as an argument, impossible to quote what's there (quotable doesn't work, because argument is a sublevel deep) # TODO: find a better way of doing this!!!

            
            "get":"[python \"self.RunConceptGet(self.CacheRetrieve(0, -1));self.CacheStore(self.CacheRetrieve(1, -1), -2)\"]",

            "run":"[python \"self.RunConceptExecute(self.CacheRetrieve(0, -1))\"]", # runs quoted syntax
            "print":"[python \"print(self.CacheRetrieve(0, -1))\"]",
            "getinput":"[python \"self.CacheStore(raw_input('Intelligence requested input: '), -2)\"]",
            "count":"[python \"if self.CacheRetrieve(0, -1) == None:\n\tself.CacheStore(int(0), -2)\nelse:\n\tself.CacheStore(eval('1+int(self.CacheRetrieve(0, -1))'), -2)\"]", # meta concept to potentially keep!
            "argument":"[python \"if self.CacheRetrieve(0, -1) == None:\n\tself.CacheStore(self.CacheRetrieve(0, -3), -2)\nelse:\n\tself.CacheStore(self.CacheRetrieve(int(self.CacheRetrieve(0, -1)), -3), -2)\"]",

            # META CORE
            "concept":"[python \"self.CacheStore(self.GetReferenceName(self.CacheRetrieve(0, -1)), -2)\"]", # gets the the name of the concept of a reference

            "runnable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\"]\\\", -2)\nelse:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\" \\\" + self.CacheRetrieve(1, -1) + \\\"]\\\", -2)\"]",

            "referable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"(\\\" + self.CacheRetrieve(0, -1) + \\\")\\\", -2)\nelse:\n\tself.CacheStore(\\\"(\\\" + self.CacheRetrieve(0, -1) + \\\" \\\" + self.CacheRetrieve(1, -1) + \\\")\\\", -2)\"]",

            "quotable":"[python \"self.CacheStore(\\\"'\\\" + self.CacheRetrieve(0, -1) + \\\"'\\\", -2)\"]",

            # META META CORE NOTE: these may have dependencies!
            
            #"map_concept":"[set (TEMP_ARG_0) [argument]][set (TEMP_MAP_CONCEPT) [value [value (TEMP_ARG_0)]]]",
            #"map_concept":"[set (TEMP_ARG_0) [argument]][set (TEMP_MAP_CONCEPT) [quotable [value (TEMP_ARG_0)]]]",
            "map_concept":"[set_quoted (TEMP_ARG_0) [argument]][set (TEMP_MAP_CONCEPT) [quotable [value (TEMP_ARG_0)]]]",


            # future concepts:
            # break concept (stops current concept)


            # concept map testing 
            "connection":"",
            "depth":"[python \"self.CacheStore(self.level - 1, -2)\"]", # this returns the level of the CONCEPT THAT CALLED IT
            
            # TESTING CONCEPTS

            "runvalue":"[set (TEMP) [argument]][return [run [value (TEMP)]]]",
            "printsafe":"[python \"print(\\\"Hello world!\\\")\"]",


            "approval":"0",
            "dictionary":{
                "a":"hello world!!!!",
                "b":"I'M ANOTHER THING!!"
                },
            "memory":"[return (print)]",
            "test":"[return (memory)]",

            "test2":"[set (TEMP) [argument [count [count]]]][return [quotable [value (TEMP)]]]"




            # OLD CONCEPTS

            #"runnable":"[python \"self.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\"]\\\", -2)\"]", # TODO: need to expand this to be able to construct arguments as well (2nd argument could be the argument string, so we get the same functional structyure thing
            #"argument":"[python \"self.CacheStore(self.CacheRetrieve(0, -3), -2)\"]",
            #"memory":"[python \"self.CacheStore(self.entity.Memory, -2)\"]",

            
            }



    def TestReferences(self):
        x = { "thing":13 }
        print(x) # {'thing':13}
        print(str(x["thing"])) # 13
        reference = "x[\"thing\"]"
        print(reference) # 'x["thing"]'
        print(eval(reference)) # 13
        exec(reference + " = 14")
        print(eval(reference)) # 14
        




# arg0: the name of the concept to map
#
#
# [set (TEMP_ARG_0) [argument]][set (TEMP_MAP_CONCEPT) [value (TEMP_ARG_0)]]
#def METAMapConcept(self):
#   conceptList = self.ParseConcepts(self.entity.Memory["TEMP_MAP_CONCEPT"])
#   self.entity.Memory["CONCEPT_MAP"] = {}
#   index = 0
#   for concept in conceptList:
#       indexString = str(index)
#       self.entity.Memory["CONCEPT_MAP"][indexString] = {}
#       self.entity.Memory["CONCEPT_MAP"][indexString]["concept"] = self.entity.Memory["TEMP_ARG_0"] # the argument, which should be the name of the concept

#       # create a straight string of the args TODO: maybe later find a way to make
#       # this a recursive structure like it would be anyway?
#       argsString = ""
#       for argument in concept[1]:
#           argsString += " " + str(argument)
#       
#       self.entity.Memory["CONCEPT_MAP"][indexString]["args"] = argsString

