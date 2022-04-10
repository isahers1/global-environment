from proof import *
from element import *
from environment import *
from group import *
from integer import *
from logicObjects import *

abelianG = forall(['x', 'y'], 'G', Eq(Mult(['x', 'y']), Mult(['y','x']),"G"))
p = Proof('Simple Abelian Proof', forall(['x'], 'G', Eq(Mult(['x', 'x']), identity('1','G'),"G")), goal=abelianG)