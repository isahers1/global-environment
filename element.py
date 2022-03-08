"""
QUESTIONS:

1. How do we deal with element properties that apply to the whole group? Should this be a group property, element property, or both?
2. Break apart elements that are multiplied together?
3. Way to do induction?
"""


class element:
    elementName = ""
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
        return self.elementName == other.elementName

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



# WE NEED TO AGREE ON EQUATION/STATEMENT/PROPERTY CLASSES BEFORE IMPLEMENTING THE BELOW CLASSES
"""
class identity(element):
    def __init__(self, elementName, pg):
        super().__init__(elementName, pg)
        lh = equation([element('x',pg),'*',self],pg)
        rh = equation([element('x',pg)],pg)
        stmnt = statement(lh,rh,pg)
        idnty = forall([element('x',pg)],stmnt,pg)
        pg.addElementProperty(idnty,elementName) # need to change

class generator(element):
    def __init__(self, elementName, pg):
        super().__init__(elementName, pg)
        pg = self.parentGroups[0]
        lh = equation([element('x',pg)],pg)
        rh = equation([self,'**',1],pg) # need to change 1 to be there exists an integer k
        stmnt = statement(lh,rh,pg) # also how can I add '**' as an operator?
        gnrtr = forall([element('x',pg)],stmnt,pg)
        pg.addElementProperty(gnrtr, elementName) # need to change

class inverse(element):
    def __init__(self, elementName, pg):
        if elementName not in pg.elements:
            raise Exception("You cannot create an inverse for an element that doesn't exist!")
        else:
            super().__init__(elementName + "^-1", g)
            lh = equation([pg.elements[elementName],'*',self],pg)
            rh = equation([pg.elements[pg.identity_identifier]],pg)
            stmnt = statement(lh,rh,pg)
            pg.addElementProperty(stmnt ,elementName) # need to change
"""

