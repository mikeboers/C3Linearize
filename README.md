C3Linearize
============

**C3Linearize** is a Python implementation of the C3 linearization algorithm that Python uses for its class method resolution order ("MRO"). The difference is that now we can perform this on any type of object!

That being said, I'll demonstrate by just using classes anyways.

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

This prints out:

    native MRO:  (Z, K1, K2, K3, D, A, B, C, E, <type 'object'>)
    c3linearize: [Z, K1, K2, K3, D, A, B, C, E, <type 'object'>]

`linearize` operates on a mapping that represents the dependency graph; keys map to a sequence of their dependencies. It will then return a dictionary mapping each and every object to its linearization.

One can either contruct these graphs by hand, or use the `build_graph` function which will construct one of these mappings from a given object and a function which returns the bases of any given object.

The docstrings offer a little more information on this process, and see http://www.python.org/download/releases/2.3/mro/ for more info on the algorithm itself.
