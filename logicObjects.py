import copy
from dataclasses import replace

from element import *

class Mult:
    def __init__(self, elemList):
        self.products = elemList
    def __repr__(self):
        string =""
        for i in range(len(self.products)-1):
            string += str(self.products[i])
            string +=" * "
        string += str(self.products[len(self.products)-1])
        return string 
    def __eq__(self,other):
        if self.products == other.products:
            return True 
        else: 
            return False
    def __mul__(self,other):
        if isinstance(other,Mult):
            return Mult(self.products+other.products) #Mult *
        else:
            return Mult(self.products+[other]) #Mult with element

    def replace(self, var, expr):
        new_products = []
        i = 0
        #print(self.products,var.products,expr.products)
        while i < len(self.products):
                if self.products[i:i+len(var.products)] == var.products:
                    new_products += expr.products
                    i+=len(var.products)
                else:
                    new_products.append(self.products[i])
                    i+=1
        return Mult(new_products)

    
class And:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def elim(self,num):
        if num==1:
            return self.arg1
        if num==2:
            return self.arg2

class Or:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def elim(self,num,implies1,implies2):
        #If we have conclusing a subproof automatically make an implies, we can use implies in our vElim
        check1 = isinstance(implies1, Implies) and implies1.assum==self.arg1
        check2 = isinstance(implies2, Implies) and implies2.assum==self.arg2
        if check1 and check2 and implies1.conc==implies2.conc:
            return implies1.conc

class Implies: # expand a little more functionality
    def __init__(self, assum, conc):
        self.assum = assum
        self.conc = conc

    def elim(self, arg):
        if arg==self.assum:
            return self.conc

class Not:
    def __init__(self, arg):
        self.arg = arg

    def elim(self, contradiction):
        if self.arg == contradiction:
            return Bottom()
    
    def __repr__(self):
        return "Not " + str(self.arg)

class Bottom:
    def elim(self, conclusion):
        return conclusion
    
    def __repr__(self):
        return "⊥"

class In:
    def __init__(self, elem, grp):
        self.elem = elem
        self.grp = grp

    def __repr__(self):
        return str(self.elem) + " ∈ " + str(self.grp)

class Eq:
    def __init__(self,LHS,RHS,pg):
        self.LHS = LHS
        self.RHS = RHS
        self.parentgroup = pg

    def __repr__(self):
        return str(self.LHS) + ' = ' + str(self.RHS)

    def __eq__(self,other):
        if self.LHS == other.LHS and self.RHS == other.RHS:
            return True 
        elif self.LHS == other.RHS and self.RHS == other.LHS: # a=b is the same as b=a
            return True 
        else: 
            return False

    def replace(self, var, expr):
        return Eq(self.LHS.replace(var,expr), self.RHS.replace(var,expr), self.parentgroup)

def reduce(exp):
    if isinstance(exp, Eq):
        return exp
    if isinstance(exp, Not):
        if isinstance(exp.arg, Not):
            exp=reduce(exp.arg.arg) #DNE
        if isinstance(exp.arg, And):
            exp=Or(reduce(Not(exp.arg.arg1)), reduce(Not(exp.arg.arg2))) #Demorgan's Law
        if isinstance(exp.arg, Or):
            exp=And(reduce(Not(exp.arg.arg1)), reduce(Not(exp.arg.arg2))) #Demorgan's Law
    if isinstance(exp, Implies):
        if isinstance(exp.conc, Bottom):
            exp=Not(reduce(exp.assum))
    return exp

#My current vision is to have an arbitrary element class and an existential element class
#A for all is an equation including an arbitrary element, and a there exists is an equation including an existential element


class forall:
    def __init__(self, vars, g, eq): # should we check that vars is arbitrary elements?
        self.arbelems = vars # list of arbitrary elements: [x,y]
        self.group = g
        self.eq = eq 

    def __repr__(self):
        return 'forall(' + str(self.arbelems) + ' in ' + str(self.group) + ', ' + str(self.eq) +')'

    def __eq__(self,other):
        if not isinstance(other,forall):
            return False
        if len(self.arbelems)==len(other.arbelems):
            print(self,other)
            new = copy.deepcopy(self)
            replaced = new.replace(other.arbelems)
            return replaced == other.eq
        else:
            return False


    def replace(self, replacements): # replacements = ['x','y'] - strings of the elements
        if len(replacements) == len(self.arbelems):
            #if all(elem in self.group.elements for elem in replacements): # check if replacements are all normal elements of self.group
            #The scope of thee elements in a for all should be contained in that for all
            #Checking if in the group should happen at elimination and introduction
            neweq = copy.deepcopy(self.eq)
            for i in range(len(replacements)):
                 neweq = neweq.replace(Mult([self.arbelems[i]]),self.group.elements[replacements[i]]) # repeatedly replace
            return neweq
            #else:
                #print(f"Replacements contains elements that are not in {self.group}")
        else:
            print("Replacements is not the same length as the list of arbitrary elements")

class thereexists:
    def __init__(self, vars, g, eq): # should we check that vars is existential elements?
        self.existelems = vars # list of existential elements: [a,b]
        self.group = g
        self.eq = eq

    def __repr__(self):
        return 'there exists(' + str(self.existelems) + ' in ' + str(self.group) + ', such that ' + str(self.eq) + ')'

    def __eq__(self,other):
        return self.existelems == other.existelems and self.group == other.group and self.expr == other.expr

    def replace(self, replacements):
        if len(replacements) == len(self.existelems):
            if all(elem in self.group.elements for elem in replacements): # check if replacements are all normal elements of self.group
                neweq = copy.deepcopy(self.eq)
                for i in range(len(replacements)):
                    neweq = neweq.replace(self.existelems[i],replacements[i]) # repeatedly replace
                return neweq
            else:
                print(f"Replacements contains elements that are not in {self.group}")
        else:
            print("Replacements is not the same length as the list of existential elements")

## Unique class

class uniqueElementProperty:
    def __init__ (self, prpty, pg):
        self.property = prpty
        self.group = pg


## Special types of elements/groups

class identity(element):
    def __init__(self, pg):
        elementName = pg.identity_identifier
        super().__init__(elementName, pg)
        lhs = Mult([arbitrary('x',pg),elementName]) # self or elementName?
        rhs = Mult([arbitrary('x',pg)])
        eq = Eq(lhs,rhs,pg)
        idnty = forall([arbitrary('x',pg)], pg, eq)
        pg.addElementProperty(idnty,elementName)

class inverse(element):
    def __init__(self, elementName, pg):
        inverseName = elementName + "^(-1)"
        super().__init__(inverseName, pg)
        lhs = Mult([inverseName,elementName]) # self or elementName?
        rhs = Mult([pg.identity_identifier])
        inverseEq = Eq(lhs,rhs,pg)
        pg.addGroupProperty(inverseEq, "Inverse of " + elementName)
