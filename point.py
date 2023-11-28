"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : point.py, contient la classe Point

"""

from settings import *
import math


class Point:

    def __init__(self, x, y) -> None:
        # Constructeur de la classe Position

        self.x = x
        self.y = y

    def __str__(self) -> str:
        # Affichage d'une position

        return f"({self.x}, {self.y})"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def distance(self, point):
        # Calcul de la distance par rapport à un autre point, par défaut le point d'origine

        return math.sqrt((self.x-point.x)**2+(self.y-point.y)**2)

    def angle(self, point):
        # Calcul de l'angle par rapport à un autre points

        return math.atan2(self.y-point.y, self.x-point.x)

    def est_du_meme_cote(self, point, droite) -> bool:
        # Détermine si self et un autre point sont du même côté d'une droite

        # if debug: print((droite.a*self.x + droite.b*self.y + droite.c) * (droite.a*point.x + droite.b*point.y + droite.c))
        return (droite.a*self.x + droite.b*self.y + droite.c) * (droite.a*point.x + droite.b*point.y + droite.c) >= 0

    def est_a_droite(self, p1, p2) -> bool:
        # Détermine si self est à droite de la droite (p1, p2) en calclulant le produit vectoriel
        if p1 == p2: print(p1, p2); raise ValueError("Les deux points sont identiques")

        # if debug: print("  ",(p1.x - self.x) * (p2.y - self.y) - (p2.x - self.x) * (p1.y - self.y))
        return (p1.x - self.x) * (p2.y - self.y) - (p2.x - self.x) * (p1.y - self.y) <= 0

    def __repr__(self):

        return f"({self.x}, {self.y})"

    def __eq__(self, other):

        return self.x == other.x and self.y == other.y

    def __ne__(self, other):

        return self.x != other.x or self.y != other.y




class Droite:

    def __init__(self, p1: Point, p2: Point) -> None:
        # Constructeur de la classe Droite, définie par deux points

        self.p1 = p1
        self.p2 = p2

        # Calcul des coefficients de la droite de la forme ax + by + c = 0
        self.a = p1.y - p2.y
        self.b = p2.x - p1.x
        self.c = p1.x*p2.y - p2.x*p1.y