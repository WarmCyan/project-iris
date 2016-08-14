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
            "self":"[set (INPUT) [quotable [getinput]]][set [run [runnable [concept (return)] [referable [value (INPUT)]]]] [quotable [runnable [concept (print)] [referable [concept (Nathan)]]]]][print [value (Nathan)]]",

            
            "mutate":"",
            "query":"",
            "remember":"",
            "recall":"",
            #"memory":"[python \"self.CacheStore(self.entity.Memory, -2)\"]",

            # CORE CONCEPTS
            "value":"[python \"self.CacheStore(eval(self.CacheRetrieve(0, -1)), -2)\"]",
            "argument":"[python \"self.CacheStore(self.CacheRetrieve(0, -3), -2)\"]",
            "return":"[python \"self.CacheStore(self.CacheRetrieve(0, -1), -3)\"]",
            "set":"[python \"exec(self.CacheRetrieve(0, -1) + \" = \" + self.CacheRetrieve(1, -1))\"]",
            "run":"[python \"self.RunConceptExecute(self.CacheRetrieve(0, -1))\"]", # runs quoted syntax
            "print":"[python \"print(self.CacheRetrieve(0, -1))\"]",
            "getinput":"[python \"self.CacheStore(raw_input('Intelligence requested input: '), -2)\"]",

            # META CORE
            "concept":"[python \"self.CacheStore(self.GetReferenceName(self.CacheRetrieve(0, -1)), -2)\"]", # gets the the name of the concept of a reference
            #"runnable":"[python \"self.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\"]\\\", -2)\"]", # TODO: need to expand this to be able to construct arguments as well (2nd argument could be the argument string, so we get the same functional structyure thing

            "runnable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\"]\\\", -2)\nelse:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\" \\\" + self.CacheRetrieve(1, -1) + \\\"]\\\", -2)\"]",

            "referable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"(\\\" + self.CacheRetrieve(0, -1) + \\\")\\\", -2)\nelse:\n\tself.CacheStore(\\\"(\\\" + self.CacheRetrieve(0, -1) + \\\" \\\" + self.CacheRetrieve(1, -1) + \\\")\\\", -2)\"]",

            "quotable":"[python \"self.CacheStore(\\\"'\\\" + self.CacheRetrieve(0, -1) + \\\"'\\\", -2)\"]",



            # future concepts:
            # break concept (stops current concept)


            # concept map testing 
            "connection":"",
            "depth":"[python \"self.CacheStore(self.level - 1, -2)\"]", # this returns the level of the CONCEPT THAT CALLED IT
            
            #"concept1":"


            # TESTING CONCEPTS

            #"runvalue":"[set (TEMP) [argument]][return [run [value (TEMP)]]]",
            "runvalue":"[set (TEMP) [argument]][return [run [value (TEMP)]]]",
            "printsafe":"[python \"print(\\\"Hello world!\\\")\"]",


            "approval":"0",
            "dictionary":{
                "a":"hello world!!!!",
                "b":"I'M ANOTHER THING!!"
                },
            "memory":"[return (print)]",
            "test":"[return (memory)]"
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
        
