from ast import Pass
from select import select


class A:
    total = 84793498

class B(A):
    pass

class C(A):
    pass 

class M:
    def get_total(self):
        print(self.total)

class D(B,M):
    pass

e = D()
e.get_total()