from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
subGroupG = G.subGroup(In('x',G))
p = Proof('Simple Subgroup Proof', None, goal=subGroupG)
p.introGroup(G)
p.introSet('S',G,In('x',G))
p.getSpecificElem('S','e')
p.setContainsIdentity('S',2)
p.getArbElem('S','a')
p.getArbElem('S','b')
p.closure(G,'a','b')
p.setClosure('S',[4,5],6)
p.introInverse(G,'a')
p.addElemToSet('S','(a)^(-1)',G)
p.setInverse('S',8)
p.concludeSubgroup('S')
p.qed(11)
