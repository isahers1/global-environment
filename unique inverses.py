from enum import unique
from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

'''
G = group('G','*')
inversePropertyOne = Eq( Mult(['a','c']) , Mult([G.identity_identifier]) , G)
inversePropertyTwo = Eq( Mult(['a','d']) , Mult([G.identity_identifier]) , G)
uniqueInverse = Implies( And(inversePropertyOne,inversePropertyTwo)  , Eq(  Mult(['d']), Mult(['c']), G)  ) 
p = Proof('Unique Inverses', assumption = None, goal=uniqueInverse)
p.introGroup(G)
p.introElement(G,'a')
p.introElement(G,'c')
p.introElement(G,'d')
p2 = p.introSubproof(And(inversePropertyOne,inversePropertyTwo))
p2.accessAssumption()
p2.andElim(4,1)
p2.andElim(4,2)
p2.rightSidesEq(5,6)
p2.cancelLeft(7, ['a'])
p2.switchSidesOfEqual(8)
p.concludeSubproof(9)
p.qed(10)
'''
print(dir(Proof))
