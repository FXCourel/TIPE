from foronoi.noeud import Arc
from foronoi.arbre.noeud import Noeud


class NoeudFeuille(Noeud):
    def __init__(self, data: "Arc"):
        super().__init__(data)

    def __repr__(self):
        return f"Feuille({self.data}, left={self.gauche}, right={self.droite})"

    def get_key(self, sweep_line=None):
        return self.data.origine.xd

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data.origine.nom}"


