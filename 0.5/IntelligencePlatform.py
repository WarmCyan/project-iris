import Intelligence
import time
from termcolor import colored
import os
import gc
import json
import thread
import Queue
import sys
import traceback

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
LOG_DIALOG = "dialog"

# log colors
LOG_CACHE_COLOR = "red"
LOG_CACHE_DETAIL_COLOR = "white"
LOG_CONCEPT_PARSE_COLOR = "blue"
LOG_INTELLIGENCE_COLOR = "yellow"
LOG_SYNTAX_COLOR = "green"
LOG_EXECUTION_COLOR = "magenta"
LOG_TIMING_COLOR = "cyan"
LOG_ERROR_COLOR = "red"
LOG_PLATFORM_COLOR = "white"
LOG_DIALOG_COLOR = "white"

LOG_PAUSE_TIME = .1 # the amount of time to pause if logging is off to simulate when actually logging (slows down the intelligence significantly so it doesn't immediately jump to completion when logging is turned off)

# log switches
logCacheOn = True
logCacheDetailOn = True
logConceptParseOn = True
logIntelligenceOn = True
logSyntaxOn = True
logExecutionOn = True
logTimingOn = True
logErrorOn = True
logPlatformOn = True
logDialogOn = True
    
class IntelligencePlatform:
    entity = None
    entityData = {}
    entityDataFolderPath = ""
    cycle = 0
    continueSelf = True
            
    level = 0
    cache = []
    argNum = []
    graphMode = "nograph"

    timeStack = []
    # TODO: add cycle execution times as well?
    timeExecutionStart = None
    timeCycleStart = None
    cycleMaxDepth = 0
    cycleExecutions = 0

    logFP = None
    platformLogFP = None

    commandHandlingActive = False
    entityRunning = False

    consoleLogEnabled = True

    # non kill-safe functions (allow even if kill-safe has been activated)
    safeFunctions = ['Log', 'platformLogFP', 'logFP', 'entityData', 'safeFunctions', 'entityRunning', 'commandHandlingActive', 'HandleCommand', 'commandQueue', 'cycle']

    commandQueue = Queue.Queue()

    # NOTE: press tab and then enter to get a platform level command prompt
    def ConsoleInput(self, cmdQueue):
        while self.commandHandlingActive:
            # wait for a tab keypress
            commandkey = raw_input() 
            if commandkey != "\t": continue

            # user wants to enter command, slow down the intelligence, hide the log, and show the prompt
            cmdQueue.put("HIDELOG")
            cmdQueue.put("DISPLAY>")
            cmd = raw_input()
            if cmd == "panic": # issue a panic stop. The entity is killed from THIS thread, (independent of what main thread is doing.)
                try:
                    self.platformLogFP.write("#### !! - PANIC-STOP ISSUED - !! ####\n")
                except:
                    pass
                self.KILL(False) # kill IMMEDIATELY if there's an issue
                # NOTE: due to issues in how the end of StartLife() is handled
                # (it doesn't know when in panic mode), the platform triggers
                # its own failsafe and shuts down when a panic stop is issued.
            cmdQueue.put("SHOWLOG")
            cmdQueue.put(cmd)

    # run any commands coming from command input thread
    def HandleCommand(self):
        # check queue filled by input thread
        while not self.commandQueue.empty():
            cmd = self.commandQueue.get()

            # log command if appropriate
            if cmd != "HIDELOG" and cmd != "SHOWLOG" and cmd != "DISPLAY>":
                reHide = False
                if self.consoleLogEnabled == False:
                    reHide = True
                    self.consoleLogEnabled = True
                self.Log("PLATFORM COMMAND - '" + cmd + "'", LOG_PLATFORM)

                if reHide: self.consoleLogEnabled = False
            
            # run commands as necessary
            if cmd == "kill":
                self.KILL(True)
            elif cmd == "HIDELOG":
                self.consoleLogEnabled = False
            elif cmd == "SHOWLOG":
                self.consoleLogEnabled = True
            elif cmd == "DISPLAY>":
                sys.stdout.write("> ")
                sys.stdout.flush()

    def CreateEntity(self):
        # start command input thread
        self.commandHandlingActive = True
        thread.start_new_thread(self.ConsoleInput, (self.commandQueue,))
        
        # load current data
        self.Log("Loading entity data...", LOG_PLATFORM)
        entityFP = open("ENTITY.dat", "r")
        self.entityData = json.load(entityFP)
        entityFP.close()

        # increment build
        self.entityData["Build"] = str(1 + int(self.entityData["Build"])) 

        # save updated
        entityFP = open("ENTITY.dat", "w")
        json.dump(self.entityData, entityFP)

        # create new run folder
        self.Log("Building data folder for new entity...", LOG_PLATFORM)
        folderName = str(self.entityData["Name"]) + " " + str(self.entityData["Version"]) + "." + str(self.entityData["Build"]) + " (" + time.strftime("%y.%m.%d-%H.%M.%S") + ")"
        self.entityDataFolderPath = "InstanceLogs/" + folderName
        os.makedirs("./" + self.entityDataFolderPath)
        self.Log("Created Folder: " + self.entityDataFolderPath) 

        # create platform log
        self.platformLogFP = open(self.entityDataFolderPath + "/_PLATFORMLOG.log", "w")

        self.InitializeIntelligence()
        

    def InitializeIntelligence(self):
        self.Log("Instantiating new intelligence instance in entity...", LOG_PLATFORM)
        self.entity = Intelligence.Intelligence()

        # display entity's intelligence meta data
        self.Log("----------------------------------------", LOG_PLATFORM)
        self.Log("\t" + str(self.entityData["Name"]) + " " + str(self.entityData["Version"]), LOG_PLATFORM)
        self.Log("\tBuild " + str(self.entityData["Build"]), LOG_PLATFORM)
        self.Log("----------------------------------------\n", LOG_PLATFORM)
        
        # record initial memory set
        self.DumpMemory(initial=True)

    def StartLife(self):
        self.Log("Starting life cycles...\n", LOG_PLATFORM)
        self.cycle = 0
        self.timeExecutionStart = time.clock()
        self.entityRunning = True

        while (self.continueSelf):
            self.Log("----- CYCLE " + str(self.cycle) + " -----", LOG_PLATFORM)
            self.timeCycleStart = time.clock()
            self.cycleMaxDepth = 0
            self.cycleExecutions = 0
            
            # create log file
            self.Log("Creating cycle " + str(self.cycle) + " log file...", LOG_PLATFORM)
            self.logFP = open(self.entityDataFolderPath + "/Cycle_" + str(self.cycle) + ".log", "w")

            self.continueSelf = False # should self sustain (keep itself alive by running itself) NOTE: RunConceptExecute will set this to true if it finds the self concept
            try: 
                self.Log("Running cycle " + str(self.cycle) + "...\n", LOG_PLATFORM)
                self.RunConceptExecute("[self]")
            except Exception as e:
                self.Log("\nERROR: Self failed to run properly", LOG_ERROR)
                self.Log("ERROR_MSG: " + str(e), LOG_ERROR)
                traceback.print_exc()
                try:
                    self.logFP.close()
                    self.logFP = None
                    self.DumpMemory()
                except:
                    self.Log("ERROR: Could not dump memory", LOG_ERROR)
                break

            # stop here if the entity was killed (NOTE: if panic stop issued,
            # THIS CODE IS NOT REACHED. Rather, it appears to break out of the
            # while, and trigger the failsafe when it tries to kill the entity
            # again)
            if not self.entityRunning: 
                self.Log("Entity killed, stopping platform...")
                try: self.platformLogFP.close()
                except: self.Log("NOTE: platform log not available")
                return
            
            # close the cycle log
            cycleTime = (time.clock() - self.timeCycleStart) * 1000
            self.Log("\nCycle " + str(self.cycle) + " finished execution (" + str(cycleTime) + " ms)", LOG_PLATFORM) 
            self.Log("Cycle reached a max depth of " + str(self.cycleMaxDepth) + " levels and ran " + str(self.cycleExecutions) + " concepts", LOG_PLATFORM)
            self.logFP.close()
            self.logFP = None

            # create a memory dump
            self.DumpMemory()
            
        self.Log("Entity is no longer self sustaining. Shutting down...", LOG_PLATFORM)
        try: 
            totalTime = (time.clock() - self.timeExecutionStart) * 1000
            self.Log("Entity lifespan: " + str(totalTime) + " ms", LOG_PLATFORM)
        except: pass
        self.KILL()

        self.platformLogFP.close()
    
    # shut down all variables, delete entity, activate fail-safe
    def KILL(self, salvageMemory = False):
        self.consoleLogEnabled = True
        self.Log("Closing file pointers...", LOG_PLATFORM)
        try: 
            self.logFP.close()
            self.logFP = None
        except: self.Log("NOTE: cycle log not available")

        # if specified, try to save what's in memory
        if salvageMemory:
            self.Log("Attempting to salvage memory...", LOG_PLATFORM)
            try: self.DumpMemory(salvage=True)
            except: self.Log("ERROR: Failed to salvage memory", LOG_ERROR)
        
        # delete all of entity and cache
        self.Log("Safely corrupting and deleting entity...", LOG_PLATFORM)
        self.entityRunning = False
        self.level = -100
        for concept in self.entity.Memory:
            self.entity.Memory[concept] = None
        self.entity.Memory = None
        delattr(IntelligencePlatform, "entity")
        delattr(IntelligencePlatform, "cache")

        # reset all attributes/functions in class to the fail-safe function
        self.Log("Activating fail safe kill switch...", LOG_PLATFORM)
        attributes = dir(self)
        for attribute in attributes:
            if str(attribute) not in self.safeFunctions: 
                setattr(self, attribute, self.FAIL_SAFE)
        gc.collect();
        self.Log("Entity deleted", LOG_PLATFORM)

    def FAIL_SAFE(self, **args):
        print("_FAIL_SAFE_ - BLOCKED ATTEMPTED ACCESS ON ATTRIBUTE AFTER KILL SWITCH WAS THROWN.")
        print("_FAIL_SAFE_ - CORRUPTING ALL REMAINING FUNCTIONS...")
        
        # gracefully shut down platform log
        try:
            self.platformLogFP.write("#### !! - FAIL-SAFE TRIGGERED - !! ####")
            self.platformLogFP.close()
        except:
            print("_FAIL_SAFE_ - COULD NOT SALVAGE PLATFORM LOG")

        # delete all attributes/functions
        attributes = dir(self)
        for attribute in attributes:
            print("\tDELETING '" + attribute + "'...")
            try: delattr(IntelligencePlatform, attribute)
            except AttributeError: print("\tNOTICE - '" + attribute + "' ALREADY NONEXISTANT")

        # shutdown
        print("_FAIL_SAFE_ - FORCING PROGRAM STOP.")
        exit()

    # Save all the memory concepts in a JSON file
    def DumpMemory(self, initial = False, salvage = False):
        backupFileName = ""
        if initial:
            self.Log("Backing up initial entity memory set...", LOG_PLATFORM)
            backupFileName = self.entityDataFolderPath + "/_Memory_INITIAL.json"
        elif salvage:
            self.Log("Salvaging entity memory set...", LOG_PLATFORM)
            backupFileName = self.entityDataFolderPath + "/_Memory_SALVAGE.json"
        else: 
            self.Log("Backing up entity's memory set for cycle " + str(self.cycle) + "...", LOG_PLATFORM)
            backupFileName = self.entityDataFolderPath + "/Memory_" + str(self.cycle) + ".json"

        backupFP = open(backupFileName, "w")
        json.dump(self.entity.Memory, backupFP, indent=4)
        backupFP.close()

        self.Log("Entity memory dumped to " + backupFileName, LOG_PLATFORM)

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
            #elif (character == "\"" or character == "'") and not ESCAPE:
            elif (character == "\"") and not ESCAPE:
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
        self.HandleCommand()
        if (self.entityRunning == False): return

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
            try: eval(preConstructedString + reference)
            except: exec(preConstructedString + reference + " = {}")
            
            reference += self.RunConceptGet(conceptList[0][1][0], True, str(preConstructedString + reference))
            runTime = (time.clock() - self.timeStack.pop()) * 1000
            self.level -= 1
            
            self.Log(indent + "[" + str(self.level) + "](argument '" + str(conceptList[0][1]) + "' obtained: .......... " + str(runTime) + " ms)", LOG_TIMING)
            
        if not multiLevel: self.CacheStore(reference)
        else: return reference

    def RunConceptExecute(self, conceptString):
        self.HandleCommand()
        if (self.entityRunning == False): return

        self.Log("Intelligence:" + conceptString, LOG_INTELLIGENCE)
        indent = self.GetLevelIndent(self.level)

        self.Log(indent + "LEVEL: " + str(self.level), LOG_SYNTAX)
        if self.level > self.cycleMaxDepth: self.cycleMaxDepth = self.level
        self.cycleExecutions += 1

        conceptList = self.ParseConcepts(conceptString, indent)

        connection_flag = False # set to true if graphing mode and connection was found

        for concept in conceptList:
            self.Log(indent + "CONCEPT: " + concept[0], LOG_SYNTAX)

            # ensure argnum exists for this level
            while len(self.argNum) <= self.level:
                self.argNum.append(0)
                
            self.argNum[self.level] = 0
            for argument in concept[1]:
                self.Log(indent + "  ARGUMENT: " + str(argument), LOG_SYNTAX)

                #if not self.entityRunning: return

                # execute argument 
                if argument.startswith("["):
                    self.Log(indent + "[" + str(self.level) + "](executing argument '" + argument + "')", LOG_EXECUTION)
                    self.level += 1
                    self.timeStack.append(time.clock()) # TIMING
                    self.RunConceptExecute(argument)
                    if not self.entityRunning: return
                    runTime = (time.clock() - self.timeStack.pop()) * 1000
                    self.level -= 1

                    self.Log(indent + "[" + str(self.level) + "](argument '" + argument + "' execution: .......... " + str(runTime) + " ms)", LOG_TIMING)

                #if not self.entityRunning: return

                # get argument
                if argument.startswith("("):
                    self.Log(indent + "[" + str(self.level) + "](getting argument '" + argument + "')", LOG_EXECUTION)
                    self.level += 1
                    self.timeStack.append(time.clock()) # TIMING
                    self.RunConceptGet(argument)
                    if not self.entityRunning: return
                    runTime = (time.clock() - self.timeStack.pop()) * 1000
                    self.level -= 1

                    self.Log(indent + "[" + str(self.level) + "](argument '" + argument + "' obtained: .......... " + str(runTime) + " ms)", LOG_TIMING)

                # literal argument (but not for the python!!!)
                if argument.startswith("\"") and concept[0] != "python":
                    self.Log(indent + "[" + str(self.level) + "](storing literal argument " + argument + ")", LOG_EXECUTION)
                    self.CacheStore(argument, 0)

                self.argNum[self.level] += 1

            # execute concept
            #if (concept[0] == "python" and (self.graphMode != "graphonly" or self.level != self.graphLevel)) or (concept[0] == "sudo"):
            if concept[0] == "python" and not connection_flag: #or concept[0] == "sudo":
                #if not self.entityRunning: return

                code = concept[1][0][1:-1]
                self.Log(indent + "EXECUTING: '" + code + "'", LOG_SYNTAX)
                exec(code)
            else:
                runstring = self.entity.Memory[concept[0]]

                if runstring == "[self]" and self.graphMode != "graphonly":
                    self.continueSelf = True
                    return

                #if self.graphMode == "graphonly" and concept[0] != "connection" and self.level == self.graphLevel:
                    #continue
                if self.graphMode == "graphonly" and concept[0] == "connection":
                    connection_flag = True
                if self.graphMode == "nograph" and concept[0] == "connection":
                    continue
                if self.graphMode == "graphonly" and connection_flag and concept[0] != "connection":
                    continue
                
                self.Log(indent + "[" + str(self.level) + "](executing concept '" + concept[0] + "')", LOG_EXECUTION)
                self.level += 1
                self.timeStack.append(time.clock()) # TIMING
                self.RunConceptExecute(runstring)
                if not self.entityRunning: return
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

    def GetInput(self):
        inputstr = raw_input('Intelligence requested input: ')
        self.Log("Creator> " + inputstr, LOG_PLATFORM)
        return inputstr

    def Display(self, msg):
        self.Log(str(self.entityData["Name"]) + " " + str(self.entityData["Version"]) + "." + str(self.entityData["Build"]) + "> " + msg, LOG_PLATFORM)
            
    def Log(self, msg, level = "default"):

        if self.logFP != None: self.logFP.write(msg + "\n")
        if self.platformLogFP != None and (level == LOG_PLATFORM or level == LOG_ERROR or level == LOG_DIALOG): self.platformLogFP.write(msg + "\n")

        if not self.consoleLogEnabled: 
            time.sleep(LOG_PAUSE_TIME);
            return
        
        if level == LOG_CACHE and logCacheOn: 
            print(colored(str(msg), LOG_CACHE_COLOR))
            return
        elif level == LOG_CACHE_DETAIL and logCacheDetailOn:
            print(colored(str(msg), LOG_CACHE_DETAIL_COLOR))
            return
        elif level == LOG_CONCEPT_PARSE and logConceptParseOn:
            print(colored(str(msg), LOG_CONCEPT_PARSE_COLOR))
            return
        elif level == LOG_INTELLIGENCE and logIntelligenceOn:
            print(colored(str(msg), LOG_INTELLIGENCE_COLOR))
            return
        elif level == LOG_SYNTAX and logSyntaxOn:
            print(colored(str(msg), LOG_SYNTAX_COLOR))
            return
        elif level == LOG_EXECUTION and logExecutionOn:
            print(colored(str(msg), LOG_EXECUTION_COLOR))
            return
        elif level == LOG_TIMING and logTimingOn:
            print(colored(str(msg), LOG_TIMING_COLOR))
            return
        elif level == LOG_ERROR and logErrorOn:
            print(colored(str(msg), LOG_ERROR_COLOR))
            return
        elif level == LOG_PLATFORM and logPlatformOn:
            print(colored(str(msg), LOG_PLATFORM_COLOR))
            return
        elif level == LOG_DIALOG and logDialogOn:
            print(colored(str(msg), LOG_DIALOG_COLOR))
            return
        elif level == "default":
            print(msg)
            return
        else:
            return


    # TODO: logically this should be in the concept itself, but slower?
    # TEMP_ARG_0 is the REFERENCE to the desired concept NOTE: this shouldn't
    # even be used!!!!!!!!!
    # TEMP_MAP_CONCEPT is the VALUE of that concept
    # TEMP_MAP_LOC is the place to store the map
    def METAMapConcept(self):
        mapStorage = self.entity.Memory["TEMP_MAP_LOC"]
        conceptList = self.ParseConcepts(self.entity.Memory["TEMP_MAP_CONCEPT"])
        self.entity.Memory[mapStorage] = {}
        index = -1
        for concept in conceptList:
            index += 1
            indexString = str(index)
            self.entity.Memory[mapStorage][indexString] = {}
            self.entity.Memory[mapStorage][indexString]["concept"] = concept[0]

            # create a straight string of the args TODO: maybe later find a way to make
            # this a recursive structure like it would be anyway?
            argsString = ""
            for argument in concept[1]:
                argsString += " " + str(argument)

            # trim extra space at beginning
            argsString = argsString[1:]
            
            self.entity.Memory[mapStorage][indexString]["args"] = argsString
