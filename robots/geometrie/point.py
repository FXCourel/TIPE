"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : point.py, contient la classe Point

"""

import math


class Point:

    def __init__(self, x, y, obstacle = -1) -> None:
        # Constructeur de la classe Position

        self.x = float(x)
        self.y = float(y)
        self.obstacle = obstacle

    def __str__(self) -> str:
        # Affichage d'une position
        return f"Point({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, other) -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)
    
    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def distance(self, point) -> float:
        # Calcul de la distance par rapport à un autre point, par défaut le point d'origine
        return math.sqrt((self.x-point.x)**2+(self.y-point.y)**2)
    
    @staticmethod
    def distance_eucli(x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)
    
    @staticmethod
    def order(p1, p2):
        if p1 < p2:
            return p1, p2
        return p2, p1

    def angle(self, point) -> float:
        # Calcul de l'angle par rapport à un autre points
        return math.atan2(self.y-point.y, self.x-point.x)

    def est_du_meme_cote(self, point, droite) -> bool:
        # Détermine si self et un autre point sont du même côté d'une droite

        # if debug: print((droite.a*self.x + droite.b*self.y + droite.c) * (droite.a*point.x + droite.b*point.y + droite.c))
        return (droite.a*self.x + droite.b*self.y + droite.c) * (droite.a*point.x + droite.b*point.y + droite.c) >= 0

    def est_a_droite(self, p1, p2) -> bool:
        # Détermine si self est à droite de la droite (p1, p2) en calclulant le produit vectoriel
        if p1 == p2: raise ValueError("Les deux points sont identiques")

        # if debug: print("  ",(p1.x - self.x) * (p2.y - self.y) - (p2.x - self.x) * (p1.y - self.y))
        return (p1.x - self.x) * (p2.y - self.y) - (p2.x - self.x) * (p1.y - self.y) <= 0

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y

    def __add__(self, other) -> 'Point':
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y, self.obstacle if self.obstacle == other.obstacle else -1)

    def __sub__(self, other) -> 'Point':
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y, self.obstacle if self.obstacle == other.obstacle else -1)
    
    def norme(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    @classmethod
    def progression_vers(cls, point: 'Point', cible: 'Point', precision: float) -> 'Point':
        # On utilise la structure Point pour stocker un vecteur
        direction = cible - point
        norme = direction.norme()
        try:
            direction.x = (direction.x / norme) * precision
            direction.y = (direction.y / norme) * precision
        except ZeroDivisionError:
            return point
        return point + direction




class Droite:

    def __init__(self, p1: Point, p2: Point) -> None:
        # Constructeur de la classe Droite, définie par deux points

        self.p1 = p1
        self.p2 = p2

        # Calcul des coefficients de la droite de la forme ax + by + c = 0
        self.a = p1.y - p2.y
        self.b = p2.x - p1.x
        self.c = p1.x*p2.y - p2.x*p1.y


if __name__ == "__main__":
    p1 = Point(1., 1.)
    p2 = Point(3., 2.)
    epsilon = Point.progression_vers(p1, p2, 0.1)
    print(epsilon)