import Intelligence
import time
from termcolor import colored

# log types
LOG_CACHE = "cache"
LOG_CACHE_DETAIL = "cachedetail"
LOG_CONCEPT_PARSE = "conceptparse"
LOG_INTELLIGENCE = "intelligence"
LOG_SYNTAX = "syntax"
LOG_EXECUTION = "execution"
LOG_TIMING = "timing"
LOG_ERROR = "error"
LOG_PLATFORM = "platform"

# log colors
LOG_CACHE_COLOR = "red"
LOG_CACHE_DETAIL_COLOR = "white"
LOG_CONCEPT_PARSE_COLOR = "blue"
LOG_INTELLIGENCE_COLOR = "yellow"
LOG_SYNTAX_COLOR = "green"
LOG_EXECUTION_COLOR = "magenta"
LOG_TIMING_COLOR = "cyan"
LOG_ERROR_COLOR = "white"
LOG_PLATFORM_COLOR = "white"


class IntelligencePlatform:


    # LOG TYPES:
    # cache - status messages about when cache is being accessed
    # cachedetail - prints what's being put into cache 
    # conceptparse - status and results of concept parsing
    # intelligence - strings intelligence is passing to platform
    # syntax - granular information about syntax parsing and what's being executed
    # error - any error messages
    # platform - platform messages

    logCacheOn = True
    logCacheDetailOn = True
    logConceptParseOn = True
    logIntelligenceOn = True
    logSyntaxOn = True
    logExecutionOn = True
    logTimingOn = True
    logErrorOn = True
    logPlatformOn = True

    entity = None
            
    level = 0
    cache = []
    argNum = []

    timeStack = []

    def InitializeIntelligence(self):
        self.Log("Instantiating new intelligence instance...", LOG_PLATFORM)
        self.entity = Intelligence.Intelligence()

    def StartLife(self):
        self.Log("Starting life...\n", LOG_PLATFORM)
        self.RunConceptExecute("[self]")
        #self.RunConceptExecute("[print [memory]]")

        #print(self.ParseConcepts("(thingy (MOARTHINGY))"))

    # get the concepts and arguments from a string   
    def ParseConcepts(self, conceptString, indent = ""):
        indent += "- " 
        self.Log(indent + "Parsing '" + conceptString + "'...", LOG_CONCEPT_PARSE)
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
            elif (character == "\"" or character == "'") and not ESCAPE:
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
                #print(character + " PAREN LEVEL " + str(parenLevel))
                if character == " " and ((braceLevel == 1 and parenLevel == 0) or (braceLevel == 0 and parenLevel == 1)) and quoteLevel == 0: # space signifies next argument (assuming not in higher level of braces
                    concepts[conceptNum][1].append("")
                    argNum += 1
                else:
                    concepts[conceptNum][1][argNum] += character
                
            if ESCAPE: ESCAPE = False
                
        self.Log(indent + "Parsed " + str(concepts), LOG_CONCEPT_PARSE)
        return concepts 


    def GetLevelIndent(self, level):
        indent = ""
        for i in range(0, level):
            indent += "    "
        return indent

    # gets the part within brackets of the reference
    def GetReferenceName(self, reference):
        conceptStartIndex = reference.find("\"", 0) + 1
        conceptEndIndex = reference.find("\"", conceptStartIndex)

        return reference[conceptStartIndex:conceptEndIndex]

    def RunConceptGet(self, conceptString, multiLevel = False, preConstructedString = ""):
        self.Log("Intelligence:" + conceptString, LOG_INTELLIGENCE)
        indent = self.GetLevelIndent(self.level)
        self.Log(indent + "LEVEL: " + str(self.level), LOG_SYNTAX)

        conceptList = self.ParseConcepts(conceptString, indent)

        reference = ""

        # the thing should be the first
        conceptName = conceptList[0][0]
        if not multiLevel: reference = "self.entity.Memory[\"" + conceptName + "\"]"
        else: reference = "[\"" + conceptName + "\"]"

        if len(conceptList[0][1]) > 0:
            self.Log(indent + "[" + str(self.level) + "](getting argument '" + str(conceptList[0][1]) + "')", LOG_EXECUTION)
            self.level += 1
            self.timeStack.append(time.clock()) # TIMING

            # make sure thing actually exists
            try:
                #self.Log("=============== evaluating '" + str(preConstructedString + reference) + "' ==================") # DEBUG
                eval(preConstructedString + reference)
            except:
                #self.Log("----------------- creating '" + str(preConstructedString + reference) + "' -----------------------") # DEBUG
                exec(preConstructedString + reference + " = {}")
            
            reference += self.RunConceptGet(conceptList[0][1][0], True, str(preConstructedString + reference))
            runTime = (time.clock() - self.timeStack.pop()) * 1000
            self.level -= 1
            
            self.Log(indent + "[" + str(self.level) + "](argument '" + str(conceptList[0][1]) + "' obtained: .......... " + str(runTime) + " ms)", LOG_TIMING)
            
        if not multiLevel: self.CacheStore(reference)
        else: return reference
        

    def RunConceptExecute(self, conceptString):
        self.Log("Intelligence:" + conceptString, LOG_INTELLIGENCE)
        indent = self.GetLevelIndent(self.level)

        self.Log(indent + "LEVEL: " + str(self.level), LOG_SYNTAX)

        conceptList = self.ParseConcepts(conceptString, indent)

        for concept in conceptList:
            self.Log(indent + "CONCEPT: " + concept[0], LOG_SYNTAX)

            # ensure argnum exists for this level
            while len(self.argNum) <= self.level:
                self.argNum.append(0)
                
            self.argNum[self.level] = 0
            for argument in concept[1]:
                self.Log(indent + "  ARGUMENT: " + str(argument), LOG_SYNTAX)

                # execute argument 
                if argument.startswith("["):
                    self.Log(indent + "[" + str(self.level) + "](executing argument '" + argument + "')", LOG_EXECUTION)
                    self.level += 1
                    self.timeStack.append(time.clock()) # TIMING
                    self.RunConceptExecute(argument)
                    runTime = (time.clock() - self.timeStack.pop()) * 1000
                    self.level -= 1

                    self.Log(indent + "[" + str(self.level) + "](argument '" + argument + "' execution: .......... " + str(runTime) + " ms)", LOG_TIMING)

                # get argument
                if argument.startswith("("):
                    self.Log(indent + "[" + str(self.level) + "](getting argument '" + argument + "')", LOG_EXECUTION)
                    self.level += 1
                    self.timeStack.append(time.clock()) # TIMING
                    self.RunConceptGet(argument)
                    runTime = (time.clock() - self.timeStack.pop()) * 1000
                    self.level -= 1

                    self.Log(indent + "[" + str(self.level) + "](argument '" + argument + "' obtained: .......... " + str(runTime) + " ms)", LOG_TIMING)

                # literal argument (but not for the python!!!)
                if argument.startswith("\"") and concept[0] != "python":
                    self.Log(indent + "[" + str(self.level) + "](storing literal argument " + argument + ")", LOG_EXECUTION)
                    self.CacheStore(argument, 0)

                self.argNum[self.level] += 1

            # execute concept
            if concept[0] == "python":
                code = concept[1][0][1:-1]
                self.Log(indent + "EXECUTING: '" + code + "'", LOG_SYNTAX)
                exec(code)
            else:
                runstring = self.entity.Memory[concept[0]]
                self.Log(indent + "[" + str(self.level) + "](executing concept '" + concept[0] + "')", LOG_EXECUTION)
                self.level += 1
                self.timeStack.append(time.clock()) # TIMING
                self.RunConceptExecute(runstring)
                runTime = (time.clock() - self.timeStack.pop()) * 1000
                self.level -= 1
                self.Log(indent + "[" + str(self.level) + "](concept '" + concept[0] + "' execution: ......... " + str(runTime) + " ms)", LOG_TIMING)
                self.CacheClear()

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
        
        self.Log("**CACHE**:: STORING at level " + str(level) + " at " + str(self.argNum[level]), LOG_CACHE)
        self.Log("########## STORE ##########\n" + str(obj) + "\n###########################\n", LOG_CACHE_DETAIL)
        self.cache[level][self.argNum[level]] = obj

    def CacheRetrieve(self, argNum, offset = 0):
        level = self.level + offset

        self.Log("**CACHE**:: RETRIEVING at level " + str(level) + " at " + str(argNum), LOG_CACHE)

        obj = None
        try: obj = self.cache[level][argNum]
        except IndexError:
            self.Log("**CACHE**:: RETRIVAL FAILURE", LOG_CACHE)
            return None
        self.Log("########## RETRIEVE ##########\n" + str(obj) + "\n##############################\n", LOG_CACHE_DETAIL)
        return obj

    def CacheClear(self, offset = 0):
        level = self.level + offset

        self.Log("**CACHE**:: CLEARING level " + str(level), LOG_CACHE)
        try: 
            self.cache[level] = []
            self.argNum[level] = 0
        except IndexError:
            self.Log("**CACHE**:: CLEARING FAILURE", LOG_CACHE)
            
    def Log(self, msg, level = "default"):
        if level == LOG_CACHE and self.logCacheOn: 
            print(colored(str(msg), LOG_CACHE_COLOR))
            return
        elif level == LOG_CACHE_DETAIL and self.logCacheDetailOn:
            print(colored(str(msg), LOG_CACHE_DETAIL_COLOR))
            return
        elif level == LOG_CONCEPT_PARSE and self.logConceptParseOn:
            print(colored(str(msg), LOG_CONCEPT_PARSE_COLOR))
            return
        elif level == LOG_INTELLIGENCE and self.logIntelligenceOn:
            print(colored(str(msg), LOG_INTELLIGENCE_COLOR))
            return
        elif level == LOG_SYNTAX and self.logSyntaxOn:
            print(colored(str(msg), LOG_SYNTAX_COLOR))
            return
        elif level == LOG_EXECUTION and self.logExecutionOn:
            print(colored(str(msg), LOG_EXECUTION_COLOR))
            return
        elif level == LOG_TIMING and self.logTimingOn:
            print(colored(str(msg), LOG_TIMING_COLOR))
            return
        elif level == LOG_ERROR and self.logErrorOn:
            print(colored(str(msg), LOG_ERROR_COLOR))
            return
        elif level == LOG_PLATFORM and self.logPlatformOn:
            print(colored(str(msg), LOG_PLATFORM_COLOR))
            return
        elif level == "default":
            print(msg)
            return
        else:
            return

#def getReferenceName(reference):
    #conceptStartIndex = reference.find("\"", 0)
    #conceptEndIndex = reference.find("\"", conceptStartIndex + 1)
    #print(conceptStartIndex)
    #print(conceptEndIndex)

    #return reference[conceptStartIndex+1:conceptEndIndex]
