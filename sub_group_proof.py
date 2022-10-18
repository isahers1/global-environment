from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
subGroupG = G.subGroup(Eq('x',G.elements['e'],G))
p = Proof('Simple Subgroup Proof', None, goal=subGroupG)
p.introGroup(G)
p.introSet('S',G,Eq('x',G.elements['e'],G)) # change to mult objects?
p.getArbElem('S','a')
p.getArbElem('S','b')
p.multBothSides(2,3)
p.identright(4)
p.setClosure('S',[2,3],5)
p.setContainsIdentity('S',2)
p.setInverse('S',5)
p.concludeSubgroup('S')
p.qed(9)