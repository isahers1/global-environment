from enum import unique
from telnetlib import GA
from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
order_of_inverse = forall(['a'], G, Eq(Order('a'),inverse('a',G),G))

p = Proof('Order Proof', assumption = None, goal = order_of_inverse)
p.introGroup(G)
p.introElement(G,'a')
p.introInteger(G,'n')

#first subproof
p.introOrder(G,'a','n')
p.orderProperty(G,'a')
p.rightMultPower('a','-n',4)
p.powerSimplifyLeft(5)
p.identright(6)
p.insertIntegerEquation("n+(-n)=0")
p.substituteIntegerRHS(7,8)
p.powerSimplifyLeft(9)
p.insertIntegerEquation("(-1)*n=-n")
p.substituteIntegerLHS(10,11)
p.splitPowerMult(12)
p.identifyOrder(13)
p.substituteIntegerLHS(14,3)

#second subproof
p.introInteger(G,'m')
p.introOrder(G,inverse('a',G),'m')
p.orderProperty(G,inverse('a',G))
p.mergePowerMult(18)
p.rightMultPower('a','m',19)
p.powerSimplifyLeft(20)
p.identright(21)
p.insertIntegerEquation("-1*m+m=0")
p.substituteIntegerRHS(22,23)
p.powerSimplifyLeft(24)
p.identifyOrder(25)
p.substituteIntegerLHS(26,17)
p.solveInequality(27, 15)

#identify order
#replace function