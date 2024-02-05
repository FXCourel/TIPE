from noeud import Noeud


class Arbre:

    def __init__(self) -> None:
        self._racine = None
        self._taille = 0
        self._hauteur = 0

    def est_vide(self):
        return self._taille == 0

    @property
    def taille(self):
        return self._taille

    def minimum(self, noeud: Noeud):
        while noeud.gauche is not None:
            noeud = noeud.gauche
        return noeud

    def maximum(self, noeud: Noeud):
        while noeud.droite is not None:
            noeud = noeud.droite
        return noeud
