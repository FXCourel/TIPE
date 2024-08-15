from foronoi.graphe.point import Point
from foronoi.graphe.vertex import Vertex


class HalfEdge:
    def __init__(self, point_incident: Point, jumelle: "HalfEdge" = None, origine: Vertex = None):

        # Pointeur vers l'origine de l'arête
        self.origine = origine

        # Le point dont l'arête est incidente (ie. le point de la cellule de Voronoi)
        self.point_incident = point_incident

        # L'autre arête incidente sur le même point (dans le sens contraire)
        self._jumelle = None
        self.jumelle = jumelle

        # Suivant et précédent
        self.suiv = None
        self.prec = None

    def __repr__(self):
        return f"{self.point_incident}/{self.jumelle.point_incident or '-'}"

    def set_suiv(self, next):

        if next:
            next.prev = self
        self.suiv = next

    def get_origine(self, y=None, max_y=None):

        if isinstance(self.origine, Vertex):
            if self.origine.xd is None or self.origine.yd is None:
                return None
            return self.origine

        if y is not None:
            return self.origine.calcul_intersection(y, max_y=max_y)

        return None

    @property
    def jumelle(self):
        """
        Donne l'arête jumelle de l'arête courante.
        """
        return self._jumelle

    @jumelle.setter
    def jumelle(self, jumelle):
        if jumelle is not None:
            jumelle._jumelle = self

        self._jumelle = jumelle

    @property
    def cible(self):
        """
        L'origine de la jumelle.
        """
        if self.jumelle is None:
            return None
        return self.jumelle.origine

    def supprimer(self):

        # Supprimer l'arête de la liste des arêtes connectées à l'origine
        if isinstance(self.origine, Vertex):
            self.origine.connected_edges.remove(self)

        # Lien entre les arêtes
        if self.prec is not None:
            self.prec.set_suiv(self.suiv)

        # Si un point incident pointaint vers cette arête, on le change
        if self.point_incident is not None and self.point_incident.arete_entree == self:

            # Les points incidents des arêtes suivantes doivent correspondre
            assert (
                self.suiv is None or self.suiv.point_incident == self.point_incident
            ), f"Les points incidents {self.suiv.point_incident} et {self.point_incident} ne correspondent pas"

            self.point_incident.arete_entree = self.suiv
