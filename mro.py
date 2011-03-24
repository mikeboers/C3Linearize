"""C3 algorithm by Samuele Pedroni (with readability enhanced by me)."""

from collections import defaultdict

class dep(object):

    by_name = {}
    
    def __init__(self, name, *deps):
        self.name = name
        self.deps = deps
        self.by_name[name] = self
    def get_deps(self):
        return [self.by_name.get(x) for x in self.deps]
    def __repr__(self):
        return self.name


class LinearizeError(ValueError):
    pass
    
def merge(seqs, cache):
    key = tuple(tuple(x) for x in seqs)
    if key in cache:
        print 'cached', seqs[0][0]
        return cache[key]
    print '\n\nCPL[%s] = merge(*%s)' % (seqs[0][0],seqs),
    print key
    res = [];
    i=0
    while 1:
      nonemptyseqs = [seq for seq in seqs if seq]
      if not nonemptyseqs:
          return res
      i += 1
      print '\n',i,'round: candidates...',
      
      for seq in nonemptyseqs: # find merge candidates among seq heads
          cand = seq[0]; print ' ',cand,
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

def linearize(root, graph):
    "Compute the class precedence list (mro) according to C3"
    # I have removed adding [C.get_deps()] on the end to remove the requirement that they are in order.
    autograph = defaultdict(list)
    for k, v in graph.items():
        autograph[k] = list(v)
    return _linearize(root, autograph, {})
    
def _linearize(root, graph, cache):
    return merge(
        [[root]] +[_linearize(x, graph, cache) for x in graph[root]],
        cache
    )

def print_mro(C):
    print '\nMRO[%s]=%s' % (C, linearize(C))



graph = {
    'a2': ['Y', 'a1'],
    'b2': ['b1'],
    'A': ['a2', 'a1'],
    'B': ['A', 'b2', 'b1'],
    'X': ['a1'],
    'root': ['X', 'Y', 'B', 'A']
    }




print linearize('root', graph)
