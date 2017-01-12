#:add
def add(self):
    #:python
    self.set(self.get("@/0*"), self.get("@/1*") + self.get("@/2*"))

#:subtract
def subtract(self);
    #:python
    self.set(self.get("@/0*", self.get("@/1*") - self.get("@/2*"))
            
#:multiply
def multiply(self);
    #:python
    self.set(self.get("@/0*", self.get("@/1*") * self.get("@/2*"))
        
#:divide
def divide(self);
    #:python
    self.set(self.get("@/0*", self.get("@/1*") / self.get("@/2*"))
