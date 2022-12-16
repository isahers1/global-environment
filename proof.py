import os, sys
from re import L

from element import *
from group import *
from integer import *
from logicObjects import *
from power import *
from tkinter import messagebox
from pylatex import Document, Section, Subsection, Command, Enumerate
from pylatex.utils import italic, NoEscape
import sympy

def replacePower(mult, var, expr):
                    new_products = []
                    i = 0
                    while i < len(mult.products):
                        if isinstance(mult.products[i],power):
                            if repr(mult.products[i].exponent) == var:
                                power_temp = copy.deepcopy(mult.products[i])
                                try:
                                    power_temp.exponent = int(expr)
                                except:
                                    power_temp.exponent = integer(expr)
                                new_products.append(power_temp)
                                i+=1
                            else:
                                new_products.append(mult.products[i])
                                i+=1
                        else:
                                new_products.append(mult.products[i])
                                i+=1
                        return new_products

def integerReplace(value, var, expr):
   
    if isinstance(value, Order):
        print(value, var)
        if value == var:
            newValue = expr
        else:
            newValue = value
    elif not isinstance(value,Order):
        value = value.value
        newValue = ""
        i = 0
        while i < len(value):
            if value[i:i+len(var.value)] == var.value:
                    newValue += expr.value
                    i+=len(var.value)
            else:
                newValue += value[i]
                i+=1
        newValue = integer(newValue)
    return newValue

def helperMergePower(input):
            while isinstance(input.element, power) or isinstance(input.element, inverse):
                if isinstance(input.element, power):
                    input = power(input.element.element, input.exponent * input.element.exponent)
                else:
                    input = (power(input.element.group.elements[input.element.elementName], input.exponent * (-1)))
            return input

class Proof:
    def __init__(self, label, assumption, goal=None, steps=[], justifications = [], depth=0, linestart=0): # make goal optional
        self.linestart = linestart
        self.label = label
        self.depth = depth
        self.assumption = assumption
        self.goal = goal # this is an implies
        self.steps = steps
        self.justifications = justifications
        self.env = {}
        self.subproof = None
        self.allgroup = group('U','*')

    
    def qed(self, lineNum):
        if self.goal == self.steps[lineNum]:
            self.steps+=["."]
            self.justifications += ["QED"]
            self.show()
        else:
            print("This is not the same as the goal")

    def undo(self):
        self.steps = self.steps[:-1]
        self.justifications = self.justifications[:-1]
        self.show()
    
    def writeLaTeXfile(self):
        doc = Document(page_numbers=False)
        doc.preamble.append(Command('title', self.label))
        doc.append(NoEscape(r'\maketitle'))
        doc.append(italic("Proof:"))
        with doc.create(Enumerate()) as enum:
            doc.append(NoEscape(r"\addtocounter{enumi}{-1}"))
            for i in range(len(self.steps)):
                if isinstance(self.steps[i],str):
                    enum.add_item(NoEscape(self.steps[i]+r"\hfill"))
                else:
                    enum.add_item(NoEscape("$"+self.steps[i].toLaTeX()+r"$\hfill"))
                enum.append(" by " + str(self.justifications[i]))
        doc.generate_tex(self.label)
        doc.generate_pdf(self.label)

    def showReturn(self):
        showstr = ""
        if self.depth==0:
            showstr += 'Proof : '
            showstr += self.label
            showstr += '\n'
            showstr += '--------------------------------'
            showstr += '\n'
        else:
            showstr += 'Subproof : assume '
            showstr += str(self.assumption)
            showstr += '\n'
            showstr += '--------------------------------'
            showstr += '\n'
        i = self.linestart
        while i < len(self.steps):
            if isinstance(self.steps[i],Proof):
                showstr += self.steps[i].show()
                i+=len(self.steps[i].steps)-self.steps[i].linestart-1
            else:
                linestr = "\t"*self.depth + str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]) + '\n'
                showstr += linestr
            i+=1 
        return showstr

    def show(self):
        if self.depth==0:
            print('')
            print('Proof : ' + self.label)
            print('--------------------------------')
        else:
            print('Subproof : assume ' + str(self.assumption))
            print('--------------------------------')
        i = self.linestart
        while i < len(self.steps):
            if isinstance(self.steps[i],Proof):
                self.steps[i].show()
                i+=len(self.steps[i].steps)-self.steps[i].linestart-1
            else:
                print("\t"*self.depth + str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]))
            i+=1

    def introAssumption(self, expr):
        self.steps += [expr]
        self.justifications += ['introAssumption'] 
        self.show()
    
    def introGroup(self, groupName):
        self.steps += [group(groupName)]
        self.justifications += ["introGroup"]
        self.show()

    def introGroup(self, grp):
        self.steps += [grp]
        self.justifications += ["introGroup"]
        #deal with environments
        self.env[grp.groupName] = grp
        self.show()
    
    def accessAssumption(self):
        self.steps += [self.assumption]
        self.justifications += ["Accessed Assumption"]
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


    def substituteRHS(self, lineNum1, lineNum2):
        """
        Given a representation of a mult object, replace all instances of it in one equation
        :param lineNum1: Line to substitute into
        :param lineNum2: Line with substitutsion of x = y, will replace all instances of x with y in lineNum1
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Eq):
            if isinstance(ev2, Eq):
                replacement = ev1.replace(ev2.LHS,ev2.RHS)
                self.steps += [replacement]
                self.justifications += [f'Replaced all instances of {ev2.LHS} with {ev2.RHS} on line {lineNum1}']
                self.show()
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")

    def substituteLHS(self, lineNum1, lineNum2):
        """
        Given a representation of a mult object, replace all instances of it in one equation
        :param lineNum1: Line to substitute into
        :param lineNum2: Line with substitutsion of y = x, will replace all instances of y with x in lineNum1
        """
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev1, Eq):
            if isinstance(ev2, Eq):
                replacement = ev1.replace(ev2.RHS,ev2.LHS)
                self.steps += [replacement]
                self.justifications += [f'Replaced all instances of {ev2.RHS} with {ev2.LHS} on line {lineNum1}']
                self.show()
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")
    
    def modus(self, lineNum1, lineNums): # lineNums because multiple assumptions may be neccessary (I think)
        """
        modus pones: given A->B and A, the function concludes B and add it as a new line in the proof
        :param lineNum1 and lineNum2: one line in the proof where the person showed A->B and one line the proof where the person showed A
        """
        ev1 = self.steps[lineNum1]
        if isinstance(lineNums, list):
            ev2 = []
            for line in lineNums:
                ev2 += self.steps[line]
            if isinstance(ev1, Implies): 
                A = ev1.assum
                B = ev1.conc
                if A == ev2: 
                    self.steps += [B]
                    self.justifications += [f'Modus Ponens on {str(lineNum1)}, {str(lineNums)}'] 
                    self.show() 
            else:
                print('Proof Error',f"Line {str(lineNum1)} is not an implies statement")
        else:
            print('Proof Error',"The second argument should be a list, maybe you only have one assumption - make sure to put it into a singleton list")

    def inverseElimRHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the right hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence,Eq): 
            l = evidence.RHS.products.copy()
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
                print('Proof Error',f"Inverse laws can't be applied on line {lineNum}")
            else:
                self.steps += [newProducts]
                self.justifications += [f'Right hand side inverse elimination on line {lineNum}'] 
                self.show()
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")
        

    def inverseElimLHS(self,lineNum):
        """
        finds the first pair of group element and its inverse and returns the group element
        :param lineNum: the line of the proof to be modified on the left hand side
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence,Eq): 
            l = evidence.LHS.products.copy()
            lawApplied = False
            for i in range(len(l)-1):
                if isinstance(l[i],element) and isinstance(l[i+1],inverse) and (l[i].elementName == l[i+1].elementName):
                    group = l[i].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.elements[group.identity_identifier]
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied=True
                    break
                elif isinstance(l[i],inverse) and isinstance(l[i+1],element) and (l[i].elementName == l[i+1].elementName):
                    group = l[i+1].parentGroups[0] # how to deal with multiple groups?
                    l[i] = group.elements[group.identity_identifier]
                    newProducts = Mult(l[:i+1]+l[i+2:]) # should we include 'e' in the Mult object?
                    lawApplied=True
                    break
            if lawApplied==False:
                print('Proof Error',f"Inverse laws can't be applied on line {lineNum}")
            else:
                self.steps += [Eq(newProducts,evidence.RHS,evidence.group)]
                self.justifications += [f'Left hand side inverse elimination on line {lineNum}'] 
                self.show()
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")
    
    ## For all and there exists elimination
     
    def forallElim(self, lineNum, replacements): 
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input
         variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, forall):
            expr = evidence.replace(replacements)
            self.steps += [expr]
            self.justifications += [f'For all elimination on line {lineNum}'] 
            self.show() 
        else:
            print('Proof Error',f"There is no forall statmenent on line {lineNum}")
            
    
    def thereexistsElim(self, lineNum, replacements): # We can only do this once!
        """
        Given an expression forall(a,b,statement), forallElim substitutes a with another input variable to create a new forall statement
        :param lineNum: The line number of the line that showed the original forall statement 
        :param replacements: the list of elements to replace the existential elements
        """
        evidence = copy.deepcopy(self.steps[lineNum])
        if isinstance(evidence, thereexists):
            expr = evidence.replace(replacements)
            self.steps += [expr]
            self.justifications += [f'There exists elimination on line {lineNum}'] 
            self.show() 
        else:
            print('Proof Error', f"There is no there exists statmenent on line {lineNum}")
            

    ## Multiplication manipulation
    def leftMult(self, elemName, lineNum):
        """
        Left Multiply both sides of an equation with the input element 
        :param lineNum: the equation in the proof that is to be modified 
        :param elemName: the name of the element to left Multiply with 
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq): 
            if elemName in eq.group.elements:
                elem = eq.group.elements[elemName]
                product = self.MultElem(elem, eq.LHS)
                result = Eq(product, self.MultElem(elem,eq.RHS), eq.group)
                self.steps += [result]
                self.justifications += ['Left multiply line {lineNum} by ' +str(elem) ] 
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    def rightMult (self, elemName, lineNum):
        """
        Right Multiply both sides of an equation with the input element 
        :param lineNum: the line in the proof that is to be modified 
        :param elemName: the name of the element to right Multiply with
        """
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                elem = eq.group.elements[elemName]
                product = self.MultElem(eq.LHS, elem)
                result = Eq(product, self.MultElem(eq.RHS, elem), eq.group)
                self.steps += [result]
                self.justifications += ['Right multiply line {lineNum} by ' +str(elem) ] 
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")


    def rightMultInverse (self, elemName, lineNum):
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                product = self.MultElem(eq.LHS,inverse(elemName,eq.group))
                result = Eq(product, self.MultElem(eq.RHS, inverse(elemName,eq.group)), eq.group)
                self.steps += [result]
                self.justifications += ['Right multiply line {lineNum} by '  + elemName]
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    def leftMultInverse (self, elemName, lineNum):
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq, Eq):
            if elemName in eq.group.elements:
                product = self.MultElem(inverse(elemName,eq.group), eq.LHS)
                result = Eq(product, self.MultElem(inverse(elemName,eq.group), eq.RHS), eq.group)
                self.steps += [result]
                self.justifications += [f'Right multiply line {lineNum} by'  + elemName]
                self.show()
            else:
                print('Proof Error', "The element " + elemName + " is not in the " + str(eq.group))
        else:
            print('Proof Error', f"Line {lineNum} is not an equation")

    def rightMultPower(self, eleName, exp, lineNum):
        eq = copy.deepcopy(self.steps[lineNum])
        if isinstance(eq,Eq):
            if eleName in eq.group.elements:
                if not isinstance(exp,integer):
                    exp = integerExpression(exp)
                multiplier = power(eq.group.elements[eleName],exp)
                product = self.MultElem(eq.LHS, multiplier)
                result = Eq(product, self.MultElem(eq.RHS, multiplier),eq.group)
                self.steps += [result]
                self.justifications += [f'Right multiply line {lineNum} by {multiplier}']
                self.show()

    ##power methods 
    def breakPower(self,input):
        """
        Given an expression like e^a where a is a python integer, return a mult object equivalent to e^a
        :param power: the power to be converted to mult
        """  
        if isinstance(input,power):  
            exp=input.exponent   
            element = input.element 
            multList=[]
            for i in range(exp):
                multList.append(element)
            self.steps += [Mult(multList)]
            self.justifications += ['Convert power object to mult object'] 
            self.show()
        else:
            print('Proof Error',f"Expected a power object but received type {type(input)}")

    def combinePower(self, mult):
        """
        Given a mult object with a single element, convert it to a power object (for example turning e*e*e to e^3)
        :param mult: the mult object to be converted 
        """  
        if isinstance(mult,Mult): 
            multList=mult.elemList
            e=multList[0]
            singletonCheck = True
            for i in multList: 
                if i != e: 
                    singletonCheck = False
            if singletonCheck == False:
                print ('\n' +"Need a single element but given multiple")
            else:
                result=power(e,len(multList)) 
                self.steps += [result]
                self.justifications += ['Convert multiplications to equivalent powers'] 
                self.show()
        else:
            print('Proof Error',f"Expected a Mult object but received type {type(mult)}")

    def splitPowerAddition(self,input):
        """
        Simplify power objects: Given an expression e^a+b, convert to e^a*e^b. Given an expression e^a*b=(e^a)^b
        :param power: the power object with addition in exponent to be modified
        """  
        if isinstance(input, power):            
            element = input.element
            exp=input.exponent
            l=exp.split("+")
            if len(l)==1:
                print('Proof Error',"No power addition to be split apart")
            else:
                multList=[]
                for i in l: 
                    elem=power(element,i)
                    multList.append(elem)
                self.steps += [Mult(multList)]
                self.justifications += ["Split up power with addition in exponents"] 
                self.show()          
        else:
            print('Proof Error',f"Expected a power object but received type {type(input)}")     
             

    
    
    ## Identity and equality elimination
    def rightSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same right side, then set left sides to equal in a new line
        :param line1: the first line with same right side
        :param line2: the second line with the same right side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.RHS == l2.RHS and l1.group == l2.group:
            self.steps += [Eq(l1.LHS,l2.LHS, l1.group)]
            self.justifications += [f"Equations with same right side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            print('Proof Error',f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same right sides")

    def leftSidesEq(self, lineNum1, lineNum2):
        """
        If two sides have the same left side, then set right sides to equal in a new line
        :param line1: the first line with same left side
        :param line2: the second line with the same left side
        """
        l1 = self.steps[lineNum1]
        l2 = self.steps[lineNum2]
        if l1.LHS == l2.LHS and l1.group == l2.group:
            self.steps += [Eq(l1.RHS,l2.RHS, l1.group)]
            self.justifications += [f"Equations with same left side on lines {str(lineNum1)}, {str(lineNum2)}"]
            self.show()
        else:
            print('Proof Error',f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same left sides")

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
                print('Proof Error',"Identity can't be applied")
            else:
                newProduct = Mult(l1)
                ret = Eq(newProduct,evidence.RHS,evidence.group)
                self.steps += [ret]
                self.justifications += ["identity elimination "] 
                self.show() 
        else: 
            print('Proof Error',f"Expected an equation on line {lineNum} but received {type(evidence)}")

        
    def identright(self, lineNum):
        """
        Identity elimination: find the first pair of element and the group identity return an element 
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence,Eq): 
            l = evidence.RHS.products
            print(type(l[0]),type(l[1]))
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
                print ('\n' + "Identity can't be applied")
            else:
                newProduct = Mult(l1)
                ret = Eq(evidence.LHS,newProduct,evidence.group)
                self.steps += [ret]
                self.justifications += ["identity elimination "] 
                self.show()
        else: 
            print('Proof Error', f"Expected an equation on line {lineNum} but received {type(evidence)}")

        

    def introReflexive(self,name,G):
        """
        Introduce a reflexive equality (like x=x)
        Necessary to show something equals something else when not given
        a starting equation
        :param eq: The equality you want to introduce
        """
        self.steps+=[Eq(name,name,G)]
        self.justifications += ["reflexive equality"] 
        self.show()
        # if eq.LHS == eq.RHS:
        #     self.steps+=[eq]
        #     self.justifications += ["reflexive equality"] 
        #     self.show()
        # else:
        #     print('Proof Error', "This is not reflexive")

    def reduceLogic(self, lineNum):
        """
        Recursively reduces a ND statement by pushing in the nots
        :param lineNum: the line of the proof to be modified 
        """
        evidence = self.steps[lineNum]
        if type(lineNum) in [And, Or, Implies, Not]:
            self.steps += [reduce(evidence)]
            self.justifications += ["logic reduction"] 
            self.show()
        else:
            print('Proof Error', "This is not a logic statement")

    def introCases(self, case):
        """
        Introduction of cases (law of excluded middle)
        :param case: the equation/logical statement of one case (the other is a not of that) 
        """
        case1 = case
        case2 = reduce(Not(case))
        self.steps += [Or(case1, case2)]
        self.justifications += ["Case introduction (LEM)"] 
        self.show()

    def introSubproof(self, assum):
        """
        WIP
        This one returns so the user has access to the new subproof
        We will have to make show recursive to make the subproof steps show
        :param assum: the assumption for the subproof
        """
        subproof = Proof(label="Subproof", assumption=assum, steps=copy.deepcopy(self.steps), justifications=copy.deepcopy(self.justifications), depth=self.depth+1, linestart=len(self.steps))
        self.show()
        self.steps+=[subproof]
        self.justifications+=["IntroSubproof"]
        return subproof

    def concludeSubproof(self, lineNum):
        """
        WIP
        You conclude a subproof from the parent subproof
        Work in progress, we should discuss how to do this.
        :param lineNum: the conclusion of the subproof to turn into an implies
        """
        evidence = self.steps[-1]
        if isinstance(evidence, Proof):
            conc = Implies(evidence.assumption,evidence.steps[lineNum])
            self.steps += [None]*(len(evidence.steps)-evidence.linestart-1)
            self.justifications += [None]*((len(evidence.steps))-evidence.linestart-1)
            self.steps += [conc]
            self.justifications += ["Conclusion of subproof"]
            self.show()
        else:
            print("You can only conclude a subproof right after one")
        

    def introElement(self,G, name):
        """
        Introduces an arbitrary element in G
        Can be used as evidence for a forall introduction
        :param G: the group the elemen is in
        :param name: the name of the new element
        """
        if G.contains(name):
            print('Proof Error', f"{name} is already in {G}")
        else:
            self.env[name] = G.newElement(name)
            self.steps += [In(name, G)]
            self.justifications += ["Introducing an arbitrary element"]
            self.show()
    
    def forAllIntroduction(self, equationLine, vars, elemIntroLines):
        '''
        Creates a for all from an equation with arbitrary variables
        :param equationLine: the equation
        :param vars: the names of the arbitrary variables
        :param elemIntroLines: the lines of the introductions of the variables (to show they are arbitrary)
        '''
        evidence = copy.deepcopy(self.steps[equationLine]) # Mo, do you need this?
        G = self.steps[elemIntroLines[0]].group
        #Checking that the lines introduce the arbitrary variables, and that the variables are all in the same group
        for i in range(len(vars)):
            v = vars[i]
            l = elemIntroLines[i]
            if self.steps[l].elem!=vars[i]:
                print('Proof Error', f'Line {l} does not introduce variable {v}')
            elif self.steps[l].group!=G:
                print('Proof Error', f'Element {v} is not in group {G}')
            else:
                #If you make it here, this is a valid for all intro
                self.steps+=[forall(vars,G,evidence)]
                self.justifications+=["For all introduction"]
                self.show()
                return

    def closure(self,G,a,b):
        '''
        Introduces ab as an element of G by closure
        :param G: the group a,b are in
        :param a: element a
        :param b: element b
        '''
        if G.contains(a) and G.contains(b):
            G.mulElements(a,b)
            self.steps+=[In(Mult([a,b]),G)]
            self.justifications+=["Closure"]
            self.show()
        else:
            if not G.contains(a):
                print('Proof Error',f"{a} is not in {G}")
            else:
                print('Proof Error',f"{b} is not in {G}")

    def cancelRight(self, lineNum, mult):
        '''
        Cancels element from right side of multiplication if it exists 
        :param lineNum: the line where the equation resides
        :param mult: the list of elements to eliminate
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhselems = evidence.RHS.products
            lhselems = evidence.LHS.products
            l = -1*len(mult)
            if rhselems[l:] == mult and lhselems[l:] == mult:
                self.steps += [Eq( Mult(lhselems[:l]), Mult(rhselems[:l]) , evidence.group )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print('Proof Error',f"It seems like the right hand sides on line {lineNum} are not equal to {mult}")
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")

    def cancelLeft(self, lineNum, mult):
        '''
        Cancels element from left side of multiplication if it exists 
        :param lineNum: the line where the equation resides
        :param mult: the list of elements to eliminate
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhselems = evidence.RHS.products
            lhselems = evidence.LHS.products
            l = len(mult)
            if rhselems[:l] == mult and lhselems[:l] == mult:
                self.steps += [Eq( Mult(lhselems[l:]), Mult(rhselems[l:]) , evidence.group )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print('Proof Error',f"It seems like the left hand sides on line {lineNum} are not equal to {mult}")
        else:
            print('Proof Error',f"It doesn't seem like line {lineNum} contains an equation")

    def switchSidesOfEqual(self, lineNum):
        '''
        Switches an equality like x=y to become y=x
        :param lineNum: the line where the equality to be flipped is on 
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhs = evidence.RHS
            lhs = evidence.LHS
            self.steps += [Eq(rhs , lhs , evidence.group )]
            self.justifications += [f"Switched sides of line {lineNum}"]
            self.show()
        else:
            print('Proof Error',f"Hmm, it doesn't look like line {lineNum} isn't an equality")
        
    def notElim(self, lineNum1, lineNum2):
        '''
        Eliminate a not into a contradiction
        :param lineNum1: the line containing the not statement
        :param lineNum2: the line which has the real statement
        '''
        evidence1 = self.steps[lineNum1]
        if isinstance(evidence1, Not):
            result = evidence1.elim(self.steps[lineNum2])
            self.steps += [result]
            self.justifications += [f'Contradiction from lines {lineNum1} and {lineNum2}']
            self.show()
        else:
            print('Proof Error',f"The statement on line {lineNum1} isn't a Not statement")

    def impliesIntroduction(self, lineNumsAssums, lineNumConc): # needs work, a lot of it
        '''
        Introduce an implication based on assumptions and a conclusion
        :param lineNumsAssums: the lines containing the assumptions
        :param lineNumConc: the line to conclude
        '''
        assums = []
        for line in lineNumsAssums:
            assums.append(self.steps[line])
        self.steps += [Implies(assums,self.steps[lineNumConc])]
        self.justifications += [f"Introduced implies based on assumptions on lines {lineNumsAssums} to conclude line {lineNumConc}"]
        self.show()

    def andElim(self, lineNum, n):
        '''
        Eliminate a not into a contradiction
        :param lineNum1: the line containing the not statement
        :param lineNum2: the line which has the real statement
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, And):
            if n==1:
                self.steps += [evidence.arg1]
                self.justifications += ["And elimination"]
                self.show()
            elif n==2:
                self.steps += [evidence.arg2]
                self.justifications += ["And elimination"]
                self.show()
            else:
                print('Proof Error',"You must choose argument 1 or 2")
        else:
            print('Proof Error',f"The statement on line {lineNum} isn't an And statement")
    
    def introInverse(self, G, name):
        if type(name) == str:
            if not G.contains(name):
                print('Proof Error', f"{name} is not defined")
                return
        else:
            for x in name.products:
                if not G.contains(x):
                   print('Proof Error', f"{x} is not defined")
                   return
        if type(name) == str:
            lhs = self.MultElem(inverse(name,G),G.elements[name])
            
        else:
            name_ = Mult([G.elements[x] for x in name.products])
            lhs = self.MultElem(inverse(name_,G),name_)
        rhs = Mult([G.elements["e"]])
        self.steps += [Eq(lhs,rhs,G)]
        self.justifications += ["Introducing the inverse of an element"]
        self.show()

    def introOrder(self, G, name, order):
        # if isinstance(name,inverse):
        #     eleName = str(name)
        #     elem = name
        # else:
        #     eleName = name
        #     elem = G.elements[name]
        if isinstance(name,inverse):
            name = str(name)
        if name in G.elements:
            G.elements[name].elementOrder = order
            self.steps += [Eq(Order(name),integer(order),G)]
            self.justifications += [f"Introduce order of an element"]
            self.show()  
        else:
            print(f"Proof Error: {name} not found")
    
    def orderProperty(self, G, name):
        if isinstance(name,inverse):
            name = str(name)
        if name in G.elements:
            elem = G.elements[name]
            if elem.elementOrder:
                lhs = Mult([power(elem, elem.elementOrder)])
                rhs = Mult([G.elements["e"]])
                eq = Eq(lhs,rhs,G)
                self.steps += [eq]
                self.justifications += ["Order property"]
                self.show() 
            else:
                print('Proof Error', f"order of {elem} is not defined")
        else:
            print('Proof Error', f'Element {elem} is not in group {G}')

            
    
    def introInteger(self, G, integername):
        G.integers.update({integername:integer(integername)})
        self.steps += [f"introduce integer {integername}"]
        self.justifications += ["Introducing an integer"]
        self.show()
    
    # combine power with same base and turn a^0 to e
    def powerSimplifyLeft(self, lineNum):
        # combine power of same base
        eq = copy.deepcopy(self.steps[lineNum])
        group = eq.group
        if isinstance(eq,Eq):
            lawApplied = False
            l = eq.LHS.products.copy()
            for i in range(len(l)-1):
                if isinstance(l[i],power) and isinstance(l[i+1],power) and (l[i].element == l[i+1].element):
                    l[i] = l[i] * l[i+1]
                    newProducts = Mult(l[:i+1]+l[i+2:])
                    lawApplied = True
                    break
        for i in range(len(l)):
            if isinstance(l[i],power) and isinstance (l[i].exponent, int) and (l[i].exponent == 0):
                group = l[i].element.parentGroups[0]
                l[i] = group.elements[group.identity_identifier]
                newProducts = Mult(l)
                lawApplied = True
        if lawApplied == True:
            self.steps += [Eq(newProducts,eq.RHS,eq.group)]
            self.justifications += [f'Power simplified on line {lineNum}'] 
            self.show()
        else:
            print("law can't be applied")


    def insertIntegerEquation(self,expr):
        lhs, rhs = expr.split("=")
        if (sympy.simplify(lhs)) == (sympy.simplify(rhs)):
            self.steps += [Eq(lhs,rhs,self.allgroup)]
            self.justifications += ['introduce integer equation'] 
            self.show()
        else:
            print("wrong equation")

    #substitute for the exponent, work only if lineNum2 has integer equation
    def substituteIntegerRHS(self, lineNum1, lineNum2):
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev2, Eq):
            if isinstance(ev1, Eq) and isinstance(ev1.LHS,Mult):

                new_products_lhs = replacePower(ev1.LHS, ev2.LHS, ev2.RHS)
                new_products_rhs = replacePower(ev1.RHS, ev2.LHS, ev2.RHS)
                
                eq = Eq(Mult(new_products_lhs), Mult(new_products_rhs), ev1.group)
                self.steps += [eq]
                self.justifications += [f'Replaced all instances of {ev2.LHS} with {ev2.RHS} on line {lineNum1}']
                self.show()
            elif isinstance(ev1, Eq) or isinstance(ev1, Inequality):


                valueLHS = integerReplace(ev1.LHS.value, ev2.LHS, ev2.RHS)
                valueRHS = integerReplace(ev1.RHS.value, ev2.LHS, ev2.RHS)

                if isinstance(ev1, Eq):
                    result = Eq(valueLHS, valueRHS, self.allgroup)
                else:
                    result = Inequality(valueLHS, valueRHS, ev1.sign)
                self.steps += [result]
                self.justifications += [f'Replaced all instances of {ev2.LHS} with {ev2.RHS} on line {lineNum1}']
                self.show()
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")

    #substitute for the exponent, work only if lineNum2 has integer equation
    def substituteIntegerLHS(self, lineNum1, lineNum2):
        ev1 = self.steps[lineNum1]
        ev2 = self.steps[lineNum2]
        if isinstance(ev2, Eq):
            if isinstance(ev1, Eq) and isinstance(ev1.LHS,Mult):
                new_products_lhs = replacePower(ev1.LHS, ev2.RHS, ev2.LHS)
                new_products_rhs = replacePower(ev1.RHS, ev2.RHS, ev2.LHS)
                eq = Eq(Mult(new_products_lhs), Mult(new_products_rhs), ev1.group)
                self.steps += [eq]
                self.justifications += [f'Replaced all instances of {ev2.LHS} with {ev2.RHS} on line {lineNum1}']
                self.show()
            elif isinstance(ev1, Eq) or isinstance(ev1, Inequality):

                valueLHS = integerReplace(ev1.LHS, ev2.RHS, ev2.LHS)
                valueRHS = integerReplace(ev1.RHS, ev2.RHS, ev2.LHS)

                if isinstance(ev1, Eq):
                    result = Eq(valueLHS, valueRHS, self.allgroup)
                else:
                    result = Inequality(integer(valueLHS), integer(valueRHS), ev1.sign)
                self.steps += [result]
                self.justifications += [f'Replaced all instances of {ev2.RHS} with {ev2.LHS} on line {lineNum1}']
                self.show()
                
            else:
                print('Proof Error',f"The statement on line {lineNum2} is not an equality, substitutition is not possible")
        else:
            print('Proof Error',f"The statement on line {lineNum1} is not an equality, substitutition is not possible")


    def mergePowerMult(self,lineNum):

        
        
        eq = self.steps[lineNum]
        lhs = eq.LHS.products
        rhs = eq.RHS.products
        newLhsList = []
        newRhsList = []
        merge = False
        for elem in lhs:
            if isinstance(elem, power) == True:       
               elem = helperMergePower(elem)
               merge = True
            newLhsList.append(elem)
        
        for elem in rhs:
            if isinstance(elem, power) == True:       
               elem = helperMergePower(elem)
               merge = True
            newRhsList.append(elem)
        newLhs = Mult(newLhsList)
        newRhs = Mult(newRhsList)
        newEq = Eq(newLhs, newRhs, eq.group)
        if merge == True:
            self.steps += [newEq]
            self.justifications += ["Split up power with multiplication in exponents"] 
            self.show()
        else:
            print('Warning',f"no power can be splitted")

        
    def splitPowerMult(self,lineNum):
        def helperSplitPower(input):
            element = input.element
            exp=input.exponent
            l=str(exp).split("*")
            if len(l)>1:
                elem=element
                for i in l: 
                    if i[0] == "(" and i[-1] == ")":
                        i = i[1:-1]
                    e=power(elem,i)
                    elem=e
            return elem
        eq = self.steps[lineNum]
        lhs = eq.LHS.products
        rhs = eq.RHS.products
        newLhsList = []
        newRhsList = []
        split = False
        for elem in lhs:
            if isinstance(elem, power) == True:       
               elem = helperSplitPower(elem)
               split = True
            newLhsList.append(elem)
        for elem in rhs:
            if isinstance(elem, power) == True:       
               elem = helperSplitPower(elem)
               split = True
            newRhsList.append(elem)
        newLhs = Mult(newLhsList)
        newRhs = Mult(newRhsList)
        newEq = Eq(newLhs, newRhs, eq.group)
        if split == True:
            self.steps += [newEq]
            self.justifications += ["Split up power with multiplication in exponents"] 
            self.show()
        else:
            print('Warning',f"no power can be splitted")
        
    def identifyOrder(self, lineNum):
        eq = self.steps[lineNum]
        if len(eq.LHS.products) == 1 and isinstance(eq.LHS.products[0],identity):
            if len(eq.RHS.products) == 1 and isinstance(eq.RHS.products[0],power):
                power_ = eq.RHS.products[0]
                ineq = Inequality(Order(power_.element), power_.exponent, "<=")
                self.steps += [ineq]
                self.justifications += [f"power of {power_.element} is less than {power_.exponent}"] 
                self.show()
        elif len(eq.RHS.products) == 1 and isinstance(eq.RHS.products[0],identity):
            if len(eq.LHS.products) == 1 and isinstance(eq.LHS.products[0],power):
                power_ = eq.LHS.products[0]
                ineq = Inequality(Order(power_.element), power_.exponent, "<=")
                self.steps += [ineq]
                self.justifications += [f"power of {power_.element} is less than {power_.exponent}"] 
                self.show()
        
    
    def solveInequality(self,lineNum1, lineNum2):
        ineq1 = self.steps[lineNum1]
        ineq2 = self.steps[lineNum2]
        if isinstance(ineq1,Inequality) and isinstance(ineq2,Inequality):

            if ineq1.LHS == ineq2.LHS and ineq1.RHS == ineq2.LHS:
                if [ineq1.sign, ineq2.sign] in [["<=",">="],[">=","<="]]:
                    print("yes")
            #elif ineq1.LHS == ineq2.RHS and 

            # elif ineq1.RHS == ineq2.LHS:
            #     print ("yes")
            #     if [ineq1.sign, ineq2.sign] in [[">=",">="],["<=","<="]]:
            #         print ("yes")
        else:
            print("not inequality")