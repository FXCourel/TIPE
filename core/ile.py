"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : ile.py, contient la classe Ile

"""

from settings import *
from point import Point, Droite
import algos
import queue


class Ile:

    def __init__(self, contours: list[Point]):

        self.centre = contours[0]
        self.contours = contours[1:] + [contours[1]]
        self.points_x = [p.x for p in self.contours]
        self.points_y = [p.y for p in self.contours]
        self.rayon = 0
        self.mise_a_jour_rayon()

    def __repr__(self):
        return f"Ile{self.centre}"

    def grahamiser_contours(self):
        self.contours = algos.parcours_de_graham(self.contours, points_redondants_possibles=True)
        self.contours = self.contours[1:] + [self.contours[1]]
        self.points_x = [p.x for p in self.contours]
        self.points_y = [p.y for p in self.contours]

    def mise_a_jour_rayon(self):
        self.rayon = max([self.centre.distance(p) for p in self.contours])

    def se_touchent(self, autre):

        if self.centre.distance(autre.centre) > self.rayon + autre.rayon:
            return False

        n = len(self.contours)-1
        m = len(autre.contours)-1

        for i in range(n):

            p1, p2 = self.contours[i], self.contours[(i+1)%n]
            for j in range(m):
                q1, q2 = autre.contours[j], autre.contours[(j+1)%m]
                if algos.se_coupent(p1, p2, q1, q2):
                    return True
        return False

    def fusionner(self, autre):

        self.contours += autre.contours
        self.grahamiser_contours()
        self.mise_a_jour_rayon()



if __name__ == "__main__":
    print("Ce fichier ne doit pas être exécuté directement")