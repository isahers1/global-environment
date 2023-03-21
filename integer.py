# INTEGER CLASS, needs to be implemented

class integer:
    def __init__(self, input):
        # if isinstance(input, str):
        self.value = input
    
    def __repr__(self):
        if isinstance(self.value, str) == True:
            return self.value
        else:
            return str(self.value)


    def __mul__(self,other):
        if isinstance(other, int):
            inputnew = str(other) + "*" + self.value
        elif isinstance(other, integer):
             inputnew = self.value + "*" + other.value
        return integer(inputnew)
    
    def __add__(self,other):
        if other.value[0] == "-":
            inputnew = self.value + "+(" + other.value +")"
        else:
            inputnew = self.value + "+" + other.value
        return integer(inputnew)
    
    def __sub__(self,other):
        inputnew = self.value + "-" + other.value
        return integer(self, inputnew)
    
    def __truediv__(self,other):
        inputnew = self.value + "/" + other.value
        return integer(self, inputnew)

    def __eq__(self, other):
        if isinstance(self.value,str):
            self_string = self.value
        else:
            self_string = str(self.value)
        
        if isinstance(other.value,str):
            other_string = other.value
        else:
            other_string = str(other.value)
            
        if self_string==other_string:
            return True 
        elif len(self_string)==len(other_string):
        ## multiplication and divison binds closer than addition/subtraction
            if "+" in self_string and "+" in other_string: 
                a1 = self_string.split["+"][0]
                b1 = self_string.split["+"][1]
                b2 = other_string.split["+"][0]
                a2 = other_string.split["+"][1]
                return a1==a2 and b1==b2
            # elif "-" in self_string and "-" in other_string: 
            #     a1 = self_string.split["-"][0]
            #     b1 = self_string.split["-"][1]
            #     b2 = other_string.split["-"][0]
            #     a2 = other_string.split["-"][1]
            #     return a1==a2 and b1==b2
            elif "*" in self_string and "*" in other_string: 
                a1 = self_string.split["*"][0]
                b1 = self_string.split["*"][1]
                b2 = other_string.split["*"][0]
                a2 = other_string.split["*"][1]
                return a1==a2 and b1==b2
            # elif "/" in self_string and "/" in other_string: 
            #     a1 = self_string.split["/"][0]
            #     b1 = self_string.split["/"][1]
            #     b2 = other_string.split["/"][0]
            #     a2 = other_string.split["/"][1]
            #     return a1==a2 and b1==b2
            else:
                return False
        else: 
            return False

