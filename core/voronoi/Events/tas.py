from event import Event

class Tas:

    def __init__(self) -> None:
        self._tas = []
        self._taille = 0
        
    @property
    def taille(self):
        return self._taille
    
    @property
    def tas(self):
        return self._tas
    
    @tas.setter
    def tas(self, tas):
        self._tas = tas
        self._taille = len(tas)
        self.tasser()
        
    def __len__(self) -> int:
        return self._taille

    def __str__(self) -> str:
        return f"Tas({self._tas})"

    def __repr__(self) -> str:
        return self.__str__()

    def gauche(self, index) -> int:
        return 2 * index + 1

    def existe_gauche(self, index) -> bool:
        return self.gauche(index) < self._taille

    def droite(self, index) -> int:
        return 2 * index + 2

    def existe_droite(self, index) -> bool:
        return self.droite(index) < self._taille

    def enfant_max(self, index) -> int:
        if self.existe_droite(index):
            gauche, droite = self.gauche(index), self.droite(index)
            if self._tas[gauche] > self._tas[droite]:
                return gauche
            else:
                return droite

    def parent(self, index) -> int:
        return (index - 1) // 2

    def est_vide(self) -> bool:
        return self._taille == 0

    def _percolation_haut(self, index) -> None:
        parent = self.parent(index)
        while index > 0 and self._tas[parent] < self._tas[index]:
            self._tas[parent], self._tas[index] = self._tas[index], self._tas[parent]
            index = parent
            parent = self.parent(index)

    def _percolation_bas(self, index) -> None:
        while self.existe_gauche(index):
            enfant = self.enfant_max(index)
            if self._tas[index] < self._tas[enfant]:
                self._tas[index], self._tas[enfant] = self._tas[enfant], self._tas[index]
                index = enfant
            else:
                break

    def tasser(self) -> None:
        for index in range(self._taille // 2, -1, -1):
            self._percolation_bas(index)

    def ajouter(self, element) -> None:
        self._tas.append(element)
        self._taille += 1
        self._percolation_haut(self._taille - 1)

    def lire_maximum(self):
        return self._tas[0]

    def extraire_maximum(self):
        maximum = self._tas[0]
        self._tas[0] = self._tas[self._taille - 1]
        self._taille -= 1
        self._percolation_bas(0)
        return maximum
    
    def est_tas(self) -> bool:
        for index in range(self._taille // 2, -1, -1):
            if self._tas[index] < self._tas[self.enfant_max(index)]:
                return False
        return True