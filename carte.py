"""

    TIPE 2023 - FRANCOIS-XAVIER COUREL
    Sujet : "Algorithme de recherche de chemin dans une carte"

    Fichier : carte.py, contient la classe Carte et la classe Ile

"""

import matplotlib.pyplot as plt
from settings import *
import random
import math
import algos
from ile import Ile
from point import Point, Droite
import time




class Carte:

    def __init__(self, seed, debug=False):

        t_debut = time.time()
        assert TAILLE_CARTE[0] >= 40 and TAILLE_CARTE[1] >= 40, "Carte trop petite"
        self.iles = []
        self.debug = debug
        self.seed = seed
        self.generate()

        if self.debug: print(f"Carte créée ({(time.time() - t_debut)*1000}ms)")


    # Création d'une carte aléatoire
    def generate(self):

        random.seed(self.seed)
        self.iles = []
        if self.debug: print(f"Génération de la carte (Graine : {self.seed})...")

        # On génère des points qui les centres d'iles
        quadrants = [(int((TAILLE_CARTE[0]-4*TAILLE_ILES)*x/3 + 2*TAILLE_ILES),int((TAILLE_CARTE[1]- 4*TAILLE_ILES)*y/3 + 2*TAILLE_ILES)) for x in range(4) for y in range(4)]
        print(quadrants)
        for i in range(3):
            for j in range(3):
                for n in range(math.ceil(NOMBRE_ILES/9)):
                    x = random.randint(quadrants[4*i+j][0], quadrants[4*(i+1)+(j+1)][0])
                    y = random.randint(quadrants[4*i+j][1], quadrants[4*(i+1)+(j+1)][1])
                    self.iles.append([Point(x, y)])

        # Autour de ces centres on génère des points à une distance entre 1/2*taille_iles et 2*taille_iles
        for k in range(len(self.iles)):

            ile = self.iles[k]
            centre = ile[0]

            # On place des points autour du centre à une distance aléatoire, dans le sens trigo
            for i in range(TAILLE_ILES * 5):

                distance_random = random.uniform(0, random.uniform(0, TAILLE_ILES))
                ile.append(Point(int(centre.x + distance_random * math.cos(2*math.pi*i/(TAILLE_ILES*5))),
                                 int(centre.y + distance_random * math.sin(2*math.pi*i/(TAILLE_ILES*5)))))

            self.iles[k] = [self.iles[k][0]] + algos.parcours_de_graham(ile)

        random.shuffle(self.iles)

        for _ in range(math.ceil(NOMBRE_ILES/9) - NOMBRE_ILES):
            self.iles.pop()

        # Conversion des points en Iles
        for i in range(len(self.iles)):
            self.iles[i] = Ile(self.iles[i])

        if self.debug: print("Iles générées, fusion des iles..."); print(self.iles)

        iles_a_supprimer = []

        # On fusionne les iles qui se touchent
        for i in range(len(self.iles)):

            ile_fusionnee = True
            while ile_fusionnee:
                ile_fusionnee = False

                for j in range(i+1, len(self.iles)):

                    if j in iles_a_supprimer: continue

                    ile1 = self.iles[i]
                    ile2 = self.iles[j]

                    # On vérifie si les iles se touchent
                    if ile1.se_touchent(ile2): 

                        # On fusionne les iles
                        if self.debug: print("Fusion des iles", i, ile1, "et", j, ile2); print(self.iles[i])
                        ile1.fusionner(ile2)
                        ile_fusionnee = True
                        iles_a_supprimer.append(j)

        iles_a_supprimer = sorted(list(set(iles_a_supprimer)), reverse=True)
        if self.debug: print("Iles à supprimer :", iles_a_supprimer)
        for ile in iles_a_supprimer:
            self.iles.pop(ile)

        return


    # Affichage de la carte avec pyplot
    def print_carte(self, titre="Carte", stop_script=True):

        plt.figure(num=titre, figsize=(TAILLE_CARTE[0], TAILLE_CARTE[1]))
        plt.xlim([0, TAILLE_CARTE[0]])
        plt.ylim([0, TAILLE_CARTE[1]])
        plt.xlabel("x")
        plt.ylabel("y")
        for ile in self.iles:
            plt.fill(ile.points_x, ile.points_y)
        plt.grid()
        plt.show(block=stop_script)
        return



if __name__ == "__main__":
    print("Ce fichier ne doit pas être exécuté directement")