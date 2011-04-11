
from c3linearize import linearize, class_graph

class meta(type):
    def __repr__(cls):
        return cls.__name__

class A(object): __metaclass__ = meta
class B(object): __metaclass__ = meta
class C(object): __metaclass__ = meta
class D(object): __metaclass__ = meta
class E(object): __metaclass__ = meta
class K1(A,B,C): pass
class K2(D,B,E): pass
class K3(D,A):   pass
class Z(K1,K2,K3): pass

print 'native MRO: ', Z.__mro__
print 'c3linearize:', linearize(class_graph(Z))[Z]

# native MRO:  (Z, K1, K2, K3, D, A, B, C, E, <type 'object'>)
# c3linearize: [Z, K1, K2, K3, D, A, B, C, E, <type 'object'>]
