"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : ocstacle.py, contient la classe Obstacle

"""

from robots.settings import Settings
from robots.geometrie.point import Point, Droite
from robots.geometrie.algos import Algos


class Obstacle:

    def __init__(self, contours: list[Point], a_centre: bool = False, fantome: bool = False):

        self.centre = contours[0] if a_centre else None
        self.a_centre = a_centre
        if a_centre:
            self.contours: list[Point] = contours[1:] + [contours[1]]
        else:
            self.contours: list[Point] = contours[0:] + [contours[0]]
        self.points_x: list = [p.x for p in self.contours]
        self.points_y: list = [p.y for p in self.contours]
        self.rayon = 0
        self.fantome = fantome
        if a_centre:
            self.mise_a_jour_rayon()

    def __repr__(self):
        return f"Obstacle{self.centre}"

    def grahamiser_contours(self):
        self.contours = Algos.parcours_de_graham(
            self.contours, points_redondants_possibles=True)
        self.contours = self.contours[1:] + [self.contours[1]]
        self.points_x = [p.x for p in self.contours]
        self.points_y = [p.y for p in self.contours]

    def mise_a_jour_rayon(self):
        self.rayon = max([self.centre.distance(p) for p in self.contours])
        
    def mise_a_jour_contours(self):
        self.points_x = [p.x for p in self.contours]
        self.points_y = [p.y for p in self.contours]

    def se_touchent(self, autre):

        if self.centre.distance(autre.centre) > self.rayon + autre.rayon:
            return False

        n = len(self.contours)-1
        m = len(autre.contours)-1

        for i in range(n):

            p1, p2 = self.contours[i], self.contours[(i+1) % n]
            for j in range(m):
                q1, q2 = autre.contours[j], autre.contours[(j+1) % m]
                if Algos.se_coupent(p1, p2, q1, q2):
                    return True
        return False

    def fusionner(self, autre):

        self.contours += autre.contours
        self.grahamiser_contours()
        self.mise_a_jour_rayon()
        
    def decoupage_contours(self, precision):
        contours = []
        for i in range(len(self.contours) - 1):
            p = self.contours[i]
            contours.append(p)
            cible = self.contours[i+1]
            p = Point.progression_vers(p, cible, precision)
            while cible.distance(p) > precision:
                contours.append(p)
                p = Point.progression_vers(p, cible, precision)
        contours.append(self.contours[-1])
        self.contours = contours
        self.mise_a_jour_contours()

if __name__ == "__main__":
    print("Ce fichier ne doit pas être exécuté directement")
