from cv2 import AgastFeatureDetector_AGAST_7_12d


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
        #Demorgans Law
        if isinstance(arg,And):
            arg = Or(Not(arg.arg1), Not(arg.arg2))
        if isinstance(arg,Or):
            arg = And(Not(arg.arg1), Not(arg.arg2))

        #DNE
        if isinstance(arg,Not):
            arg = arg.arg

        self.arg = arg

    def elim(self,num,implies1,implies2):
        check1 = isinstance(implies1, Implies) and implies1.assum==self.arg1
        check2 = isinstance(implies2, Implies) and implies2.assum==self.arg2
        if check1 and check2 and implies1.conc==implies2.conc:
            return implies1.conc

#for all and there exists should be represented by a sub environment, so not a logic object?