"""C3 algorithm by Samuele Pedroni (with readability enhanced by me)."""


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



def merge(seqs):
    print '\n\nCPL[%s]=%s' % (seqs[0][0],seqs),
    res = []; i=0
    while 1:
      nonemptyseqs=[seq for seq in seqs if seq]
      if not nonemptyseqs: return res
      i+=1; print '\n',i,'round: candidates...',
      for seq in nonemptyseqs: # find merge candidates among seq heads
          cand = seq[0]; print ' ',cand,
          nothead=[s for s in nonemptyseqs if cand in s[1:]]
          if nothead: cand=None #reject candidate
          else: break
      if not cand: raise "Inconsistent hierarchy"
      res.append(cand)
      for seq in nonemptyseqs: # remove cand
          if seq[0] == cand: del seq[0]

def mro(C):
    "Compute the class precedence list (mro) according to C3"
    # I have removed adding [C.get_deps()] on the end to remove the requirement that they are in order.
    return merge([[C]]+map(mro,C.get_deps()))

def print_mro(C):
    print '\nMRO[%s]=%s' % (C,mro(C))





dep('a1')
dep('a2', 'Y', 'a1')
dep('b1')
dep('b2', 'b1')
dep('A', 'a2', 'a1')
dep('B', 'A', 'b2', 'b1')

dep('X', 'a1')
dep('Y')

root = dep('root', 'X', 'Y', 'B', 'A')



print_mro(root)
