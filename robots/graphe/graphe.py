from robots.geometrie.point import Point

from queue import PriorityQueue
from typing import Any, List, Dict, Tuple, Union


class CheminNonTrouve(Exception):
    pass


class Graphe:

    def __init__(self) -> None:

        self.sommets: set[Point] = set()
        self.adjacence: dict[Any, set[Tuple[Point, int | float]]] = {}
        self.unique_adjacence: dict[Any, Union[int, float]] = {}
        self.sommets_old: set[Point] = None
        self.unique_adjacence_old: dict[Any, Union[int, float]] = None

    def __repr__(self) -> str:
        return '\n'.join([f'{p1} -> {self.adjacence[p1]}' for p1 in self.sommets])

    def ajouter_arete(self, point1, point2, cout) -> bool:

        ret: bool = False
        if point1 not in self.sommets:
            self.sommets.add(point1)
            self.adjacence[point1] = set()
            ret = True
        if point2 not in self.sommets:
            self.sommets.add(point2)
            self.adjacence[point2] = set()
            ret = True
        self.adjacence[point1].add((point2, cout))
        self.adjacence[point2].add((point1, cout))
        self.unique_adjacence[Point.order(point1, point2)] = cout
        return ret

    def dijkstra(self, depart, arrivee) -> List:

        deja_vus = set()
        queue = PriorityQueue()
        parents = {}
        queue.put((0, (depart, None)))

        while not queue.empty():
            distance, (point, parent) = queue.get()
            if point in deja_vus:
                continue
            parents[point] = parent
            deja_vus.add(point)
            if point == arrivee:
                break
            try:
                for voisin, cout in self.adjacence[point]:
                    queue.put((distance + cout, (voisin, point)))
            except TypeError:
                print(self.adjacence[point], "\n\n", self.adjacence)
                raise TypeError
            except KeyError as err:
                print(err, point, depart)
                raise

        if arrivee not in parents:
            raise CheminNonTrouve()

        chemin = [arrivee]
        p = arrivee
        while p != depart:
            p = parents[p]
            chemin.append(p)
        chemin.reverse()
        return chemin


if __name__ == "__main__":
    g = Graphe()
    g.ajouter_arete(1, 2, 10)
    g.ajouter_arete(2, 3, 2)
    g.ajouter_arete(3, 4, 1)
    g.ajouter_arete(1, 5, 1)
    g.ajouter_arete(3, 5, 3)
    g.ajouter_arete(4, 6, 7)
    g.ajouter_arete(5, 6, 8)
    g.ajouter_arete(6, 7, 4)
    print(g.dijkstra(2, 7))
