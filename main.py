"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : main.py, contient le code principal du programme

"""

from settings import *
import carte
import algos
import point
import random
import voronoi
import matplotlib.pyplot as plt
import sys


def main():
    
    #### VARIABLES GLOBALES

    ## Variables de debug
    debug = False
    if "--debug" in sys.argv:
        debug = True

    if debug: print(f"SEED = {SEED}\nTAILLE_CARTE = {TAILLE_CARTE}\nNOMBRE_ILES = {NOMBRE_ILES}\nTAILLE_ILES = {TAILLE_ILES}\n")

    seed = SEED if 0 <= SEED < 2**32 else random.randint(0, 2**32)
    
    c = carte.Carte(seed, debug)
    c.print_carte()

    if debug : input("Programme éxécuté avec succès, appuyez sur une touche pour quitter...")
    return



if __name__ == "__main__":

    main()