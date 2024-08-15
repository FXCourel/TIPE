import math
from decimal import Decimal

from foronoi.graphe.coordonee import Coordonee


class Breakpoint:
    """
    Un point d'intersection entre deux arcs.
    """

    def __init__(self, breakpoint: tuple, edge=None):
        """
        The breakpoint is stored by an ordered tuple of sites (:obj:`p_i`, :obj:`p_j`) where :obj:`p_i` defines the
        parabola left of the breakpoint and :obj:`p_j` defines the parabola to the right. Furthermore, the internal node
        :obj:`v` has a pointer to the half edge in the doubly connected edge list of the Voronoi diagram. More
        precisely, :obj:`v` has a pointer to one of the half-edges of the edge being traced out by the breakpoint
        represented by :obj:`v`.

        Parameters
        ----------
        breakpoint: (Point, Point)
            A point where two arcs intersect, represented as a tuple of the two site points that the arcs refer to
        """

        # The tuple of the points whose arcs intersect
        self.breakpoint = breakpoint

        # The edge this breakpoint is tracing out
        self._edge = None
        self.edge = edge

    def __repr__(self):
        return f"Breakpoint({self.breakpoint[0].nom}, {self.breakpoint[1].nom})"

    def s_intersectent(self):
        """
        A guard that handles the edge-case where two arcs were initialized at the same time due to their sites
        having the same :obj:`y`-coordinate. This guard makes sure that the left arc intersects once with the right arc
        and not the other way around.
        """
        i, j = self.breakpoint
        return not (i.yd == j.yd and j.xd < i.xd)

    def calcul_intersection(self, l, max_y=None):
        """
        Calcul de l'intersection avec la ligne
        Depuis https://www.cs.hmc.edu/~mbrubeck/voronoi.html
        """

        i, j = self.breakpoint

        # Initialisation
        result = Coordonee()
        p: Coordonee = i

        a = i.xd
        b = i.yd
        c = j.xd
        d = j.yd
        u = 2 * (b - l)
        v = 2 * (d - l)

        # Cas spécial
        if i.yd == j.yd:
            result.xd = (i.xd + j.xd) / 2

            if j.xd < i.xd:
                result.yd = max_y or float('inf')
                return result

        # Handle cases where one point's y-coordinate is the same as the sweep line
        elif i.yd == l:
            result.xd = i.xd
            p = j
        elif j.yd == l:
            result.xd = j.xd
        else:
            # We now need to solve for x
            # 1/u * (x**2 - 2*a*x + a**2 + b**2 - l**2) = 1/v * (x**2 - 2*c*x + c**2 + d**2 - l**2)
            # Then we let Wolfram alpha do the heavy work for us, and we put it here in the code :D
            try:
                x = -(Decimal.sqrt(
                    v * (a ** 2 * u - 2 * a * c * u + b ** 2 * (u - v) + c ** 2 * u) + d ** 2 * u * (v - u) + l ** 2 * (
                        u - v) ** 2) + a * v - c * u) / (u - v)
            except:
                x = 0
            result.xd = x

        # We have to re-evaluate this, since the point might have been changed
        a = p.xd
        b = p.yd
        x = result.xd
        u = 2 * (b - l)

        # Handle degenerate case where parabolas don't intersect
        if u == 0:
            result.yd = float("inf")
            return result

        # And we put everything back in y
        result.yd = 1 / u * (x ** 2 - 2 * a * x + a ** 2 + b ** 2 - l ** 2)
        return result
