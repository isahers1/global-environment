class integer:
    def __init__(self, input):
        if isinstance(input, str):
            self.value = "("+input+")"
    
    def __repr__(self):
        return "integer(" + self.value + ")"

    def __mul__(self,other):
        inputnew = self.value + "*" + other.value
        return integer(self, inputnew)
    
    def __add__(self,other):
        inputnew = self.value + "+" + other.value
        return integer(self, inputnew)
    
    def __sub__(self,other):
        inputnew = self.value + "-" + other.value
        return integer(self, inputnew)
    
    def __truediv__(self,other):
        inputnew = self.value + "/" + other.value
        return integer(self, inputnew)

    def __eq__(self, other):
        self_string=self.value
        other_string=other.value
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
            elif "-" in self_string and "-" in other_string: 
                a1 = self_string.split["-"][0]
                b1 = self_string.split["-"][1]
                b2 = other_string.split["-"][0]
                a2 = other_string.split["-"][1]
                return a1==a2 and b1==b2
            elif "*" in self_string and "*" in other_string: 
                a1 = self_string.split["*"][0]
                b1 = self_string.split["*"][1]
                b2 = other_string.split["*"][0]
                a2 = other_string.split["*"][1]
                return a1==a2 and b1==b2
            elif "/" in self_string and "/" in other_string: 
                a1 = self_string.split["/"][0]
                b1 = self_string.split["/"][1]
                b2 = other_string.split["/"][0]
                a2 = other_string.split["/"][1]
                return a1==a2 and b1==b2
            else:
                return False
        else: 
            return False

