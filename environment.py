import copy

class Environment:
    env = [{}]
    assumption = []
    depth = 0
    
    #ELEMENTS

    def getElem(self, elem):
        return self.env[self.depth]["Elements"][elem]

    def addElemProp(self, elem, type, prop):
        #type could be in group, or equality, ect
        self.env[self.depth]["Elements"][elem][type].append(prop)

    #GROUPS

    def getGroup(self, group):
        return self.env[self.depth]["Groups"][group]

    def addGroupProp(self, group, type, prop):
        #type could be for all, contains, ect
        self.env[self.depth]["Groups"][group][type].append(prop)
    
    def newSubproof(self, assume):
        self.env.append(self.env[-1].copy())
        self.assumption.append(assume)
        self.depth+=1

    def endSubproof(self):
        self.env.pop()
        self.depth -= 1
        return self.assumption.pop()