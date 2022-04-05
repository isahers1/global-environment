from element import *
from environment import *
from group import *
from integer import *
from logicObjects import *


class Proof:
    def __init__(self, label, assumption, goal=None, steps=[], justifications = []): # make goal optional
        self.label = label
        self. assumption = assumption
        self.goal = goal # this is an implies
        self.justifications = []
        self.environment = {} # add strings names to environment for parsing 
        self.depth = 0
        self.currAssumption = [goal.assum]
        self.show() 
    
    def qed(self):
        return self.goal.conc in self.steps

    def undo(self):
        self.steps = self.steps[:-1]
        self.justifications = self.justifications[:-1]
        self.show()
        
    def show(self):
        print('')
        print('Proof : ' + self.label)
        print('--------------------------------')
        for i in range(len(self.steps)):
            print(str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]))
        print('')

    def introAssumption(self, expr):
        self.steps += [expr]
        self.justifications += ['introAssumption'] 
        self.show()

    def MultElem(self, element1, element2):
        l=[]
        if isinstance(element1,Mult) and isinstance(element2, Mult):
            l=element1.products+element2.products
        elif isinstance(element1,Mult) and isinstance(element2, Mult) == False:
            l= element1.products
            l.append(element2)
        elif isinstance(element1,Mult)==False and isinstance(element2, Mult):
            l = element2.products
            l.insert(0, element1)
        else:
            l.append(element1)
            l.append(element2)
        return Mult(l)
    
    def modus(self, lineNum1, lineNum2):
        """
        modus pones: given A->B and A, the function concludes B and add it as a new line in the proof
        lineNum1 and lineNum2: one line in the proof where the person showed A->B and one line the proof where the person showed A
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Implies): 
            A = ev1.assum
            B = ev1.conc
            if A == ev2: 
                self.steps += [B]
                self.justifications += [f'Modus Ponens on {str(lineNum1)}, {str(lineNum2)}'] 
                self.show() 
        elif isinstance(ev2, Implies):
            A = ev2.assum
            B = ev2.conc
            if A == ev1: 
                self.steps += [B]
                self.justifications += [f'Modus Ponens on {str(lineNum2)}, {str(lineNum1)}'] 
                self.show()
        else:
            raise Exception (f"Neither of {str(lineNum1)}, {str(lineNum2)} are an implies statement")

    def identElimRHS(self, lineNum):
        """"
        Remove all instances of the identity from an equation
        :param lineNum: the line of the proof to be modified on the right hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        rhsevidence = evidence.RHS
        if isinstance(rhsevidence,Mult):
            l = copy.deepcopy(rhsevidence.prodcuts)
            try:
                while True:
                    l.remove(evidence.parentgroup.identity_identifier)
            except ValueError:
                pass
            return Mult(l)
        else:
            raise Exception (f"The right hand side on line {lineNum} is not a Mult object")

    def identElimLHS(self, lineNum):
        """"
        Remove all instances of the identity from an equation
        :param lineNum: the line of the proof to be modified on the left hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        lhsevidence = evidence.LHS
        if isinstance(lhsevidence,Mult):
            l = copy.deepcopy(lhsevidence.prodcuts)
            try:
                while True:
                    l.remove(evidence.parentgroup.identity_identifier)
            except ValueError:
                pass
            return Mult(l)
        else:
            raise Exception (f"The left hand side on line {lineNum} is not a Mult object")

    def inverseElimRHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the right hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum]).RHS
        if isinstance(evidence,Mult): 
            l = evidence.products.copy()
            lawApplied = False
            for i in range(len(l)-1):
                if isinstance(l[i],element) and isinstance(l[i+1],inverse) and (l[i].elementName == l[i+1].elementName):
                    group = l[i].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied=True
                    break
                elif isinstance(l[i],inverse) and isinstance(l[i+1],element) and (l[i].elementName == l[i+1].elementName):
                    group = l[i+1].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:]) # should we include 'e' in the Mult object?
                    lawApplied=True
                    break
            if lawApplied==False:
                raise Exception (f"Inverse laws can't be applied on line {lineNum}")
        self.steps += [newProducts]
        self.justifications += [f'Right hand side inverse elimination on line {lineNum}'] 
        self.show()
    
    def inverseElimLHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the left hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum]).LHS
        if isinstance(evidence,Mult): 
            l = evidence.products.copy()
            lawApplied = False
            for i in range(len(l)-1):
                if isinstance(l[i],element) and isinstance(l[i+1],inverse) and (l[i].elementName == l[i+1].elementName):
                    group = l[i].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied=True
                    break
                elif isinstance(l[i],inverse) and isinstance(l[i+1],element) and (l[i].elementName == l[i+1].elementName):
                    group = l[i+1].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.identity_identifier
                    newProducts = Mult(l[:i+1]+l[i+2:]) # should we include 'e' in the Mult object?
                    lawApplied=True
                    break
            if lawApplied==False:
                raise Exception (f"Inverse laws can't be applied on line {lineNum}")
        self.steps += [newProducts]
        self.justifications += [f'Left hand side inverse elimination on line {lineNum}'] 
        self.show()
    
    ## For all and there exists elimination
     
    def forallElim(self, lineNum, replacements): 
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, forall) == False:
            raise Exception(f"There is no forall statmenent on line {lineNum}")
        evidence.replace(replacements)
        self.steps += [evidence.expr]
        self.justifications += [f'For all elimination on line {lineNum}'] 
        self.show() 
    
    def thereexistsElim(self, lineNum, replacements): # We can only do this once!
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, thereexists) == False:
            raise Exception(f"There is no there exists statmenent on line {lineNum}")
        evidence.replace(replacements)
        self.steps += [evidence.expr]
        self.justifications += [f'There exists elimination on line {lineNum}'] 
        self.show() 

    ## Multiplication manipulation
    def leftMult (self, elem, lineNum):
        """
        Left Multiply both sides of an equation with the input element 
        :param lineNum: the equation in the proof that is to be modified 
        :param elem: the element to left Multiply with 
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq) == False:
            raise Exception (f"Line {lineNum} is not an equation")
        product = self.MultElem(elem, eq.LHS)
        result = Eq(product, self.MultElem(elem,eq.RHS), eq.parentgroup)
        self.steps += [result]
        self.justifications += ['Left multiply line {lineNum} by ' +str(elem) ] 
        self.show()

    def rightMult (self, elem, lineNum):
        """
        Right Multiply both sides of an equation with the input element 
        :param lineNum: the line in the proof that is to be modified 
        :param elem: the element to right Multiply 
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq) == False:
            raise Exception (f"Line {lineNum} is not an equation")
        product = self.MultElem(eq.LHS, elem)
        result = Eq(product, self.MultElem(eq.RHS,elem), eq.parentgroup)
        self.steps += [result]
        self.justifications += [f'Right multiply line {lineNum} by ' +str(elem)] 
        self.show()

    ##power methods 
    def breakPower(self,power):
        """
        Given an expression like e^a where a is a python integer, return a mult object equivalent to e^a
        :param power: the power to be converted to mult
        """   
        exp=power.exponent   
        element = power.element 
        multList=[]
        for i in range(exp):
            multList.append(element)
        self.steps += [Mult(multList)]
        self.justifications += ['Convert power object to mult object'] 
        self.show()

    def combinePower(self, mult):
        """
        Given a mult object with a single element, convert it to a power object (for example turning e*e*e to e^3)
        :param mult: the mult object to be converted 
        """  
        multList=mult.elemList
        e=multList[0]
        for i in multList: 
            if i != e: 
                raise Exception ("Need a single element but given multiple")
        result=power(e,len(multList)) 
        self.steps += [result]
        self.justifications += ['Convert multiplications to equivalent powers'] 
        self.show()

    def splitPowerAddition(self,power):
        """
        Simplify power objects: Given an expression e^a+b, convert to e^a*e^b. Given an expression e^a*b=(e^a)^b
        :param power: the power object with addition in exponent to be modified
        """  
        element = self.element
        exp=self.exponent
        l=exp.split("+")
        if len(l)==1:
            raise Exception ("No power addition to be split apart") 
        multList=[]
        for i in l: 
            elem=power(element,i)
            multList.append(elem)
        self.steps += [Mult(multList)]
        self.justifications += ["split up power with addition in exponents"] 
        self.show()       
             

    def splitPowerMult(self,power):
        """
        Simplify power objects: Given an expression e^a*b=(e^a)^b
        :param lineNum: the power object with mult in exponent to be modified
        """  
        element = self.element
        exp=self.exponent
        l=exp.split("*")
        if len(l)==1:
            raise Exception ("No power multiplication to be split apart") 
        elem=element
        for i in l: 
            e=power(elem,i)
            elem=e
        self.steps += [elem]
        self.justifications += ["split up power with multiplication in exponents"] 
        self.show()
    
    ## Identity and equality elimination
    def rightSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same right side, then set left sides to equal in a new line
        :param line1: the first line with same right side
        :param line2: the second line with the same right side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.RHS == l2.RHS and l1.parentgroup == l2.parentgroup:
            self.steps += [Eq(l1.LHS,l2.LHS, l1.parentgroup)]
            self.justifications += [f"Equations with same right side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            raise Exception (f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same right sides")

    def leftSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same left side, then set right sides to equal in a new line
        :param line1: the first line with same left side
        :param line2: the second line with the same left side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.LHS == l2.LHS and l1.parentgroup == l2.parentgroup:
            self.steps += [Eq(l1.RHS,l2.RHS, l1.parentgroup)]
            self.justifications += [f"Equations with same left side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            raise Exception (f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same left sides")

    def identleft(self, lineNum):
        """
        Identity elimination: find the first pair of element and the group identity return an element 
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence,Eq): 
            l = evidence.LHS.products
            l1=[]
            for i in range(len(l)-1):
                # deals with the case a*1
                # if isinstance(l[i],groupElement) and isinstance(l[i+1],ident):
                if isinstance(l[i+1],identity):
                    l1 = l[:i+1]+l[i+2:]
                    break
                # deals with the case 1*a
                # elif isinstance(l[i],ident) and isinstance(l[i+1],groupElement):
                elif isinstance(l[i],identity):
                    l1 = l[i+1:]
                    break
                # else we can't apply identity elimination 
            if l1==[]:
                raise Exception ("identity can't be applied")
            newProduct = Mult(l1)
            ret = Eq(newProduct,evidence.RHS,evidence.parentgroup)

        self.steps += [ret]
        self.justifications += ["identity elimination "] 
        self.show() 

    def identright(self, lineNum):
        """
        Identity elimination: find the first pair of element and the group identity return an element 
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence,Eq) and isinstance(evidence.arg2, Mult): 
            l = evidence.RHS.products
            l1=[]
            for i in range(len(l)-1):
                # deals with the case a*1
                # if isinstance(l[i],groupElement) and isinstance(l[i+1],ident):
                if isinstance(l[i+1],identity):
                    l1 = l[:i+1]+l[i+2:]
                    break
                # deals with the case 1*a
                # elif isinstance(l[i],ident) and isinstance(l[i+1],groupElement):
                elif isinstance(l[i],identity):
                    l1 = l[i+1:]
                    break
                # else we can't apply identity elimination 
            if l1==[]:
                raise Exception ("identity can't be applied")
            newProduct = Mult(l1)
            ret = Eq(evidence.LHS,newProduct,evidence.parentgroup)

        self.steps += [ret]
        self.justifications += ["identity elimination "] 
        self.show()

    def introReflexive(self,eq):
        """
        Introduce a reflexive equality (like x=x)
        Necessary to show something equals something else when not given
        a starting equation
        """
        if eq.LHS == eq.RHS:
            self.steps+=[eq]
            self.justifications += ["reflexive equality"] 
            self.show()
        else:
            raise Exception ("this is not reflexive")

    def reduceLogic(self, lineNum):
        """Recursively reduces a ND statement by pushing the nots in
        """
        evidence = self.steps[lineNum]
        if type(lineNum) in [And, Or, Implies, Not]:
            self.steps += [reduce(evidence)]
            self.justifications += ["logic reduction"] 
            self.show()
        else:
            raise Exception ("this is not a logic statement")

    def introCases(self, case):
        """Introduction of cases (law of excluded middle)
        """
        case1 = case
        case2 = reduce(Not(case))
        self.steps += [Or(case1, case2)]
        self.justifications += ["case introduction (LEM)"] 
        self.show()

    def introSubproof(self, assum):
        """This one returns so the user has access to the new subproof
        We will have to make show recursive to make the subproof steps show
        """
        subproof = Proof(label="Subproof", steps=[self.steps], justifications = [self.justifications])
        self.steps += [subproof]
        self.justifications += ["intro subproof"]
        return subproof

    def concludeSubproof(self, lineNum):
        """You conclude a subproof from the parent subproof
        Work in progress, we should discuss how to do this.
        """
        conc = Implies(self.assumption, self.steps[lineNum])
        return conc