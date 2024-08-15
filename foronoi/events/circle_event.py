import math
from decimal import *

from foronoi.events.event import Event
from foronoi.graphe.coordonee import Coordonee
from foronoi.noeud.noeud_feuille import NoeudFeuille
from foronoi.noeud.arc import Arc


class CircleEvent(Event):
    circle_event = True

    def __init__(self, centre: Coordonee, rayon: Decimal, noeud_arc: NoeudFeuille, point_triple=None, arc_triple=None) -> None:
        """
        Un évènement de type cercle (circle event).
        """
        self.centre = centre
        self.rayon = rayon
        self.arc_pointer = noeud_arc
        self.est_valide = True
        self.point_triple = point_triple
        self.arc_triple = arc_triple

    def __repr__(self) -> str:
        return f"CircleEvent({self.point_triple}, y-radius={self.centre.yd - self.rayon:.2f}, y={self.centre.yd:.2f}, radius={self.rayon:.2f})"

    @property
    def xd(self) -> Decimal:
        return self.centre.xd

    @property
    def yd(self) -> Decimal:
        return self.centre.yd - self.rayon

    def _get_triangle(self) -> tuple:
        return (
            (self.point_triple[0].xd, self.point_triple[0].yd),
            (self.point_triple[1].xd, self.point_triple[1].yd),
            (self.point_triple[2].xd, self.point_triple[2].yd),
        )

    def fausse_alerte(self) -> "CircleEvent":
        """
        Marque l'évènement comme étant une fausse alerte.
        """
        self.est_valide = False
        return self

    @staticmethod
    def creer_circle_event(noeud_gauche: NoeudFeuille, noeud_milieu: NoeudFeuille, noeud_droit: NoeudFeuille, sweep_line) -> "CircleEvent":
        """
        Crée un évènement de cercle à partir de trois noeuds.
        """
        # Vérifie que les noeuds ne sont pas None
        if noeud_gauche is None or noeud_droit is None or noeud_milieu is None:
            return None

        # On récupère les arcs
        arc_gauche: Arc = noeud_gauche.get_value()
        arc_milieu: Arc = noeud_milieu.get_value()
        arc_droit: Arc = noeud_droit.get_value()

        # On récupère les points des arcs
        a, b, c = arc_gauche.origine, arc_milieu.origine, arc_droit.origine

        # On regarde si on peut creer un cercle
        if (circle_event := CircleEvent.creer_cercle(a, b, c)):
            # On crée l'évènement de cercle
            x, y, rayon = circle_event

            # Return circle event
            return CircleEvent(centre=Coordonee(x, y), rayon=rayon, noeud_arc=noeud_milieu, point_triple=(a, b, c),
                               arc_triple=(arc_gauche, arc_milieu, arc_droit))

        return None

    @staticmethod
    def creer_cercle(a: Coordonee, b: Coordonee, c: Coordonee) -> tuple:
        """
        Crée un cercle passant par les trois points donnés.
        """

        # Algorithme de O'Rourke
        A = b.xd - a.xd
        B = b.yd - a.yd
        C = c.xd - a.xd
        D = c.yd - a.yd
        E = (b.xd - a.xd) * (a.xd + b.xd) + (b.yd - a.yd) * (a.yd + b.yd)
        F = (c.xd - a.xd) * (a.xd + c.xd) + (c.yd - a.yd) * (a.yd + c.yd)
        G = 2 * ((b.xd - a.xd) * (c.yd - b.yd) - (b.yd - a.yd) * (c.xd - b.xd))

        if G == 0:
            # Cas où les points sont colinéaires
            return False

        # Centre et rayon du cercle
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G

        radius = Decimal.sqrt((a.xd - x) ** 2 + (a.yd - y) ** 2)

        return x, y, radius
