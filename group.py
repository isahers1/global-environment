exec(compile(source=open('element.py').read(), filename='element.py', mode='exec'))

class group:
    # TRUTHS for all classes - need to add more here
    identity_identifier = 'e'
    elements = {}
    groupProperties = {} 
    binaryOperator = ""
    groupName = ""

    def __init__(self, name, binOp, additionalGroupProperties = None):
        self.groupName = name
        self.binaryOperator = binOp
        self.elements.update({self.identity_identifier:identity(self.identity_identifier,self)})
        if additionalGroupProperties != None:
            self.groupProperties.update(additionalGroupProperties)

    # basic functions

    def __repr__(self):
        return "group(" + self.groupName + ")"
    def __eq__(self,other):
        return self.groupName == other.groupName
    def __mul__(self,other): # group cartesian product. Worry about this later
        newName = self.groupName + "x" + other.groupName
        newProperties = list(set(self.properties) & set(other.properties))
        return group(newName, [self.binaryOperator,other.binaryOperator], newProperties)

    # group functions

    # declare new element in group with elementName
    def newElement(self,elementName):
        if elementName not in self.elements:
            self.elements.update({elementName:element(elementName,self)})
        else:
            print("Sorry, that element already exists!")

    # create new element that is elem1 operated on with elem2
    def mulElements(self, elem1, elem2): # should this return an equation?
        if elem1 == self.identity_identifier or elem2 == self.identity_identifier:
            print("Sorry, multiplying by the identity doesn't do anything!")
        else:
            try:
                gelem1 = self.elements[elem1]
                gelem2 = self.elements[elem2]
                result = gelem1.mult(gelem2, self) # need to specify which group we are multiplying in
                self.elements.update({result:element(result,self)}) # is this the right?
            except:
                print("Sorry, one or both of these elements are not in the group!")

    def addGroupProperty(self, property, propertyName):
        self.groupProperties[propertyName] = property