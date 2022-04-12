from proof import *
from element import *
from environment import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), G.elements['e'],G)), goal=abelianG)
p.introGroup(G)
G.newElement('a')
G.newElement('b')
G.mulElements('a','b')
p.accessAssumption()
p.forallElim(1,['a * b'])
p.leftMult(G.elements['a'],2)
p.forallElim(1,['a'])
p.substituteRHS(3,4)
p.identleft(5)
p.identright(6)
p.rightMult(G.elements['b'],7)
p.forallElim(1,['b'])
p.substituteRHS(8,9)
p.identleft(10)
p.qed(['b','a'],11)
