

class _Node():
    
    def __init__(self, prio, data) -> None:
        self.prio = prio
        self.data = data
        
    def __lt__(self, other):
        return self.prio < other.prio


class FilePriorite():

    def __init__(self) -> None:
        self.tas = []
        self.len = 0
        
    def __len__(self):
        return self.len
        
    def _percoler_haut(self, i):
        while i > 0:
            p = (i-1)//2
            if self.tas[i] < self.tas[p]:
                self.tas[i], self.tas[p] = self.tas[p], self.tas[i]
                i = p
            else:
                break
            
    def _percoler_bas(self, i):
        while 2*i+1 < self.len:
            f = 2*i+1
            if f+1 < self.len and self.tas[f+1] < self.tas[f]:
                f += 1
            if self.tas[f] < self.tas[i]:
                self.tas[i], self.tas[f] = self.tas[f], self.tas[i]
                i = f
            else:
                break
            
    def ajouter(self, prio, data):
        self.tas.append(_Node(prio, data))
        self._percoler_haut(self.len)
        self.len += 1
        
    def extraire_min(self):
        if self.len == 0:
            raise IndexError("FilePriorite vide")
        self.len -= 1
        self.tas[0], self.tas[self.len] = self.tas[self.len], self.tas[0]
        self._percoler_bas(0)
        return self.tas[self.len].data
    
    def lire_min(self):
        if self.len == 0:
            raise IndexError("FilePriorite vide")
        return self.tas[0].data