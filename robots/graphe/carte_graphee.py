from robots.graphe.graphe import Graphe, CheminNonTrouve
from robots.carte.carte import Carte
from robots.carte.obstacle import Obstacle
from robots.settings import Settings
from robots.geometrie.point import Point
from foronoi import Voronoi, Vertex, HalfEdge, Point_V, BoundingBox

from typing import List, Dict, Union, Tuple


class CarteGraphee(Graphe):

    def __init__(self, carte_origine) -> None:
        super().__init__()
        self.carte_origine = carte_origine
        self.chemin_entre: dict[Tuple[Point, Point], List[Point]] = {}
        self.est_dans_arete: dict[Point, Tuple[Point, Point]] = {}
        self.optimisee: bool = False

    @classmethod
    def from_voronoi(cls, voronoi: Voronoi, carte_origine: Carte) -> 'CarteGraphee':
        sites: List[Point_V] = list(voronoi.sites)
        aretes: List[HalfEdge] = voronoi.edges
        vertices: List[Vertex] = voronoi.vertices

        def vertex_to_tuple(vertex: Vertex):
            return (vertex.x, vertex.y)

        def point_to_tuple(p: Point):
            return (p.x, p.y)

        def pointV_to_tuple(p: Point_V):
            return (p.x, p.y)

        def est_meme_obstacle(p1: Point_V, p2: Point_V):
            t1 = pointV_to_tuple(p1)
            t2 = pointV_to_tuple(p2)
            s1 = site_to_num_obstacle[t1]
            s2 = site_to_num_obstacle[t2]
            return s1 >= 0 and s1 == s2

        vertex_to_point: Dict[tuple, Point] = {
            vertex_to_tuple(vertex): Point(vertex.xd, vertex.yd) for vertex in vertices}

        site_to_num_obstacle: Dict[tuple, Obstacle] = {
            k: [] for k in range(len(carte_origine.obstacles))}
        for k, o in enumerate(carte_origine.obstacles):
            for p in o.contours:
                site_to_num_obstacle[point_to_tuple(p)] = k

        carte: CarteGraphee = cls(carte_origine)

        for e in aretes:
            center: Point_V = e.point_incident
            point_oppose: Point_V = e.jumelle.point_incident
            if point_oppose is not None:
                d = Point.distance_eucli(
                    center.xd, center.yd, point_oppose.xd, point_oppose.yd)
                try:
                    if d >= Settings.MULT_ESPACEMENT_SITES * Settings.PRECISION and not (carte_origine.obstacles_convexes and est_meme_obstacle(center, point_oppose)):

                        carte.ajouter_arete((source := vertex_to_point[vertex_to_tuple(e.origine)]), (
                            dest := vertex_to_point[vertex_to_tuple(e.cible)]), source.distance(dest))
                except KeyError as err:
                    print(err)
                    pass

        return carte

    @classmethod
    def from_scratch(cls, nom_fichier: str, bounding_size: Tuple[Tuple[float, float], Tuple[float, float]], force_bound: bool = True) -> 'CarteGraphee':
        carte_raw: Carte = Carte.lire_carte(nom_fichier)
        (x_min, x_max), (y_min, y_max) = bounding_size
        if force_bound:
            carre = [
                Point(x_min, y_min),
                Point(x_min, y_max),
                Point(x_max, y_max),
                Point(x_max, y_min)
            ]
            carte_raw.obstacles.append(Obstacle(carre, False, True))
        carte_raw.decouper_obstacles(Settings.PRECISION)
        bounding_box = BoundingBox(x_min, x_max, y_min, y_max)
        v = Voronoi(bounding_box)
        v.create_diagram(points=list(carte_raw.voronoi_set()))
        carte: CarteGraphee = cls.from_voronoi(v, carte_raw)
        carte.simplifier_graphe()
        # carte.supprimer_culs_de_sac()
        return carte

    def point_le_plus_proche(self, point: Point) -> Point:
        best: Point = None
        dist = -1
        liste_sommets = self.sommets_old or self.sommets
        for p in liste_sommets:
            if (d := point.distance(p)) < dist or dist < 0:
                dist = d
                best = p
        assert best is not None
        return best

    def ajouter_point(self, *points: Point) -> None:

        for point in points:
            if point in self.sommets:
                continue
            pp = self.point_le_plus_proche(point)
            d_pp = point.distance(pp)
            self.sommets.add(point)
            self.adjacence[pp].add((point, d_pp))
            self.adjacence[point] = set()
            self.adjacence[point].add((pp, d_pp))
            self.unique_adjacence[Point.order(point, pp)] = d_pp
            assert self.chemin_entre
            self.chemin_entre[Point.order(point, pp)] = [point, pp]

    def simplifier_graphe(self) -> None:

        intersections: set[Point] = set()
        for sommet in self.sommets:
            deg_s = len(self.adjacence[sommet])
            # Si le degre est différent de 2, on fusionne l'arete
            if deg_s != 2:
                intersections.add(sommet)

        new_adjacence = {p: set() for p in intersections}
        new_unique_adjacence = {}
        traites = set()
        for intersection in intersections:
            for branche in self.adjacence[intersection]:
                if branche[0] in traites:
                    continue
                prec = intersection
                s, cout = branche
                longueur_chemin: Union[float, int] = cout
                trajet = [intersection]
                while s not in intersections:
                    traites.add(s)
                    trajet.append(s)
                    voisins_suivants = self.adjacence[s]
                    assert len(
                        voisins_suivants) == 2, f"set was {len(voisins_suivants)}"
                    (s1, c1), (s2, c2) = tuple(voisins_suivants)
                    assert (s1 == prec) ^ (s2 == prec)
                    # On avance dans la direction inexplorée
                    if s1 == prec:
                        longueur_chemin += c2
                        prec = s
                        s = s2
                    else:
                        longueur_chemin += c1
                        prec = s
                        s = s1
                # s est maintenant l'intersection suivante dans la brache partant de intersection
                trajet.append(s)
                self.chemin_entre[Point.order(
                    intersection, s)] = trajet if intersection < s else trajet[::-1]
                for u in trajet:
                    self.est_dans_arete[u] = Point.order(trajet[0], trajet[-1])

                new_adjacence[intersection].add((s, longueur_chemin))
                new_adjacence[s].add((intersection, longueur_chemin))
                new_unique_adjacence[Point.order(
                    intersection, s)] = longueur_chemin

        self.sommets_old = self.sommets
        self.unique_adjacence_old = self.unique_adjacence
        self.adjacence_old = self.adjacence

        self.sommets = intersections
        self.adjacence = new_adjacence
        self.unique_adjacence = new_unique_adjacence
        self.optimisee = True

    def _supprimer_cul_de_sac(self, v) -> None:
        v2, _ = self.adjacence[v].pop()
        self.adjacence[v2].remove((v, _))
        del self.adjacence[v]
        del self.chemin_entre[Point.order(v, v2)]
        del self.unique_adjacence[Point.order(v, v2)]

    def supprimer_culs_de_sac(self) -> None:

        suppr = set()

        for v in self.sommets:
            if len(self.adjacence[v]) == 1:
                # On supprime le cul de sac
                self._supprimer_cul_de_sac(v)
                suppr.add(v)

        for v in suppr:
            self.sommets.remove(v)

    def calculer_chemin(self, depart, arrivee) -> List[Point]:

        depart_pp = self.point_le_plus_proche(depart)
        arrivee_pp = self.point_le_plus_proche(arrivee)

        if self.optimisee:

            a_depart, b_depart = self.est_dans_arete[depart_pp]
            a_arrivee, b_arrivee = self.est_dans_arete[arrivee_pp]
            chemin_depart = self.chemin_entre[(a_depart, b_depart)]
            chemin_arrivee = self.chemin_entre[(a_arrivee, b_arrivee)]
            i_depart = chemin_depart.index(depart_pp)
            i_arrivee = chemin_arrivee.index(arrivee_pp)

            if a_depart == chemin_depart[0]:
                # try:
                cout_a_to_depart = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_depart[:i_depart], chemin_depart[1:i_depart+1]))
                self.ajouter_arete(depart_pp, a_depart, cout_a_to_depart)
                # except KeyError:
                #     for p, p_next in zip(chemin_depart[:i_depart], chemin_depart[1:i_depart+1]):
                #         print(self.adjacence_old[p], p, '\n', self.adjacence_old[p_next], p_next)
                #         assert p in self.sommets_old, p
                #         print((p, p_next) in self.unique_adjacence_old, (p_next, p) in self.unique_adjacence_old)
                #         d = Point.distance_eucli(p.x, p.y, p_next.x, p_next.y)
                #         print((p, d) in self.adjacence_old[p_next], (p_next, d) in self.adjacence_old[p])
                #     raise
                cout_b_to_depart = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_depart[i_depart:-1], chemin_depart[i_depart+1:]))
                self.ajouter_arete(depart_pp, b_depart, cout_b_to_depart)
                self.chemin_entre[Point.order(a_depart, depart_pp)] = chemin_depart[:i_depart +
                                                                                    1] if a_depart < depart_pp else chemin_depart[:i_depart+1][::-1]
                self.chemin_entre[Point.order(
                    b_depart, depart_pp)] = chemin_depart[i_depart:] if depart_pp < b_depart else chemin_depart[i_depart:][::-1]
            else:
                assert b_depart == chemin_depart
                cout_b_to_depart = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_depart[:i_depart], chemin_depart[1:i_depart+1]))
                self.ajouter_arete(depart_pp, b_depart, cout_b_to_depart)
                cout_a_to_depart = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_depart[i_depart:-1], chemin_depart[i_depart+1:]))
                self.ajouter_arete(depart_pp, a_depart, cout_a_to_depart)
                self.chemin_entre[Point.order(
                    b_depart, depart_pp)] = chemin_depart[:i_depart+1] if b_depart < depart_pp else chemin_depart[:i_depart+1]
                self.chemin_entre[Point.order(
                    a_depart, depart_pp)] = chemin_depart[i_depart:] if depart_pp < a_depart else chemin_depart[i_depart:][::-1]

            if a_arrivee == chemin_arrivee[0]:
                cout_a_to_arrivee = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_arrivee[:i_arrivee], chemin_arrivee[1:i_arrivee+1]))
                self.ajouter_arete(arrivee_pp, a_arrivee, cout_a_to_arrivee)
                cout_b_to_arrivee = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_arrivee[i_arrivee:-1], chemin_arrivee[i_arrivee+1:]))
                self.ajouter_arete(arrivee_pp, b_arrivee, cout_b_to_arrivee)
                self.chemin_entre[Point.order(a_arrivee, arrivee_pp)] = chemin_arrivee[:i_arrivee +
                                                                                       1] if a_arrivee < arrivee_pp else chemin_arrivee[:i_arrivee+1][::-1]
                self.chemin_entre[Point.order(
                    b_arrivee, arrivee_pp)] = chemin_arrivee[i_arrivee:] if arrivee_pp < b_arrivee else chemin_arrivee[i_arrivee:][::-1]
            else:
                cout_b_to_arrivee = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_arrivee[:i_arrivee], chemin_arrivee[1:i_arrivee+1]))
                self.ajouter_arete(arrivee_pp, b_arrivee, cout_b_to_arrivee)
                cout_a_to_arrivee = sum(self.unique_adjacence_old[Point.order(p, p_next)] for p, p_next in zip(
                    chemin_arrivee[i_arrivee:-1], chemin_arrivee[i_arrivee+1:]))
                self.ajouter_arete(arrivee_pp, a_arrivee, cout_a_to_arrivee)
                assert b_arrivee == chemin_arrivee
                self.chemin_entre[Point.order(
                    b_arrivee, arrivee_pp)] = chemin_arrivee[:i_arrivee+1] if b_arrivee < arrivee_pp else chemin_arrivee[:i_arrivee+1]
                self.chemin_entre[Point.order(
                    a_arrivee, arrivee_pp)] = chemin_arrivee[i_arrivee:] if arrivee_pp < a_arrivee else chemin_arrivee[i_arrivee:][::-1]

        chemin = self.dijkstra(depart_pp, arrivee_pp)

        if self.optimisee:
            # Ceci est le chemin dans le graphe simplifié, on recompose le chemin complet ensuite
            chemin_complet = [depart]
            for p, p_next in zip(chemin[:-1], chemin[1:]):
                if p < p_next:
                    chemin_complet.extend(
                        self.chemin_entre[Point.order(p, p_next)])
                else:
                    chemin_complet.extend(
                        self.chemin_entre[Point.order(p_next, p)][::-1])
        else:
            chemin_complet = [depart] + chemin

        chemin_complet.append(arrivee)

        return chemin_complet
