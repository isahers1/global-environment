exec(compile(source=open('integer.py').read(), filename='integer.py', mode='exec'))
exec(compile(source=open('element.py').read(), filename='element.py', mode='exec'))

from integer import *
from logicObjects import *
##need to deal with operations with one variable and an actual int (ex. x+2 or e^x*e^2)
##subtypes/subclasses? a power object is also a mult object which is also an element. 

class power: 
    def __init__(self, element, exp):
        if isinstance(exp, str):
            exp = integer(exp)
        self.exponent = exp
        self.element= element
        
    
    def __repr__(self):
        if isinstance(self.element,power):
            return f"({self.element}) ^ ({self.exponent})"
        else:
            return f"{self.element} ^ ({self.exponent})"
    ##cases: 1.e^a*e^b 2.e1^a*e2^b
    def __mul__(self,other):
        if self.element == other.element: 
            if isinstance(self.exponent,integer) and isinstance(other.exponent,integer):  
                expnew = self.exponent + other.exponent
                return power(self.element, expnew)
            elif isinstance(self.exponent,int) and isinstance(other.exponent,integer):
                expnew = str(self.exponent) + "+" + other.exponent
                return power(self, expnew)
            elif isinstance(self.exponent,integer) and isinstance(other.exponent,int):  
                expnew = self.exponent + "+" + str(other.exponent)
                return power(self, expnew)
            elif isinstance(self.exponent,int) and isinstance(other.exponent,int): 
                expnew = self.exponent + other.exponent
                return power(self, expnew)
        ##if they are not both powers, we can just use mult from elements
        else: 
            return Mult[self,other, self.element.group]

    def __truediv__(self,other):
        if self.element == other.element: 
            expnew = self.exponent + "-" + other.exponent
            return power(self, expnew)
        elif isinstance(self.exponent,int) and isinstance(other.exponent,integer):
                expnew = str(self.exponent) + "-" + other.exponent
                return power(self, expnew)
        elif isinstance(self.exponent,integer) and isinstance(other.exponent,int):  
                expnew = self.exponent + "-" + str(other.exponent)
                return power(self, expnew)
        elif isinstance(self.exponent,int) and isinstance(other.exponent,int): 
                expnew = self.exponent - other.exponent
                return power(self, expnew)
    

    def __eq__(self, other):
        if isinstance(self,power) and isinstance(other,power):
            if self.element==other.element and self.exponent == other.exponent: 
                return True 
            else: 
                return False 

        #e^2=e*e property 
        # we can't have a mult object of length x, so this should only work for ints 
        #is encoding of mult still a list? 
        elif isinstance(self,power) and isinstance(other,power)==False:
            if isinstance(self.exponent,int):
                if self.element == other.element and self.exponent == len(other.list):
                    return True 

        elif isinstance(other,power) and isinstance(self,power)==False:   
            if isinstance(other.exponent,int):
                if self.element == other.element and other.exponent == len(self.list):
                    return True 
        ## Deal with x^{a+2}=x^a*x^2? 
        












       
        

        
