import being
import re

class Interpreter:

    entity = None
    conceptPattern = """\[([\w\-\_]+)((?:(?:\s?\[\w+[\[()\s\w\-\_\."]*\])|(?:[\s"()\w\-\_\$\.\=]*))*)\]"""
    argumentPattern = """((?:"[\w\s\-\_\.(?:\\\")\=$\[\]]*")|(?:\([\w\-\_\.]+\))|(?:\[(?:[\w\-\_\.]+)(?:(?:(?:\s?\[\w+[\[()\s\w\-\_\."]*\])|(?:[\s"()\w\-\_\.\$\=]*))*)\]))"""
    compiledConceptPattern = None
    compiledArgumentPattern = None

    level = 0
    cache = [[],[],[],[],[],[],[]] # find better way to do this!!!
    argNum = [0,0,0,0,0,0,0,0] # AND THIS!!!
    
    def __init__(self):
        self.compiledConceptPattern = re.compile(self.conceptPattern)
        self.compiledArgumentPattern = re.compile(self.argumentPattern)
    
    def Inception(self):
        print("Instantiating new instance of being...")
        self.entity = being.Being()

    def StartExistence(self):
        #exec("thing = eval(\"self.entity.Concepts\")")
        #print(thing)
        #print(self.entity.Concepts["exist"])
        #self.RunConcept(self.entity.Concepts["exist"])



        self.RunConcept("[mutate [concept-list]]")
        #self.ParseConcepts("[mutate [concept-list]][thing][thingy (and) \"yes and no and \\\"QUOTES!!!\\\"\"]")



        #self.RunConcept("[python \"eval(\"self.entity.Concepts\")\"]")

    #def ParseHighConcepts(self, concept):
        #matches = re.findall(self.compiledConceptPattern, concept)
        #return matches


    def ParseConcepts(self, concept):
        print("Parsing '" + concept + "'...")
        braceLevel = 0
        quoteLevel = 0
        parenLevel = 0
        recordingConcept = True
        conceptNum = 0
        argNum = -1
        concepts = []

        ESCAPE = False

        for character in concept:
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
                if character == " " and braceLevel == 1 and quoteLevel == 0: # space signifies next argument (assuming not in higher level of braces
                    concepts[conceptNum][1].append("")
                    argNum += 1
                else:
                    concepts[conceptNum][1][argNum] += character
                
            if ESCAPE: ESCAPE = False
                

        print(concepts)
        return concepts
    
    #def CompileConcept(self, concepts):
        # does the reverse of the function above, so we can both construct and deconstruct concepts


    def RunConcept(self, conceptString):
        conceptList = self.ParseConcepts(conceptString)
        
        for concept in conceptList:
            print("CONCEPT: " + concept[0])
            for argument in concept[1]:
                print("\tARGUMENT: " + str(argument))

        
    def RunConcept2(self, concept):
        print(concept)
        matches = self.ParseHighConcepts(concept)
        #print(matches)
        for match in matches:
            print(match[0])

            # evaluate arguments
            args = match[1][1:]
            argmatches = re.findall(self.compiledArgumentPattern, args)

            self.argNum[self.level] = 0
            for arg in argmatches:
                print("ARGUMENT - " + str(arg))
                if arg.startswith("["):
                    self.level += 1
                    self.RunConcept(arg)
                    self.level -= 1
                self.argNum[self.level] += 1
            

            # run python if it's python
            if match[0] == "python":
                code = match[1][2:-1]
                #if code.contains("$"):
                    # do stuff
                #print(code)
                exec(code)
            else:
                runstring = self.entity.Concepts[match[0]] #[0]
                self.RunConcept(runstring)
