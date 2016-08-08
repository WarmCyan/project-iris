import Intelligence
import re

class IntelligencePlatform:

    entity = None
            
    level = 0
    cache = []
    argNum = []

    def InitializeIntelligence(self):
        print("Instantiating new intelligence instance...")
        self.entity = Intelligence.Intelligence()

    def StartLife(self):
        print("Starting life...\n")
        self.RunConceptExecute("[self]")
        #self.RunConceptExecute("[print [memory]]")

        #print(self.ParseConcepts("(thingy (MOARTHINGY))"))

    # get the concepts and arguments from a string   
    def ParseConcepts(self, conceptString, indent = ""):
        indent += "- " 
        print(indent + "Parsing '" + conceptString + "'...")
        braceLevel = 0
        quoteLevel = 0
        parenLevel = 0
        recordingConcept = True
        conceptNum = 0
        argNum = -1
        concepts = []

        ESCAPE = False

        for character in conceptString:
            if character == "[": braceLevel += 1
            elif character == "]":
                braceLevel -= 1
                if braceLevel == 0:
                    conceptNum += 1
                    recordingConcept = True # if completely finished that part of concept, and potentially starting new one, turn recording back on
                    argNum = -1
            elif character == "(": parenLevel += 1
            elif character == ")": parenLevel -= 1
            elif character == "\\": 
                ESCAPE = True 
                continue
            elif character == "\"" and not ESCAPE:
                if quoteLevel == 0: quoteLevel += 1
                elif quoteLevel == 1: quoteLevel -= 1
            elif character == " ": recordingConcept = False
            elif recordingConcept:
                try: concepts[conceptNum]
                except IndexError: concepts.append([])
                try: concepts[conceptNum][0]
                except IndexError:
                    concepts[conceptNum].append("") # concept name
                    concepts[conceptNum].append([]) # args
                concepts[conceptNum][0] += character
                
            # argument handling
            if not recordingConcept:
                if character == " " and (braceLevel == 1 or parenLevel == 1) and quoteLevel == 0: # space signifies next argument (assuming not in higher level of braces
                    concepts[conceptNum][1].append("")
                    argNum += 1
                else:
                    concepts[conceptNum][1][argNum] += character
                
            if ESCAPE: ESCAPE = False
                
        print(indent + "Parsed " + str(concepts))
        return concepts 


    def GetLevelIndent(self, level):
        indent = ""
        for i in range(0, level):
            indent += "    "
        return indent

    def RunConceptGet(self, conceptString):
        print("Intelligence:" + conceptString)
        indent = self.GetLevelIndent(self.level)
        print(indent + "LEVEL: " + str(self.level))

        conceptList = self.ParseConcepts(conceptString, indent)

        # the thing should be the first
        conceptName = conceptList[0][0]
        self.CacheStore("self.entity.Memory[\"" + conceptName + "\"]")
        

    def RunConceptExecute(self, conceptString):
        print("Intelligence:" + conceptString)
        indent = self.GetLevelIndent(self.level)

        print(indent + "LEVEL: " + str(self.level))

        conceptList = self.ParseConcepts(conceptString, indent)

        for concept in conceptList:
            print(indent + "CONCEPT: " + concept[0])

            # ensure argnum exists for this level
            while len(self.argNum) <= self.level:
                self.argNum.append(0)
                
            self.argNum[self.level] = 0
            for argument in concept[1]:
                print(indent + "  ARGUMENT: " + str(argument))

                # execute argument 
                if argument.startswith("["):
                    print(indent + "[" + str(self.level) + "](executing argument '" + argument + "')")
                    self.level += 1
                    self.RunConceptExecute(argument)
                    self.level -= 1

                # get argument
                if argument.startswith("("):
                    print(indent + "[" + str(self.level) + "](getting argument '" + argument + "')")
                    self.level += 1
                    self.RunConceptGet(argument)
                    self.level -= 1

                self.argNum[self.level] += 1

            # execute concept
            if concept[0] == "python":
                code = concept[1][0][1:-1]
                print(indent + "EXECUTING: '" + code + "'")
                exec(code)
            else:
                runstring = self.entity.Memory[concept[0]]
                print(indent + "[" + str(self.level) + "](executing concept '" + concept[0] + "')")
                self.level += 1
                self.RunConceptExecute(runstring)
                self.level -= 1

    # verifies appropriate structures exist in cache, then stores object in cache based on level
    # if for some reason trying to get a different level's cache, specify an offset
    # (by default, since this is generally for arguments, arguments are for the
    # level above it?)
    def CacheStore(self, obj, offset = -1):
        level = self.level + offset

        # ensure structures exist
        while len(self.cache) <= level:
            self.cache.append([])
        while len(self.argNum) <= level:
            self.argNum.append(0)
        while len(self.cache[level]) <= self.argNum[level]:
            self.cache[level].append("")
        
        print("**CACHE**:: STORING at level " + str(level) + " at " + str(self.argNum[level]))
        self.cache[level][self.argNum[level]] = obj

    def CacheRetrieve(self, argNum, offset = 0):
        level = self.level + offset

        print("**CACHE**:: RETRIEVING at level " + str(level) + " at " + str(argNum))

        obj = None
        try: obj = self.cache[level][argNum]
        except IndexError:
            print("**CACHE**:: RETRIVAL FAILURE")
            return None
        return obj
            
