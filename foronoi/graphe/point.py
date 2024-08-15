import numpy as np

from foronoi.graphe.vertex import Vertex
from foronoi.graphe.coordonee import Coordonee


class Point(Coordonee):

    def __init__(self, x=None, y=None, nom=None, arete_entree=None) -> None:
        """
        Un site. Extension de la classe Coordonee.
        """
        super().__init__(x, y)

        self.nom = nom
        self.arete_entree = arete_entree

    def __repr__(self):
        if self.nom is not None:
            return f"P{self.nom}"
        return f"Point({self.xd:.2f}, {self.xd:.2f})"

    def bordure(self) -> list:
        """
        Retourne la liste des arêtes qui entourent ce site.
        """

        if self.arete_entree is None:
            return []
        arete = self.arete_entree
        aretes = [arete]
        while arete.suiv != self.arete_entree:
            if arete.suiv is None:
                return aretes
            arete = arete.suiv
            aretes.append(arete)
        return aretes

    def sommets_bords(self):
        """
        Get a list of all the vertices that surround this cell point.

        Returns
        -------
        vertices: list(Vertex) or None
            The list of vertices, or None if not all borders are present (when the voronoi diagram is under
            construction)
        """
        bordure = self.bordure()
        if bordure is None:
            return None
        return [border.origine for border in bordure if isinstance(border.origine, Vertex)]

    def _get_xy(self):
        coords = self.sommets_bords()
        if coords is None:
            return [], []
        x = [coord.x for coord in coords]
        y = [coord.y for coord in coords]
        return x, y

    def __sub__(self, other):
        return Point(x=self.xd - other.xd, y=self.yd - other.yd)