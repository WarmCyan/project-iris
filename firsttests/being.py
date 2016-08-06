class Being:
    Concepts = {
            "exist":"[mutate (exist) [concept-list]][query \"approve\"][remember (exist) [recall \"approval\"]][exist]",
            "mutate":"[python \"print(self.cache)\"]",
            "query":"",
            "remember":"",
            "recall":"",
            "concept-list":"[python \"self.cache = self.entity.Concepts\"]"
            }

    Memory = {}


    #def mutate(concept, conceptList):
        #print(conceptList)
        
