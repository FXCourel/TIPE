from ..Graphe import *
import numpy as np


class Maths:

    @staticmethod
    # Retourne le cercle passant par les points a, b et c sous la forme Point(centre), rayon
    def cercle(a: Point, b: Point, c: Point):
        M = np.matrix(
            [[2 * a.x, 2 * a.y, 1], [2 * b.x, 2 * b.y, 1], [2 * c.x, 2 * c.y, 1]])
        Y = np.matrix(
            [[-(a.x**2 + a.y**2)], [-(b.x**2 + b.y**2)], [-(c.x**2 + c.y**2)]])
        X = np.linalg.solve(M, Y)
        x = - X[0, 0]
        y = - X[1, 0]
        r = np.sqrt(x**2 + y**2 - X[2, 0] ** 2)
        return Point(x, y), r

    @staticmethod
    def centre_cercle(a: Point, b: Point, c: Point):
        return Maths.cercle(a, b, c)[0]

    @staticmethod
    def bas_cercle(a: Point, b: Point, c: Point):
        centre, rayon = Maths.cercle(a, b, c)
        return Point(centre.x, centre.y - rayon)
