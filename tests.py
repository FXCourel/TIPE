from robots.carte.carte import Carte
from robots.geometrie.point import Point
from robots.settings import Settings
from robots.graphe.carte_graphee import CarteGraphee
from robots.naif.carte_naif import CarteNaif
from robots.naif.visualisation import Visualisation_Naif
from robots.graphe.visualisation import Visualisation
from foronoi import Voronoi, Visualizer, BoundingBox


def main():

    # c = Carte.creer_carte()
    # c.print_carte()
    # c.sauvegarder("test.map")

    # input("Test lecture de carte [Entrée]:")

    Settings.PRECISION = 0.323
    
    DEBUT = Point(0.5, 15.5)
    FIN = Point(8, 8)
    bsize = ((-1., 17.), (-1., 17.))
    lecture = Carte.lire_carte("labyrinthe_16x16.map")
    lecture.decouper_obstacles(Settings.PRECISION)
    # lecture.print_carte()

    points = lecture.voronoi_set()
    

    # bounding_box = BoundingBox(0., 40., 0., 30.)

    # v = Voronoi(bounding_box)

    # v.create_diagram(
    #     points=points,
    # )

    # edges = v.edges
    # vertices = v.vertices
    # arcs = v.arcs
    # points = v.sites

    # # Plotting
    # Visualizer(v, canvas_offset=1) \
    #     .plot_sites(points, show_labels=False) \
    #     .plot_edges(edges, show_labels=False) \
    #     .show()
    #     # .plot_vertices(vertices)\
    # # .plot_vertices(vertices) \
    # # .plot_polygon()\
    # # .plot_border_to_site() \

    carte_g = CarteGraphee.from_scratch("labyrinthe_16x16.map", bsize)
    visualizer = Visualisation(carte_g)
    visualizer.plot(show_finally=True)
    

    # carte_g.simplifier_graphe()
    # visualizer.plot(show_finally=True)
    
    # carte_g.supprimer_culs_de_sac()
    # visualizer.clear()
    # visualizer.plot(show_finally=True)
    
    # debut = Point(3.25, 5.75)
    # arrivee = Point(3.75, 2.75)
    
    # carte_g.ajouter_point(debut, arrivee)
    
    # chemin = carte_g.calculer_chemin(debut, arrivee)
    # visualizer.plot_chemin(chemin)
    # visualizer.show()
    
def test_naif():
    
    # carte_naive = CarteNaif.from_scratch("bateaux.map", ((0., 40), (0., 30.)))
    # carte_naive = CarteNaif.from_scratch("labyrinthe_5x5.map", ((0., 7.), (0., 7.)))
    # viz = Visualisation_Naif(carte_naive)
    
    # chemin = carte_naive.dijkstra((1, 1), (29, 29))
    # chemin_2 = carte_naive.a_star((1, 1), (29, 29))
    # viz.plot()
    # viz.plot_chemin_int(chemin)
    # viz.plot_chemin_int(chemin_2, "red")
    # viz.show()
    return


if __name__ == "__main__":
    main()
    # test_naif()
