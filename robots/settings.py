#### VARIABLES GLOBALES
class Settings:
    
    DEBUG = False

    ## Variables de génération
    SEED = -1 # -1 pour une graine aléatoire, sinon une graine entière <= 2**32
    TAILLE_CARTE = (7, 7)
    NOMBRE_ILES = 8
    TAILLE_ILES = 5

    ## Variables de l'algorithme
    PRECISION = 0.2 # espacements entre deux points d'une droite
    MULT_ESPACEMENT_SITES = 1.25 # Multiplicateur de la précision pour laquelle les aretes entre les sites sont supprimées
    
    NAIF_MARGE = 1 # Marge de l'algorithme naif

    ## Plt
    PLT_ENABLE_GRID = False