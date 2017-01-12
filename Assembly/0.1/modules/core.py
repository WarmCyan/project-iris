# NOTE: ':' represents map

#:concatenate
def concatenate(self):
    #:python
    self.set(self.get("@/0*"), str(self.get("@/1*")) + str(self.get("@/2*")))

# sets a connection
# ex: map test is thing 1.0 0.0
#:map
def map(self):
    #:concatenate ~/mapConcept ':/' @/0*
    self.set(self.get("~/mapConcept"), str(self.get("':/'")) + str(self.get("@/0*")))

    #:concatenate ~/mapConcept ~/mapConcept* '*'
    self.set(self.get("~/mapConcept"), str(self.get("~/mapConcept*")) + str(self.get("'*'")))

    #:concatenate ~/mapConceptEnd ~/mapConcept* '/end'
    self.set(self.get("~/mapConceptEnd"), str(self.get("~/mapConcept*")) + str(self.get("'/end'")))

    #:concatenate ~/mapConceptType ~/mapConcept* '/type'
    self.set(self.get("~/mapConceptType"), str(self.get("~/mapConcept*") + str(self.get("'/type'"))))

    #:concatenate ~/mapConceptQuality ~/mapConcept* '/quality'
    self.set(self.get("~/mapConceptQuality"), str(self.get("~/mapConcept*") + str(self.get("'/quality'"))))
    
    #:concatenate ~/mapConceptQuantity ~/mapConcept* '/quantity'
    self.set(self.get("~/mapConceptQuantity"), str(self.get("~/mapConcept*") + str(self.get("'/quantity'"))))
    
    #:python
    self.set(self.get("~/mapConceptEnd*"), self.get("@/2*"))
    self.set(self.get("~/mapConceptType*"), self.get("@/1*"))
    self.set(self.get("~/mapConceptQuality*"), self.get("@/3*"))
    self.set(self.get("~/mapConceptQuantity*"), self.get("@/4*"))
