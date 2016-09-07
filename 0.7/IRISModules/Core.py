platform = None #NOTE: this is the convention, so that every module can use the platform!

def Test():
    print("Hello world!")

def Stack():
    StackActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1))

def Peek():
    platform.CacheStore(PeekActuator(platform.CacheRetrieve(0, -1)), -2)

def Unstack():
    UnstackActuator(platform.CacheRetrieve(0, -1))

def Loop():
    LoopActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1), platform.CacheRetrieve(2, -1), platform.CacheRetrieve(3, -1))


# creates a STACK_ string from the literal concept name 
# returns the evaluated memory reference
def BuildStackNameFromConcept(conceptName):
    concept = str("self.entity.Memory[\"STACK_" + conceptName + "\"]")
    return EnsureRetrieveMemory(concept)

# return the actual memory reference for the string, and if it didn't exist,
# initialize it to an empty dictionary
def EnsureRetrieveMemory(memoryReferenceString):
    # make sure the memory slot exists
    try: platform.Evaluator(memoryReferenceString)
    except: platform.Executor(memoryReferenceString + " = {}")

    # get the memory reference and return it
    conceptMem = platform.Evaluator(memoryReferenceString)
    return conceptMem

# pass in either a memory reference string or a concept name, and it returns
# ONLY a concept name NOTE: this doesn't work with subconcepts
def ResolveNameFromMemoryOrConcept(string):
    if string.startswith("self.entity.Memory"):
        conceptName = platform.GetReferenceName(string)
    else:
        conceptName = string
    return conceptName

# a verbatim concept name string should ONLY be passed in by other literal
# python code, not IRIS code
# value is the LITERAL VALUE STORED.
def StackActuator(stackConcept, value):
    conceptName = ResolveNameFromMemoryOrConcept(stackConcept)
    conceptMem = BuildStackNameFromConcept(conceptName)
    length = len(conceptMem.keys())
    conceptMem[str(length)] = value

def PeekActuator(stackConcept):
    conceptName = ResolveNameFromMemoryOrConcept(stackConcept)
    conceptMem = BuildStackNameFromConcept(conceptName)
    length = len(conceptMem.keys())
    return conceptMem[str(length - 1)]

def UnstackActuator(stackConcept):
    conceptName = ResolveNameFromMemoryOrConcept(stackConcept)
    conceptMem = BuildStackNameFromConcept(conceptName)
    length = len(conceptMem.keys())
    del conceptMem[str(length - 1)]

# index: number to start at
# end: number to stop the loop at
# operationCode: literal string of code to run to change index
# runCode: literal string of code to run every loop
def LoopActuator(index, end, operationCode, runCode):
    while (str(index) != str(end)):
        platform.entity.Memory["TEMP_LOOP_INDEX"] = index
        platform.RunConceptExecute(runCode)
        #platform.entity.Memory["TEMP_LOOP_INDEX"] = index
        platform.RunConceptExecute(operationCode)
        #index = platform.entity.Memory["TEMP_LOOP_INDEX_TEMP"]
        index = platform.CacheRetrieve(0, -2)
