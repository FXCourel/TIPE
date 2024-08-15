import numpy as np
from foronoi.graphe import Coordonee


class Geometrie:
    @staticmethod
    def distance(point_a: Coordonee, point_b: Coordonee) -> float:
        x1 = point_a.xd
        x2 = point_b.xd
        y1 = point_a.yd
        y2 = point_b.yd

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1)**2)

    @staticmethod
    def norme(vecteur) -> float:
        return np.sqrt(np.dot(np.array(vecteur), np.array(vecteur)))

    @staticmethod
    def normalise(vecteur) -> np.array:
        if Geometrie.norme(np.array(vecteur)) == 0:
            return np.array(vecteur)
        return np.array(vecteur) / Geometrie.norme(np.array(vecteur))

    @staticmethod
    def point_intersection_droite(droite_orig, droite_fin, point_1, point_2) -> list:
        orig = np.array(droite_orig, dtype=float)
        end = np.array(droite_fin, dtype=float)
        direction = np.array(Geometrie.normalise(end - orig), dtype=float)
        point_1 = np.array(point_1, dtype=float)
        point_2 = np.array(point_2, dtype=float)

        v1 = orig - point_1
        v2 = point_2 - point_1
        v3 = np.array([-direction[1], direction[0]])

        if np.dot(v2, v3) == 0:
            return []

        t1 = np.cross(v2, v1) / np.dot(v2, v3)
        t2 = np.dot(v1, v3) / np.dot(v2, v3)

        if t1 > 0.0 and 0.0 <= t2 <= 1.0:
            return [orig + t1 * direction]
        return []

    @staticmethod
    def trouver_intersection(orig: Coordonee, end: Coordonee, p1: Coordonee, p2: Coordonee) -> Coordonee:
        if not orig or not end:
            return None

        point = Geometrie.point_intersection_droite(
            [orig.xd, orig.yd], [end.xd, end.yd], [p1.xd, p1.yd], [p2.xd, p2.yd])

        if len(point) == 0:
            return None

        return Coordonee(point[0][0], point[0][1])

    @staticmethod
    def calculer_angle(point, center) -> float:
        dx = point.xd - center.xd
        dy = point.yd - center.yd
        return np.math.degrees(np.math.atan2(dy, dx)) % 360

    @staticmethod
    def angle_est_horaire(a, b, c, center) -> bool:
        angle_1 = Geometrie.calculer_angle(a, center)
        angle_2 = Geometrie.calculer_angle(b, center)
        angle_3 = Geometrie.calculer_angle(c, center)

        est_direct = (
            angle_3 - angle_1) % 360 > (angle_3 - angle_2) % 360

        if est_direct:
            return False

        return True
