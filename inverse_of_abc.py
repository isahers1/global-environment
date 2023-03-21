# from enum import unique
# from telnetlib import GA
from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
abc_inverse = forall(['a','b','c'], G, Eq(Mult([inverse('c',G),inverse('b',G),inverse('a',G)]),Mult([inverse(Mult(['a','b','c']),G)]),G))
p = Proof('Inverse of ab Proof', assumption = None, goal = abc_inverse)
p.introGroup(G)
p.introElement(G,'a')
p.introElement(G,'b')
p.introElement(G,'c')
p.introInverse(G, Mult(['a','b','c']))
p.rightMultInverse('c',4)
p.inverseElimLHS(5)
p.identleft(6)
p.identright(7)
p.rightMultInverse('b',8)
p.inverseElimLHS(9)
p.identleft(10)
p.rightMultInverse('a',11)
p.inverseElimLHS(12)
p.identleft(13)
p.forAllIntroduction(14,["a","b","c"],[1,2,3])
p.qed(15)