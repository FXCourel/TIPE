from foronoi.arbre.noeud import Noeud
from foronoi.noeud.breakpoint import Breakpoint


class NoeudInterne(Noeud):
    def __init__(self, data: "Breakpoint"):
        super().__init__(data)

    def __repr__(self):
        return f"Interne({self.data}, left={self.gauche}, right={self.droite})"

    def get_key(self, sweep_line=None):
        return self.data.calcul_intersection(sweep_line).xd

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data.breakpoint[0].nom},{self.data.breakpoint[1].nom}"
