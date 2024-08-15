from robots.graphe.graphe import Graphe, CheminNonTrouve
from robots.carte.carte import Carte
from robots.carte.obstacle import Obstacle
from robots.settings import Settings
from robots.geometrie.point import Point

from typing import List, Dict, Union, Tuple, Callable

from queue import PriorityQueue
from random import shuffle


class CarteNaif():

    def __init__(self, carte_origine, matrice, dist_obstacle, bouding_box) -> None:
        self.matrice = matrice
        self.dist_obstacle = dist_obstacle
        self.carte_origine = carte_origine
        self.bouding_box = bouding_box

    @staticmethod
    def snap_quadrillage_int(point: Point | tuple) -> tuple:
        if isinstance(point, Point):
            point = Point.to_tuple(point)
        px, py = point
        cintx, cinty = (round(px / Settings.PRECISION),
                        round(py / Settings.PRECISION))
        return (cintx, cinty)

    @staticmethod
    def snap_quadrillage(point: Point | tuple) -> tuple:
        cintx, cinty = CarteNaif.snap_quadrillage_int(point)
        return (cintx * Settings.PRECISION, cinty * Settings.PRECISION)

    @staticmethod
    def voisins_points(i: int, j: int) -> List[tuple[int, int]]:
        l = [(i + 1, j),
             (i - 1, j),
             (i, j + 1),
             (i, j - 1),
             (i + 1, j + 1),
             (i - 1, j - 1),
             (i - 1, j + 1),
             (i + 1, j - 1)]
        shuffle(l)
        return l

    @classmethod
    def from_scratch(cls, nom_fichier: str, bounding_size: Tuple[Tuple[float, float], Tuple[float, float]]) -> 'CarteNaif':
        carte_raw: Carte = Carte.lire_carte(nom_fichier)
        (x_min, x_max), (y_min, y_max) = bounding_size
        bas_gauche = CarteNaif.snap_quadrillage_int((x_min, y_min))
        haut_droite = CarteNaif.snap_quadrillage_int((x_max, y_max))
        matrice = {(i, j): Point((snap := CarteNaif.snap_quadrillage((i * Settings.PRECISION, j * Settings.PRECISION)))[0], snap[1])
                   for i in range(bas_gauche[0], haut_droite[0]+1) for j in range(bas_gauche[1], haut_droite[1]+1)}
        dist_obstacles = {key: Settings.NAIF_MARGE for key in matrice}

        contours_obstacles = set()
        for obs in carte_raw.obstacles:
            for i in range(len(obs.contours) - 1):
                p = obs.contours[i]
                cible = obs.contours[i+1]
                p = Point.progression_vers(p, cible, Settings.PRECISION)
                while cible.distance(p) > Settings.PRECISION:
                    contours_obstacles.add(CarteNaif.snap_quadrillage_int(p))
                    p = Point.progression_vers(p, cible, Settings.PRECISION)

        def bfs_distances(points: PriorityQueue) -> None:
            vus = set()
            while not points.empty():
                distance, (i, j) = points.get(0)
                if distance >= Settings.NAIF_MARGE or (i, j) in vus:
                    continue
                vus.add((i, j))
                voisins = CarteNaif.voisins_points(i, j)
                if dist_obstacles[(i, j)] > distance:
                    dist_obstacles[(i, j)] = distance
                for voisin in voisins:
                    if voisin in dist_obstacles:
                        points.put((distance + Settings.PRECISION, voisin))

        queue = PriorityQueue()
        for p in contours_obstacles:
            queue.put((0, p))
        bfs_distances(queue)

        return cls(carte_raw, matrice, dist_obstacles, bounding_size)

    def _a_star(self, heuristique: Callable, depart: tuple, arrivee: tuple) -> List[tuple[int, int]]:

        depart = CarteNaif.snap_quadrillage_int(depart)
        arrivee = CarteNaif.snap_quadrillage_int(arrivee)
        i_dep, j_dep = depart
        i_arr, j_arr = arrivee

        def reconstituer_chemin():
            chemin = [arrivee]
            p = arrivee
            while p != depart:
                p = parents[p]
                chemin.append(p)
            chemin.append(depart)
            chemin.reverse()
            return chemin

        queue = PriorityQueue()
        queue.put((0, (i_dep, j_dep)))

        parents = {}

        longueur_plus_court_chemin = {}
        longueur_plus_court_chemin[(i_dep, j_dep)] = 0

        while not queue.empty():
            _, point = queue.get()
            i, j = point
            if point == (i_arr, j_arr):
                return reconstituer_chemin()
            for voisin in CarteNaif.voisins_points(i, j):
                if voisin not in self.matrice or self.dist_obstacle[voisin] < Settings.NAIF_MARGE:
                    continue
                tentative_chemin = longueur_plus_court_chemin[point] + Point.distance_eucli(
                    i, j, *voisin)
                if voisin not in longueur_plus_court_chemin or tentative_chemin < longueur_plus_court_chemin[voisin]:
                    parents[voisin] = point
                    longueur_plus_court_chemin[voisin] = tentative_chemin
                    meilleure_heuristique = tentative_chemin + \
                        heuristique(voisin, (i_arr, j_arr))
                    queue.put((meilleure_heuristique, voisin))

        raise CheminNonTrouve("Chemin naïf non trouvé")

    def a_star(self, depart: tuple, arrivee: tuple) -> List[tuple[int, int]]:
        def dist(p1: tuple, p2: tuple) -> float:
            i1, j1 = p1
            i2, j2 = p2
            return Point.distance_eucli(i1, j1, i2, j2)
        return self._a_star(dist, depart, arrivee)

    def dijkstra(self, depart, arrivee) -> List:
        return self._a_star(lambda p1, p2: 0, depart, arrivee)
