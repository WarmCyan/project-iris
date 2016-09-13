class Intelligence:

    Memory = {
            #"self":"[mutate (self)][query (approval)][remember (self) (approval)][self]",

            
            "self":"[print [+ [dequotable \"5\"] [dequotable \"4\"]]]",

            

            # SELF UNIT TESTS

            # NOTE: mapping and graphing
            #"self":"[map (mutate) (MUTATEMAP)][graph (mutate) (MAGRAPH)][print [reconstruct (MUTATEMAP)]][print [value (MAGRAPH)]]",

            # NOTE: getting input
            #"self":"[set (INPUT) [getinput]][print [value (INPUT)]]",

            # NOTE: conditionals
            #"self":"[if [= \"5\" \"6\"] [runnable [concept (print)] [runnable [concept (dequotable)] \"They equal!\"]] [runnable [concept (print)] [runnable [concept (dequotable)] \"They no equal :(\"]]]",

            # NOTE: connection searching
            #"self":"[graph (mutate) (GRAPH)][findconnections_by_type (GRAPH) (mutate) (needs) (RESULTS)][print [value (RESULTS)]]",
            #"self":"[graph (mutate) (GRAPH)][findconnections_by_end (GRAPH) (needs) (referable) (RESULTS)][print [value (RESULTS)]]",

            # NOTE: looping
            #"self":"[loop [dequotable \"0\"] [dequotable \"50\"] [runnable [concept (return)] [runnable [concept (+)] [concat [runnable [concept (value)] [referable [concept (TEMP_LOOP_INDEX)]]] [concat [dequotable \" \"] [runnable [concept (count)] [runnable [concept (count)]]]]]]] [runnable [concept (print)] [runnable [concept (value)] [referable [concept (TEMP_LOOP_INDEX)]]]]]",
            

            # mutate needs:
            #   1. List concepts
            #   2. Choose one randomly
            #   3. Get self string, 
            #   4. Get all base and first level concepts
            #   5. Randomly choose one to modify with the self string


            "mutate":"[-> (needs) (referable)][-> (is) (thing)][print [dequotable \"mutating!\"]]", # theoretically, this needs some kind of way to list all the available concepts.
            "query":"",
            "remember":"",
            "recall":"",

            # BOOLEAN CONCEPTS
            "=":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" == \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "<":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" < \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            ">":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" > \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "<=":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" <= \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            ">=":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" >= \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "!=":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" != \" + str(self.CacheRetrieve(1, -1))), -2)\"]",

            # MATH CONCEPTS
            "-":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" - \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "+":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" + \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "*":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" * \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "/":"[python \"self.CacheStore(eval(str(self.CacheRetrieve(0, -1)) + \" / \" + str(self.CacheRetrieve(1, -1))), -2)\"]",
            "random":"[python \"self.CacheStore(random.randint(int(self.CacheRetrieve(0, -1)), int(self.CacheRetrieve(1, -1))), -2)\"]",

            # LANGUAGE CONCEPTS
            "value":"[python \"self.CacheStore(eval(self.CacheRetrieve(0, -1)), -2)\"]",
            "return":"[python \"self.CacheStore(self.CacheRetrieve(0, -1), -3)\"]",
            "set":"[python \"exec(str(self.CacheRetrieve(0, -1)) + \" = '\" + str(self.CacheRetrieve(1, -1)) + \"'\")\"]", 

            
            "get":"[python \"self.RunConceptGet(self.CacheRetrieve(0, -1));self.CacheStore(self.CacheRetrieve(1, -1), -2)\"]",

            "run":"[python \"self.RunConceptExecute(self.CacheRetrieve(0, -1))\"]", # runs quoted syntax
            "print":"[python \"self.Display(str(self.CacheRetrieve(0, -1)))\"]",
            "getinput":"[python \"self.CacheStore(self.GetInput(), -2)\"]",
            "count":"[python \"if self.CacheRetrieve(0, -1) == None:\n\tself.CacheStore(int(0), -2)\nelse:\n\tself.CacheStore(eval('1+int(self.CacheRetrieve(0, -1))'), -2)\"]", # meta concept to potentially keep!

            "argument":"[python \"if self.CacheRetrieve(0, -1) == None:\n\tself.CacheStore(self.CacheRetrieve(0, -3), -2)\nelse:\n\tself.CacheStore(self.CacheRetrieve(int(self.CacheRetrieve(0, -1)), -3), -2)\"]",


            "concat":"[python \"self.CacheStore(str(self.CacheRetrieve(0, -1)) + str(self.CacheRetrieve(1, -1)), -2)\"]",


            "if":"[python \"if (eval(str(self.CacheRetrieve(0, -1))) == True):self.RunConceptExecute(self.CacheRetrieve(1, -1))\nelif self.CacheRetrieve(2, -1) != None:self.RunConceptExecute(self.CacheRetrieve(2, -1))\"]",

            "length":"[python \"try: self.CacheStore(len(eval(str(self.CacheRetrieve(0, -1))).keys()), -2)\nexcept: self.CacheStore(0, -2)\"]",
            
            "delete":"[python \"exec('del ' + str(self.CacheRetrieve(0, -1)))\"]",


            # META LANGUAGE CONCEPTS
            "concept":"[python \"self.CacheStore(self.GetReferenceName(self.CacheRetrieve(0, -1)), -2)\"]", # gets the the name of the concept of a reference

            "runnable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\"]\\\", -2)\nelse:\n\tself.CacheStore(\\\"[\\\" + self.CacheRetrieve(0, -1) + \\\" \\\" + self.CacheRetrieve(1, -1) + \\\"]\\\", -2)\"]",

            "referable":"[python \"if self.CacheRetrieve(1, -1) == None:\n\tself.CacheStore(\\\"(\\\" + str(self.CacheRetrieve(0, -1)) + \\\")\\\", -2)\nelse:\n\tself.CacheStore(\\\"(\\\" + str(self.CacheRetrieve(0, -1)) + \\\" \\\" + str(self.CacheRetrieve(1, -1)) + \\\")\\\", -2)\"]",

            "quotable":"[python \"self.CacheStore(\\\"'\\\" + str(self.CacheRetrieve(0, -1)) + \\\"'\\\", -2)\"]",

            "dequotable":"[python \"self.CacheStore(str(self.CacheRetrieve(0, -1))[1:-1], -2)\"]",

            # CORE CONCEPTS
            "graph":""+
                "[stack (TEMP_BUILDING_GRAPH_CONCEPT) [argument]]"+
                "[stack (TEMP_BUILDING_GRAPH_LOC) [argument [count [count]]]]"+
                "[python \"self.RunConceptExecute(eval(Core.PeekActuator('TEMP_BUILDING_GRAPH_CONCEPT')), connectionDepth=1, connectionsOnly=True)\"]"+
                "[unstack (TEMP_BUILDING_GRAPH_CONCEPT)]"+
                "[unstack (TEMP_BUILDING_GRAPH_LOC)]",
            
            "map":"[python \"Core.Map()\"]",

            "reconstruct":"[python \"Core.Reconstruct()\"]",

            #"build_array_gettable_additive":""+
                #"[set_quoted (TEMP_BUILD_ARRAY_GETTABLE_LOC) [argument]]"+
                #"[set (TEMP_BUILD_ARRAY_GETTABLE_INDEX) [argument [count [count]]]]"+ #NOTE: OUTDATED
                #"[set (TEMP_BUILD_ARRAY_GETTABLE_ADDITIVE) [argument [count [count [count]]]]]"+ #NOTE: OUTDATED
                #"[return [referable [concept [value (TEMP_BUILD_ARRAY_GETTABLE_LOC)]] [referable [value (TEMP_BUILD_ARRAY_GETTABLE_INDEX)] [referable [value (TEMP_BUILD_ARRAY_GETTABLE_ADDITIVE)]]]]]",

            #"build_array_gettable":""+
                #"[set_quoted (TEMP_BUILD_ARRAY_GETTABLE_LOC) [argument]]"+ #NOTE: OUTDATED
                #"[set (TEMP_BUILD_ARRAY_GETTABLE_INDEX) [argument [count [count]]]]"+ #NOTE: OUTDATED
                #"[return [referable [concept [value (TEMP_BUILD_ARRAY_GETTABLE_LOC)]] [referable [value (TEMP_BUILD_ARRAY_GETTABLE_INDEX)]]]]",

            "array_shift":"[python \"Core.ArrayShift()\"]",

            "stack":"[python \"Core.Stack()\"]",
            "peek":"[python \"Core.Peek()\"]",
            "unstack":"[python \"Core.Unstack()\"]",

            # NOTE: there's going to have to be a way to "name" a loop and have
            # that be part of all the temporary storages, otherwise nested loops
            # will just overwrite eachother
            # arguments to pass in:
            # 0 - number to start at
            # 1 - number to end at
            # 2 - operation for number (THIS IS CODE) [NOTE: this should return something!!!!]
            # 3 - function to run (THIS IS CODE)
            "loop":"[python \"Core.Loop()\"]",

            # concept map testing 
            # TODO: find a way to pass in get reference hierarchy as reference
            # to graph location
            # TODO: or potentially find a way to post-add to a reference chain?
            # NOTE: assumes that TEMP_BUILDING_GRAPH_LOC is a REFERENCE to graph (NOTE: unfortunately this only takes base level concepts....)
            # concept and TEMP_BUILDING_GRAPH_CONCEPT is the LITERAL CONCEPT
            # NAME that we're adding the connection properties to 
            "->":"[python \"Core.Connection()\"]",

            "findconnections_by_type":"[python \"Core.FindConnectionsByType()\"]",
            "findconnections_by_end":"[python \"Core.FindConnectionsByEnd()\"]",

            #"construct_random":""+
                #"[set_quoted (TEMP_CONSTRUCT_CONCEPT_NAME) [argument]]"+
                #"[set_quoted (TEMP_CONSTRUCT_GRAPH) [argument [count [count]]]]"+
                #"[findconnections_by_type [value (TEMP_CONSTRUCT_GRAPH)] [get [referable [value (TEMP_CONSTRUCT_CONCEPT_NAME)]]] (needs) (TEMP_CONSTRUCT_RESULTS_NEEDS)]",



            
            # TESTING CONCEPTS
            "depth":"[python \"self.CacheStore(self.level - 1, -2)\"]", # this returns the level of the CONCEPT THAT CALLED IT

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

        # NOTE: you can TOTALLY do an eval statement and run [] keys on said
        # statement
