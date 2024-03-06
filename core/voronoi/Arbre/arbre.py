from noeud import Noeud


class Arbre:

    @staticmethod
    def est_vide(self, noeud: Noeud):
        return noeud is None
        

    @property
    def taille(self, noeud: Noeud):
        return noeud.taille

    @staticmethod
    def minimum(noeud: Noeud):
        while noeud.gauche is not None:
            noeud = noeud.gauche
        return noeud

    @staticmethod
    def maximum(noeud: Noeud):
        while noeud.droite is not None:
            noeud = noeud.droite
        return noeud
