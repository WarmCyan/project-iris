platform = None #NOTE: this is the convention, so that every module can use the platform!

def Stack():
    StackActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1))

def Peek():
    platform.CacheStore(PeekActuator(platform.CacheRetrieve(0, -1)), -2)

def Unstack():
    UnstackActuator(platform.CacheRetrieve(0, -1))

def Loop():
    LoopActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1), platform.CacheRetrieve(2, -1), platform.CacheRetrieve(3, -1))

def Map():
    MapActuator(platform.Evaluator(platform.CacheRetrieve(0, -1)), platform.CacheRetrieve(1, -1))

def Connection():
    argumentWeight = platform.CacheRetrieve(2, -1)
    if argumentWeight != None: 
        argumentWeight = argumentWeight.strip("\"")
        weight = float(argumentWeight)
    else: weight = 1.0
    print("WEIGHT: " + str(weight))
    ConnectionActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1), weight)   

def Reconstruct():
    platform.CacheStore(ReconstructActuator(platform.CacheRetrieve(0, -1)), -2)

def ArrayShift():
    ArrayShiftActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1))

def FindConnectionsByType():
    FindConnectionsByTypeActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1), platform.CacheRetrieve(2, -1), platform.CacheRetrieve(3, -1))

def FindConnectionsByEnd():
    FindConnectionsByEndActuator(platform.CacheRetrieve(0, -1), platform.CacheRetrieve(1, -1), platform.CacheRetrieve(2, -1), platform.CacheRetrieve(3, -1))

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

# =================================================================================
# STACKING
# =================================================================================

# creates a STACK_ string from the literal concept name 
# returns the evaluated memory reference
def BuildStackNameFromConcept(conceptName):
    concept = str("self.entity.Memory[\"STACK_" + conceptName + "\"]")
    return EnsureRetrieveMemory(concept)

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

# =================================================================================
# LOOPING
# =================================================================================

# index: number to start at
# end: number to stop the loop at
# operationCode: literal string of code to run to change index
# runCode: literal string of code to run every loop
def LoopActuator(index, end, operationCode, runCode):
    while (str(index) != str(end)):
        platform.entity.Memory["TEMP_LOOP_INDEX"] = index
        platform.RunConceptExecute(runCode)
        platform.RunConceptExecute(operationCode)
        index = platform.CacheRetrieve(0, -2)

# =================================================================================
# ARRAYS
# =================================================================================

def ArrayShiftActuator(memoryReferenceString, index):
    arrayMem = platform.Evaluator(memoryReferenceString)
    
    length = len(arrayMem.keys())

    for i in range(length, index - 1, -1):
        if i == index:
            platform.Executor(memoryReferenceString + "['" + str(i) + "'] = ''")
        else:
            platform.Executor(memoryReferenceString + "['" + str(i) + "'] = " + memoryReferenceString + "['" + str(int(i-1)) + "']")

# =================================================================================
# MAPPING
# =================================================================================

def MapActuator(conceptString, memoryReferenceString):
    #mapMem = platform.Evaluator(memoryReferenceString)
    mapMem = EnsureRetrieveMemory(memoryReferenceString)
    conceptList = platform.ParseConcepts(conceptString)

    #mapMem = {}
    index = -1
    for concept in conceptList:
        index += 1
        indexString = str(index)
        mapMem[indexString] = {}
        mapMem[indexString]["concept"] = concept[0]

        # create a straight string of the args TODO: maybe later find a way to make
        # this a recursive structure like it would be anyway?
        argsString = ""
        for argument in concept[1]:
            argsString += " " + str(argument)

        # trim extra space at beginning
        argsString = argsString[1:]
        mapMem[indexString]["args"] = argsString

def ReconstructActuator(memoryReferenceString):
    mapMem = platform.Evaluator(memoryReferenceString)
    
    conceptString = ""
    for indexKey in mapMem:
        conceptString += "[" + mapMem[indexKey]["concept"] 
        argsString = mapMem[indexKey]["args"]
        if argsString != "":
            conceptString += " " + argsString
        conceptString += "]"
    
    return conceptString

# =================================================================================
# GRAPHING
# =================================================================================

def CheckIfConnectionInGraph(reftype, startConcept = "", typeConcept = "", endConcept = "", conceptMem=None):
    for indexKey in conceptMem:
        connectionData = conceptMem[indexKey]
        if reftype != connectionData["reftype"]: continue
        
        if reftype == "direct":
            if typeConcept != connectionData["type"]: continue
            if endConcept != connectionData["end"]: continue
        elif reftype == "descriptor":
            if startConcept != connectionData["start"]: continue
            if endConcept != connectionData["end"]: continue
        elif reftype == "indirect":
            if startConcept != connectionData["start"]: continue
            if typeConcept != connectionData["type"]: continue

        # passed all tests and still here, we must have found a match
        return True

    return False

# NOTE: requires TEMP_BUILDING_GRAPH_LOC and TEMP_BUILDING_GRAPH_CONCEPT stack to be set (both of which should be reference strings)
def ConnectionActuator(connectionTypeReferenceString, connectionEndReferenceString, weight=1.0):
    connectionTypeConcept = platform.GetReferenceName(connectionTypeReferenceString)
    connectionEndConcept = platform.GetReferenceName(connectionEndReferenceString)
    connectionStartConcept = platform.GetReferenceName(PeekActuator("TEMP_BUILDING_GRAPH_CONCEPT"))
    baseGraphReferenceString = PeekActuator("TEMP_BUILDING_GRAPH_LOC")

    graphMem = EnsureRetrieveMemory(baseGraphReferenceString)
    startMem = EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionStartConcept + "']")
    typeMem = EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionTypeConcept + "']")
    endMem = EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionEndConcept + "']")

    # direct connection
    if not CheckIfConnectionInGraph("direct", endConcept=connectionEndConcept, typeConcept=connectionTypeConcept, conceptMem=startMem):
        newIndex = str(len(startMem.keys()))
        EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionStartConcept + "']['" + newIndex +"']")
        startMem[newIndex]["reftype"] = "direct"
        startMem[newIndex]["type"] = connectionTypeConcept
        startMem[newIndex]["end"] = connectionEndConcept
        startMem[newIndex]["weight"] = weight

    # descriptor connection
    if not CheckIfConnectionInGraph("descriptor", endConcept=connectionEndConcept, startConcept=connectionStartConcept, conceptMem=typeMem):
        newIndex = str(len(typeMem.keys()))
        EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionTypeConcept + "']['" + newIndex +"']")
        typeMem[newIndex]["reftype"] = "descriptor"
        typeMem[newIndex]["start"] = connectionStartConcept
        typeMem[newIndex]["end"] = connectionEndConcept
        typeMem[newIndex]["weight"] = weight

    # indirect connection
    if not CheckIfConnectionInGraph("indirect", typeConcept=connectionTypeConcept, startConcept=connectionStartConcept, conceptMem=endMem):
        newIndex = str(len(endMem.keys()))
        EnsureRetrieveMemory(baseGraphReferenceString + "['" + connectionEndConcept + "']['" + newIndex +"']")
        endMem[newIndex]["reftype"] = "indirect"
        endMem[newIndex]["start"] = connectionStartConcept
        endMem[newIndex]["type"] = connectionTypeConcept
        endMem[newIndex]["weight"] = weight

def FindConnectionsByTypeActuator(graphReferenceString, conceptReferenceString, typeReferenceString, resultsReferenceString):
    graphMem = EnsureRetrieveMemory(graphReferenceString)
    resultsMem = EnsureRetrieveMemory(resultsReferenceString)
    concept = platform.GetReferenceName(conceptReferenceString)
    typeConcept = platform.GetReferenceName(typeReferenceString)

    resultsIndex = len(resultsMem.keys())

    for indexKey in graphMem[concept]:
        entry = graphMem[concept][indexKey]

        if entry["reftype"] == "direct" and entry["type"] == typeConcept:
            resultsMem[str(resultsIndex)] = str(entry["end"])
            resultsIndex += 1

def FindConnectionsByEndActuator(graphReferenceString, typeReferenceString, conceptReferenceString, resultsReferenceString):
    graphMem = EnsureRetrieveMemory(graphReferenceString)
    resultsMem = EnsureRetrieveMemory(resultsReferenceString)
    typeConcept = platform.GetReferenceName(typeReferenceString)
    concept = platform.GetReferenceName(conceptReferenceString)

    resultsIndex = len(resultsMem.keys())

    for indexKey in graphMem[concept]:
        entry = graphMem[concept][indexKey]

        if entry["reftype"] == "indirect" and entry["type"] == typeConcept:
            resultsMem[str(resultsIndex)] = str(entry["start"])
            resultsIndex += 1
