from proof import *
from element import *
from environment import *
from group import *
from integer import *
from logicObjects import *

G = group('G','*')
abelianG = forall(['x', 'y'], G, Eq(Mult(['x', 'y']), Mult(['y','x']),G))
p = Proof('Simple Abelian Proof', forall(['x'], G, Eq(Mult(['x', 'x']), identity('1',G),G)), goal=abelianG)
p.introGroup(G)
G.newElement('a')
G.newElement('b')

"""
p.introGroup('G')
p.introGroupElement('a', 'G')
p.introGroupElement('b', 'G')
p.closure(3,4)
p.forallElim(1,[["x",mult(["a","b"])]])
p.leftmult('a',6)
p.forallElim(1,[["x", "a"]])
p.substitution(7,8)
p.identleft(9)
p.identright(10)
p.rightmult('b',11)
p.forallElim(1,[["x", "b"]])
p.substitution(12,13)
p.identleft(14)
p.abelian(15)
"""