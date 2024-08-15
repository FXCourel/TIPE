from robots.naif.carte_naif import CarteNaif
from robots.settings import Settings
from robots.carte.obstacle import Obstacle
from robots.geometrie.point import Point
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numpy import arange
from typing import Any


class Visualisation_Naif:
    
    COLOR = {
        "chemin": "blue",
    }

    def __init__(self, carte: CarteNaif) -> None:
        self.carte: CarteNaif = carte
        
    def _plot_point(self, i: int, j: int, color: str) -> None:
        square = Rectangle((i * Settings.PRECISION, j * Settings.PRECISION), Settings.PRECISION, Settings.PRECISION, color=color)
        plt.gca().add_patch(square)

    def plot_point_obstacle(self, i: int, j: int) -> None:
        # assert (i, j) in self.carte.dist_obstacle
        color = 0
        if self.carte.dist_obstacle[(i, j)] > 0:
            color = 0.5 + 0.5 * min(1, self.carte.dist_obstacle[(i, j)] / Settings.NAIF_MARGE)
        self._plot_point(i, j, f'{color}')

    def plot_chemin_int(self, chemin: list[tuple[int, int]], color: str = "") -> None:
        # for (i, j), (i_next, j_next) in zip(chemin[:-1], chemin[1:]):
        #     plt.plot([i * Settings.PRECISION, i_next * Settings.PRECISION], [j * Settings.PRECISION, j_next * Settings.PRECISION],
        #              color or Visualisation_Naif.COLOR["chemin"])
        for (i, j) in chemin:
            self._plot_point(i, j, color or Visualisation_Naif.COLOR["chemin"])
                    

    def plot(self, show_finally: bool = False) -> None:
        for (i, j) in self.carte.dist_obstacle:
            if self.carte.dist_obstacle[(i, j)] >= Settings.NAIF_MARGE:
                continue
            self.plot_point_obstacle(i, j)
        if show_finally:
            self.show()

    def show(self, block_program: bool = True) -> None:
        plt.grid(True, which='minor', axis='both', linewidth=0.3, color='lightgray')
        plt.gca().set_aspect('equal')
        (x_min, x_max), (y_min, y_max) = self.carte.bouding_box
        major_ticks_x = arange(x_min, x_max + Settings.PRECISION, Settings.PRECISION)
        major_ticks_y = arange(y_min, y_max + Settings.PRECISION, Settings.PRECISION)
        plt.xticks(major_ticks_x, "", minor=True)
        plt.yticks(major_ticks_y, "", minor=True)
        plt.show(block=block_program)

    def clear(self) -> None:
        plt.clf()
