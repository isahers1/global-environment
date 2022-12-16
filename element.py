"""
QUESTIONS:

1. How do we deal with element properties that apply to the whole group? Should this be a group property, element property, or both?
2. Break apart elements that are multiplied together?
3. Way to do induction?
"""


class element:
    elementName = ""
    elementOrder = None
    parentGroups = []
    elementProperties = {}

    def __init__(self, elementName, g, elementProperties = None):
        self.elementName = elementName
        self.parentGroups = [g]
        if elementProperties != None:
            self.elementProperties.update(elementProperties)

    def __repr__(self):
        return self.elementName

    def __eq__(self,other):
        try:
            return self.elementName == other.elementName
        except:
            return False

    def mult(self,other, group): # this is just for representation
        binOp = group.binaryOperator
        if binOp in other.elementName and '(' != other.elementName[0]:
            return self.elementName + binOp + "(" +other.elementName + ")"
        elif binOp in self.elementName and ')' != self.elementName[-1]:
            return "(" + self.elementName + ")" + binOp + other.elementName
        else:
            
            return self.elementName + binOp + other.elementName

    def addToGroup(self, group):
        self.parentGroups.append(group) # check if isinstance group?

    def fullDescription(self):
        groupl = [g.groupName for g in self.parentGroups]
        return self.elementName + " in groups " + groupl

    def addProperty(self, property, propertyName):
        self.elementProperties[propertyName] = property
    
    def order(self):
        return self.elementOrder

#My current vision is to have an arbitrary element class and an existential element class
#A for all is an equation including an arbitrary element, and a there exists is an equation including an existential element

class existential(element):
    def __init__(self, elementName, pg):
        super().__init__(elementName, pg)
    
    def fullDescription(self):
        return  "Arbitrary element " + self.elementName + " in group" + self.parentGroups[0].groupName # can only belong to one group

class arbitrary(element):
    def __init__(self, elementName, pg):
        super().__init__(elementName, pg)
    
    def fullDescription(self):
        return  "Existential element " + self.elementName + " in group" + self.parentGroups[0].groupName # can only belong to one group


## need to add: generator