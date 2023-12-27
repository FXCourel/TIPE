class Noeud:

    def __init__(self, data) -> None:
        self._data = data
        self._gauche = None
        self._droite = None
        self._parent = None
        self._hauteur = None

    def __str__(self) -> str:
        return f"Noeud({self._data}, {self._gauche}, {self._droite})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def data(self):
        return self._data

    @property
    def gauche(self):
        return self._gauche

    @gauche.setter
    def gauche(self, left):
        self._gauche = left
        if left is not None:
            left.parent = self

    @property
    def droite(self):
        return self._droite

    @droite.setter
    def droite(self, droite):
        self._droite = droite
        if droite is not None:
            droite.parent = self

    @property
    def hauteur(self):
        if self._hauteur is None:
            self.calculer_hauteur()
        return self._hauteur

    def calculer_hauteur(self):
        self._hauteur = 1 + max(self._gauche.hauteur, self._droite.hauteur
                                ) if self._gauche is not None and self._droite is not None else 1
        return self._hauteur

    @property
    def balance(self):
        left_hauteur = self.left.hauteur if self.left is not None else 0
        right_hauteur = self.right.hauteur if self.right is not None else 0
        return left_hauteur - right_hauteur
