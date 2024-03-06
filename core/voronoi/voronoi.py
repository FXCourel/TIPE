from Events import *
from Arbre import *
from Graphe import *
from Maths import *


class Voronoi:

    def __init__(self, points_set: list[tuple[float, float]], bounding_box: Polygone = None, build: bool = True):
        self.bounding_box = bounding_box
        self.points_set = set(Point(x, y) for x, y in points_set)
        self.events = Tas()
        self.bleach_line: Noeud = None
        self.dcel = DCEL()
        self.sweep_line = float("inf")
        
        self.sites = None
        self.edges = list()
        self._vertices = set()
        self._arcs = set()

        if build:
            self.diagram = self.construction(points_set)
            
    @property
    def vertices(self):
        return list(self._vertices)
    
    @property
    def arcs(self):
        return list(self._arcs)
    
    def construction(self):

        # Input. A set P := {p1, . . . , pn} of point sites in the plane.
        # Output. The Voronoi diagram Vor(P) given inside a bounding box in a doubly-connected edge list D.
        # 1. Initialize the event queue Q with all site events, initialize an empty status
        # structure T and an empty doubly-connected edge list D.
        self.sites = self.points_set
        self.events.tas = [Event(p, SITE_EVENT) for p in self.points_set]
        assert self.events.est_tas()

        # 2. while Q is not empty
        while not self.events.est_vide():

            # 3. do Remove the event with largest y-coordinate from Q.
            event: Event = self.events.extraire_maximum()

            # 4. if the event is a site event, occurring at site p i
            if event.is_site_event():
                pi = event.site
                assert isinstance(pi, Point)
                self.sweep_line = pi.yd

                # 5. then HandleSiteEvent(p i)
                self.handle_site_event(pi)

            else:

                # 6. else HandleCircleEvent(γ), where γ is the leaf of T repre-
                # senting the arc that will disappear
                self.sweep_line = event

                gamma = event.circle
                self.handle_circle_event(gamma)

        # 7. The internal nodes still present in T correspond to the half-infinite edges of
        # the Voronoi diagram. Compute a bounding box that contains all vertices of
        # the Voronoi diagram in its interior, and attach the half-infinite edges to the
        # bounding box by updating the doubly-connected edge list appropriately.

        # 8. Traverse the half-edges of the doubly-connected edge list to add the cell
        # records and the pointers to and from them


    def handle_site_event(self, pi):
        # 1. If T is empty, insert pi into it (so that T consists of a single leaf storing pi)
        # and return. Otherwise, continue with steps 2– 5.
        if Arbre.est_vide(self.bleach_line):
            self.bleach_line = Noeud(pi)
            return

        # 2. Search in T for the arc α vertically above pi. If the leaf representing α has
        # a pointer to a circle event in Q, then this circle event is a false alarm and it
        # must be deleted from Q.
        alpha: Noeud = self.bleach_line.recherche()

        assert isinstance(alpha.data, Event)

        if alpha.data.is_circle_event():
            alpha.data.fausse_alerte = True

        # 3. Replace the leaf of T that represents α with a subtree having three leaves.
        # The middle leaf stores the new site pi and the other two leaves store the site
        # p j that was originally stored with α. Store the tuples 〈p j, p i〉 and 〈p i, p j〉
        # representing the new breakpoints at the two new internal nodes. Perform
        # rebalancing operations on T if necessary.

        # 4. Create new half-edge records in the Voronoi diagram structure for the
        # edge separating V(pi) and V(p j), which will be traced out by the two new
        # breakpoints.

        # 5. Check the triple of consecutive arcs where the new arc for pi is the left arc
        # to see if the breakpoints converge. If so, insert the circle event into Q and
        # add pointers between the node in T and the node in Q. Do the same for the
        # triple where the new arc is the right arc.
        pass


    def handle_circle_event(self, gamma):
        # 1. Delete the leaf γ that represents the disappearing arc α from T. Update
        # the tuples representing the breakpoints at the internal nodes. Perform
        # rebalancing operations on T if necessary. Delete all circle events involving
        # α from Q; these can be found using the pointers from the predecessor and
        # the successor of γ in T. (The circle event where α is the middle arc is
        # currently being handled, and has already been deleted from Q.)
        self.bleach_line.supprimer(gamma)

        # 2. Add the center of the circle causing the event as a vertex record to the
        # doubly-connected edge list D storing the Voronoi diagram under construc-
        # tion. Create two half-edge records corresponding to the new breakpoint
        # of the beach line. Set the pointers between them appropriately. Attach the
        # three new records to the half-edge records that end at the vertex.

        # 3. Check the new triple of consecutive arcs that has the former left neighbor
        # of α as its middle arc to see if the two breakpoints of the triple converge.
        # If so, insert the corresponding circle event into Q. and set pointers between
        # the new circle event in Q and the corresponding leaf of T. Do the same for
        # the triple where the former right neighbor is the middle arc.
        pass
