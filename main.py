from foronoi import *
from robots import *

from typing import Tuple
from time import perf_counter_ns, perf_counter
from sys import argv


def afficher_parametres():

    print(f"{Settings.DEBUG=}")
    print(f"{Settings.PRECISION=}")
    print(f"{Settings.MULT_ESPACEMENT_SITES=}")
    print(f"{Settings.NAIF_MARGE=}")


def main(nom_carte: str, bounding_size: Tuple[Tuple[float, float], Tuple[float, float]]):

    afficher_parametres()

    time_start = perf_counter()
    carte = CarteGraphee.from_scratch(nom_carte, bounding_size)
    time_end = perf_counter()
    viz_vo = Visualisation(carte)
    print(
        f"Temps de création de la carte (Voronoi): {time_end - time_start:.2f}s")

    time_start = perf_counter()
    carte_naif = CarteNaif.from_scratch(nom_carte, bounding_size)
    time_end = perf_counter()
    print(
        f"Temps de création de la carte (Naif): {time_end - time_start:.2f}s")
    viz_na = Visualisation_Naif(carte_naif)

    viz_vo.plot(show_finally=True)
    viz_vo.clear()

    viz_na.plot(show_finally=True)
    viz_na.clear()

    debut_x = input("Entrer l'abcisse (x) de départ: ")
    debut_y = input("Entrer l'ordonnée (y) de départ: ")
    debut = Point(float(debut_x), float(debut_y))
    arrivee_x = input("Entrer l'abcisse (x) d'arrivée: ")
    arrivee_y = input("Entrer l'ordonnée (y) d'arrivée: ")
    arrivee = Point(float(arrivee_x), float(arrivee_y))

    time_start = perf_counter_ns()
    chemin = carte.calculer_chemin(debut, arrivee)
    time_end = perf_counter_ns()
    print(f"Temps de calcul du chemin (Voronoi): {
          (time_end - time_start)/10e6:.3f}ms")

    time_start = perf_counter_ns()
    chemin_naif_dij = carte_naif.dijkstra(debut, arrivee)
    time_end = perf_counter_ns()
    print(
        f"Temps de calcul du chemin (Naif, Dijkstra): {(time_end - time_start)/10e6:.3f}ms")
    chemin_naif_dij = carte_naif.a_star(debut, arrivee)

    time_start = perf_counter_ns()
    chemin_naif_astar = carte_naif.dijkstra(debut, arrivee)
    time_end = perf_counter_ns()
    print(
        f"Temps de calcul du chemin (Naif, A*): {(time_end - time_start)/10e6:.3f}ms")
    chemin_naif_astar = carte_naif.a_star(debut, arrivee)

    viz_na.plot()
    viz_na.plot_chemin_int(chemin_naif_dij)
    viz_na.plot_chemin_int(chemin_naif_astar, "red")
    viz_na.show()
    viz_na.clear()

    viz_vo.plot()
    viz_vo.plot_chemin(chemin)
    viz_vo.show()


if __name__ == "__main__":
    # main("labyrinthe_5x5.map", ((0., 7.), (0., 7.)))
    main("labyrinthe_16x16.map", ((-1., 17.), (-1., 17.)))
    # main("bateaux.map", ((0., 40.), (0., 30.)))
