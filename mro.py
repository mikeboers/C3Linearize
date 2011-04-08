"""C3 algorithm by Samuele Pedroni (with readability enhanced by me)."""

from collections import defaultdict


class LinearizeError(ValueError):
    pass


def merge(sequences):
    
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
            raise LinearizeError("inconsistent hierarchy")
        
        # Move the head from the front of all sequences to the end of results.
        result.append(head)
        for seq in sequences:
            if seq[0] == head:
                del seq[0]


def linearize(graph, order=True):
    "Compute the class precedence list (MRO or method resolution order) according to C3"
    results = {}
    graph = defaultdict(list, graph)
    for head in sorted(graph, key=lambda k: len(graph[k])):
        _linearize(head, graph, order, results)
    return results
    
def _linearize(head, graph, order, results):
    if head in results:
        return results[head]
    res = merge(
        [[head]] +
        [_linearize(x, graph, order, results) for x in graph[head]] +
        ([graph[head]] if order else [])
    )
    results[head] = res
    return res


if __name__ == '__main__':
    
    A, B, C, D, E, F, G, O = 'ABCDEFGO'
    
    assert merge([[O]]) == [O]
    assert merge([[D], [D, O]]) == [D, O]
    assert merge([[E], [E, O]]) == [E, O]
    assert merge([[F], [F, O]]) == [F, O]
    assert merge([[B], [B, D, E], [D, O], [E, O]]) == [B, D, E, O]
    assert merge([[C], [C, D, F], [D, O], [F, O]]) == [C, D, F, O]
    assert merge([[A], [A, B, C], [B, D, E], [C, D, F], [D, O], [E, O], [F, O]]) == [A, B, C, D, E, F, O]
    
    assert linearize({
        D: [O],
    }) == {
        D: [D, O],
        O: [O],
    }
    
    assert linearize({
        D: [O],
        E: [O],
        B: [D, E],
    }) == {
        D: [D, O],
        E: [E, O],
        B: [B, D, E, O],
        O: [O]
    }
    
    assert linearize({
        D: [O],
        E: [O],
        F: [O],
        B: [D, E],
        C: [D, F],
        A: [B, C],
    })[A] == [A, B, C, D, E, F, O]
    
    exit()
    graph = {
        'a2': ['Y', 'a1'],
        'b2': ['b1'],
        'A': ['a2', 'a1'],
        'B': ['A', 'b2', 'b1'],
        'X': ['a1'],
        'root': ['X', 'Y', 'B', 'A']
        }
    print linearize('root', graph)
