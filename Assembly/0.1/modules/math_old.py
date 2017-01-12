#:plus
def plus(self):
    #print("plusing!")
    self.set(self.get("@/0*"), self.get("@/1*") + self.get("@/2*"))

#:doThing
def doThing(self):
    #:plus thing 2 5
    self.set(self.get("thing*"), self.get("2") + self.get("5"))
    print("> " + str(self.get("thing*")))
