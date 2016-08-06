import being
import re

class Interpreter:

    entity = None
    conceptPattern = """\[([\w\-\_]+)((?:(?:\s?\[\w+[\[()\s\w\-\_\."]*\])|(?:[\s"()\w\-\_\$\.\=]*))*)\]"""
    argumentPattern = """((?:"[\w\s\-\_\.(?:\\\")\=$]*")|(?:\([\w\-\_\.]+\))|(?:\[(?:[\w\-\_\.]+)(?:(?:(?:\s?\[\w+[\[()\s\w\-\_\."]*\])|(?:[\s"()\w\-\_\.\$\=]*))*)\]))"""
    compiledConceptPattern = None
    compiledArgumentPattern = None

    
    
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
        #self.RunConcept("[python \"eval(\"self.entity.Concepts\")\"]")

    def RunConcept(self, concept):
        print(concept)
        matches = re.findall(self.compiledConceptPattern, concept)
        #print(matches)
        for match in matches:
            print(match[0])

            # evaluate arguments
            args = match[1][1:]
            argmatches = re.findall(self.compiledArgumentPattern, args)

            for arg in argmatches:
                print("ARGUMENT - " + str(arg))
                if arg.startswith("["):
                    self.RunConcept(arg)
            

            # run python if it's python
            if match[0] == "python":
                code = match[1][2:-1]
                #if code.contains("$"):
                    # do stuff
                #print(code)
                exec(code)
            else:
                runstring = self.entity.Concepts[match[0]]
                self.RunConcept(runstring)
