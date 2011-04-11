"""A module to perform C3 linearization on arbitrary objects.

The primary usage of this module is to build a depency graph using
`build_graph`, which returns a dict mapping objects to a list of their
dependencies. Then, to linearize the graph with the `linearize` function.


"""

from collections import defaultdict


class Error(ValueError):
    pass


def merge(sequences):
    """Merge object sequences preserving order in initial sequences.
    
    This is the merge function as described for C3, see:
    http://www.python.org/download/releases/2.3/mro/
    
    """
    
    # Make sure we don't actually mutate anything we are getting as input.
    sequences = [list(x) for x in sequences]
    
    result = []
    
    while True:
        
        # Clear out blank sequences.
        sequences = [x for x in sequences if x]
        if not sequences:
            return result

        # Find the first clean head.
        for seq in sequences:
            head = seq[0]
            # If this is not a bad head (ie. not in any other sequence)...
            if not any(head in s[1:] for s in sequences):
                break
        else:
            raise Error("inconsistent hierarchy")
        
        # Move the head from the front of all sequences to the end of results.
        result.append(head)
        for seq in sequences:
            if seq[0] == head:
                del seq[0]



def build_graph(obj, bases_func):
    """Build a graph of an object given a function to return it's bases."""
    graph = {}
    _add_to_graph(obj, graph, bases_func)
    return graph

def _add_to_graph(obj, graph, bases_func):
    """Internally used for `build_graph`."""
    if obj not in graph:
        graph[obj] = bases_func(obj)
        for x in graph[obj]:
            _add_to_graph(x, graph, bases_func)


def class_graph(cls):
    """Extract a graph from a given class."""
    return build_graph(cls, lambda cls: cls.__bases__)
    
    
def linearize(graph, heads=None, order=True):
    """Linearize a dependency graph using the C3 method.
    
    Parameters:
        graph: A mapping from objects to a sequence of their dependencies.
        heads: A sequence of the objects to linearize; defaults to
            linearizing the entire graph.
        order: Whether to maintain the order of direct dependants (defaults to
            True to match the Python MRO).
    
    Returns a dict mapping objects to their linearization.
    
    """
    
    results = {}
    graph = defaultdict(list, graph)
    
    for head in heads or sorted(graph, key=lambda k: len(graph[k])):
        _linearize(head, graph, order, results)
    return results


def _linearize(head, graph, order, results):
    """Internally used by linearize."""
    if head in results:
        return results[head]
    res = merge(
        [[head]] +
        [_linearize(x, graph, order, results) for x in graph[head]] +
        ([graph[head]] if order else [])
    )
    results[head] = res
    return res







# TESTS

def assertEqual(a, b):
    if a != b:
        assert False, '%r != %r' % (a, b)


def test_merge():
    
    A, B, C, D, E, F, G, O = 'ABCDEFGO'
    def do_test_merge(seqs, res):
        assertEqual(merge(seqs), res)
    
    yield do_test_merge, [[O]], [O]
    yield do_test_merge, [[D], [D, O]], [D, O]
    yield do_test_merge, [[E], [E, O]], [E, O]
    yield do_test_merge, [[F], [F, O]], [F, O]
    yield do_test_merge, [[B], [B, D, E], [D, O], [E, O]], [B, D, E, O]
    yield do_test_merge, [[C], [C, D, F], [D, O], [F, O]], [C, D, F, O]
    yield do_test_merge, [[A], [A, B, C], [B, D, E], [C, D, F], [D, O], [E, O], [F, O]], [A, B, C, D, E, F, O]


def test_linearize():
    
    A, B, C, D, E, F, G, O = 'ABCDEFGO'
    
    def do_test_linearize(head, graph, expected):
        res = linearize(graph, heads=[head] if head else None)
        if head:
            res = res[head]
        assertEqual(res, expected)
        
    yield do_test_linearize, None, {
        D: [O],
    }, {
        D: [D, O],
        O: [O],
    }
    
    yield do_test_linearize, None, {
        D: [O],
        E: [O],
        B: [D, E],
    }, {
        D: [D, O],
        E: [E, O],
        B: [B, D, E, O],
        O: [O]
    }
    
    yield do_test_linearize, A, {
        D: [O],
        E: [O],
        F: [O],
        B: [D, E],
        C: [D, F],
        A: [B, C],
    }, [A, B, C, D, E, F, O]


def test_class_mro():
    
    O = object
    def assert_class_mro(cls):
        graph = class_graph(cls)
        linear = linearize(graph)
        for cls, mro in linear.iteritems():
            assertEqual(mro, list(cls.__mro__))
    
    class B(O): pass
    class C(O): pass
    class A1(B, C): pass
    yield assert_class_mro, A1
    
    class F(O): pass
    class E(O): pass
    class D(O): pass
    class C(D,F): pass
    class B(D,E): pass
    class A2(B,C): pass
    yield assert_class_mro, A2
    
    class A(O): pass
    class B(O): pass
    class C(O): pass
    class D(O): pass
    class E(O): pass
    class K1(A,B,C): pass
    class K2(D,B,E): pass
    class K3(D,A):   pass
    class Z(K1,K2,K3): pass
    yield assert_class_mro, Z


if __name__ == '__main__':
    import nose
    nose.runmodule()
    