"""C3 algorithm by Samuele Pedroni (with readability enhanced by me)."""

from collections import defaultdict


class LinearizeError(ValueError):
    pass
    
def merge(seqs):
    # Make sure we don't actually mutate anything we are getting as input.
    seqs = [x[:] for x in seqs]
    # print 'merge', seqs
    res = [];
    i=0
    while 1:
      nonemptyseqs = [seq for seq in seqs if seq]
      if not nonemptyseqs:
          return res
      i += 1
      # print '\n',i,'round: candidates...',
      
      for seq in nonemptyseqs: # find merge candidates among seq heads
          cand = seq[0]
          # print ' ',cand,
          nothead=[s for s in nonemptyseqs if cand in s[1:]]
          if nothead:
              cand=None #reject candidate
          else:
              break
      if not cand:
          raise LinearizeError("inconsistent hierarchy")
      res.append(cand)
      for seq in nonemptyseqs: # remove cand
          if seq[0] == cand: del seq[0]

def linearize(graph, order=True):
    "Compute the class precedence list (MRO or method resolution order) according to C3"
    # I have removed adding [C.get_deps()] on the end to remove the requirement that they are in order.
    results = {}
    graph = defaultdict(list, dict(
        (k, list(v)) for k, v in graph.iteritems()
    ))
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
