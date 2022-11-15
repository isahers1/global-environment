from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *


G = group('G','*')
abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), Mult([G.elements['e']]),G)), goal=abelianG)
p.introGroup(G)
p.introElement(G,'a')
p.introElement(G,'b')
p.closure(G,'a','b')
p.accessAssumption() # this and below one
p.forallElim(4,['a * b']) # combine two steps
p.leftMult('a',5)
p.forallElim(4,['a'])
p.substituteRHS(6,7)
p.identleft(8)
p.identright(9)
p.rightMult('b',10)
p.forallElim(4,['b'])
p.substituteRHS(11,12)
p.identleft(13)
p.forAllIntroduction(14,["a","b"],[1,2])
p.qed(15)
