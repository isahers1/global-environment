from re import L

from element import *
from group import *
from integer import *
from logicObjects import *


class Proof:
    def __init__(self, label, assumption, goal=None, steps=[], justifications = []): # make goal optional
        self.label = label
        self.assumption = assumption
        self.goal = goal # this is an implies
        self.steps = []
        self.justifications = []
        self.env = {}
        self.subproof = None
    
    def qed(self, lineNum):
        if self.goal == self.steps[lineNum]:
            self.steps+=["□"]
            self.justifications += ["QED"]
            self.show()
        else:
            print("This is not the same as the goal")

    def undo(self):
        self.steps = self.steps[:-1]
        self.justifications = self.justifications[:-1]
        self.show()
        
    def show(self):
        print('')
        print('Proof : ' + self.label)
        print('--------------------------------')
        subProofIndent = "" # might need to change, this is just for now
        for i in range(len(self.steps)):
            if self.justifications[i] == "Intro Subproof Assumption":
                subProofIndent += '\t'
            if self.justifications[i] == "Concluded Subproof":
                subProofIndent = subProofIndent.replace('\t', '', 1)
            print(subProofIndent + str(i) + ': ' + str(self.steps[i]) + '\t' + str(self.justifications[i]))
        print('')

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
                print("Cannot substitute without an Equation")
        else:
            print("Cannot substitute without an Equation")

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
                print("Cannot substitute without an Equation")
        else:
            print("Cannot substitute without an Equation")
    
    def modus(self, lineNum1, lineNums): # lineNums because multiple assumptions may be neccessary (I think)
        """
        modus pones: given A->B and A, the function concludes B and add it as a new line in the proof
        :param lineNum1 and lineNum2: one line in the proof where the person showed A->B and one line the proof where the person showed A
        """
        ev1 = self.steps[lineNum1]
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
            print (f"Line {str(lineNum1)} is not an implies statement")

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
                print (f"Inverse laws can't be applied on line {lineNum}")
                return
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
                print (f"Inverse laws can't be applied on line {lineNum}")
                return
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
            print(f"There is no forall statmenent on line {lineNum}")
        else:
            expr = evidence.replace(replacements)
            self.steps += [expr]
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
            print(f"There is no there exists statmenent on line {lineNum}")
        else:
            expr = evidence.replace(replacements)
            self.steps += [expr]
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
            print (f"Line {lineNum} is not an equation")
            return
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
            print (f"Line {lineNum} is not an equation")
            return
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
                print ("Need a single element but given multiple")
                return
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
            print ("No power addition to be split apart")
            return
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
            print ("No power multiplication to be split apart")
            return
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
            print (f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same right sides")
            return

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
            print (f"The equations on lines {str(lineNum1)}, {str(lineNum2)} do not have the same left sides")
            return

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
                print ("identity can't be applied")
                return
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
        if isinstance(evidence,Eq): 
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
                print ("identity can't be applied")
                return
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
        :param eq: The equality you want to introduce
        """
        if eq.LHS == eq.RHS:
            self.steps+=[eq]
            self.justifications += ["reflexive equality"] 
            self.show()
        else:
            print ("this is not reflexive")

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
            print ("this is not a logic statement")

    def introCases(self, case):
        """
        Introduction of cases (law of excluded middle)
        :param case: the equation/logical statement of one case (the other is a not of that) 
        """
        case1 = case
        case2 = reduce(Not(case))
        self.steps += [Or(case1, case2)]
        self.justifications += ["case introduction (LEM)"] 
        self.show()

    def introSubproof(self, assum):
        """
        WIP
        This one returns so the user has access to the new subproof
        We will have to make show recursive to make the subproof steps show
        :param assum: the assumption for the subproof
        """
        subproof = Proof(label="Subproof", assumption=assum, steps=[self.steps], justifications = [self.justifications]) # how do we deal with this?
        self.steps += [assum]
        self.justifications += ["Intro Subproof Assumption"] # How can we track subproof throughout parent proof?
        self.show()

    def concludeSubproof(self, lineNum):
        """
        WIP
        You conclude a subproof from the parent subproof
        Work in progress, we should discuss how to do this.
        :param lineNum: the conclusion of the subproof to turn into an implies
        """
        evidence = self.steps[lineNum]
        if isinstance(evidence, Not):
            self.steps += [evidence.arg]
            self.justifications += ["Concluded Subproof"]
            self.show()
        else:
            print(f"Cannot conclude subproof") # THIS IS A MESS, NEED TO ACTUALLY CATCH ERRORS

    def introElement(self,G, name):
        """
        Introduces an arbitrary element in G
        Can be used as evidence for a forall introduction
        :param G: the group the elemen is in
        :param name: the name of the new element
        """
        if G.contains(name):
            print(f"{name} is already in {G}")
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
        evidence = copy.deepcopy(self.steps[equationLine])
        G = self.steps[elemIntroLines[0]].grp
        #Checking that the lines introduce the arbitrary variables, and that the variables are all in the same group
        for i in range(len(vars)):
            v = vars[i]
            l = elemIntroLines[i]
            if self.steps[l].elem!=vars[i]:
                print("Line", l, "does not introduce variable", v)
                return
            if self.steps[l].grp!=G:
                print("Element", v, "is not in group", G)
                return
        #If you make it here, this is a valid for all intro
        self.steps+=[forall(vars,G,self.steps[equationLine])]
        self.justifications+=["For all introduction"]
        self.show()

    def closure(self,G,a,b):
        '''
        Introduces ab as an element of G by closure
        :param G: the group a,b are in
        :param a: element a
        :param b: element b
        '''
        if G.contains(a) and G.contains(b):
            G.mulElements(a,b)
            self.steps+=[In(G,Mult([a,b]))]
            self.justifications+=["Closure"]
            self.show()
        else:
            if not G.contains(a):
                print(f"{a} is not in {G}")
            else:
                print(f"{b} is not in {G}")

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
                self.steps += [Eq( Mult(lhselems[:l]), Mult(rhselems[:l]) , evidence.parentgroup )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print(f"It seems like the right hand sides on line {lineNum} are equal to {mult}")
        else:
            print(f"It doesn't seem like line {lineNum} contains an equation")

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
                self.steps += [Eq( Mult(lhselems[l:]), Mult(rhselems[l:]) , evidence.parentgroup )]
                self.justifications += [f"Right side cancellation of {mult} on line {lineNum}"]
                self.show()
            else:
                print(f"It seems like the left hand sides on line {lineNum} are equal to {mult}")
        else:
            print(f"It doesn't seem like line {lineNum} contains an equation")

    def switchSidesOfEqual(self, lineNum):
        '''
        Switches an equality like x=y to become y=x
        :param lineNum: the line where the equality to be flipped is on 
        '''
        evidence = self.steps[lineNum]
        if isinstance(evidence, Eq):
            rhs = evidence.RHS
            lhs = evidence.LHS
            self.steps += [Eq(rhs , lhs , evidence.parentgroup )]
            self.justifications += [f"Switched sides of line {lineNum}"]
            self.show()
        else:
            print(f"Hmm, it doesn't look like line {lineNum} isn't an equality")
        
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
            print(f"The statement on line {lineNum1} isn't a Not")

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