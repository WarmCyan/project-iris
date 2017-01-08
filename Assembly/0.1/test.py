class IRIS:
    

    memory = {}

    
    def __init__(self):
        pass

    def get(self, query):
        # check if just the concept, not getting in it
        if "*" not in str(query): 
            if "/" in str(query):
                parts = str(query).split("/")
                return parts[len(parts) - 1]
            return query

        query = str(query).replace("*", "")

        # check if just a simple thing
        if query in self.memory.keys(): return self.memory[query]

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
            return result

    def set(self, query, obj):
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

    #def run(self, python):
        #exec(python)


    def execute(instruction):
        if instruction[0] == "python": exec(instruction[1]); return
        
          
