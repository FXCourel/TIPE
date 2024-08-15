from robots.settings import Settings
from robots.geometrie.algos import Algos
from robots.carte.obstacle import Obstacle
from robots.geometrie.point import Point, Droite
import matplotlib.pyplot as plt
import math
import random
import os
import sys
import re


class Carte:

    def __init__(self, seed: int = 0, obstacles_convexes: bool = False) -> None:

        self.obstacles: list[Obstacle] = []
        self.seed = seed
        self.obstacles_convexes = obstacles_convexes

    # Création d'une carte aléatoire
    def generate(self) -> None:

        assert Settings.TAILLE_CARTE[0] >= 40 and Settings.TAILLE_CARTE[1] >= 40, "Carte trop petite pour génération"
        random.seed(self.seed)
        self.obstacles = []
        self.obstacles_convexes = True
        if Settings.DEBUG:
            print(f"Génération de la carte (Graine : {self.seed})...")

        # On génère des points qui les centres d'obstacles
        quadrants = [(int((Settings.TAILLE_CARTE[0]-4*Settings.TAILLE_ILES)*x/3 + 2*Settings.TAILLE_ILES), int(
            (Settings.TAILLE_CARTE[1] - 4*Settings.TAILLE_ILES)*y/3 + 2*Settings.TAILLE_ILES)) for x in range(4) for y in range(4)]
        if Settings.DEBUG:
            print(quadrants)
        for i in range(3):
            for j in range(3):
                for _ in range(math.ceil(Settings.NOMBRE_ILES/9)):
                    x = random.randint(
                        quadrants[4*i+j][0], quadrants[4*(i+1)+(j+1)][0])
                    y = random.randint(
                        quadrants[4*i+j][1], quadrants[4*(i+1)+(j+1)][1])
                    self.obstacles.append([Point(x, y)])

        # Autour de ces centres on génère des points à une distance entre 1/2*taille_obstacles et 2*taille_obstacles
        for k in range(len(self.obstacles)):

            obstacle = self.obstacles[k]
            centre = obstacle[0]

            # On place des points autour du centre à une distance aléatoire, dans le sens trigo
            for i in range(Settings.TAILLE_ILES * 5):

                distance_random = random.uniform(
                    0, random.uniform(0, Settings.TAILLE_ILES))
                obstacle.append(Point(int(centre.x + distance_random * math.cos(2*math.pi*i/(Settings.TAILLE_ILES*5))),
                                      int(centre.y + distance_random * math.sin(2*math.pi*i/(Settings.TAILLE_ILES*5)))))

            self.obstacles[k] = [self.obstacles[k][0]] + \
                Algos.parcours_de_graham(obstacle)

        random.shuffle(self.obstacles)

        for _ in range(math.ceil(Settings.NOMBRE_ILES/9) - Settings.NOMBRE_ILES):
            self.obstacles.pop()

        # Conversion des points en Obstacles
        for i in range(len(self.obstacles)):
            self.obstacles[i] = Obstacle(self.obstacles[i], True)

        if Settings.DEBUG:
            print("Obstacles générées, fusion...")
            print(self.obstacles)

        obstacles_a_supprimer = []

        # On fusionne les obstacles qui se touchent
        for i in range(len(self.obstacles)):

            obstacle_fusionne = True
            while obstacle_fusionne:
                obstacle_fusionne = False

                for j in range(i+1, len(self.obstacles)):

                    if j in obstacles_a_supprimer:
                        continue

                    obstacle1 = self.obstacles[i]
                    obstacle2 = self.obstacles[j]

                    # On vérifie si les obstacles se touchent
                    if obstacle1.se_touchent(obstacle2):

                        # On fusionne les obstacles
                        if Settings.DEBUG:
                            print("Fusion des obstacles", i,
                                  obstacle1, "et", j, obstacle2)
                            print(self.obstacles[i])
                        obstacle1.fusionner(obstacle2)
                        obstacle_fusionne = True
                        obstacles_a_supprimer.append(j)

        obstacles_a_supprimer = sorted(
            list(set(obstacles_a_supprimer)), reverse=True)
        if Settings.DEBUG:
            print("Obstacles à supprimer :", obstacles_a_supprimer)
        for obstacle in obstacles_a_supprimer:
            self.obstacles.pop(obstacle)

    def decouper_obstacles(self, precision) -> None:
        for o in self.obstacles:
            o.decoupage_contours(precision)

    def voronoi_set(self) -> set[tuple]:
        s = set()
        for o in self.obstacles:
            for p in o.contours:
                s.add(p.to_tuple())
        return s

    # Affichage de la carte avec pyplot

    def print_carte_fill(self, titre="Carte", stop_script=True) -> None:

        plt.figure(num=titre, figsize=(
            Settings.TAILLE_CARTE[0], Settings.TAILLE_CARTE[1]))
        plt.xlim([0, Settings.TAILLE_CARTE[0]])
        plt.ylim([0, Settings.TAILLE_CARTE[1]])
        plt.xlabel("x")
        plt.ylabel("y")
        for obstacle in self.obstacles:
            plt.fill(obstacle.points_x, obstacle.points_y)
        plt.grid()
        plt.show(block=stop_script)

    def print_carte(self, titre="Carte", stop_script=True) -> None:

        plt.figure(num=titre, figsize=(
            Settings.TAILLE_CARTE[0], Settings.TAILLE_CARTE[1]))
        plt.xlim([0, Settings.TAILLE_CARTE[0]])
        plt.ylim([0, Settings.TAILLE_CARTE[1]])
        plt.xlabel("x")
        plt.ylabel("y")
        for obstacle in self.obstacles:
            contours = obstacle.contours
            for i in range(len(contours) - 1):
                p_i: Point = contours[i]
                p_i_next: Point = contours[i + 1]
                plt.plot([p_i.x, p_i_next.x], [p_i.y, p_i_next.y])
        if Settings.PLT_ENABLE_GRID:
            plt.grid()
        plt.show(block=stop_script)

    def sauvegarder(self, nom_fichier) -> None:
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        nom_fichier = script_directory + "/cartes/" + nom_fichier
        with open(nom_fichier, 'w') as f:
            f.write(f"SEED={self.seed}\n")
            f.write("HAS_CENTER\n")
            if self.obstacles_convexes:
                f.write("CONVEXE\n")
            f.write("----------\n")
            for obstacle in self.obstacles:
                f.write("\n")
                for point in obstacle.contours:
                    f.write(f"Point:{point.x}|{point.y}\n")
            f.write("\nEOF\n")
        return

    @classmethod
    def creer_carte(cls, seed: int = 0) -> 'Carte':
        if Settings.DEBUG:
            print(
                f"SEED = {Settings.SEED}\nSettings.TAILLE_CARTE = {Settings.TAILLE_CARTE}\nSettings.NOMBRE_ILES = {Settings.NOMBRE_ILES}\nSettings.TAILLE_ILES = {Settings.TAILLE_ILES}\n")

        seed = Settings.SEED if 0 <= Settings.SEED < 2**32 else random.randint(
            0, 2**32)

        c = cls(seed)
        c.generate()

        if Settings.DEBUG:
            input("Carte générée succès, appuyez sur une touche pour continuer...")

        return c

    @classmethod
    def lire_carte(cls, nom_fichier: str) -> 'Carte':
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        nom_fichier = script_directory + "/cartes/" + nom_fichier
        carte = cls()
        with open(nom_fichier, 'r') as f:
            obstacle = []
            num_obstacle = 1
            has_center = False
            for ligne in f.readlines():
                ligne = ligne.removesuffix('\n')
                if ligne.startswith("SEED="):
                    carte.seed = int(ligne[5:])
                elif ligne.startswith("HAS_CENTER"):
                    has_center = True
                elif ligne.startswith("CONVEXE"):
                    carte.obstacles_convexes = True
                elif obstacle != [] and (ligne == "" or False):
                    carte.obstacles.append(Obstacle(obstacle, has_center))
                    obstacle = []
                    num_obstacle += 1
                elif ligne.startswith("Point:"):
                    l = ligne[6:]
                    coords = l.split('|')
                    assert len(coords) == 2
                    obstacle.append(
                        Point(float(coords[0]), float(coords[1]), num_obstacle))
        if Settings.DEBUG:
            carte.print_carte(nom_fichier)

        return carte


if __name__ == "__main__":
    print("Ce fichier ne doit pas être exécuté directement")
