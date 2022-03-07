exec(compile(source=open('element.py').read(), filename='element.py', mode='exec'))
exec(compile(source=open('environment.py').read(), filename='environment.py', mode='exec'))
exec(compile(source=open('group.py').read(), filename='group.py', mode='exec'))
exec(compile(source=open('integer.py').read(), filename='integer.py', mode='exec'))

class Proof:
    def __init__(self, label):
        self.label = label
        self.steps = []
        self.justifications = []
        self.environment = {} # add strings names to environment for parsing 
        self.depth = 0
        self.currAssumption = []
        self.show() 
    
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
    
    