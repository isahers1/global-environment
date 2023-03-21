from proof import *
from element import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
order_of_inverse = forall(['a','g'], G, Eq(Order('a'), Order(Mult(['g','a',inverse('g',G)])),G))

p = Proof('Order Proof', assumption = None, goal = order_of_inverse)
p.introGroup(G)
p.introElement(G,'a')
p.introOrder(G,'b','n')
