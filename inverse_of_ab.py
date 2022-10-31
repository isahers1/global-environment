from enum import unique
from telnetlib import GA
from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
ab_inverse = forall(['a','b'], G, Eq(Mult([inverse('b',G),inverse('a',G)]),Mult([inverse(Mult(['a','b']),G)]),G))
p = Proof('Inverse of ab Proof', assumption = None, goal = ab_inverse)
p.introGroup(G)
p.introElement(G,'a')
p.introElement(G,'b')
p.closure(G,'a','b')
p.introInverse(G, Mult(['a','b']))
p.rightMultInverse('b',4)
p.inverseElimLHS(5)
p.identleft(6)
p.identright(7)
p.rightMultInverse('a',8)
p.inverseElimLHS(9)
p.identleft(10)
p.switchSidesOfEqual(11)
p.forAllIntroduction(12,["a","b"],[1,2])
p.qed(13)