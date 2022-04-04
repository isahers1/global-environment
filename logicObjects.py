from cv2 import AgastFeatureDetector_AGAST_7_12d
import copy

exec(compile(source=open('element.py').read(), filename='element.py', mode='exec'))
exec(compile(source=open('environment.py').read(), filename='environment.py', mode='exec'))
exec(compile(source=open('group.py').read(), filename='group.py', mode='exec'))
exec(compile(source=open('integer.py').read(), filename='integer.py', mode='exec'))

class Proof:
    def __init__(self, label, goal): # make goal optional
        self.label = label
        self.goal = goal # this is an implies
        self.steps = []
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
    
    def leftMult (self, elem, lineNum):
        """
        Left Multiply both sides of an equation with the input element 
        :param lineNum: the equation in the proof that is to be modified 
        :param elem: the element to left Multiply with 
        """
        elem2 = copy.deepcopy(self.steps[lineNum])
        product = self.MultElem(elem, elem2.LHS)
        result = Eq(product, self.MultElem(elem,elem2.RHS))
        self.steps += [result]
        self.justifications += ['Left Multiply by ' +str(elem) ] 
        self.show()

    def rightMult (self, elem, lineNum):
        """
        Right Multiply both sides of an equation with the input element 
        :param lineNum: the line in the proof that is to be modified 
        :param elem: the element to right Multiply 
        """
        elem1 = copy.deepcopy(self.steps[lineNum])
        product = self.MultElem(elem1.LHS, elem)
        result = Eq(product, self.MultElem(elem1.RHS,elem))
        self.steps += [result]
        self.justifications += ['Right Multiply by ' +str(elem)] 
        self.show()

    ##power methods 
    def breakPower(self,power):
        """
        Given an expression like e^a where a is a python integer, return a mult object equivalent to e^a
        :param power: the power to be converted to mult
        """   
        exp=self.exponent   
        element = self.element 
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
    
    def rightSidesEq(self, line1, line2):
        """
        If two sides have the same right side, then set left sides to equal in a new line
        :param line1: the first line with same right side
        :param line2: the second line with the same right side
        """
        l1 = self.steps[line1]
        l2 = self.steps[line2]
        if l1.RHS == l2.RHS:
            self.steps += [Eq(l1.LHS,l2.LHS)]
            self.justifications += [f"Equations with same right side on lines {str(line1)}, {str(line2)}"]
            self.show()

    def leftSidesEq(self, line1, line2):
        """
        If two sides have the same left side, then set left sides to equal in a new line
        :param line1: the first line with same left side
        :param line2: the second line with the same left side
        """
        l1 = self.steps[line1]
        l2 = self.steps[line2]
        if l1.LHS == l2.LHS:
            self.steps += [Eq(l1.RHS,l2.RHS)]
            self.justifications += [f"Equations with same left side on lines {str(line1)}, {str(line2)}"]
            self.show()

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
            ret = Eq(newProduct,evidence.RHS)

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
            ret = Eq(evidence.LHS,newProduct)

        self.steps += [ret]
        self.justifications += ["identity elimination "] 
        self.show()

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

class Bottom:
    def elim(self, conclusion):
        return conclusion

class Eq:
    def __init__(self,LHS,RHS):
        self.LHS = LHS
        self.RHS = RHS

def reduce(exp):
    if isinstance(exp, Not):
        if isinstance(exp.arg, Not):
            exp=exp.arg.arg #DNE
        if isinstance(exp.arg, And):
            exp=Or(Not(exp.arg.arg1), Not(exp.arg.arg2)) #Demorgan's Law
        if isinstance(exp.arg, Or):
            exp=And(Not(exp.arg.arg1), Not(exp.arg.arg2)) #Demorgan's Law
    if isinstance(exp, Implies):
        if isinstance(exp.conc, Bottom):
            exp=Not(exp.assum)
    return exp

#My current vision is to have an arbitrary element class and an existential element class
#A for all is an equation including an arbitrary element, and a there exists is an equation including an existential element



