from sys import argv, setrecursionlimit
from matplotlib import pyplot as plt
import numpy as np
from math import floor

from foronoi import *
from robots import *

from typing import Tuple
from time import perf_counter_ns


CONSTRUCTION_VORONOI = 0
CONSTRUCTION_NAIF = 1
CHEMIN_VORONOI = 2
CHEMIN_DIJKSTRA = 3
CHEMIN_ASTAR = 4

DIC_PRECISION = 9
DIC_VORONOI = 10
DIC_DIJKSTRA = 11
DIC_ASTAR = 12
SPECIAL_CONSTRUCTION = 13
SPECIAL_CHEMIN = 14
BOTTOM = 15


def afficher_parametres() -> None:

    print(f"{Settings.DEBUG=}")
    print(f"{Settings.PRECISION=}")
    print(f"{Settings.MULT_ESPACEMENT_SITES=}")
    print(f"{Settings.NAIF_MARGE=}")


def test_voronoi(nom_carte: str, precision: float, bounding_size: Tuple, debut: Tuple[float, float], arrivee: Tuple[float, float]) -> dict[int, float]:
    
    Settings.PRECISION = precision

    temps = {}

    time_start = perf_counter_ns()
    carte = CarteGraphee.from_scratch(nom_carte, bounding_size)
    time_end = perf_counter_ns()
    print(f"Construction vor:{time_end - time_start} ns")
    temps[CONSTRUCTION_VORONOI] = time_end - time_start
    
    time_start = perf_counter_ns()
    _ = carte.calculer_chemin(debut, arrivee)
    time_end = perf_counter_ns()
    temps[CHEMIN_VORONOI] = time_end - time_start
    
    return temps


def test_naif(nom_carte: str, precision: float, bounding_size: Tuple, debut: Tuple[float, float], arrivee: Tuple[float, float]) -> dict[int, float]:

    Settings.PRECISION = precision
    
    temps = {}

    time_start = perf_counter_ns()
    carte = CarteNaif.from_scratch(nom_carte, bounding_size)
    time_end = perf_counter_ns()
    print(f"Construction naif:{time_end - time_start} ns")
    temps[CONSTRUCTION_NAIF] = time_end - time_start
    
    time_start = perf_counter_ns()
    try:
        _ = carte.dijkstra(debut, arrivee)
    except CheminNonTrouve as err:
        print(err)
    time_end = perf_counter_ns()
    temps[CHEMIN_DIJKSTRA] = time_end - time_start
    
    time_start = perf_counter_ns()
    try:
        _ = carte.a_star(debut, arrivee)
    except CheminNonTrouve as err:
        print(err)
    time_end = perf_counter_ns()
    temps[CHEMIN_ASTAR] = time_end - time_start
    
    print(temps)
    
    return temps


def test_bateaux():
    
    CARTE = "bateaux.map"
    BOUNDING = ((0., 40.), (0., 30.))
    DEBUT = Point(12, 2)
    FIN = Point(34, 23)

    PRECISION_STEP = 0.01
    PRECISION_MIN = 0.01
    PRECISION_MAX = 0.2
    
    n_steps = floor((PRECISION_MAX - PRECISION_MIN) / PRECISION_STEP) + 1
    i = 0
    # SPECIAL = 1
    
    resultats = {
        DIC_PRECISION: np.empty(n_steps),
        CONSTRUCTION_VORONOI: np.empty(n_steps),
        CHEMIN_VORONOI: np.empty(n_steps),
        CONSTRUCTION_NAIF: np.empty(n_steps),
        CHEMIN_DIJKSTRA: np.empty(n_steps),
        CHEMIN_ASTAR: np.empty(n_steps),
        SPECIAL_CONSTRUCTION: np.empty(n_steps),
        SPECIAL_CHEMIN: np.empty(n_steps)
    }

    precision = PRECISION_MIN
    while precision < PRECISION_MAX:
        
        assert i < n_steps, f"{i=}, {n_steps=}, {precision=}, {PRECISION_MAX}"

        temps_vor = test_voronoi(CARTE, precision, BOUNDING, DEBUT, FIN)
        temps_naif = test_naif(CARTE, precision, BOUNDING, DEBUT, FIN)

        resultats[DIC_PRECISION][i] = precision
        resultats[CHEMIN_VORONOI][i] = temps_vor[CHEMIN_VORONOI]
        resultats[CONSTRUCTION_VORONOI][i] = temps_vor[CONSTRUCTION_VORONOI]
        resultats[CONSTRUCTION_NAIF][i] = temps_naif[CONSTRUCTION_NAIF]
        resultats[CHEMIN_DIJKSTRA][i] = temps_naif[CHEMIN_DIJKSTRA]
        resultats[CHEMIN_ASTAR][i] = temps_naif[CHEMIN_ASTAR]

        afficher_parametres()
        precision += PRECISION_STEP
        i += 1
        
    # assert i == n_steps
    
    # SPECIAL

    # temps_vor = test_voronoi(CARTE, SPECIAL, BOUNDING, DEBUT, FIN)
    # temps_naif = test_naif(CARTE, SPECIAL, BOUNDING, DEBUT, FIN)
    
    # resultats[SPECIAL_CONSTRUCTION] = [temps_vor[CONSTRUCTION_VORONOI], temps_naif[CONSTRUCTION_NAIF], temps_naif[CONSTRUCTION_NAIF]]
    # resultats[SPECIAL_CHEMIN] = [temps_vor[CHEMIN_VORONOI], temps_naif[CHEMIN_DIJKSTRA], temps_naif[CHEMIN_ASTAR]]


    plt.figure()
    
    colonnes = ("Voronoi",
                "Naif\nChemin Dijkstra",
                "Naif\nChemin A*"
        )
    
    # bottom = [0, 0, 0]
    # WIDTH = 1
    
    # Construction
    # plt.bar(colonnes, resultats[SPECIAL_CONSTRUCTION], WIDTH, label="Construction", bottom=bottom)
    # for i in range(len(bottom)):
    #     bottom[i] = resultats[SPECIAL_CONSTRUCTION][i]
    # plt.bar(colonnes, resultats[SPECIAL_CHEMIN], WIDTH, label="Chemin", bottom=bottom)
    
    # Voronoi
    plt.bar(x=resultats[DIC_PRECISION], height=resultats[CONSTRUCTION_VORONOI], label="Voronoï (Construction)", color="#d23333", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION], height=resultats[CHEMIN_VORONOI], label="Voronoï (Chemin)", bottom=resultats[CONSTRUCTION_VORONOI], color="#e68b8b", width=PRECISION_STEP/5)

    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/4, height=resultats[CONSTRUCTION_NAIF], color="#ffcd00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/2, height=resultats[CONSTRUCTION_NAIF], label="Naïf (Construction)", color="#ffcd00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/4, height=resultats[CHEMIN_DIJKSTRA], bottom=resultats[CONSTRUCTION_NAIF], label="Naïf (Dijkstra)", color="#35ce00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/2, height=resultats[CHEMIN_ASTAR], bottom=resultats[CONSTRUCTION_NAIF], label="Naïf (A*)", color="#0093ce", width=PRECISION_STEP/5)

    plt.xlabel("Précision (ua)", fontsize=30)
    plt.ylabel("Temps de calcul (ns)", fontsize=30)
    plt.title("Comparaison de l'efficacité des méthodes en fonction de la précision", fontweight='bold', fontsize=30)
    plt.legend(fontsize=20)
    plt.show()

def test_grand_labyrinthe():
    
    CARTE = "labyrinthe_16x16.map"
    BOUNDING = ((-1., 17.), (-1., 17.))
    DEBUT = Point(0.5, 15.5)
    FIN = Point(8, 8)

    PRECISION_STEP = 0.1
    PRECISION_MIN = 0.1
    PRECISION_MAX = 0.4
    
    n_steps = floor((PRECISION_MAX - PRECISION_MIN) / PRECISION_STEP) + 1
    i = 0
    # SPECIAL = 1
    
    resultats = {
        DIC_PRECISION: np.empty(n_steps),
        CONSTRUCTION_VORONOI: np.empty(n_steps),
        CHEMIN_VORONOI: np.empty(n_steps),
        CONSTRUCTION_NAIF: np.empty(n_steps),
        CHEMIN_DIJKSTRA: np.empty(n_steps),
        CHEMIN_ASTAR: np.empty(n_steps),
        SPECIAL_CONSTRUCTION: np.empty(n_steps),
        SPECIAL_CHEMIN: np.empty(n_steps)
    }

    # precision = PRECISION_MIN
    precision = PRECISION_MAX

    while precision <= PRECISION_MAX and precision >= PRECISION_MIN:
        
        assert i < n_steps, f"{i=}, {n_steps=}, {precision=}, {PRECISION_MAX}"

        temps_vor = test_voronoi(CARTE, precision, BOUNDING, DEBUT, FIN)
        temps_naif = test_naif(CARTE, precision, BOUNDING, DEBUT, FIN)

        resultats[DIC_PRECISION][i] = precision
        resultats[CHEMIN_VORONOI][i] = temps_vor[CHEMIN_VORONOI]
        resultats[CONSTRUCTION_VORONOI][i] = temps_vor[CONSTRUCTION_VORONOI]
        resultats[CONSTRUCTION_NAIF][i] = temps_naif[CONSTRUCTION_NAIF]
        resultats[CHEMIN_DIJKSTRA][i] = temps_naif[CHEMIN_DIJKSTRA]
        resultats[CHEMIN_ASTAR][i] = temps_naif[CHEMIN_ASTAR]

        afficher_parametres()
        # precision += PRECISION_STEP
        precision -= PRECISION_STEP
        i += 1
        
    # assert i == n_steps
    
    # SPECIAL

    # temps_vor = test_voronoi(CARTE, SPECIAL, BOUNDING, DEBUT, FIN)
    # temps_naif = test_naif(CARTE, SPECIAL, BOUNDING, DEBUT, FIN)
    
    # resultats[SPECIAL_CONSTRUCTION] = [temps_vor[CONSTRUCTION_VORONOI], temps_naif[CONSTRUCTION_NAIF], temps_naif[CONSTRUCTION_NAIF]]
    # resultats[SPECIAL_CHEMIN] = [temps_vor[CHEMIN_VORONOI], temps_naif[CHEMIN_DIJKSTRA], temps_naif[CHEMIN_ASTAR]]


    plt.figure()
    
    colonnes = ("Voronoi",
                "Naif\nChemin Dijkstra",
                "Naif\nChemin A*"
        )
    
    # bottom = [0, 0, 0]
    # WIDTH = 1
    
    # Construction
    # plt.bar(colonnes, resultats[SPECIAL_CONSTRUCTION], WIDTH, label="Construction", bottom=bottom)
    # for i in range(len(bottom)):
    #     bottom[i] = resultats[SPECIAL_CONSTRUCTION][i]
    # plt.bar(colonnes, resultats[SPECIAL_CHEMIN], WIDTH, label="Chemin", bottom=bottom)
    
    # Voronoi
    plt.bar(x=resultats[DIC_PRECISION], height=resultats[CONSTRUCTION_VORONOI], label="Voronoï (Construction)", color="#d23333", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION], height=resultats[CHEMIN_VORONOI], label="Voronoï (Chemin)", bottom=resultats[CONSTRUCTION_VORONOI], color="#e68b8b", width=PRECISION_STEP/5)

    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/4, height=resultats[CONSTRUCTION_NAIF], color="#ffcd00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/2, height=resultats[CONSTRUCTION_NAIF], label="Naïf (Construction)", color="#ffcd00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/4, height=resultats[CHEMIN_DIJKSTRA], bottom=resultats[CONSTRUCTION_NAIF], label="Naïf (Dijkstra)", color="#35ce00", width=PRECISION_STEP/5)
    plt.bar(x=resultats[DIC_PRECISION] + PRECISION_STEP/2, height=resultats[CHEMIN_ASTAR], bottom=resultats[CONSTRUCTION_NAIF], label="Naïf (A*)", color="#0093ce", width=PRECISION_STEP/5)

    plt.legend(prop={'size': 6})
    plt.show()


def main() -> None:
    
    setrecursionlimit(1000000)
    
    test_bateaux()
    # test_grand_labyrinthe()

    return

if __name__ == "__main__":
    main()
    