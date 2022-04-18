from enum import unique
from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *


G = group('G','*')
inversePropertyOne = Eq( Mult(['a','c']) , Mult([G.identity_identifier]) , G)
inversePropertyTwo = Eq( Mult(['a','d']) , Mult([G.identity_identifier]) , G)
uniqueInverse = Implies( [inversePropertyOne,inversePropertyTwo]  , Eq(  Mult(['d']), Mult(['c']), G)  ) 
p = Proof('u', assumption = None, goal=uniqueInverse)
p.introGroup(G)
p.introElement(G,'a')
p.introElement(G,'c')
p.introElement(G,'d')
p.introAssumption(inversePropertyOne)
p.introAssumption(inversePropertyTwo)
p.introSubproof(Not(Eq(Mult(['d']), Mult(['c']), G)))
p.rightSidesEq(4,5)
p.cancelLeft(7, ['a'])
p.switchSidesOfEqual(8)
p.notElim(6,9)
p.concludeSubproof(6)
#p.impliesIntroduction([4,5],11)