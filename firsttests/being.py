class Being:
    Concepts = {
            "exist":"[mutate (exist) [concept-list]][query \"approve\"][remember (exist) [recall \"approval\"]][exist]",
            #"mutate":["[python \"print(self.cache[self.level][0])\"]",2], # 2 represents number of arguments it takes
            "mutate":"[python \"print(self.cache[self.level][0])\"]", # 2 represents number of arguments it takes
            "query":"",
            "remember":"",
            "recall":"",
            "concept-list":"[python \"self.cache[self.level][self.argNum[self.level]] = self.entity.Concepts\"]"
            #"approval":"[python \"self.cache[self.level] # YES, do this
            }

    Memory = {
            "approval":0
            }


    #def mutate(concept, conceptList):
        #print(conceptList)
        
