class IRIS:
    

    memory = {}

    numSets = 0
    numGets = 0
    numExecutions = 0
    
    def __init__(self):
        self.numSets = 0
        self.numGets = 0
        self.numExecutions = 0

    def printStats(self):
        print("\n\n\tSets:\t\t" + str(self.numSets))
        print("\tGets:\t\t" + str(self.numGets))
        print("\tExecutions:\t" + str(self.numExecutions))

    def tryReturnGet(self, query):
        if str(query).endswith("*"):
            return self.get(query)
        return query

    # TODO - any query surrounded in '' enforces literal
    def get(self, query):
        self.numGets += 1
        #print("attempting to get '" + str(query) + "'...") # DEBUG
        # check if just the concept, not getting in it
        if "*" not in str(query): 
            #if "/" in str(query):
                #parts = str(query).split("/")
                ##return parts[len(parts) - 1]
                #return self.tryReturnGet(parts[len(parts) - 1])
            ##return query
            return self.tryReturnGet(query)

        query = str(query).replace("*", "")

        # check if just a simple thing
        #if query in self.memory.keys(): return self.memory[query]
        if query in self.memory.keys(): return self.tryReturnGet(self.memory[query])

        # break up structure
        if "/" in str(query):
            parts = str(query).split("/")
            result = self.memory

            index = 0
            for part in parts:
                # try to convert to number (for array)
                try: part = int(part)
                except ValueError: pass

                if index == len(parts) - 1:
                    result = result[part]
                    break

                index += 1
                
                result = result[part]
            #return result
            return self.tryReturnGet(result)

    def set(self, query, obj):
        self.numSets += 1
        #print("Setting '" + str(query) + "' to '" + str(obj) + "'...") # DEBUG
        # break up structure
        if "/" in str(query):
            parts = str(query).split("/")
            slot = self.memory

            # construct non-existant parts
            for i in range(0, len(parts) - 1):
                part = parts[i]

                try: slot[part]
                except KeyError:
                    # check next one
                    number = False
                    try: 
                        parts[i+1] = int(parts[i+1]) 
                        number = True
                        slot[part] = []
                    except ValueError: 
                        slot[part] = {}
                except IndexError:
                    # check next one
                    number = False
                    try: 
                        parts[i+1] = int(parts[i+1]) 
                        number = True
                        slot.append([])
                    except ValueError: 
                        slot.append({})
                    

                slot = slot[part]
                    
            # final part
            finalPart = parts[len(parts) - 1]
        
            number = False
            try: finalPart = int(finalPart); number = True
            except ValueError: pass

            if number and number >= len(slot): slot.append(obj)
            else: slot[finalPart] = obj 
            
        else:
            self.memory[query] = obj


    def execute(self, instruction):
        self.numExecutions += 1
        #print("Executing '" + str(instruction) + "'...") # DEBUG
        if instruction[0] == "python": 
            #print("executing python " + str(instruction[1])) # DEBUG
            exec(instruction[1]);
            return
        
        # set current instruction and arguments
        self.set("&", instruction)
        self.set("@", instruction[1:])

        # set current instruction arguments
        instructionContents = self.get(instruction[0] + "*")
        for i in range(0, len(instructionContents)):
            # set argument counter
            self.set("#", i)
            self.execute(instructionContents[i])


    def importthing(self):
        import modules.math
        #print(str(dir(modules.math)))
        for thing in dir(modules.math):
            if not thing.startswith("__"):
                print(str(thing))
            exec("self." + str(thing) + " = modules.math." + str(thing))
        #self.plus(self)
