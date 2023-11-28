from settings import *



def construire(iles, debug):

    # On construit le diagramme de Voronoi en utilisant l'algorithme de Shamos et Hoey, en utilisant diviser pour régner, en O(n log n)

    # On commence par trier les iles par ordre croissant de leur abscisse
    iles = sorted(iles, key=lambda ile: ile.centre.x)

    # On construit le diagramme de Voronoi
    voronoi_diagram = []

    return