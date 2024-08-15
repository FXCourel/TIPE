from robots.graphe.carte_graphee import CarteGraphee
from robots.carte.carte import Carte
from robots.carte.obstacle import Obstacle
from robots.geometrie.point import Point
import matplotlib.pyplot as plt


class Visualisation:

    COLOR = {
        "obstacle": "black",
        "cible": "green",
        "chemin": "blue",
        "arete": "red"
    }

    def __init__(self, carte: CarteGraphee) -> None:
        self.carte: CarteGraphee = carte

    def _plot_edge(self, s1, s2, color) -> None:
        plt.plot([s1.x, s2.x], [s1.y, s2.y], color)

    def _plot_obstacle(self, obstacle: Obstacle, color) -> None:
        n = len(obstacle.contours)
        for i in range(n-1):
            p_i = obstacle.contours[i]
            p_i_next = obstacle.contours[(i+1) % n]
            if p_i == p_i_next:
                plt.plot(p_i.x, p_i.y, "o", color=color)
            else:
                plt.plot([p_i.x, p_i_next.x], [p_i.y, p_i_next.y], color)

    def plot_chemin(self, chemin: list[Point], color: str = "") -> None:
        for p, p_next in zip(chemin[:-1], chemin[1:]):
            plt.plot([p.x, p_next.x], [p.y, p_next.y],
                     color or Visualisation.COLOR["chemin"])

    def plot(self, show_finally: bool = False) -> None:
        assert self.carte is not None
        if not self.carte.optimisee:
            for sommet1, sommet2 in self.carte.unique_adjacence:
                self._plot_edge(sommet1, sommet2, Visualisation.COLOR["arete"])
        else:
            for sommet1, sommet2 in self.carte.unique_adjacence:
                self.plot_chemin(self.carte.chemin_entre[(sommet1, sommet2)], Visualisation.COLOR["arete"])
        for obstacle in self.carte.carte_origine.obstacles:
            if not obstacle.fantome:
                self._plot_obstacle(obstacle, Visualisation.COLOR["obstacle"])
        if show_finally:
            self.show(True)

    def show(self, block_program: bool = True) -> None:
        plt.grid(False)
        plt.gca().set_aspect('equal')
        plt.show(block=block_program)

    def clear(self) -> None:
        plt.clf()
